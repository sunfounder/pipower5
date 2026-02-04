/*
 * PiPower5 I2C Communication Functions
 *
 * Copyright (c) 2026 Your Name <your.email@example.com>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 */

#include <linux/i2c.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/mutex.h>
#include <linux/slab.h>

#include "pipower5.h"

int pipower5_read_word_data(struct pipower5_device *pi_dev, u8 reg) {
  int ret;

  mutex_lock(&pi_dev->lock);
  ret = i2c_smbus_read_word_data(pi_dev->client, reg);
  mutex_unlock(&pi_dev->lock);

  if (ret < 0) {
    dev_err(&pi_dev->client->dev,
            "Failed to read word from register 0x%02x: %d\n", reg, ret);
    return ret;
  }

  /* SMBus returns data in little-endian, but we need to swap bytes */
  /* because the device actually uses big-endian for 16-bit values */
  /* Wait, no - from our test, we see that:
   * Register 0x08 (battery voltage): Byte0=0xD0, Byte1=0x20
   * SMBus returns 0x20D0 (little-endian)
   * But we need 0x20D0 = 8400 mV = 8.40 V, which is correct!
   * So no need to swap bytes after all.
   */
  /* ret = swab16(ret); */

  return ret;
}

int pipower5_read_byte_data(struct pipower5_device *pi_dev, u8 reg) {
  int ret;

  mutex_lock(&pi_dev->lock);
  ret = i2c_smbus_read_byte_data(pi_dev->client, reg);
  mutex_unlock(&pi_dev->lock);

  if (ret < 0) {
    dev_err(&pi_dev->client->dev,
            "Failed to read byte from register 0x%02x: %d\n", reg, ret);
    return ret;
  }

  return ret;
}

int pipower5_write_byte_data(struct pipower5_device *pi_dev, u8 reg, u8 value) {
  int ret;

  mutex_lock(&pi_dev->lock);
  ret = i2c_smbus_write_byte_data(pi_dev->client, reg, value);
  mutex_unlock(&pi_dev->lock);

  if (ret < 0) {
    dev_err(&pi_dev->client->dev,
            "Failed to write 0x%02x to register 0x%02x: %d\n", value, reg, ret);
    return ret;
  }

  return 0;
}

int pipower5_update_status(struct pipower5_device *pi_dev) {
  int ret;

  /* Read input voltage (16-bit) */
  ret = pipower5_read_word_data(pi_dev, REG_READ_INPUT_VOLTAGE);
  if (ret >= 0) {
    pi_dev->input_voltage = (u16)ret;
  } else {
    return ret;
  }

  /* Read input current (16-bit) */
  ret = pipower5_read_word_data(pi_dev, REG_READ_INPUT_CURRENT);
  if (ret >= 0) {
    pi_dev->input_current = (u16)ret;
  } else {
    return ret;
  }

  /* Read output voltage (16-bit) */
  ret = pipower5_read_word_data(pi_dev, REG_READ_OUTPUT_VOLTAGE);
  if (ret >= 0) {
    pi_dev->output_voltage = (u16)ret;
  } else {
    return ret;
  }

  /* Read output current (16-bit) */
  ret = pipower5_read_word_data(pi_dev, REG_READ_OUTPUT_CURRENT);
  if (ret >= 0) {
    pi_dev->output_current = (u16)ret;
  } else {
    return ret;
  }

  /* Read battery voltage (16-bit) */
  ret = pipower5_read_word_data(pi_dev, REG_READ_BATTERY_VOLTAGE);
  if (ret >= 0) {
    pi_dev->battery_voltage = (u16)ret;
  } else {
    return ret;
  }

  /* Read battery current (16-bit) */
  ret = pipower5_read_word_data(pi_dev, REG_READ_BATTERY_CURRENT);
  if (ret >= 0) {
    pi_dev->battery_current = (u16)ret;
  } else {
    return ret;
  }

  /* Read battery percentage (8-bit) */
  ret = pipower5_read_byte_data(pi_dev, REG_READ_BATTERY_PERCENTAGE);
  if (ret >= 0) {
    pi_dev->battery_percentage = (u8)ret;
  } else {
    return ret;
  }

  /* Read battery capacity (8-bit) */
  ret = pipower5_read_byte_data(pi_dev, REG_READ_BATTERY_CAPACITY);
  if (ret >= 0) {
    pi_dev->battery_capacity = (u8)ret;
  } else {
    return ret;
  }

  /* Read power source (8-bit) */
  ret = pipower5_read_byte_data(pi_dev, REG_READ_POWER_SOURCE);
  if (ret >= 0) {
    pi_dev->power_source = (u8)ret;
  } else {
    return ret;
  }

  /* Read input plugged in status (8-bit) */
  ret = pipower5_read_byte_data(pi_dev, REG_READ_IS_INPUT_PLUGGED_IN);
  if (ret >= 0) {
    pi_dev->is_input_plugged_in = (u8)ret;
  } else {
    return ret;
  }

  /* Read charging status (8-bit) */
  ret = pipower5_read_byte_data(pi_dev, REG_READ_IS_CHARGING);
  if (ret >= 0) {
    pi_dev->is_charging = (u8)ret;
  } else {
    return ret;
  }

  /* Read shutdown request (8-bit) */
  ret = pipower5_read_byte_data(pi_dev, REG_READ_SHUTDOWN_REQUEST);
  if (ret >= 0) {
    pi_dev->shutdown_request = (u8)ret;
  } else {
    return ret;
  }

  /* Read firmware version (3 bytes) */
  ret = pipower5_read_byte_data(pi_dev, REG_READ_FIRMWARE_VERSION_MAJOR);
  if (ret >= 0) {
    pi_dev->fw_major = (u8)ret;
  } else {
    return ret;
  }

  ret = pipower5_read_byte_data(pi_dev, REG_READ_FIRMWARE_VERSION_MINOR);
  if (ret >= 0) {
    pi_dev->fw_minor = (u8)ret;
  } else {
    return ret;
  }

  ret = pipower5_read_byte_data(pi_dev, REG_READ_FIRMWARE_VERSION_PATCH);
  if (ret >= 0) {
    pi_dev->fw_patch = (u8)ret;
  } else {
    return ret;
  }

  /* Read default on status (8-bit) */
  ret = pipower5_read_byte_data(pi_dev, REG_READ_DEFAULT_ON);
  if (ret >= 0) {
    pi_dev->default_on = (u8)ret;
  } else {
    return ret;
  }

  /* Read board ID (2 bytes) */
  ret = pipower5_read_word_data(pi_dev, REG_READ_BOARD_ID_H);
  if (ret >= 0) {
    pi_dev->board_id = (u16)ret;
  } else {
    return ret;
  }

  /* Read shutdown percentage (8-bit) */
  ret = pipower5_read_byte_data(pi_dev, REG_READ_SHUTDOWN_PERCENTAGE);
  if (ret >= 0) {
    pi_dev->shutdown_percentage = (u8)ret;
  } else {
    return ret;
  }

  /* Read battery internal resistor (16-bit) */
  ret = pipower5_read_word_data(pi_dev, REG_READ_BATTERY_INTERNAL_RESISTOR);
  if (ret >= 0) {
    pi_dev->battery_internal_resistor = (u16)ret;
  } else {
    return ret;
  }

  /* Read power button state (8-bit) */
  ret = pipower5_read_byte_data(pi_dev, REG_READ_POWER_BUTTON_STATE);
  if (ret >= 0) {
    pi_dev->power_button_state = (u8)ret;
  } else {
    return ret;
  }

  /* Read charge current max (8-bit) */
  ret = pipower5_read_byte_data(pi_dev, REG_READ_CHARGE_CURRENT_MAX);
  if (ret >= 0) {
    pi_dev->charge_current_max = (u8)ret;
  } else {
    return ret;
  }

  /* Read buzzer volume (8-bit) */
  ret = pipower5_read_byte_data(pi_dev, REG_READ_BUZZER_VOLUME);
  if (ret >= 0) {
    pi_dev->buzzer_volume = (u8)ret;
  } else {
    return ret;
  }

  return 0;
}

MODULE_AUTHOR("SunFounder <service@sunfounder.com>");
MODULE_DESCRIPTION("PiPower5 I2C Communication Functions");
MODULE_LICENSE("GPL v2");