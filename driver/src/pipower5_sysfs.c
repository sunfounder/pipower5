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
#include <linux/string.h>
#include <linux/sysfs.h>
#include <linux/workqueue.h>

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

  /* Do I2C write + cache update under one lock */
  mutex_lock(&pi_dev->lock);
  ret = __pipower5_write_byte(pi_dev, REG_WRITE_SHUTDOWN_PERCENTAGE,
                              (u8)value);
  if (ret == 0) {
    pi_dev->shutdown_percentage = (u8)value;
    ret = count;
  }
  mutex_unlock(&pi_dev->lock);

  return ret;
}

static struct device_attribute dev_attr_shutdown_percentage =
    __ATTR(shutdown_percentage, 0664, shutdown_percentage_show,
           shutdown_percentage_store);

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

  /* Only accept 0 to reset the power button state register */
  if (value != 0)
    return -EINVAL;

  /* Hold lock for the I2C write */
  mutex_lock(&pi_dev->lock);
  ret = __pipower5_write_byte(pi_dev, REG_WRITE_POWER_BTN_STATE, 0);
  mutex_unlock(&pi_dev->lock);

  if (ret == 0)
    return count;
  return ret;
}

static struct device_attribute dev_attr_power_button_state =
    __ATTR(power_button_state, 0664, power_button_state_show,
           power_button_state_store);

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

  /* Cache update + I2C write under one lock */
  mutex_lock(&pi_dev->lock);
  pi_dev->buzzer_volume = (u8)value;
  ret = __pipower5_write_byte(pi_dev, REG_WRITE_BUZZER_VOL, (u8)value);
  mutex_unlock(&pi_dev->lock);

  if (ret < 0) {
    return ret;
  }

  return count;
}

static struct device_attribute dev_attr_buzzer_volume =
    __ATTR(buzzer_volume, 0664, buzzer_volume_show,
           buzzer_volume_store);

/* ==================== Buzzer Playback ==================== */

/* Maximum duration for a single continuous tone (5s safety limit). */
#define PIPOWER5_BUZZER_MAX_SINGLE_MS  5000
/* Maximum per-note duration (30s safety limit). */
#define PIPOWER5_BUZZER_MAX_NOTE_MS   30000

/*
 * Buzzer work callback — runs on pi_dev->wq.
 * Writes frequencies to hardware with explicit lock management:
 * caller holds no lock, this function acquires/releases as needed.
 */
static void pipower5_buzzer_work_func(struct work_struct *work) {
  struct delayed_work *dwork = to_delayed_work(work);
  struct pipower5_device *pi_dev =
      container_of(dwork, struct pipower5_device, buzzer_work);
  struct buzzer_note *note;

  /* Safety: no more notes or empty sequence → silence */
  if (pi_dev->buzzer_note_index >= pi_dev->buzzer_note_count) {
    mutex_lock(&pi_dev->lock);
    __pipower5_write_byte(pi_dev, REG_WRITE_BUZZER_FEQ_L, 0);
    __pipower5_write_byte(pi_dev, REG_WRITE_BUZZER_FEQ_H, 0);
    mutex_unlock(&pi_dev->lock);
    pi_dev->buzzer_playing = false;
    return;
  }

  note = &pi_dev->buzzer_notes[pi_dev->buzzer_note_index];

  if (pi_dev->buzzer_playing) {
    /* Finished playing current note → turn off buzzer, advance */
    mutex_lock(&pi_dev->lock);
    __pipower5_write_byte(pi_dev, REG_WRITE_BUZZER_FEQ_L, 0);
    __pipower5_write_byte(pi_dev, REG_WRITE_BUZZER_FEQ_H, 0);
    mutex_unlock(&pi_dev->lock);
    pi_dev->buzzer_playing = false;
    pi_dev->buzzer_note_index++;

    if (pi_dev->buzzer_note_index < pi_dev->buzzer_note_count) {
      /* Start next note immediately */
      queue_delayed_work(pi_dev->wq, &pi_dev->buzzer_work, 0);
    }
  } else {
    /* Start playing a new note */
    mutex_lock(&pi_dev->lock);
    __pipower5_write_byte(pi_dev, REG_WRITE_BUZZER_FEQ_L,
                          note->freq & 0xFF);
    __pipower5_write_byte(pi_dev, REG_WRITE_BUZZER_FEQ_H,
                          (note->freq >> 8) & 0xFF);
    mutex_unlock(&pi_dev->lock);
    pi_dev->buzzer_playing = true;

    /* Schedule note-off after duration (with safety cap) */
    if (note->duration_ms > 0) {
      unsigned int dur = note->duration_ms;
      if (dur > PIPOWER5_BUZZER_MAX_NOTE_MS)
        dur = PIPOWER5_BUZZER_MAX_NOTE_MS;
      queue_delayed_work(pi_dev->wq, &pi_dev->buzzer_work,
                         msecs_to_jiffies(dur));
    } else {
      /* Zero duration → turn off immediately */
      queue_delayed_work(pi_dev->wq, &pi_dev->buzzer_work, 1);
    }
  }
}

/*
 * buzzer_play write-only sysfs:
 *   Event name: "power_disconnected" → plays built-in sequence
 *   Sequence:   "freq,dur;freq,dur;..."
 *   Single:     "freq"  → auto-stops after 5 s
 *   Stop:       "0"     → immediate silence
 */

/* Event name -> buzzer sequence lookup table */
/* Event name -> buzzer sequence lookup */
static const struct {
  const char *name;
  const char *seq;
} buzzer_events[] = {
  {"battery_activated",                 "1046,50;0,100;1975,50"},
  {"low_battery",                       "1046,50;0,100;1046,50"},
  {"power_disconnected",                "1174,50;0,100;784,50"},
  {"power_restored",                    "784,50;0,100;1174,50"},
  {"power_insufficient",                "987,50;0,100;987,50;0,100;987,100"},
  {"battery_critical_shutdown",         "2093,50;0,60;2093,50;0,60;2093,100"},
  {"battery_voltage_critical_shutdown", "2093,50;0,60;2093,50;0,60;2093,100;0,60;2093,100"},
};

static const char *buzzer_lookup_event(const char *name) {
  int i;
  for (i = 0; i < ARRAY_SIZE(buzzer_events); i++) {
    if (strcmp(name, buzzer_events[i].name) == 0)
      return buzzer_events[i].seq;
  }
  return NULL;
}

static ssize_t buzzer_play_store(struct device *dev,
                                 struct device_attribute *attr,
                                 const char *buf, size_t count) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  char *tmp, *pair, *token;
  int i = 0;
  unsigned int single_freq;
  const char *seq;
  char trimmed[64];

  /* Cancel any ongoing playback */
  cancel_delayed_work_sync(&pi_dev->buzzer_work);

  pi_dev->buzzer_note_count = 0;
  pi_dev->buzzer_note_index = 0;
  pi_dev->buzzer_playing = false;

  /* Trim trailing newline */
  strscpy(trimmed, buf, sizeof(trimmed));
  trimmed[strcspn(trimmed, "\n")] = '\0';

  /* Check for event name (no comma/semicolon, not a number) */
  if (!strpbrk(trimmed, ",;") && sscanf(trimmed, "%u", &single_freq) != 1) {
    seq = buzzer_lookup_event(trimmed);
    if (seq) {
      /* Found event -> use built-in sequence, skip kstrndup */
      tmp = kstrdup(seq, GFP_KERNEL);
      if (!tmp) return count;
      goto parse_loop;
    }
    /* Unknown name, treat as stop */
    mutex_lock(&pi_dev->lock);
    __pipower5_write_byte(pi_dev, REG_WRITE_BUZZER_FEQ_L, 0);
    __pipower5_write_byte(pi_dev, REG_WRITE_BUZZER_FEQ_H, 0);
    mutex_unlock(&pi_dev->lock);
    dev_warn(dev, "buzzer_play: unknown event '%s'\n", trimmed);
    return count;
  }

  /* Single-frequency mode (no comma/semicolon, is a number) */
  if (!strpbrk(buf, ",;")) {
    if (sscanf(buf, "%u", &single_freq) == 1) {
      if (single_freq == 0 || single_freq > 65534) {
        mutex_lock(&pi_dev->lock);
        __pipower5_write_byte(pi_dev, REG_WRITE_BUZZER_FEQ_L, 0);
        __pipower5_write_byte(pi_dev, REG_WRITE_BUZZER_FEQ_H, 0);
        mutex_unlock(&pi_dev->lock);
      } else {
        mutex_lock(&pi_dev->lock);
        __pipower5_write_byte(pi_dev, REG_WRITE_BUZZER_FEQ_L,
                              single_freq & 0xFF);
        __pipower5_write_byte(pi_dev, REG_WRITE_BUZZER_FEQ_H,
                              (single_freq >> 8) & 0xFF);
        mutex_unlock(&pi_dev->lock);
        pi_dev->buzzer_notes[0].freq = (u16)single_freq;
        pi_dev->buzzer_notes[0].duration_ms = PIPOWER5_BUZZER_MAX_SINGLE_MS;
        pi_dev->buzzer_note_count = 1;
        pi_dev->buzzer_note_index = 0;
        pi_dev->buzzer_playing = true;
        queue_delayed_work(pi_dev->wq, &pi_dev->buzzer_work,
                           msecs_to_jiffies(PIPOWER5_BUZZER_MAX_SINGLE_MS));
      }
    }
    return count;
  }

  /* Blank/newline only -> stop */
  if (count <= 1)
    return count;

  /* Make a writable copy for strsep */
parse_sequence:
  tmp = kstrndup(buf, count, GFP_KERNEL);
  if (!tmp)
    return -ENOMEM;

  /* Parse "freq,dur;freq,dur;..." pairs */
parse_loop:
  pair = tmp;
  while ((token = strsep(&pair, ";\n")) != NULL) {
    unsigned int freq, dur;

    /* Skip empty tokens */
    while (*token == ' ' || *token == '\t')
      token++;
    if (*token == '\0')
      continue;

    if (sscanf(token, "%u,%u", &freq, &dur) != 2)
      continue;
    if (i >= PIPOWER5_MAX_BUZZER_SEQUENCE)
      break;

    /* Cap per-note duration */
    if (dur > PIPOWER5_BUZZER_MAX_NOTE_MS)
      dur = PIPOWER5_BUZZER_MAX_NOTE_MS;

    pi_dev->buzzer_notes[i].freq = (u16)freq;
    pi_dev->buzzer_notes[i].duration_ms = (u16)dur;
    i++;
  }

  kfree(tmp);
  pi_dev->buzzer_note_count = i;

  if (i > 0) {
    /* Start playback */
    pi_dev->buzzer_note_index = 0;
    pi_dev->buzzer_playing = false;
    queue_delayed_work(pi_dev->wq, &pi_dev->buzzer_work, 0);
  }

  return count;
}

static struct device_attribute dev_attr_buzzer_play =
    __ATTR(buzzer_play, 0664, NULL, buzzer_play_store);

/* Initialise buzzer delayed work (called from probe) */
void pipower5_buzzer_init(struct pipower5_device *pi_dev) {
  INIT_DELAYED_WORK(&pi_dev->buzzer_work, pipower5_buzzer_work_func);
  pi_dev->buzzer_note_count = 0;
  pi_dev->buzzer_note_index = 0;
  pi_dev->buzzer_playing = false;
}

/* ── Event-triggered buzzer ────────────────────────────────────────────── */

/* Default sequences (freq,dur;freq,dur;...) — matching old Python config */
static const char *buzzer_default_seq[] = {
  "1046,50;0,100;1975,50",                    /* battery_activated */
  "1046,50;0,100;1046,50",                    /* low_battery */
  "1174,50;0,100;784,50",                     /* power_disconnected */
  "784,50;0,100;1174,50",                     /* power_restored */
  "987,50;0,100;987,50;0,100;987,100",        /* power_insufficient */
  "2093,50;0,60;2093,50;0,60;2093,100",       /* critical_shutdown */
  "2093,50;0,60;2093,50;0,60;2093,100;0,60;2093,100", /* voltage_critical */
};

/* Event-triggered buzzer: lookup event name in table and play sequence */
void pipower5_buzzer_event(struct pipower5_device *pi_dev, const char *event_name)
{
  const char *seq = buzzer_lookup_event(event_name);
  char *tmp, *pair, *token;
  int i = 0;
  unsigned int freq, dur;

  if (!seq)
    return;
  if (!buzz_on)  /* bitmask 0 = all disabled */
    return;

  cancel_delayed_work_sync(&pi_dev->buzzer_work);
  pi_dev->buzzer_note_count = 0;
  pi_dev->buzzer_note_index = 0;
  pi_dev->buzzer_playing = false;

  tmp = kstrdup(seq, GFP_KERNEL);
  if (!tmp) return;

  pair = tmp;
  while ((token = strsep(&pair, ";")) != NULL) {
    while (*token == ' ' || *token == '\t') token++;
    if (*token == '\0') continue;
    if (i >= PIPOWER5_MAX_BUZZER_SEQUENCE) break;
    if (sscanf(token, "%u,%u", &freq, &dur) != 2) continue;
    pi_dev->buzzer_notes[i].freq = (u16)freq;
    pi_dev->buzzer_notes[i].duration_ms = (u16)dur;
    i++;
  }
  kfree(tmp);
  pi_dev->buzzer_note_count = i;
  if (i > 0) {
    pi_dev->buzzer_note_index = 0;
    pi_dev->buzzer_playing = false;
    queue_delayed_work(pi_dev->wq, &pi_dev->buzzer_work, 0);
  }
}

/* buzz_on sysfs: show/set 8-bit mask */
static ssize_t buzz_on_show(struct device *dev, struct device_attribute *attr,
                            char *buf) {
  return snprintf(buf, PAGE_SIZE, "0x%02X\n", (unsigned int)buzz_on);
}
static ssize_t buzz_on_store(struct device *dev, struct device_attribute *attr,
                             const char *buf, size_t count) {
  unsigned long val;
  if (kstrtoul(buf, 0, &val) == 0)
    buzz_on = (unsigned int)(val & 0x7F);
  return count;
}
static DEVICE_ATTR_RW(buzz_on);

/* vbus_enable: control input power (for power failure simulation) */
static ssize_t vbus_enable_show(struct device *dev,
                                struct device_attribute *attr, char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  return snprintf(buf, PAGE_SIZE, "%d\n", pi_dev->vbus_enabled ? 1 : 0);
}
static ssize_t vbus_enable_store(struct device *dev,
                                 struct device_attribute *attr,
                                 const char *buf, size_t count) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  unsigned long val;
  if (kstrtoul(buf, 10, &val) != 0)
    return -EINVAL;
  if (val)
    pipower5_enable_vbus(pi_dev);
  else
    pipower5_disable_vbus(pi_dev);
  return count;
}
static DEVICE_ATTR_RW(vbus_enable);

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

/* Events log attribute */
static ssize_t events_show(struct device *dev,
                           struct device_attribute *attr, char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  int len = 0;
  int i, idx;
  unsigned long now = jiffies;

  mutex_lock(&pi_dev->lock);
  for (i = 0; i < pi_dev->event_count; i++) {
    idx = (pi_dev->event_head - pi_dev->event_count + i + PIPOWER5_EVENT_LOG_SIZE)
          % PIPOWER5_EVENT_LOG_SIZE;
    unsigned long age_sec = (now - pi_dev->event_times[idx]) / HZ;
    len += snprintf(buf + len, PAGE_SIZE - len,
                    "[%lus ago] %s\n", age_sec, pi_dev->event_log[idx]);
  }
  mutex_unlock(&pi_dev->lock);

  if (len == 0)
    len = snprintf(buf, PAGE_SIZE, "(no events yet)\n");
  return len;
}
static DEVICE_ATTR_RO(events);

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
    &dev_attr_firmware_version.attr,
    &dev_attr_default_on.attr,
    &dev_attr_board_id.attr,
    &dev_attr_shutdown_percentage.attr,
    &dev_attr_battery_internal_resistor.attr,
    &dev_attr_power_button_state.attr,
    &dev_attr_charge_current_max.attr,
    &dev_attr_buzzer_volume.attr,
    &dev_attr_vbus_enable.attr,
    &dev_attr_buzz_on.attr,
    &dev_attr_buzzer_play.attr,
    &dev_attr_events.attr,
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