/*
 * PiPower5 UPower Driver
 *
 * This file implements the UPower integration for the PiPower5 driver,
 * providing battery and power supply information to the UPower system.
 *
 * Copyright (c) 2026 SunFounder <service@sunfounder.com>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 */

#include <linux/i2c.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/power_supply.h>
#include <linux/slab.h>

#include "pipower5.h"

struct pipower5_power {
  struct power_supply_desc desc;
  struct pipower5_device *pi_dev;
};

static enum power_supply_property pipower5_power_props[] = {
    POWER_SUPPLY_PROP_PRESENT,
    POWER_SUPPLY_PROP_ONLINE,
    POWER_SUPPLY_PROP_STATUS,
    POWER_SUPPLY_PROP_CAPACITY,
    POWER_SUPPLY_PROP_CAPACITY_LEVEL,
    POWER_SUPPLY_PROP_VOLTAGE_NOW,
    POWER_SUPPLY_PROP_VOLTAGE_MAX,
    POWER_SUPPLY_PROP_VOLTAGE_MIN,
    POWER_SUPPLY_PROP_VOLTAGE_MAX_DESIGN,
    POWER_SUPPLY_PROP_VOLTAGE_MIN_DESIGN,
    POWER_SUPPLY_PROP_CHARGE_FULL_DESIGN,
    POWER_SUPPLY_PROP_CHARGE_NOW,
    POWER_SUPPLY_PROP_CHARGE_FULL,
    POWER_SUPPLY_PROP_CURRENT_NOW,
    POWER_SUPPLY_PROP_ENERGY_NOW,
    POWER_SUPPLY_PROP_ENERGY_EMPTY,
    POWER_SUPPLY_PROP_ENERGY_FULL,
    POWER_SUPPLY_PROP_ENERGY_FULL_DESIGN,
    POWER_SUPPLY_PROP_MODEL_NAME,
    POWER_SUPPLY_PROP_MANUFACTURER,
    POWER_SUPPLY_PROP_TECHNOLOGY,
    POWER_SUPPLY_PROP_SCOPE,
};

static int pipower5_power_get_property(struct power_supply *psy,
                                       enum power_supply_property psp,
                                       union power_supply_propval *val) {
  struct pipower5_power *pwr = power_supply_get_drvdata(psy);
  struct pipower5_device *pi_dev = pwr->pi_dev;

  mutex_lock(&pi_dev->lock);
  switch (psp) {
  case POWER_SUPPLY_PROP_PRESENT:
    val->intval = 1;
    break;

  case POWER_SUPPLY_PROP_ONLINE:
    val->intval = pi_dev->is_input_plugged_in;
    break;

  case POWER_SUPPLY_PROP_STATUS:
    if (pi_dev->is_charging) {
      val->intval = POWER_SUPPLY_STATUS_CHARGING;
    } else {
      if (pi_dev->battery_percentage >= 98) {
        val->intval = POWER_SUPPLY_STATUS_FULL;
      } else {
        val->intval = POWER_SUPPLY_STATUS_DISCHARGING;
      }
    }
    break;

  case POWER_SUPPLY_PROP_CAPACITY:
    val->intval = pi_dev->battery_percentage;
    break;

  case POWER_SUPPLY_PROP_VOLTAGE_NOW:
    val->intval = pi_dev->battery_voltage * 1000;
    break;
  case POWER_SUPPLY_PROP_VOLTAGE_MAX:
  case POWER_SUPPLY_PROP_VOLTAGE_MAX_DESIGN:
      val->intval = PIPOWER5_BATTERY_MAX_VOLTAGE * 1000; // mV to uV
      break;
  case POWER_SUPPLY_PROP_VOLTAGE_MIN:
  case POWER_SUPPLY_PROP_VOLTAGE_MIN_DESIGN:
      val->intval = PIPOWER5_BATTERY_MIN_VOLTAGE * 1000; // mV to uV
      break;
  case POWER_SUPPLY_PROP_CURRENT_NOW:
      val->intval = pi_dev->battery_current * 1000; // mA to uA
      break;
  case POWER_SUPPLY_PROP_ENERGY_FULL:
  case POWER_SUPPLY_PROP_ENERGY_FULL_DESIGN:
  case POWER_SUPPLY_PROP_CHARGE_FULL:
  case POWER_SUPPLY_PROP_CHARGE_FULL_DESIGN:
      val->intval = PIPOWER5_BATTERY_FULL_CHARGE_MAH * 1000; // mAh to uAh
      break;
  case POWER_SUPPLY_PROP_ENERGY_NOW:
  case POWER_SUPPLY_PROP_CHARGE_NOW:
      val->intval = (PIPOWER5_BATTERY_FULL_CHARGE_MAH * pi_dev->battery_percentage / 100) * 1000; // mAh to uAh
      break;
  case POWER_SUPPLY_PROP_ENERGY_EMPTY:
      val->intval = 0;
      break;
  case POWER_SUPPLY_PROP_MODEL_NAME:
      val->strval = "PiPower 5";
      break;
  case POWER_SUPPLY_PROP_MANUFACTURER:
      val->strval = "SunFounder";
      break;
  case POWER_SUPPLY_PROP_TECHNOLOGY:
      val->intval = POWER_SUPPLY_TECHNOLOGY_LION;
      break;
  case POWER_SUPPLY_PROP_SCOPE:
      val->intval = POWER_SUPPLY_SCOPE_SYSTEM;
      break;
  case POWER_SUPPLY_PROP_CAPACITY_LEVEL:
      if (pi_dev->battery_percentage >= 90)
          val->intval = POWER_SUPPLY_CAPACITY_LEVEL_FULL;
      else if (pi_dev->battery_percentage >= 70)
          val->intval = POWER_SUPPLY_CAPACITY_LEVEL_HIGH;
      else if (pi_dev->battery_percentage >= 30)
          val->intval = POWER_SUPPLY_CAPACITY_LEVEL_NORMAL;
      else if (pi_dev->battery_percentage >= 10)
          val->intval = POWER_SUPPLY_CAPACITY_LEVEL_LOW;
      else
          val->intval = POWER_SUPPLY_CAPACITY_LEVEL_CRITICAL;
      break;
  default:
    mutex_unlock(&pi_dev->lock);
    return -EINVAL;
  }
  mutex_unlock(&pi_dev->lock);

  return 0;
}

int pipower5_create_upower(struct pipower5_device *pi_dev) {
  struct pipower5_power *pwr;
  struct power_supply_config cfg = {};
  int ret;

  pwr = devm_kzalloc(&pi_dev->client->dev, sizeof(*pwr), GFP_KERNEL);
  if (!pwr) {
    return -ENOMEM;
  }

  pwr->desc.name = "pipower5";
  pwr->desc.type = POWER_SUPPLY_TYPE_BATTERY;
  pwr->desc.properties = pipower5_power_props;
  pwr->desc.num_properties = ARRAY_SIZE(pipower5_power_props);
  pwr->desc.get_property = pipower5_power_get_property;
  pwr->pi_dev = pi_dev;

  cfg.drv_data = pwr;

  pi_dev->power_supply =
      power_supply_register(&pi_dev->client->dev, &pwr->desc, &cfg);
  if (IS_ERR(pi_dev->power_supply)) {
    ret = PTR_ERR(pi_dev->power_supply);
    dev_err(&pi_dev->client->dev, "Failed to register power supply: %d\n", ret);
    return ret;
  }

  return 0;
}

void pipower5_remove_upower(struct pipower5_device *pi_dev) {
  if (pi_dev->power_supply) {
    power_supply_unregister(pi_dev->power_supply);
    pi_dev->power_supply = NULL;
  }
}

MODULE_AUTHOR("SunFounder <service@sunfounder.com>");
MODULE_DESCRIPTION("PiPower5 UPower Driver");
MODULE_LICENSE("GPL v2");