/*
 * PiPower5 I2C Driver Header
 *
 * Copyright (c) 2026 Your Name <your.email@example.com>
 * Based on various power supply drivers in the Linux kernel
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 */

#ifndef _PIPOWER5_H
#define _PIPOWER5_H

#include <linux/device.h>
#include <linux/i2c.h>
#include <linux/mutex.h>
#include <linux/timer.h>
#include <linux/workqueue.h>

/* I2C Register definitions */
#define REG_READ_INPUT_VOLTAGE 0        /* 16-bit, unit: mV */
#define REG_READ_INPUT_CURRENT 2        /* 16-bit, unit: mA */
#define REG_READ_OUTPUT_VOLTAGE 4       /* 16-bit, unit: mV */
#define REG_READ_OUTPUT_CURRENT 6       /* 16-bit, unit: mA */
#define REG_READ_BATTERY_VOLTAGE 8      /* 16-bit, unit: mV */
#define REG_READ_BATTERY_CURRENT 10     /* 16-bit, unit: mA */
#define REG_READ_BATTERY_PERCENTAGE 12  /* 8-bit, unit: % */
#define REG_READ_BATTERY_CAPACITY 13    /* 8-bit, unit: % */
#define REG_READ_POWER_SOURCE 15        /* 8-bit, 0=USB, 1=Battery */
#define REG_READ_IS_INPUT_PLUGGED_IN 16 /* 8-bit, 0=Not plugged, 1=Plugged */
#define REG_READ_IS_CHARGING 18         /* 8-bit, 0=Not charging, 1=Charging */
#define REG_READ_SHUTDOWN_REQUEST 20    /* 8-bit, 0=No, 1=Yes */

#define REG_READ_FIRMWARE_VERSION_MAJOR 128
#define REG_READ_FIRMWARE_VERSION_MINOR 129
#define REG_READ_FIRMWARE_VERSION_PATCH 130

#define REG_READ_DEFAULT_ON 139

#define REG_READ_BOARD_ID_H 140
#define REG_READ_BOARD_ID_L 141

#define REG_READ_SHUTDOWN_PERCENTAGE 143

#define REG_READ_BATTERY_INTERNAL_RESISTOR 145 /* 16-bit, unit: mΩ */

#define REG_READ_POWER_BUTTON_STATE 154
#define REG_READ_CHARGE_CURRENT_MAX 155 /* N*100mA */
#define REG_READ_BUZZER_VOLUME 162      /* 8-bit, unit: % */

#define REG_WRITE_SHUTDOWN_PERCENTAGE 9
#define REG_WRITE_CHARGE_SELECT 11
#define REG_WRITE_POWER_BTN_STATE 12
#define REG_WRITE_BUZZER_FEQ_L 13
#define REG_WRITE_BUZZER_FEQ_H 14
#define REG_WRITE_BUZZER_VOL 15

/* Shutdown request values */
#define SHUTDOWN_REQUEST_NONE 0
#define SHUTDOWN_REQUEST_LOW_BATTERY 1
#define SHUTDOWN_REQUEST_BUTTON 2
#define SHUTDOWN_REQUEST_LOW_VOLTAGE 3

/* Driver version */
#define PIPOWER5_DRIVER_VERSION "1.0.0"

/* Device ID values */
#define PIPOWER5_DEVICE_ID 0x50 /* Example device ID */

/* Polling interval in milliseconds */
#define PIPOWER5_POLL_INTERVAL 1000

/* Constants */
#define PIPOWER5_BATTERY_MAX_VOLTAGE 8400 /* mV */
#define PIPOWER5_BATTERY_STANDARD_VOLTAGE 7400 /* mV */
#define PIPOWER5_BATTERY_MIN_VOLTAGE 6400 /* mV */
#define PIPOWER5_BATTERY_FULL_CHARGE_MAH 2000 /* mAh */

struct pipower5_device {
  struct i2c_client *client;
  struct mutex lock;
  struct device *hwmon_dev;
  struct power_supply *power_supply;
  struct device *pipower5_dev;

  /* Polling and workqueue */
  struct workqueue_struct *wq;
  struct delayed_work poll_work;

  /* Input device for power button */
  struct input_dev *input_dev;
  int power_button_irq;

  /* Cached values */
  u16 input_voltage;
  u16 input_current;
  u16 output_voltage;
  u16 output_current;
  u16 battery_voltage;
  u16 battery_current;
  u8 battery_percentage;
  u8 battery_capacity;
  u8 power_source;
  u8 is_input_plugged_in;
  u8 is_charging;
  u8 shutdown_request;
  u8 fw_major;
  u8 fw_minor;
  u8 fw_patch;
  u8 default_on;
  u16 board_id;
  u8 shutdown_percentage;
  u16 battery_internal_resistor;
  u8 power_button_state;
  u8 charge_current_max;
  u8 buzzer_volume;
  u8 last_power_button_state;
};

/* Function prototypes for I2C operations */
int pipower5_read_word_data(struct pipower5_device *pi_dev, u8 reg);
int pipower5_read_byte_data(struct pipower5_device *pi_dev, u8 reg);
int pipower5_write_byte_data(struct pipower5_device *pi_dev, u8 reg, u8 value);
int pipower5_update_status(struct pipower5_device *pi_dev);

/* Function prototypes for sysfs operations */
int pipower5_create_sysfs(struct pipower5_device *pi_dev);
void pipower5_remove_sysfs(struct pipower5_device *pi_dev);

/* Function prototypes for upower operations */
int pipower5_create_upower(struct pipower5_device *pi_dev);
void pipower5_remove_upower(struct pipower5_device *pi_dev);

/* Function prototypes for button operations */
int pipower5_button_init(struct pipower5_device *pi_dev);
void pipower5_button_cleanup(struct pipower5_device *pi_dev);
void pipower5_button_check(struct pipower5_device *pi_dev);

/* Function prototypes for shutdown operations */
void pipower5_handle_shutdown(struct pipower5_device *pi_dev);

#endif /* _PIPOWER5_H */