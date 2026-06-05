# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PiPower 5 is a Python library, CLI, and systemd service for the SunFounder PiPower 5 UPS HAT for Raspberry Pi. It monitors power states (battery, input voltage/current, charging), reads hardware buttons, controls a buzzer for alerts, sends email notifications on power events, exposes battery status to the Linux power_supply subsystem via a custom kernel module, and optionally runs a web dashboard (`pm_dashboard`).

## Build & Development Commands

This project targets Raspberry Pi OS (Debian-based) and must be built/run on a Pi with the PiPower 5 HAT attached.

```bash
# Full installation (from project root, on a Raspberry Pi):
sudo python install.py                     # Install service + dashboard
sudo python install.py --disable-dashboard # Install without dashboard

# Build and install the kernel driver (DKMS + overlay + config.txt):
cd driver && sudo make install

# Check driver status:
cd driver && make status
pipower5 doctor                 # Health check
pipower5 doctor --fix           # Auto-repair

# Uninstall everything:
pipower5 uninstall              # Python package + driver + DKMS

# Install Python package only after code changes:
sudo /opt/pipower5/venv/bin/pip3 uninstall pipower5 -y
sudo /opt/pipower5/venv/bin/pip3 install . --no-build-isolation

# Copy email templates after template changes:
sudo rm -r /opt/pipower5/email_templates/
sudo cp -r ~/pipower5/email_templates/ /opt/pipower5/

# Service control:
sudo systemctl stop pipower5.service
sudo systemctl start pipower5.service
sudo systemctl restart pipower5.service

# Read hardware status via CLI:
pipower5 --all                    # All sensor readings
pipower5 -bv                      # Battery voltage
pipower5 -bp                      # Battery percentage
pipower5 --firmware               # PiPower5 firmware version
pipower5 --shutdown-percentage 20 # Set shutdown threshold
pipower5 --power-failure-simulation 60  # Simulate power outage for 60s

# View logs:
journalctl -xefu pipower5.service
cat /var/log/pipower5/pipower5.log

# Raw sysfs access (no Python needed):
cat /sys/class/pipower5/pipower5/battery_percentage
cat /sys/class/pipower5/pipower5/battery_voltage
```

## Architecture

### Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│ Kernel (Native Driver — no Python needed for HW)     │
│  pipower5.ko ────────────────────────────────────── │
│  ├── I2C reads (direct register access)             │
│  ├── sysfs (/sys/class/pipower5/pipower5/)          │
│  ├── power_supply (UPower battery integration)      │
│  ├── input device (power button via /dev/input/)    │
│  └── shutdown handling (kernel_power_off)           │
├─────────────────────────────────────────────────────┤
│ Python Service (optional: alerts, dashboard, buzzer)│
│  PiPower5Manager ────────────────────────────────── │
│  ├── PiPower5Service (sysfs reads + I2C writes)     │
│  │   └── PiPower5 (reads sysfs, writes via smbus2)  │
│  ├── PiPower5System (CPU/mem/disk/net via sf_rpi)   │
│  └── PMDashboard (optional web UI)                   │
└─────────────────────────────────────────────────────┘
```

Hardware data flows:
- **kernel → sysfs** (sensor readings, cached every 1s by workqueue)
- **sysfs → Python** (PiPower5 reads all sensor data from sysfs)
- **Python → I2C** (only for control writes: buzzer, VBUS, shutdown %)

### Key Files

| File | Role |
|------|------|
| `driver/src/pipower5_main.c` | I2C driver framework, probe/remove, workqueue polling |
| `driver/src/pipower5_i2c.c` | I2C register read/write (SMBus) |
| `driver/src/pipower5_sysfs.c` | 24 sysfs attributes at `/sys/class/pipower5/pipower5/` |
| `driver/src/pipower5_power.c` | Native power_supply / UPower registration |
| `driver/src/pipower5_button.c` | Power button input device |
| `driver/src/pipower5_shutdown.c` | Low battery / button shutdown handling |
| `driver/include/pipower5.h` | Register map, struct, function prototypes |
| `driver/dkms.conf` | DKMS config for kernel-update survival |
| `pipower5/pipower5.py` | Hardware class: sysfs reads + smbus2 I2C writes |
| `pipower5/pipower5_service.py` | Async event loop: polling, alerts, callbacks |
| `pipower5/pipower5_manager.py` | Orchestrator: wires service + system + dashboard |
| `pipower5/pipower5_system.py` | RPi system metrics (CPU, mem, disk, net) |
| `pipower5/device.py` | Device detection, config.txt mgmt, doctor, uninstall |
| `pipower5/email_sender.py` | SMTP email alerts for power events |
| `pipower5/battery_device.py` | **Deprecated** — kernel driver handles power_supply natively |

### Utility Classes

- **`LazyCaller`** (`lazy_caller.py`): Rate-limits function calls. Supports `interval` (minimum seconds between calls) and `oneshot` (call only once until `reset()` is called).
- **`Debounce`** (`debounce.py`): Only returns a new value after it has remained stable for a configurable timeout. Used for debouncing `is_input_plugged_in` (1s timeout), `is_battery_activated` (3s), and `is_power_insufficient` (3s).
- **`Logger`** (`logger.py`): Custom logger with ANSI-colored console output and rotating file logs at `/var/log/pipower5/pipower5.log` (100MB max, 5 backups).
- **`utils.log_error`**: Decorator that wraps class methods, catching all exceptions and logging them via `self.log.exception()`.
- **`note.py`**: MIDI-compatible note-to-frequency mapping for the buzzer.

### Kernel Driver (`driver/`)

A native Linux I2C kernel driver that operates independently of Python:

- **`pipower5_main.c`** — I2C driver with device tree binding (`sunfounder,pipower5`), workqueue polling at 1 Hz
- **`pipower5_i2c.c`** — SMBus I2C register reads/writes (reads all 20+ registers each poll cycle)
- **`pipower5_sysfs.c`** — 24 sysfs attributes at `/sys/class/pipower5/pipower5/` (RO sensors, RW: shutdown_percentage, buzzer_volume, power_button_state)
- **`pipower5_power.c`** — Native `power_supply` registration (`/sys/class/power_supply/pipower5/`), UPower compatible
- **`pipower5_button.c`** — Registers `/dev/input/eventX` for power button (KEY_POWER)
- **`pipower5_shutdown.c`** — Handles low-battery/button/low-voltage shutdown via `kernel_power_off()`
- **DKMS** — Auto-rebuilds on kernel updates (`dkms.conf` + `make dkms_install`)

The driver loads via `dtoverlay=sunfounder-pipower5` in `/boot/config.txt` (not HAT EEPROM).

### CLI (`pipower5/__init__.py`)

The `main()` function provides a comprehensive argparse CLI. Convention: every setting has a `--flag` that shows current value when passed without argument (None value triggers read), or sets a new value when given one. The `pipower5` console script is registered via `pyproject.toml` as `pipower5:main`.

### Configuration

Stored as JSON at the path from `importlib.resources` for the `pipower5` package (typically under `/opt/pipower5/venv/lib/`), overridable via `--config-path`. Default config structure is in `constants.py` (see `SYSTEM_DEFAULT_CONFIG`). The `update_config_file()` function in `__init__.py` does a deep merge of new settings into the existing JSON.

### Event System

Defined in `pipower5.py` as `Event` enum:
- `BATTERY_ACTIVATED`, `LOW_BATTERY`, `POWER_DISCONNECTED`
- `POWER_RESTORED`, `POWER_INSUFFICIENT`
- `BATTERY_CRITICAL_SHUTDOWN`, `BATTERY_VOLTAGE_CRITICAL_SHUTDOWN`

Each event can independently trigger email notifications (`send_email_on` config) and buzzer sequences (`pipower5_buzz_on` / `pipower5_buzz_sequence` config). Power insufficient means input is plugged in BUT battery is still discharging (adapter too weak).

### Button States and Shutdown Requests

Button states (`ButtonState` enum): `RELEASED`, `CLICK`, `DOUBLE_CLICK`, `LONG_PRESS_2S`, `LONG_PRESS_2S_RELEASED`, `LONG_PRESS_5S`, `LONG_PRESS_5S_RELEASED`.

Shutdown requests (`ShutdownRequest` enum): `NONE`, `LOW_BATTERY` (percentage below threshold), `BUTTON` (long press), `LOW_VOLTAGE` (battery voltage critical).

After reading button state from `REG_PWR_BTN_STATE` (register 154), the code must write 0 to `REG_WRITE_POWER_BTN_STATE` (register 12) to reset it. The power button must be read before `read_all()` to prevent a race condition on register 12.

### Dependencies

- **`smbus2`** (pip dep): Minimal I2C access for write operations (buzzer, VBUS control).
- **`sf_rpi_status`** (installed by `install.py`): System metrics (CPU temp/usage, memory, disk, network, IP, MAC).
- **`pm_dashboard`** (optional, installed by `install.py`): Web dashboard for monitoring and configuration.
- **Kernel driver** (`pipower5.ko`): Reads I2C directly, registers power_supply, exposes sysfs. Requires `dtoverlay=sunfounder-pipower5` in config.txt. Installed via DKMS to survive kernel updates.

### Power Failure Simulation Flow

`PiPower5.power_failure_simulation(test_time)`:
1. Validates battery >= 80% and input plugged in
2. Lowers shutdown percentage to 10% temporarily
3. Disables VBUS input via advanced I2C command (`ADV_CMD_VBUS_EN = 0`)
4. Samples battery voltage/current and output voltage/current every 0.5s for `test_time` seconds
5. Re-enables input and restores original shutdown percentage
6. Writes report to `/opt/pipower5/blackout_simulation.json`
7. Returns dict with mAh used, average/max values, estimated remaining runtime
