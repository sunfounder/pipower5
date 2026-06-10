/*
 * PiPower5 I2C Driver Framework
 *
 * Copyright (c) 2026 Your Name <your.email@example.com>
 *
 * Based on various power supply drivers in the Linux kernel
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 */

#include <linux/device.h>
#include <linux/hwmon-sysfs.h>
#include <linux/hwmon.h>
#include <linux/i2c.h>
#include <linux/init.h>
#include <linux/kmod.h>
#include <linux/module.h>
#include <linux/mutex.h>
#include <linux/of.h>
#include <linux/power_supply.h>
#include <linux/reboot.h>
#include <linux/slab.h>
#include <linux/workqueue.h>
#include "pipower5.h"

#define DRIVER_NAME "pipower5"
#define CLASS_NAME "pipower5"

static int pipower5_probe(struct i2c_client *client);
static void pipower5_remove(struct i2c_client *client);
static void pipower5_poll_work(struct work_struct *work);

static struct class *pipower5_class;

/*
 * Fix sysfs permissions for non-root users.
 * class_create() / device_create() may create directories without the
 * execute bit, preventing traversal.  Run chmod + chgrp via usermodehelper.
 */
static void pipower5_fix_sysfs_perms(void) {
  char *argv[] = {
    "/bin/sh", "-c",
    "chmod 755 /sys/class/pipower5 /sys/class/pipower5/pipower5 && "
    "chgrp gpio /sys/class/pipower5/pipower5 && "
    "chmod 664 /sys/class/pipower5/pipower5/* && "
    "chgrp gpio /sys/class/pipower5/pipower5/*",
    NULL
  };
  char *envp[] = { NULL };
  int ret;

  ret = call_usermodehelper(argv[0], argv, envp, UMH_WAIT_PROC);
  if (ret)
    pr_warn("pipower5: fix_sysfs_perms failed: %d\n", ret);
}

static const struct of_device_id pipower5_of_match[] = {
    {
        .compatible = "sunfounder,pipower5",
    },
    {},
};
MODULE_DEVICE_TABLE(of, pipower5_of_match);

static const struct i2c_device_id pipower5_id[] = {{"pipower5", 0}, {}};
MODULE_DEVICE_TABLE(i2c, pipower5_id);

static struct i2c_driver pipower5_driver = {
    .driver =
        {
            .name = DRIVER_NAME,
            .of_match_table = of_match_ptr(pipower5_of_match),
        },
    .probe = pipower5_probe,
    .remove = pipower5_remove,
    .id_table = pipower5_id,
};



static void pipower5_poll_work(struct work_struct *work) {
  struct delayed_work *dwork = to_delayed_work(work);
  struct pipower5_device *pi_dev =
      container_of(dwork, struct pipower5_device, poll_work);
  int ret;

  /* Read all registers and update cached values */
  ret = pipower5_update_status(pi_dev);
  if (ret < 0) {
    dev_err(&pi_dev->client->dev, "Failed to update status: %d\n", ret);
  } else {
    /* Notify power_supply subsystem so desktop/UIs see updated battery data */
    if (pi_dev->power_supply) {
      power_supply_changed(pi_dev->power_supply);
    }

    /* Check for power button state change */
    pipower5_button_check(pi_dev);

    /* Check for shutdown request */
    if (pi_dev->shutdown_request != SHUTDOWN_REQUEST_NONE) {
      pipower5_handle_shutdown(pi_dev);
    }
  }

  /* Reschedule work */
  queue_delayed_work(pi_dev->wq, &pi_dev->poll_work,
                     msecs_to_jiffies(PIPOWER5_POLL_INTERVAL));
}

static int pipower5_probe(struct i2c_client *client) {
  struct device *dev = &client->dev;
  struct pipower5_device *pi_dev;
  int ret;

  /* Check if device is accessible */
  if (!i2c_check_functionality(client->adapter, I2C_FUNC_SMBUS_BYTE_DATA |
                                                    I2C_FUNC_SMBUS_WORD_DATA)) {
    dev_err(dev, "I2C adapter doesn't support required functionality\n");
    return -EIO;
  }

  pi_dev = devm_kzalloc(dev, sizeof(*pi_dev), GFP_KERNEL);
  if (!pi_dev)
    return -ENOMEM;

  pi_dev->client = client;
  mutex_init(&pi_dev->lock);

  /* Create device under /sys/class/pipower5/ as virtual device.
   * Using NULL parent avoids I2C device directory permission issues
   * (I2C core creates 1-005c without execute bit, blocking traversal). */
  pi_dev->pipower5_dev =
      device_create(pipower5_class, NULL, MKDEV(0, 0), pi_dev, "pipower5");
  if (IS_ERR(pi_dev->pipower5_dev)) {
    ret = PTR_ERR(pi_dev->pipower5_dev);
    dev_err(dev, "Failed to create pipower5 device: %d\n", ret);
    pi_dev->pipower5_dev = NULL;
    return ret;
  }
  dev_info(dev, "Created pipower5 device at /sys/class/pipower5/pipower5\n");

  /* Try to initialize cached values, but continue even if it fails */
  ret = pipower5_update_status(pi_dev);
  if (ret < 0) {
    dev_warn(dev, "Failed to read initial status: %d, continuing anyway\n", ret);
  }

  /* Create workqueue for polling */
  pi_dev->wq = create_singlethread_workqueue("pipower5_poll");
  if (!pi_dev->wq) {
    dev_err(dev, "Failed to create workqueue\n");
    device_destroy(pipower5_class, MKDEV(0, 0));
    return -ENOMEM;
  }

  /* Initialize delayed work */
  INIT_DELAYED_WORK(&pi_dev->poll_work, pipower5_poll_work);

  /* Start polling */
  queue_delayed_work(pi_dev->wq, &pi_dev->poll_work,
                     msecs_to_jiffies(PIPOWER5_POLL_INTERVAL));

  i2c_set_clientdata(client, pi_dev);

  /* Register hwmon device */
  pi_dev->hwmon_dev = hwmon_device_register(dev);
  if (IS_ERR(pi_dev->hwmon_dev)) {
    ret = PTR_ERR(pi_dev->hwmon_dev);
    dev_err(dev, "Failed to register hwmon device: %d\n", ret);
    cancel_delayed_work_sync(&pi_dev->poll_work);
    destroy_workqueue(pi_dev->wq);
    device_destroy(pipower5_class, MKDEV(0, 0));
    return ret;
  }

  /* Initialize buzzer playback */
  pipower5_buzzer_init(pi_dev);

  /* Create sysfs interface only if device exists */
  if (pi_dev->pipower5_dev) {
    ret = pipower5_create_sysfs(pi_dev);
    if (ret < 0) {
      dev_err(dev, "Failed to create sysfs interface: %d\n", ret);
      hwmon_device_unregister(pi_dev->hwmon_dev);
      cancel_delayed_work_sync(&pi_dev->poll_work);
      destroy_workqueue(pi_dev->wq);
      device_destroy(pipower5_class, MKDEV(0, 0));
      return ret;
    }
    /* Fix directory permissions so non-root users can traverse */
    pipower5_fix_sysfs_perms();
  }

  /* Create upower interface */
  ret = pipower5_create_upower(pi_dev);
  if (ret < 0) {
    dev_err(dev, "Failed to create upower interface: %d\n", ret);
    if (pi_dev->pipower5_dev) {
      pipower5_remove_sysfs(pi_dev);
    }
    hwmon_device_unregister(pi_dev->hwmon_dev);
    cancel_delayed_work_sync(&pi_dev->poll_work);
    destroy_workqueue(pi_dev->wq);
    if (pi_dev->pipower5_dev) {
      device_destroy(pipower5_class, MKDEV(0, 0));
    }
    return ret;
  }

  pipower5_log_event(pi_dev, "STARTUP driver v%s bat=%d%% bat_voltage=%dmV",
                     PIPOWER5_DRIVER_VERSION,
                     pi_dev->battery_percentage, pi_dev->battery_voltage);
  dev_info(dev, "PiPower5 driver initialized successfully\n");

  return 0;
}

static void pipower5_remove(struct i2c_client *client) {
  struct pipower5_device *pi_dev = i2c_get_clientdata(client);

  /* Cancel work */
  cancel_delayed_work_sync(&pi_dev->buzzer_work);
  cancel_delayed_work_sync(&pi_dev->poll_work);
  destroy_workqueue(pi_dev->wq);

  /* Remove upower interface */
  pipower5_remove_upower(pi_dev);

  /* Remove hwmon device */
  hwmon_device_unregister(pi_dev->hwmon_dev);

  /* Remove sysfs interface only if device exists */
  if (pi_dev->pipower5_dev) {
    pipower5_remove_sysfs(pi_dev);
  }

  /* Destroy device */
  if (pi_dev->pipower5_dev) {
    device_destroy(pipower5_class, MKDEV(0, 0));
    pi_dev->pipower5_dev = NULL;
  }

  dev_info(&client->dev, "PiPower5 driver removed\n");
}

static int __init pipower5_driver_init(void) {
  pipower5_class = class_create(CLASS_NAME);
  if (IS_ERR(pipower5_class)) {
    pr_err("pipower5: failed to create class\n");
    return PTR_ERR(pipower5_class);
  }
  return i2c_add_driver(&pipower5_driver);
}

static void __exit pipower5_driver_exit(void) {
  i2c_del_driver(&pipower5_driver);
  if (pipower5_class) {
    class_destroy(pipower5_class);
    pipower5_class = NULL;
  }
}

module_init(pipower5_driver_init);
module_exit(pipower5_driver_exit);

MODULE_AUTHOR("SunFounder <service@sunfounder.com>");
MODULE_DESCRIPTION("PiPower5 Power Management Driver Framework");
MODULE_LICENSE("GPL v2");
MODULE_ALIAS("i2c:pipower5");