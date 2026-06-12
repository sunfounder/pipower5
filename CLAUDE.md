# PiPower5 Development Guide

## Architecture

```
Kernel Driver (pipower5.ko)
  └── /sys/class/pipower5/pipower5/   sysfs interface
      ├── battery_voltage, battery_current, ...
      ├── buzz_on, buzzer_volume, buzzer_play
      ├── power_failure_test, estimated_runtime
      └── shutdown_percentage, shutdown_request

Python Library (pipower5/)
  └── pipower5.py      PiPower5 class — sysfs read/write
  └── device.py        Driver detection, doctor, uninstall
  └── email_sender.py  SMTP email sending
  └── __init__.py      CLI entry point

pm_auto Addon (PiPower5Addon)
  └── Bridges driver sysfs to pironman5/pm_auto event bus
  └── Config sync: web ↔ config.json ↔ sysfs
  └── Button events → OLED page control

Email Flow:
  kernel uevent → udev → systemd-run → pipower5 send-email
```

## Key Branches

- `feature/native-driver` — Active development (kernel driver + Python lib)
- `main` — Stable release (I2C-based, older architecture)

## Install Script

pironman5/install.sh handles pipower5 via `--variant pipower5` (standalone) or `--pipower5` (plugin).

## Testing

On test devices after deploy:
```bash
pipower5 doctor          # Verify driver loaded
pipower5 -a              # Check all sensors
pipower5 send-email test # Test email
cat /sys/class/pipower5/pipower5/buzz_on  # Check buzzer config
```
