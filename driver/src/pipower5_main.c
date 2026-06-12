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
#include <linux/file.h>
#include <linux/fs.h>
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

/* ── Module parameters (persisted via /etc/modprobe.d/pipower5.conf) ── */
unsigned int buzz_on = 0x7F;
module_param(buzz_on, uint, 0644);
MODULE_PARM_DESC(buzz_on, "Buzzer event bitmask (default 0x7F = all on)");

unsigned int buzzer_volume = 3;
module_param_named(volume, buzzer_volume, uint, 0644);
MODULE_PARM_DESC(volume, "Buzzer volume 0-10 (default 3)");

unsigned int shutdown_pct = 10;
module_param_named(shutdown_percentage, shutdown_pct, uint, 0644);
MODULE_PARM_DESC(shutdown_percentage, "Auto-shutdown battery % (default 10)");

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



/* Fast button poll — reads button register at 50 Hz with proper locking */
static void pipower5_button_poll_work(struct work_struct *work) {
  struct delayed_work *dwork = to_delayed_work(work);
  struct pipower5_device *pi_dev =
      container_of(dwork, struct pipower5_device, button_poll_work);
  int ret;

  mutex_lock(&pi_dev->lock);
  ret = __pipower5_read_byte(pi_dev, REG_READ_POWER_BUTTON_STATE);
  if (ret >= 0) {
    if ((u8)ret != 0) {
      /* Button event detected: cache value, reset MCU register,
       * and record timestamp so sysfs holds the value for 2s. */
      pi_dev->power_button_state = (u8)ret;
      pi_dev->button_event_jiffies = jiffies;
      __pipower5_write_byte(pi_dev, REG_WRITE_POWER_BTN_STATE, 0);
    } else if (pi_dev->power_button_state != 0 &&
               time_after(jiffies, pi_dev->button_event_jiffies + 2 * HZ)) {
      /* 2 seconds elapsed since last event, show RELEASED */
      pi_dev->power_button_state = 0;
    }
  }
  mutex_unlock(&pi_dev->lock);

  if (ret >= 0 && (u8)ret != 0)
    pipower5_button_check(pi_dev);

  queue_delayed_work(pi_dev->wq, &pi_dev->button_poll_work,
                     msecs_to_jiffies(PIPOWER5_BUTTON_POLL_INTERVAL));
}

/* Main poll work — reads all data + events + notifies UPower at 1 Hz */
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
    /* Update always-on statistics (averages, peaks, mAh, estimated runtime) */
    pipower5_stats_update(pi_dev);

    /* Notify power_supply subsystem so desktop/UIs see updated battery data */
    if (pi_dev->power_supply) {
      power_supply_changed(pi_dev->power_supply);
    }

    /* ── Event detection (first poll skipped to avoid false events) ── */
    if (pi_dev->events_initialized) {
      s16 batt_cur = (s16)pi_dev->battery_current; /* signed: +charge, -discharge */

      /* POWER_DISCONNECTED / POWER_RESTORED */
      if (pi_dev->is_input_plugged_in != pi_dev->last_is_input_plugged_in) {
        char *envp[] = { NULL, NULL, NULL, NULL };
        if (pi_dev->is_input_plugged_in) {
          envp[0] = "PIPOWER5_EVENT=power_restored";
          pipower5_log_event(pi_dev, "POWER_RESTORED");
        } else {
          envp[0] = "PIPOWER5_EVENT=power_disconnected";
          pipower5_log_event(pi_dev, "POWER_DISCONNECTED");
        }
        kobject_uevent_env(&pi_dev->pipower5_dev->kobj, KOBJ_CHANGE, envp);
        pipower5_buzzer_event(pi_dev,
          pi_dev->is_input_plugged_in ?
          "power_restored" : "power_disconnected");
      }

      /* BATTERY_ACTIVATED: switched to battery power */
      if (pi_dev->power_source != pi_dev->last_power_source &&
          pi_dev->power_source == 1) {
        char *envp[] = { "PIPOWER5_EVENT=battery_activated", NULL };
        pipower5_log_event(pi_dev, "BATTERY_ACTIVATED bat=%d%%",
                           pi_dev->battery_percentage);
        kobject_uevent_env(&pi_dev->pipower5_dev->kobj, KOBJ_CHANGE, envp);
        pipower5_buzzer_event(pi_dev, "battery_activated");
      }

      /* POWER_INSUFFICIENT: input plugged in but battery still discharging.
       * Rate-limited to once per 60s or on state change. */
      if (pi_dev->is_input_plugged_in && !pi_dev->is_charging &&
          batt_cur < -100) {  /* significant discharge (>100mA), not float current */
        static unsigned long last_pwr_insuf_log;
        if (time_after(jiffies, last_pwr_insuf_log + 60 * HZ) ||
            pi_dev->is_input_plugged_in != pi_dev->last_is_input_plugged_in) {
          char *envp[] = { "PIPOWER5_EVENT=power_insufficient", NULL };
          pipower5_log_event(pi_dev, "POWER_INSUFFICIENT bat=%d%% cur=%dmA",
                             pi_dev->battery_percentage, batt_cur);
          kobject_uevent_env(&pi_dev->pipower5_dev->kobj, KOBJ_CHANGE, envp);
          pipower5_buzzer_event(pi_dev, "power_insufficient");
          last_pwr_insuf_log = jiffies;
        }
      }

      /* LOW_BATTERY: percentage below shutdown threshold. Rate-limited 60s. */
      if (pi_dev->battery_percentage < pi_dev->shutdown_percentage) {
        static unsigned long last_low_bat_log;
        if (time_after(jiffies, last_low_bat_log + 60 * HZ)) {
          char *envp[] = { "PIPOWER5_EVENT=low_battery", NULL };
          pipower5_log_event(pi_dev, "LOW_BATTERY bat=%d%% threshold=%d%%",
                             pi_dev->battery_percentage,
                             pi_dev->shutdown_percentage);
          kobject_uevent_env(&pi_dev->pipower5_dev->kobj, KOBJ_CHANGE, envp);
          pipower5_buzzer_event(pi_dev, "low_battery");
          last_low_bat_log = jiffies;
        }
      }
    }

    /* Save state for next poll */
    pi_dev->last_is_input_plugged_in = pi_dev->is_input_plugged_in;
    pi_dev->last_power_source = pi_dev->power_source;
    pi_dev->last_is_charging = pi_dev->is_charging;
    pi_dev->events_initialized = true;

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
  pi_dev->vbus_enabled = true;  /* VBUS starts enabled */

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
  INIT_DELAYED_WORK(&pi_dev->button_poll_work, pipower5_button_poll_work);

  /* Start polling */
  queue_delayed_work(pi_dev->wq, &pi_dev->poll_work,
                     msecs_to_jiffies(PIPOWER5_POLL_INTERVAL));
  queue_delayed_work(pi_dev->wq, &pi_dev->button_poll_work,
                     msecs_to_jiffies(PIPOWER5_BUTTON_POLL_INTERVAL));

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

  /* Load user-custom buzzer sequences from /etc/pipower5/buzz_seq.conf */
  {
    struct file *f = filp_open("/etc/pipower5/buzz_seq.conf", O_RDONLY, 0);
    if (!IS_ERR(f)) {
      loff_t pos = 0;
      char *kbuf = kmalloc(4096, GFP_KERNEL);
      if (kbuf) {
        ssize_t len = kernel_read(f, kbuf, 4095, &pos);
        if (len > 0) {
          kbuf[len] = '\0';
          dev_info(dev, "Loading custom buzz sequences from /etc/pipower5/buzz_seq.conf\n");
          pipower5_buzz_seq_load(kbuf, len);
        }
        kfree(kbuf);
      }
      filp_close(f, NULL);
    }
  }

  /* Apply module parameters to hardware */
  pi_dev->buzzer_volume = (u8)buzzer_volume;
  pi_dev->shutdown_percentage = (u8)shutdown_pct;
  /* User scale 0-10, MCU expects 0-100 */
  __pipower5_write_byte(pi_dev, REG_WRITE_BUZZER_VOL,
      buzzer_volume >= 10 ? 100 : (u8)(buzzer_volume * 10));
  __pipower5_write_byte(pi_dev, REG_WRITE_SHUTDOWN_PERCENTAGE, (u8)shutdown_pct);

  /* Initialize always-on statistics and power failure test */
  pipower5_stats_init(pi_dev);
  pipower5_pft_init(pi_dev);

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

  /* Initialize button input device */
  ret = pipower5_button_init(pi_dev);
  if (ret) {
    dev_warn(dev, "Failed to init button input device, continuing: %d\n", ret);
    /* Non-fatal: everything else works without the button */
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
  cancel_delayed_work_sync(&pi_dev->pft_work);
  cancel_delayed_work_sync(&pi_dev->buzzer_work);
  cancel_delayed_work_sync(&pi_dev->poll_work);
  cancel_delayed_work_sync(&pi_dev->button_poll_work);
  destroy_workqueue(pi_dev->wq);

  /* Ensure VBUS is re-enabled on unload */
  if (!pi_dev->vbus_enabled)
    pipower5_enable_vbus(pi_dev);

  /* Remove upower interface */
  pipower5_remove_upower(pi_dev);

  /* Remove button input device */
  pipower5_button_cleanup(pi_dev);

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