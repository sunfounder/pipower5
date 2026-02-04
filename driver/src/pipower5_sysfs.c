/*
 * PiPower5 SysFS Interface
 *
 * This file implements the sysfs interface for the PiPower5 driver,
 * providing individual files for each parameter.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 */

#include <linux/device.h>
#include <linux/hwmon-sysfs.h>
#include <linux/hwmon.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/mutex.h>
#include <linux/slab.h>

#include "pipower5.h"

/* Input voltage attribute */
static ssize_t input_voltage_show(struct device *dev,
                                  struct device_attribute *attr, char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  int ret;

  mutex_lock(&pi_dev->lock);
  ret = snprintf(buf, PAGE_SIZE, "%u\n", pi_dev->input_voltage);
  mutex_unlock(&pi_dev->lock);

  return ret;
}

static DEVICE_ATTR_RO(input_voltage);

/* Input current attribute */
static ssize_t input_current_show(struct device *dev,
                                  struct device_attribute *attr, char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  int ret;

  mutex_lock(&pi_dev->lock);
  ret = snprintf(buf, PAGE_SIZE, "%u\n", pi_dev->input_current);
  mutex_unlock(&pi_dev->lock);

  return ret;
}

static DEVICE_ATTR_RO(input_current);

/* Output voltage attribute */
static ssize_t output_voltage_show(struct device *dev,
                                   struct device_attribute *attr, char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  int ret;

  mutex_lock(&pi_dev->lock);
  ret = snprintf(buf, PAGE_SIZE, "%u\n", pi_dev->output_voltage);
  mutex_unlock(&pi_dev->lock);

  return ret;
}

static DEVICE_ATTR_RO(output_voltage);

/* Output current attribute */
static ssize_t output_current_show(struct device *dev,
                                   struct device_attribute *attr, char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  int ret;

  mutex_lock(&pi_dev->lock);
  ret = snprintf(buf, PAGE_SIZE, "%u\n", pi_dev->output_current);
  mutex_unlock(&pi_dev->lock);

  return ret;
}

static DEVICE_ATTR_RO(output_current);

/* Battery voltage attribute */
static ssize_t battery_voltage_show(struct device *dev,
                                    struct device_attribute *attr, char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  int ret;

  mutex_lock(&pi_dev->lock);
  ret = snprintf(buf, PAGE_SIZE, "%u\n", pi_dev->battery_voltage);
  mutex_unlock(&pi_dev->lock);

  return ret;
}

static DEVICE_ATTR_RO(battery_voltage);

/* Battery current attribute */
static ssize_t battery_current_show(struct device *dev,
                                    struct device_attribute *attr, char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  int ret;

  mutex_lock(&pi_dev->lock);
  ret = snprintf(buf, PAGE_SIZE, "%u\n", pi_dev->battery_current);
  mutex_unlock(&pi_dev->lock);

  return ret;
}

static DEVICE_ATTR_RO(battery_current);

/* Battery percentage attribute */
static ssize_t battery_percentage_show(struct device *dev,
                                       struct device_attribute *attr,
                                       char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  int ret;

  mutex_lock(&pi_dev->lock);
  ret = snprintf(buf, PAGE_SIZE, "%u\n", pi_dev->battery_percentage);
  mutex_unlock(&pi_dev->lock);

  return ret;
}

static DEVICE_ATTR_RO(battery_percentage);

/* Battery capacity attribute */
static ssize_t battery_capacity_show(struct device *dev,
                                     struct device_attribute *attr, char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  int ret;

  mutex_lock(&pi_dev->lock);
  ret = snprintf(buf, PAGE_SIZE, "%u\n", pi_dev->battery_capacity);
  mutex_unlock(&pi_dev->lock);

  return ret;
}

static DEVICE_ATTR_RO(battery_capacity);

/* Power source attribute */
static ssize_t power_source_show(struct device *dev,
                                 struct device_attribute *attr, char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  int ret;

  mutex_lock(&pi_dev->lock);
  ret = snprintf(buf, PAGE_SIZE, "%u\n", pi_dev->power_source);
  mutex_unlock(&pi_dev->lock);

  return ret;
}

static DEVICE_ATTR_RO(power_source);

/* Input plugged in attribute */
static ssize_t is_input_plugged_in_show(struct device *dev,
                                        struct device_attribute *attr,
                                        char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  int ret;

  mutex_lock(&pi_dev->lock);
  ret = snprintf(buf, PAGE_SIZE, "%u\n", pi_dev->is_input_plugged_in);
  mutex_unlock(&pi_dev->lock);

  return ret;
}

static DEVICE_ATTR_RO(is_input_plugged_in);

/* Charging status attribute */
static ssize_t is_charging_show(struct device *dev,
                                struct device_attribute *attr, char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  int ret;

  mutex_lock(&pi_dev->lock);
  ret = snprintf(buf, PAGE_SIZE, "%u\n", pi_dev->is_charging);
  mutex_unlock(&pi_dev->lock);

  return ret;
}

static DEVICE_ATTR_RO(is_charging);

/* Shutdown request attribute */
static ssize_t shutdown_request_show(struct device *dev,
                                     struct device_attribute *attr, char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  int ret;

  mutex_lock(&pi_dev->lock);
  ret = snprintf(buf, PAGE_SIZE, "%u\n", pi_dev->shutdown_request);
  mutex_unlock(&pi_dev->lock);

  return ret;
}

static DEVICE_ATTR_RO(shutdown_request);

/* Firmware version attribute */
static ssize_t firmware_version_show(struct device *dev,
                                     struct device_attribute *attr, char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  int ret;

  mutex_lock(&pi_dev->lock);
  ret = snprintf(buf, PAGE_SIZE, "%u.%u.%u\n", pi_dev->fw_major,
                 pi_dev->fw_minor, pi_dev->fw_patch);
  mutex_unlock(&pi_dev->lock);

  return ret;
}

static DEVICE_ATTR_RO(firmware_version);

/* Default on attribute */
static ssize_t default_on_show(struct device *dev,
                               struct device_attribute *attr, char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  int ret;

  mutex_lock(&pi_dev->lock);
  ret = snprintf(buf, PAGE_SIZE, "%u\n", pi_dev->default_on);
  mutex_unlock(&pi_dev->lock);

  return ret;
}

static DEVICE_ATTR_RO(default_on);

/* Board ID attribute */
static ssize_t board_id_show(struct device *dev, struct device_attribute *attr,
                             char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  int ret;

  mutex_lock(&pi_dev->lock);
  ret = snprintf(buf, PAGE_SIZE, "0x%04X\n", pi_dev->board_id);
  mutex_unlock(&pi_dev->lock);

  return ret;
}

static DEVICE_ATTR_RO(board_id);

/* Shutdown percentage attribute */
static ssize_t shutdown_percentage_show(struct device *dev,
                                        struct device_attribute *attr,
                                        char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  int ret;

  mutex_lock(&pi_dev->lock);
  ret = snprintf(buf, PAGE_SIZE, "%u\n", pi_dev->shutdown_percentage);
  mutex_unlock(&pi_dev->lock);

  return ret;
}

static ssize_t shutdown_percentage_store(struct device *dev,
                                         struct device_attribute *attr,
                                         const char *buf, size_t count) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  unsigned long value;
  int ret;

  ret = kstrtoul(buf, 10, &value);
  if (ret)
    return ret;

  if (value > 100)
    return -EINVAL;

  mutex_lock(&pi_dev->lock);
  ret = pipower5_write_byte_data(pi_dev, REG_WRITE_SHUTDOWN_PERCENTAGE,
                                 (u8)value);
  if (ret == 0) {
    pi_dev->shutdown_percentage = (u8)value;
    ret = count;
  }
  mutex_unlock(&pi_dev->lock);

  return ret;
}

static DEVICE_ATTR_RW(shutdown_percentage);

/* Battery internal resistor attribute */
static ssize_t battery_internal_resistor_show(struct device *dev,
                                              struct device_attribute *attr,
                                              char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  int ret;

  mutex_lock(&pi_dev->lock);
  ret = snprintf(buf, PAGE_SIZE, "%u\n", pi_dev->battery_internal_resistor);
  mutex_unlock(&pi_dev->lock);

  return ret;
}

static DEVICE_ATTR_RO(battery_internal_resistor);

/* Power button state attribute */
static ssize_t power_button_state_show(struct device *dev,
                                       struct device_attribute *attr,
                                       char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  int ret;

  mutex_lock(&pi_dev->lock);
  ret = snprintf(buf, PAGE_SIZE, "%u\n", pi_dev->power_button_state);
  mutex_unlock(&pi_dev->lock);

  return ret;
}

static ssize_t power_button_state_store(struct device *dev,
                                        struct device_attribute *attr,
                                        const char *buf, size_t count) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  unsigned long value;
  int ret;

  ret = kstrtoul(buf, 10, &value);
  if (ret)
    return ret;

  if (value > 1)
    return -EINVAL;

  mutex_lock(&pi_dev->lock);
  ret = pipower5_write_byte_data(pi_dev, REG_WRITE_POWER_BTN_STATE, (u8)value);
  if (ret == 0) {
    pi_dev->power_button_state = (u8)value;
    ret = count;
  }
  mutex_unlock(&pi_dev->lock);

  return ret;
}

static DEVICE_ATTR_RW(power_button_state);

/* Charge current max attribute */
static ssize_t charge_current_max_show(struct device *dev,
                                       struct device_attribute *attr,
                                       char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  int ret;

  mutex_lock(&pi_dev->lock);
  ret = snprintf(buf, PAGE_SIZE, "%u\n", pi_dev->charge_current_max);
  mutex_unlock(&pi_dev->lock);

  return ret;
}

static DEVICE_ATTR_RO(charge_current_max);

/* Buzzer volume attribute */
static ssize_t buzzer_volume_show(struct device *dev,
                                  struct device_attribute *attr, char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  int ret;

  mutex_lock(&pi_dev->lock);
  ret = snprintf(buf, PAGE_SIZE, "%u\n", pi_dev->buzzer_volume);
  mutex_unlock(&pi_dev->lock);

  return ret;
}

static ssize_t buzzer_volume_store(struct device *dev,
                                   struct device_attribute *attr,
                                   const char *buf, size_t count) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  unsigned int value;
  int ret;

  ret = kstrtouint(buf, 10, &value);
  if (ret) {
    return ret;
  }

  if (value > 100) {
    value = 100;
  }

  mutex_lock(&pi_dev->lock);
  pi_dev->buzzer_volume = (u8)value;
  ret = pipower5_write_byte_data(pi_dev, REG_WRITE_BUZZER_VOL, (u8)value);
  mutex_unlock(&pi_dev->lock);

  if (ret < 0) {
    return ret;
  }

  return count;
}

static DEVICE_ATTR_RW(buzzer_volume);

/* Driver version attribute */
static ssize_t driver_version_show(struct device *dev,
                                   struct device_attribute *attr, char *buf) {
  return snprintf(buf, PAGE_SIZE, "%s\n", PIPOWER5_DRIVER_VERSION);
}

static DEVICE_ATTR_RO(driver_version);

/* Input power attribute (voltage * current, mW) */
static ssize_t input_power_show(struct device *dev,
                                struct device_attribute *attr, char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  unsigned int power;
  int ret;

  mutex_lock(&pi_dev->lock);
  power = (unsigned int)pi_dev->input_voltage * pi_dev->input_current;
  ret = snprintf(buf, PAGE_SIZE, "%u\n", power);
  mutex_unlock(&pi_dev->lock);

  return ret;
}

static DEVICE_ATTR_RO(input_power);

/* Battery power attribute (voltage * current, mW) */
static ssize_t battery_power_show(struct device *dev,
                                  struct device_attribute *attr, char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  unsigned int power;
  int ret;

  mutex_lock(&pi_dev->lock);
  power = (unsigned int)pi_dev->battery_voltage * pi_dev->battery_current;
  ret = snprintf(buf, PAGE_SIZE, "%u\n", power);
  mutex_unlock(&pi_dev->lock);

  return ret;
}

static DEVICE_ATTR_RO(battery_power);

/* Output power attribute (voltage * current, mW) */
static ssize_t output_power_show(struct device *dev,
                                 struct device_attribute *attr, char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  unsigned int power;
  int ret;

  mutex_lock(&pi_dev->lock);
  power = (unsigned int)pi_dev->output_voltage * pi_dev->output_current;
  ret = snprintf(buf, PAGE_SIZE, "%u\n", power);
  mutex_unlock(&pi_dev->lock);

  return ret;
}

static DEVICE_ATTR_RO(output_power);

/* Attribute group */
static struct attribute *pipower5_attrs[] = {
    &dev_attr_input_voltage.attr,
    &dev_attr_input_current.attr,
    &dev_attr_input_power.attr,
    &dev_attr_output_voltage.attr,
    &dev_attr_output_current.attr,
    &dev_attr_output_power.attr,
    &dev_attr_battery_voltage.attr,
    &dev_attr_battery_current.attr,
    &dev_attr_battery_power.attr,
    &dev_attr_battery_percentage.attr,
    &dev_attr_battery_capacity.attr,
    &dev_attr_power_source.attr,
    &dev_attr_is_input_plugged_in.attr,
    &dev_attr_is_charging.attr,
    &dev_attr_shutdown_request.attr,
    &dev_attr_firmware_version.attr,
    &dev_attr_default_on.attr,
    &dev_attr_board_id.attr,
    &dev_attr_shutdown_percentage.attr,
    &dev_attr_battery_internal_resistor.attr,
    &dev_attr_power_button_state.attr,
    &dev_attr_charge_current_max.attr,
    &dev_attr_buzzer_volume.attr,
    &dev_attr_driver_version.attr,
    NULL,
};

static const struct attribute_group pipower5_group = {
    .attrs = pipower5_attrs,
};

int pipower5_create_sysfs(struct pipower5_device *pi_dev) {
  int ret;

  ret = sysfs_create_group(&pi_dev->pipower5_dev->kobj, &pipower5_group);
  if (ret) {
    dev_err(&pi_dev->client->dev, "Failed to create sysfs attributes\n");
    return ret;
  }

  return 0;
}

void pipower5_remove_sysfs(struct pipower5_device *pi_dev) {
  sysfs_remove_group(&pi_dev->pipower5_dev->kobj, &pipower5_group);
}

MODULE_AUTHOR("SunFounder <service@sunfounder.com>");
MODULE_DESCRIPTION("PiPower5 SysFS Interface");
MODULE_LICENSE("GPL v2");