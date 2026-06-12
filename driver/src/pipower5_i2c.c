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

/*
 * Low-level I2C primitives — caller MUST hold pi_dev->lock.
 * No internal locking: the caller is responsible for serialisation.
 * This avoids mutex self-deadlock when a locked caller calls these.
 */
int __pipower5_read_word(struct pipower5_device *pi_dev, u8 reg) {
  int ret;

  ret = i2c_smbus_read_word_data(pi_dev->client, reg);
  if (ret < 0) {
    dev_err(&pi_dev->client->dev,
            "Failed to read word from register 0x%02x: %d\n", reg, ret);
    return ret;
  }

  return ret;
}

int __pipower5_read_byte(struct pipower5_device *pi_dev, u8 reg) {
  int ret;

  ret = i2c_smbus_read_byte_data(pi_dev->client, reg);
  if (ret < 0) {
    dev_err(&pi_dev->client->dev,
            "Failed to read byte from register 0x%02x: %d\n", reg, ret);
    return ret;
  }

  return ret;
}

int __pipower5_write_byte(struct pipower5_device *pi_dev, u8 reg, u8 value) {
  int ret;

  ret = i2c_smbus_write_byte_data(pi_dev->client, reg, value);
  if (ret < 0) {
    dev_err(&pi_dev->client->dev,
            "Failed to write 0x%02x to register 0x%02x: %d\n", value, reg, ret);
    return ret;
  }

  return 0;
}

/* Raw I2C write (no SMBus protocol, just i2c_master_send) — caller holds lock */
int __pipower5_write_block(struct pipower5_device *pi_dev, u8 cmd, u8 *data, u8 len) {
  u8 buf[8];  /* cmd + up to 7 data bytes */
  struct i2c_msg msg = {
    .addr = pi_dev->client->addr,
    .flags = 0,
    .len = len + 1,
    .buf = buf,
  };
  if (len + 1 > sizeof(buf))
    return -EINVAL;
  buf[0] = cmd;
  memcpy(buf + 1, data, len);
  int ret = i2c_transfer(pi_dev->client->adapter, &msg, 1);
  if (ret < 0) {
    dev_err(&pi_dev->client->dev, "raw i2c write cmd=0x%02x failed: %d\n", cmd, ret);
    return ret;
  }
  return 0;
}

/* Raw I2C read (no register address, just i2c_master_recv) — caller holds lock */
int __pipower5_read_raw_byte(struct pipower5_device *pi_dev) {
  u8 val;
  struct i2c_msg msg = {
    .addr = pi_dev->client->addr,
    .flags = I2C_M_RD,
    .len = 1,
    .buf = &val,
  };
  int ret = i2c_transfer(pi_dev->client->adapter, &msg, 1);
  if (ret < 0) {
    dev_err(&pi_dev->client->dev, "raw i2c read failed: %d\n", ret);
    return ret;
  }
  return val;
}

/*
 * Read all registers in one pass, holding pi_dev->lock for the entire
 * I2C transaction batch.  This is more efficient than lock/unlock per
 * register and prevents sysfs readers from seeing half-updated data.
 */
int pipower5_update_status(struct pipower5_device *pi_dev) {
  int ret;

  mutex_lock(&pi_dev->lock);

  /* Read input voltage (16-bit) */
  ret = __pipower5_read_word(pi_dev, REG_READ_INPUT_VOLTAGE);
  if (ret >= 0)
    pi_dev->input_voltage = (u16)ret;
  else
    goto out;

  ret = __pipower5_read_word(pi_dev, REG_READ_INPUT_CURRENT);
  if (ret >= 0)
    pi_dev->input_current = (u16)ret;
  else
    goto out;

  ret = __pipower5_read_word(pi_dev, REG_READ_OUTPUT_VOLTAGE);
  if (ret >= 0)
    pi_dev->output_voltage = (u16)ret;
  else
    goto out;

  ret = __pipower5_read_word(pi_dev, REG_READ_OUTPUT_CURRENT);
  if (ret >= 0)
    pi_dev->output_current = (u16)ret;
  else
    goto out;

  ret = __pipower5_read_word(pi_dev, REG_READ_BATTERY_VOLTAGE);
  if (ret >= 0)
    pi_dev->battery_voltage = (u16)ret;
  else
    goto out;

  ret = __pipower5_read_word(pi_dev, REG_READ_BATTERY_CURRENT);
  if (ret >= 0)
    pi_dev->battery_current = (u16)ret;
  else
    goto out;

  ret = __pipower5_read_byte(pi_dev, REG_READ_BATTERY_PERCENTAGE);
  if (ret >= 0)
    pi_dev->battery_percentage = (u8)ret;
  else
    goto out;

  ret = __pipower5_read_byte(pi_dev, REG_READ_BATTERY_CAPACITY);
  if (ret >= 0)
    pi_dev->battery_capacity = (u8)ret;
  else
    goto out;

  ret = __pipower5_read_byte(pi_dev, REG_READ_POWER_SOURCE);
  if (ret >= 0)
    pi_dev->power_source = (u8)ret;
  else
    goto out;

  ret = __pipower5_read_byte(pi_dev, REG_READ_IS_INPUT_PLUGGED_IN);
  if (ret >= 0)
    pi_dev->is_input_plugged_in = (u8)ret;
  else
    goto out;

  ret = __pipower5_read_byte(pi_dev, REG_READ_IS_CHARGING);
  if (ret >= 0)
    pi_dev->is_charging = (u8)ret;
  else
    goto out;

  ret = __pipower5_read_byte(pi_dev, REG_READ_SHUTDOWN_REQUEST);
  if (ret >= 0)
    pi_dev->shutdown_request = (u8)ret;
  else
    goto out;

  ret = __pipower5_read_byte(pi_dev, REG_READ_FIRMWARE_VERSION_MAJOR);
  if (ret >= 0)
    pi_dev->fw_major = (u8)ret;
  else
    goto out;

  ret = __pipower5_read_byte(pi_dev, REG_READ_FIRMWARE_VERSION_MINOR);
  if (ret >= 0)
    pi_dev->fw_minor = (u8)ret;
  else
    goto out;

  ret = __pipower5_read_byte(pi_dev, REG_READ_FIRMWARE_VERSION_PATCH);
  if (ret >= 0)
    pi_dev->fw_patch = (u8)ret;
  else
    goto out;

  ret = __pipower5_read_byte(pi_dev, REG_READ_DEFAULT_ON);
  if (ret >= 0)
    pi_dev->default_on = (u8)ret;
  else
    goto out;

  ret = __pipower5_read_word(pi_dev, REG_READ_BOARD_ID_H);
  if (ret >= 0)
    pi_dev->board_id = (u16)ret;
  else
    goto out;

  ret = __pipower5_read_byte(pi_dev, REG_READ_SHUTDOWN_PERCENTAGE);
  if (ret >= 0)
    pi_dev->shutdown_percentage = (u8)ret;
  else
    goto out;

  ret = __pipower5_read_word(pi_dev, REG_READ_BATTERY_INTERNAL_RESISTOR);
  if (ret >= 0)
    pi_dev->battery_internal_resistor = (u16)ret;
  else
    goto out;

  ret = __pipower5_read_byte(pi_dev, REG_READ_POWER_BUTTON_STATE);
  if (ret >= 0) {
    pi_dev->power_button_state = (u8)ret;
    /* Reset button state register so next poll gets fresh value */
    __pipower5_write_byte(pi_dev, REG_WRITE_POWER_BTN_STATE, 0);
  } else
    goto out;

  ret = __pipower5_read_byte(pi_dev, REG_READ_CHARGE_CURRENT_MAX);
  if (ret >= 0)
    pi_dev->charge_current_max = (u8)ret;
  else
    goto out;

  ret = __pipower5_read_byte(pi_dev, REG_READ_BUZZER_VOLUME);
  if (ret >= 0)
    /* MCU returns 0-100, expose 0-10 to userspace */
    pi_dev->buzzer_volume = (u8)(ret >= 99 ? 10 : ret / 10);
  else
    goto out;

out:
  mutex_unlock(&pi_dev->lock);
  return ret;
}

/* ADV_CMD protocol for VBUS control (power failure simulation).
 * Sends block command and waits for status byte.
 *   ADV_CMD_START=0xAC, ADV_CMD_VBUS_EN=0x01, ADV_CMD_END=0xAE
 *   OK=0xE0, ERR=0xEF
 */
#define ADV_CMD_START  0xAC
#define ADV_CMD_VBUS_EN 0x01
#define ADV_CMD_END    0xAE
#define ADV_CMD_OK     0xE0
#define ADV_CMD_TIMEOUT_MS 5000  /* 5s timeout for ADV_CMD response */

int pipower5_enable_vbus(struct pipower5_device *pi_dev) {
  u8 cmd[] = {ADV_CMD_VBUS_EN, 1, ADV_CMD_END};
  int status, retries = 0;
  unsigned long deadline = jiffies + msecs_to_jiffies(ADV_CMD_TIMEOUT_MS);

  mutex_lock(&pi_dev->lock);
  while (time_before(jiffies, deadline)) {
    retries++;
    __pipower5_write_block(pi_dev, ADV_CMD_START, cmd, sizeof(cmd));
    status = __pipower5_read_raw_byte(pi_dev);
    if (status == ADV_CMD_OK) {
      mutex_unlock(&pi_dev->lock);
      pi_dev->vbus_enabled = true;
      dev_info(&pi_dev->client->dev, "VBUS enabled after %d retries\n", retries);
      return 0;
    }
  }
  mutex_unlock(&pi_dev->lock);
  dev_err(&pi_dev->client->dev, "VBUS enable failed after %d retries\n", retries);
  return -EIO;
}

int pipower5_disable_vbus(struct pipower5_device *pi_dev) {
  u8 cmd[] = {ADV_CMD_VBUS_EN, 0, ADV_CMD_END};
  int status, retries = 0;
  unsigned long deadline = jiffies + msecs_to_jiffies(ADV_CMD_TIMEOUT_MS);

  mutex_lock(&pi_dev->lock);
  while (time_before(jiffies, deadline)) {
    retries++;
    __pipower5_write_block(pi_dev, ADV_CMD_START, cmd, sizeof(cmd));
    status = __pipower5_read_raw_byte(pi_dev);
    if (status == ADV_CMD_OK) {
      mutex_unlock(&pi_dev->lock);
      pi_dev->vbus_enabled = false;
      dev_info(&pi_dev->client->dev, "VBUS disabled after %d retries\n", retries);
      return 0;
    }
  }
  mutex_unlock(&pi_dev->lock);
  dev_err(&pi_dev->client->dev, "VBUS disable failed after %d retries\n", retries);
  return -EIO;
}

MODULE_AUTHOR("SunFounder <service@sunfounder.com>");
MODULE_DESCRIPTION("PiPower5 I2C Communication Functions");
MODULE_LICENSE("GPL v2");