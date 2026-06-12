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

/* Battery current attribute (signed: +charge, -discharge; report abs) */
static ssize_t battery_current_show(struct device *dev,
                                    struct device_attribute *attr, char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  s16 cur;
  int ret;

  mutex_lock(&pi_dev->lock);
  cur = (s16)pi_dev->battery_current;
  ret = snprintf(buf, PAGE_SIZE, "%u\n", (u16)(cur < 0 ? -cur : cur));
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

/* Shutdown request attribute */
static ssize_t shutdown_request_show(struct device *dev,
                                     struct device_attribute *attr,
                                     char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  int ret;

  mutex_lock(&pi_dev->lock);
  ret = snprintf(buf, PAGE_SIZE, "%u\n", pi_dev->shutdown_request);
  mutex_unlock(&pi_dev->lock);

  return ret;
}

static DEVICE_ATTR_RO(shutdown_request);

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

  /* User-facing scale: 0-10. Clamp. */
  if (value > 10) {
    value = 10;
  }

  buzzer_volume = value;

  /* MCU expects 0-100, scale up */
  mutex_lock(&pi_dev->lock);
  pi_dev->buzzer_volume = (u8)value;
  ret = __pipower5_write_byte(pi_dev, REG_WRITE_BUZZER_VOL,
      value >= 10 ? 100 : (u8)(value * 10));
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
/* Event buzzer sequences (frequencies matching original main branch constants.py)
 *   battery_activated:             A4,50:p,100:B4,50
 *   low_battery:                   A4,50:p,100:A4,50
 *   power_disconnected:            D5,50:p,100:G4,50
 *   power_restored:                G4,50:p,100:D5,50
 *   power_insufficient:            B4,50:p,100:B4,50:p,100:B4,100
 *   battery_critical_shutdown:     C6,50:p,60:C6,50:p,60:C6,100
 *   battery_voltage_critical:      C6,50:p,60:C6,50:p,60:C6,100:p,60:C6,100
 */
/* Maximum sequence string length per event */
#define BUZZER_MAX_SEQ_LEN 256
static char buzzer_event_seqs[7][BUZZER_MAX_SEQ_LEN];

static const struct {
  const char *name;
  const char *default_seq;
} buzzer_events[] = {
  {"battery_activated",                 "440,50;0,100;494,50"},
  {"low_battery",                       "440,50;0,100;440,50"},
  {"power_disconnected",                "587,50;0,100;392,50"},
  {"power_restored",                    "392,50;0,100;587,50"},
  {"power_insufficient",                "494,50;0,100;494,50;0,100;494,100"},
  {"battery_critical_shutdown",         "1047,50;0,60;1047,50;0,60;1047,100"},
  {"battery_voltage_critical_shutdown", "1047,50;0,60;1047,50;0,60;1047,100;0,60;1047,100"},
};

static const char *buzzer_lookup_event(const char *name) {
  int i;
  for (i = 0; i < ARRAY_SIZE(buzzer_events); i++) {
    if (strcmp(name, buzzer_events[i].name) == 0)
      return buzzer_event_seqs[i][0] ? buzzer_event_seqs[i]
                                     : buzzer_events[i].default_seq;
  }
  return NULL;
}

static int buzzer_event_index(const char *name) {
  int i;
  for (i = 0; i < ARRAY_SIZE(buzzer_events); i++)
    if (strcmp(name, buzzer_events[i].name) == 0) return i;
  return -1;
}

/* buzz_seq sysfs: show/set all event sequences (key=value per line) */
static ssize_t buzz_seq_show(struct device *dev,
                             struct device_attribute *attr, char *buf) {
  int i, len = 0;
  for (i = 0; i < ARRAY_SIZE(buzzer_events); i++) {
    const char *s = buzzer_event_seqs[i][0] ? buzzer_event_seqs[i]
                                            : buzzer_events[i].default_seq;
    len += snprintf(buf + len, PAGE_SIZE - len, "%s=%s\n",
                    buzzer_events[i].name, s);
  }
  return len;
}

static ssize_t buzz_seq_store(struct device *dev,
                              struct device_attribute *attr,
                              const char *buf, size_t count) {
  char *line, *tmp, *orig, *eq;
  orig = kstrndup(buf, count, GFP_KERNEL);
  if (!orig) return -ENOMEM;
  tmp = orig;
  while ((line = strsep(&tmp, "\n")) != NULL) {
    while (*line == ' ' || *line == '\t') line++;
    if (!*line) continue;
    eq = strchr(line, '=');
    if (!eq) continue;
    *eq = '\0';
    int idx = buzzer_event_index(line);
    if (idx >= 0) {
      char *val = eq + 1;
      while (*val == ' ') val++;
      strscpy(buzzer_event_seqs[idx], val, BUZZER_MAX_SEQ_LEN);
      dev_info(dev, "buzz_seq: %s updated\n", buzzer_events[idx].name);
    }
  }
  kfree(orig);
  return count;
}
static DEVICE_ATTR_RW(buzz_seq);

/* Load sequences from config file (called at probe) */
void pipower5_buzz_seq_load(const char *buf, size_t len) {
  char *tmp, *orig, *line, *eq;
  orig = kmalloc(len + 1, GFP_KERNEL);
  if (!orig) return;
  memcpy(orig, buf, len);
  orig[len] = '\0';
  tmp = orig;
  while ((line = strsep(&tmp, "\n")) != NULL) {
    while (*line == ' ' || *line == '\t') line++;
    if (!*line || *line == '#') continue;
    eq = strchr(line, '=');
    if (!eq) continue;
    *eq = '\0';
    int idx = buzzer_event_index(line);
    if (idx >= 0)
      strscpy(buzzer_event_seqs[idx], eq + 1, BUZZER_MAX_SEQ_LEN);
  }
  kfree(orig);
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

/* Battery power attribute (voltage * |current|, μW) */
static ssize_t battery_power_show(struct device *dev,
                                  struct device_attribute *attr, char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  s16 cur;
  unsigned int power;
  int ret;

  mutex_lock(&pi_dev->lock);
  cur = (s16)pi_dev->battery_current;
  power = (unsigned int)pi_dev->battery_voltage * (cur < 0 ? -cur : cur);
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

/* ── Estimated runtime (always-on, updated every poll) ────────────── */
static ssize_t estimated_runtime_show(struct device *dev,
                                      struct device_attribute *attr,
                                      char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  u32 runtime;
  mutex_lock(&pi_dev->lock);
  runtime = pi_dev->estimated_runtime;
  mutex_unlock(&pi_dev->lock);
  return snprintf(buf, PAGE_SIZE, "%u\n", runtime);
}
static DEVICE_ATTR_RO(estimated_runtime);

/* ── Power Failure Test ──────────────────────────────────────────── */

static void pipower5_pft_work_func(struct work_struct *work) {
  struct delayed_work *dwork = to_delayed_work(work);
  struct pipower5_device *pi_dev =
      container_of(dwork, struct pipower5_device, pft_work);
  s16 batt_cur;
  u16 bv, bc, ov, oc;

  mutex_lock(&pi_dev->lock);

  if (!pi_dev->pft_running) {
    mutex_unlock(&pi_dev->lock);
    return;
  }

  pi_dev->pft_elapsed++;

  /* Sample current values */
  bv = pi_dev->battery_voltage;
  bc = (u16)abs((s16)pi_dev->battery_current); /* discharge as positive */
  ov = pi_dev->output_voltage;
  oc = pi_dev->output_current;

  /* Running aggregates */
  pi_dev->pft_samples++;
  pi_dev->pft_bat_v_sum += bv;
  pi_dev->pft_bat_c_sum += bc;
  pi_dev->pft_out_v_sum += ov;
  pi_dev->pft_out_c_sum += oc;
  if (bv > pi_dev->pft_bat_v_max) pi_dev->pft_bat_v_max = bv;
  if (bc > pi_dev->pft_bat_c_max) pi_dev->pft_bat_c_max = bc;
  if (ov > pi_dev->pft_out_v_max) pi_dev->pft_out_v_max = ov;
  if (oc > pi_dev->pft_out_c_max) pi_dev->pft_out_c_max = oc;
  if (bv < pi_dev->pft_bat_v_min || pi_dev->pft_bat_v_min == 0) pi_dev->pft_bat_v_min = bv;
  if (bc < pi_dev->pft_bat_c_min || pi_dev->pft_bat_c_min == 0) pi_dev->pft_bat_c_min = bc;
  if (ov < pi_dev->pft_out_v_min || pi_dev->pft_out_v_min == 0) pi_dev->pft_out_v_min = ov;
  if (oc < pi_dev->pft_out_c_min || pi_dev->pft_out_c_min == 0) pi_dev->pft_out_c_min = oc;

  if (pi_dev->pft_elapsed >= pi_dev->pft_test_time) {
    /* Test complete — re-enable VBUS, compute results */
    u32 n = pi_dev->pft_samples;
    u64 delta_mah = pi_dev->mah_consumed - pi_dev->pft_mah_start;

    mutex_unlock(&pi_dev->lock);
    pipower5_enable_vbus(pi_dev);
    mutex_lock(&pi_dev->lock);
    pi_dev->vbus_enabled = true;
    pi_dev->pft_running = false;

    {
      u8 bat_pct_end = pi_dev->battery_percentage;
      u8 bat_pct_used = pi_dev->pft_bat_pct_start > bat_pct_end ?
                        pi_dev->pft_bat_pct_start - bat_pct_end : 0;
      s32 avail_pct = (s32)bat_pct_end - (s32)pi_dev->shutdown_percentage;
      u32 avail_cap = avail_pct > 0 ?
                      (u32)avail_pct * PIPOWER5_BATTERY_FULL_CHARGE_MAH * 9 / 1000 : 0;

      scnprintf(pi_dev->pft_result, sizeof(pi_dev->pft_result),
        "{\"elapsed_s\":%u,\"samples\":%u,"
        "\"bat_voltage_avg\":%u,\"bat_current_avg\":%u,"
        "\"bat_voltage_max\":%u,\"bat_current_max\":%u,"
        "\"bat_voltage_min\":%u,\"bat_current_min\":%u,"
        "\"out_voltage_avg\":%u,\"out_current_avg\":%u,"
        "\"out_voltage_max\":%u,\"out_current_max\":%u,"
        "\"out_voltage_min\":%u,\"out_current_min\":%u,"
        "\"delta_mah\":%llu,\"estimated_runtime_s\":%u,"
        "\"bat_percent_used\":%u,\"available_bat_capacity\":%u}",
        pi_dev->pft_elapsed, n,
        n ? (u32)(pi_dev->pft_bat_v_sum / n) : 0,
        n ? (u32)(pi_dev->pft_bat_c_sum / n) : 0,
        pi_dev->pft_bat_v_max, pi_dev->pft_bat_c_max,
        pi_dev->pft_bat_v_min, pi_dev->pft_bat_c_min,
        n ? (u32)(pi_dev->pft_out_v_sum / n) : 0,
        n ? (u32)(pi_dev->pft_out_c_sum / n) : 0,
        pi_dev->pft_out_v_max, pi_dev->pft_out_c_max,
        pi_dev->pft_out_v_min, pi_dev->pft_out_c_min,
        delta_mah, pi_dev->estimated_runtime,
        bat_pct_used, avail_cap);
    }

    dev_info(&pi_dev->client->dev,
      "PFT done: %us, %u samples, delta_mah=%llu, est_runtime=%us\n",
      pi_dev->pft_elapsed, n, delta_mah, pi_dev->estimated_runtime);
  } else {
    /* Schedule next sample in 1 second */
    queue_delayed_work(pi_dev->wq, &pi_dev->pft_work, msecs_to_jiffies(1000));
  }
  mutex_unlock(&pi_dev->lock);
}

static ssize_t power_failure_test_show(struct device *dev,
                                       struct device_attribute *attr,
                                       char *buf) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  int ret;

  mutex_lock(&pi_dev->lock);
  if (pi_dev->pft_running)
    ret = snprintf(buf, PAGE_SIZE, "running %u %u\n",
                   pi_dev->pft_elapsed, pi_dev->pft_test_time);
  else if (pi_dev->pft_result[0])
    ret = snprintf(buf, PAGE_SIZE, "done %s\n", pi_dev->pft_result);
  else
    ret = snprintf(buf, PAGE_SIZE, "idle\n");
  mutex_unlock(&pi_dev->lock);

  return ret;
}

static ssize_t power_failure_test_store(struct device *dev,
                                        struct device_attribute *attr,
                                        const char *buf, size_t count) {
  struct pipower5_device *pi_dev = dev_get_drvdata(dev);
  unsigned long val;

  if (kstrtoul(buf, 10, &val) != 0)
    return -EINVAL;

  mutex_lock(&pi_dev->lock);

  if (val == 0) {
    /* Cancel */
    if (pi_dev->pft_running) {
      cancel_delayed_work_sync(&pi_dev->pft_work);
      pi_dev->pft_running = false;
      pi_dev->pft_result[0] = '\0';
      mutex_unlock(&pi_dev->lock);
      pipower5_enable_vbus(pi_dev);
      dev_info(&pi_dev->client->dev, "PFT cancelled\n");
      return count;
    }
    mutex_unlock(&pi_dev->lock);
    return count;
  }

  /* Clamp test time */
  if (val < 10) val = 10;
  if (val > 600) val = 600;

  if (pi_dev->pft_running) {
    mutex_unlock(&pi_dev->lock);
    dev_warn(&pi_dev->client->dev, "PFT already running\n");
    return -EBUSY;
  }

  /* Pre-check: must be on external power, battery > 80% */
  if (!pi_dev->is_input_plugged_in) {
    mutex_unlock(&pi_dev->lock);
    dev_warn(&pi_dev->client->dev, "PFT requires external power\n");
    return -EINVAL;
  }

  /* Reset PFT state */
  pi_dev->pft_running = true;
  pi_dev->pft_test_time = (u32)val;
  pi_dev->pft_elapsed = 0;
  pi_dev->pft_samples = 0;
  pi_dev->pft_bat_v_sum = pi_dev->pft_bat_c_sum = 0;
  pi_dev->pft_out_v_sum = pi_dev->pft_out_c_sum = 0;
  pi_dev->pft_bat_v_max = pi_dev->pft_bat_c_max = 0;
  pi_dev->pft_out_v_max = pi_dev->pft_out_c_max = 0;
  pi_dev->pft_bat_v_min = pi_dev->pft_bat_c_min = 0;
  pi_dev->pft_out_v_min = pi_dev->pft_out_c_min = 0;
  pi_dev->pft_mah_start = pi_dev->mah_consumed;
  pi_dev->pft_bat_pct_start = pi_dev->battery_percentage;
  pi_dev->pft_result[0] = '\0';
  pi_dev->pft_start_jiffies = jiffies;

  mutex_unlock(&pi_dev->lock);

  /* Disable VBUS (external power off) */
  pipower5_disable_vbus(pi_dev);
  pi_dev->vbus_enabled = false;
  dev_info(&pi_dev->client->dev, "PFT started: %us\n", pi_dev->pft_test_time);

  /* Start sampling in 1 second */
  queue_delayed_work(pi_dev->wq, &pi_dev->pft_work, msecs_to_jiffies(1000));

  return count;
}
static DEVICE_ATTR_RW(power_failure_test);

/* ── Stats & PFT lifecycle ───────────────────────────────────────── */

void pipower5_stats_init(struct pipower5_device *pi_dev) {
  pi_dev->mah_consumed = 0;
  pi_dev->last_sample_jiffies = jiffies;
  pi_dev->estimated_runtime = 0;
}

void pipower5_stats_update(struct pipower5_device *pi_dev) {
  s16 batt_cur = (s16)pi_dev->battery_current;
  unsigned long now = jiffies;
  unsigned long dt_jiffies;
  u32 batt_pct, shutdown_pct;
  s32 remaining_pct;
  u32 avg_ma;

  /* ── Cumulative mAh discharge ── */
  if (batt_cur < 0) {
    /* Discharging: batt_cur negative → use absolute value */
    u32 discharge_ma = (u32)(-batt_cur);
    dt_jiffies = now - pi_dev->last_sample_jiffies;
    /* mah_consumed stored as mAh * 1000 (fixed-point).
     * ΔmAh = mA * (Δjiffies / HZ) / 3600 * 1000
     *      = mA * Δjiffies * 1000 / (HZ * 3600) */
    pi_dev->mah_consumed +=
        (u64)discharge_ma * dt_jiffies * 1000 / (HZ * 3600);
  }
  pi_dev->last_sample_jiffies = now;

  /* ── Estimated runtime ── */
  batt_pct = pi_dev->battery_percentage;
  shutdown_pct = pi_dev->shutdown_percentage;

  if (batt_pct <= shutdown_pct) {
    pi_dev->estimated_runtime = 0;
  } else if (batt_cur >= 0) {
    /* Charging or idle → effectively unlimited (cap for display) */
    pi_dev->estimated_runtime = 999999;
  } else {
    remaining_pct = (s32)batt_pct - (s32)shutdown_pct;
    if (remaining_pct <= 0) {
      pi_dev->estimated_runtime = 0;
    } else {
      /* Use a short moving average of discharge current to smooth jitter.
       * Simple: use current sample directly (updated at 1Hz, already stable). */
      avg_ma = (u32)(-batt_cur);
      if (avg_ma == 0) avg_ma = 1;
      /* Capacity available: remaining_pct% of 2000mAh × 0.9 (usable) */
      pi_dev->estimated_runtime =
          (u32)((u64)remaining_pct * PIPOWER5_BATTERY_FULL_CHARGE_MAH * 9 *
                3600 / (avg_ma * 1000));
    }
  }
}

void pipower5_pft_init(struct pipower5_device *pi_dev) {
  INIT_DELAYED_WORK(&pi_dev->pft_work, pipower5_pft_work_func);
  pi_dev->pft_running = false;
  pi_dev->pft_result[0] = '\0';
}

void pipower5_pft_start(struct pipower5_device *pi_dev, u32 test_time) {
  /* Wrapper for sysfs store — not used externally */
}

void pipower5_pft_cancel(struct pipower5_device *pi_dev) {
  if (pi_dev->pft_running) {
    cancel_delayed_work_sync(&pi_dev->pft_work);
    pi_dev->pft_running = false;
    pi_dev->pft_result[0] = '\0';
  }
}

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
    &dev_attr_shutdown_request.attr,
    &dev_attr_charge_current_max.attr,
    &dev_attr_buzzer_volume.attr,
    &dev_attr_vbus_enable.attr,
    &dev_attr_buzz_seq.attr,
    &dev_attr_buzz_on.attr,
    &dev_attr_buzzer_play.attr,
    &dev_attr_events.attr,
    &dev_attr_driver_version.attr,
    &dev_attr_estimated_runtime.attr,
    &dev_attr_power_failure_test.attr,
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