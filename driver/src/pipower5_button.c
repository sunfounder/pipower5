/*
 * PiPower5 Button Driver
 *
 * This file implements the input device for the power button
 * for the PiPower5 driver.
 *
 * Copyright (c) 2026 SunFounder <service@sunfounder.com>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 */

#include <linux/device.h>
#include <linux/input.h>
#include <linux/module.h>
#include <linux/slab.h>

#include "pipower5.h"

int pipower5_button_init(struct pipower5_device *pi_dev)
{
    struct device *dev = &pi_dev->client->dev;
    int ret;

    dev_info(dev, "Initializing input device for power button\n");
    pi_dev->input_dev = input_allocate_device();
    if (!pi_dev->input_dev) {
        dev_err(dev, "Failed to allocate input device\n");
        return -ENOMEM;
    }

    pi_dev->input_dev->name = "pipower5-power-button";
    pi_dev->input_dev->phys = "pipower5/input0";
    pi_dev->input_dev->dev.parent = dev;
    pi_dev->input_dev->id.bustype = BUS_I2C;
    pi_dev->input_dev->id.vendor = 0x0000;
    pi_dev->input_dev->id.product = 0x0000;
    pi_dev->input_dev->id.version = 0x0001;

    input_set_capability(pi_dev->input_dev, EV_KEY, KEY_POWER);

    dev_info(dev, "Registering input device\n");
    ret = input_register_device(pi_dev->input_dev);
    if (ret) {
        dev_err(dev, "Failed to register input device: %d\n", ret);
        input_free_device(pi_dev->input_dev);
        pi_dev->input_dev = NULL;
        return ret;
    }
    dev_info(dev, "Input device registered successfully\n");

    /* Initialize last power button state */
    pi_dev->last_power_button_state = pi_dev->power_button_state;

    return 0;
}

void pipower5_button_cleanup(struct pipower5_device *pi_dev)
{
    if (pi_dev->input_dev) {
        input_unregister_device(pi_dev->input_dev);
        pi_dev->input_dev = NULL;
    }
}

void pipower5_button_check(struct pipower5_device *pi_dev)
{
    /* Button state register (154) values from MCU:
     * 0=RELEASED, 1=CLICK, 2=DOUBLE_CLICK,
     * 3=LONG_PRESS_2S, 4=LONG_PRESS_2S_RELEASED,
     * 5=LONG_PRESS_5S, 6=LONG_PRESS_5S_RELEASED
     *
     * Shutdown is handled by the MCU via shutdown_request register (20).
     * We only log button events here; do NOT send KEY_POWER to avoid
     * systemd-logind triggering immediate shutdown. */

    if (pi_dev->power_button_state != pi_dev->last_power_button_state &&
        pi_dev->power_button_state != 0) {

        switch (pi_dev->power_button_state) {
        case 1:
            pipower5_log_event(pi_dev, "BUTTON click");
            break;
        case 2:
            pipower5_log_event(pi_dev, "BUTTON double_click");
            break;
        case 3:
            pipower5_log_event(pi_dev, "BUTTON long_press_2s");
            break;
        case 5:
            pipower5_log_event(pi_dev, "BUTTON long_press_5s");
            break;
        }

        pi_dev->last_power_button_state = pi_dev->power_button_state;
    }
}

MODULE_AUTHOR("SunFounder <service@sunfounder.com>");
MODULE_DESCRIPTION("PiPower5 Button Driver");
MODULE_LICENSE("GPL v2");
