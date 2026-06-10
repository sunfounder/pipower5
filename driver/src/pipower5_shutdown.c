/*
 * PiPower5 Shutdown & Event Logging
 *
 * Copyright (c) 2026 SunFounder <service@sunfounder.com>
 * GPL v2
 */

#include <linux/device.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/reboot.h>
#include <linux/jiffies.h>
#include <linux/slab.h>

#include "pipower5.h"

/* Record a timestamped event in the ring buffer */
void pipower5_log_event(struct pipower5_device *pi_dev, const char *fmt, ...)
{
  va_list args;
  unsigned long now = jiffies;
  int idx = pi_dev->event_head;

  va_start(args, fmt);
  vsnprintf(pi_dev->event_log[idx], PIPOWER5_EVENT_MSG_LEN, fmt, args);
  va_end(args);

  pi_dev->event_times[idx] = now;
  pi_dev->event_head = (idx + 1) % PIPOWER5_EVENT_LOG_SIZE;
  if (pi_dev->event_count < PIPOWER5_EVENT_LOG_SIZE)
    pi_dev->event_count++;

  /* Also print to kernel log */
  dev_info(&pi_dev->client->dev, "%s\n", pi_dev->event_log[idx]);
}

void pipower5_handle_shutdown(struct pipower5_device *pi_dev)
{
  const char *reason;

  switch (pi_dev->shutdown_request) {
  case SHUTDOWN_REQUEST_LOW_BATTERY:
    reason = "low_battery";
    break;
  case SHUTDOWN_REQUEST_BUTTON:
    reason = "button";
    break;
  case SHUTDOWN_REQUEST_LOW_VOLTAGE:
    reason = "low_voltage";
    break;
  default:
    return;
  }

  pipower5_log_event(pi_dev,
    "SHUTDOWN reason=%s bat=%d%% bat_voltage=%dmV input_plugged=%d",
    reason, pi_dev->battery_percentage, pi_dev->battery_voltage,
    pi_dev->is_input_plugged_in);

  kernel_power_off();
}

MODULE_AUTHOR("SunFounder <service@sunfounder.com>");
MODULE_DESCRIPTION("PiPower5 Shutdown & Event Driver");
MODULE_LICENSE("GPL v2");
