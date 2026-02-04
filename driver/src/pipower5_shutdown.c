/*
 * PiPower5 Shutdown Driver
 *
 * This file implements the shutdown detection functionality
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
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/reboot.h>

#include "pipower5.h"

void pipower5_handle_shutdown(struct pipower5_device *pi_dev)
{
  switch (pi_dev->shutdown_request) {
  case SHUTDOWN_REQUEST_LOW_BATTERY:
    dev_info(&pi_dev->client->dev, "Low battery shutdown request\n");
    break;
  case SHUTDOWN_REQUEST_BUTTON:
    dev_info(&pi_dev->client->dev, "Power button shutdown request\n");
    break;
  case SHUTDOWN_REQUEST_LOW_VOLTAGE:
    dev_info(&pi_dev->client->dev, "Low voltage shutdown request\n");
    break;
  default:
    return;
  }

  /* Schedule system shutdown */
  dev_info(&pi_dev->client->dev, "Scheduling system shutdown...\n");
  kernel_power_off();
}

MODULE_AUTHOR("SunFounder <service@sunfounder.com>");
MODULE_DESCRIPTION("PiPower5 Shutdown Driver");
MODULE_LICENSE("GPL v2");
