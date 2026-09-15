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

/*
 * Decide whether the MCU's shutdown request may be acted upon.
 *
 * The request is a single byte read over I2C once per second; a corrupted
 * transfer (e.g. -EREMOTEIO on a busy bus) can fabricate a non-zero value, and
 * acting on it cuts the power immediately.  Two guards are used:
 *
 *   1. only the three values the MCU is known to send are accepted at all, and
 *   2. the MCU has to report the same value shutdown_confirm polls in a row
 *      (default 3, i.e. roughly 2-3 seconds), so a single bad read is filtered.
 *
 * There is deliberately no cross-check against the cached battery readings:
 * the MCU knows better than our up-to-one-second-old copy, and refusing a
 * genuine low-battery/low-voltage request would risk over-discharge (or a hard
 * cut by the MCU itself) - worse than the problem being fixed here.
 */
bool pipower5_shutdown_request_confirmed(struct pipower5_device *pi_dev)
{
  unsigned int need = shutdown_confirm ? shutdown_confirm : 1;
  u8 req = pi_dev->shutdown_request;

  if (req == SHUTDOWN_REQUEST_NONE) {
    pi_dev->shutdown_candidate = SHUTDOWN_REQUEST_NONE;
    pi_dev->shutdown_confirm_count = 0;
    return false;
  }

  /* Unknown values can only come from a corrupted transfer */
  if (req != SHUTDOWN_REQUEST_LOW_BATTERY &&
      req != SHUTDOWN_REQUEST_BUTTON &&
      req != SHUTDOWN_REQUEST_LOW_VOLTAGE) {
    dev_warn(&pi_dev->client->dev,
             "ignoring unknown shutdown request %u\n", req);
    pi_dev->shutdown_candidate = SHUTDOWN_REQUEST_NONE;
    pi_dev->shutdown_confirm_count = 0;
    return false;
  }

  if (req != pi_dev->shutdown_candidate) {
    pi_dev->shutdown_candidate = req;
    pi_dev->shutdown_confirm_count = 1;
  } else if (pi_dev->shutdown_confirm_count < need) {
    pi_dev->shutdown_confirm_count++;
  }

  if (pi_dev->shutdown_confirm_count < need) {
    dev_info(&pi_dev->client->dev,
             "shutdown request %u not confirmed yet (%u/%u)\n",
             req, pi_dev->shutdown_confirm_count, need);
    return false;
  }

  return true;
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

  {
    char *envp[] = { NULL, NULL };
    char event_buf[64];

    snprintf(event_buf, sizeof(event_buf),
             "PIPOWER5_EVENT=%s", reason);
    envp[0] = event_buf;

    pipower5_log_event(pi_dev,
      "SHUTDOWN reason=%s req=%u bat=%d%% batV=%dmV inV=%dmV outV=%dmV plugged=%d src=%d",
      reason, pi_dev->shutdown_request, pi_dev->battery_percentage,
      pi_dev->battery_voltage, pi_dev->input_voltage,
      pi_dev->output_voltage, pi_dev->is_input_plugged_in,
      pi_dev->power_source);

    kobject_uevent_env(&pi_dev->pipower5_dev->kobj, KOBJ_OFFLINE, envp);
  }

  kernel_power_off();
}

MODULE_AUTHOR("SunFounder <service@sunfounder.com>");
MODULE_DESCRIPTION("PiPower5 Shutdown & Event Driver");
MODULE_LICENSE("GPL v2");
