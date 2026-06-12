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
#include <linux/input.h>
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
#define PIPOWER5_DRIVER_VERSION "2.1.0"

/* Device ID values */
#define PIPOWER5_DEVICE_ID 0x50 /* Example device ID */

/* Polling interval in milliseconds */
#define PIPOWER5_POLL_INTERVAL 500  /* 2 Hz, faster power event detection */
#define PIPOWER5_BUTTON_POLL_INTERVAL 20  /* 50 Hz for responsive button */

/* Constants */
#define PIPOWER5_BATTERY_MAX_VOLTAGE 8400 /* mV */
#define PIPOWER5_BATTERY_STANDARD_VOLTAGE 7400 /* mV */
#define PIPOWER5_BATTERY_MIN_VOLTAGE 6400 /* mV */
#define PIPOWER5_BATTERY_FULL_CHARGE_MAH 2000 /* mAh */

/* Buzzer playback */
#define PIPOWER5_MAX_BUZZER_SEQUENCE 32

struct buzzer_note {
  u16 freq;
  u16 duration_ms;
};

struct pipower5_device {
  struct i2c_client *client;
  struct mutex lock;
  struct device *hwmon_dev;
  struct power_supply *power_supply;
  struct device *pipower5_dev;

  /* Polling and workqueue */
  struct workqueue_struct *wq;
  struct delayed_work poll_work;
  struct delayed_work button_poll_work;
  bool events_initialized;

  /* Cached values */
  u16 input_voltage;
  u16 input_current;
  u16 output_voltage;
  u16 output_current;
  u16 battery_voltage;
  u16 battery_current;   /* raw; use (s16) cast: +charge, -discharge */
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
  u8 last_power_button_state;
  unsigned long button_event_jiffies;  /* timestamp for 2s hold */
  u8 charge_current_max;
  struct input_dev *input_dev;

  /* VBUS control (for power failure simulation) */
  bool vbus_enabled;

  /* ── Cumulative tracking (always updated every poll) ──────────── */
  u64 mah_consumed;               /* mAh*1000 — cumulative discharge since boot */
  unsigned long last_sample_jiffies;
  u32 estimated_runtime;          /* seconds at current discharge rate */

  /* ── Power failure test ────────────────────────────────────────── */
  struct delayed_work pft_work;
  bool pft_running;
  u32 pft_elapsed;
  u32 pft_test_time;
  unsigned long pft_start_jiffies;
  u64 pft_mah_start;              /* snapshot of mah_consumed at test start */
  u8  pft_bat_pct_start;          /* snapshot of battery_percentage at test start */
  /* Running aggregates during test period */
  u32 pft_samples;
  u64 pft_bat_v_sum, pft_bat_c_sum, pft_out_v_sum, pft_out_c_sum;
  u16 pft_bat_v_max, pft_bat_c_max, pft_out_v_max, pft_out_c_max;
  u16 pft_bat_v_min, pft_bat_c_min, pft_out_v_min, pft_out_c_min;
  char pft_result[512];

  /* State tracking for event detection */
  u8 last_is_input_plugged_in;
  u8 last_power_source;
  u8 last_is_charging;
  unsigned long power_restored_jiffies;  /* debounce: skip POWER_INSUFFICIENT for 5s after restore */
  u8 buzzer_volume;

  /* Buzzer playback sequence */
  struct delayed_work buzzer_work;
  struct buzzer_note buzzer_notes[PIPOWER5_MAX_BUZZER_SEQUENCE];
  int buzzer_note_count;
  int buzzer_note_index;
  bool buzzer_playing;

  /* Event log ring buffer */
  #define PIPOWER5_EVENT_LOG_SIZE 16
  #define PIPOWER5_EVENT_MSG_LEN 128
  char event_log[PIPOWER5_EVENT_LOG_SIZE][PIPOWER5_EVENT_MSG_LEN];
  unsigned long event_times[PIPOWER5_EVENT_LOG_SIZE];
  int event_head;
  int event_count;
};

/*
 * Low-level I2C primitives — caller MUST hold pi_dev->lock.
 * Named with leading __ to signal this requirement.
 */
int __pipower5_read_word(struct pipower5_device *pi_dev, u8 reg);
int __pipower5_read_byte(struct pipower5_device *pi_dev, u8 reg);
int __pipower5_write_byte(struct pipower5_device *pi_dev, u8 reg, u8 value);
int __pipower5_write_word(struct pipower5_device *pi_dev, u8 reg, u16 value);
int __pipower5_write_block(struct pipower5_device *pi_dev, u8 cmd, u8 *data, u8 len);
int __pipower5_read_raw_byte(struct pipower5_device *pi_dev);
int pipower5_update_status(struct pipower5_device *pi_dev);
int pipower5_enable_vbus(struct pipower5_device *pi_dev);
int pipower5_disable_vbus(struct pipower5_device *pi_dev);

/* Function prototypes for sysfs operations */
int pipower5_create_sysfs(struct pipower5_device *pi_dev);
void pipower5_remove_sysfs(struct pipower5_device *pi_dev);
void pipower5_buzzer_init(struct pipower5_device *pi_dev);
void pipower5_buzzer_event(struct pipower5_device *pi_dev, const char *event_name);
void pipower5_buzz_seq_load(const char *buf, size_t len);
void pipower5_stats_init(struct pipower5_device *pi_dev);
void pipower5_stats_update(struct pipower5_device *pi_dev);
void pipower5_pft_init(struct pipower5_device *pi_dev);
void pipower5_pft_start(struct pipower5_device *pi_dev, u32 test_time);
void pipower5_pft_cancel(struct pipower5_device *pi_dev);

/* Module parameters (extern for sysfs access) */
extern unsigned int buzz_on;
extern unsigned int buzzer_volume;
extern unsigned int shutdown_pct;

/* Function prototypes for upower operations */
int pipower5_create_upower(struct pipower5_device *pi_dev);
void pipower5_remove_upower(struct pipower5_device *pi_dev);

/* Function prototypes for button operations */
int pipower5_button_init(struct pipower5_device *pi_dev);
void pipower5_button_cleanup(struct pipower5_device *pi_dev);
void pipower5_button_check(struct pipower5_device *pi_dev);

/* Function prototypes for shutdown operations */
void pipower5_log_event(struct pipower5_device *pi_dev, const char *fmt, ...);
void pipower5_handle_shutdown(struct pipower5_device *pi_dev);

#endif /* _PIPOWER5_H */