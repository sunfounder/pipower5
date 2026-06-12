# PiPower 5

UPS HAT for Raspberry Pi 5 — I2C-based kernel driver with sysfs interface.

## Quick Install

PiPower 5 standalone:

```bash
curl -sSL https://raw.githubusercontent.com/sunfounder/pironman5/ups/install.sh | sudo bash -s -- --variant pipower5
```

Or as Pironman 5 plugin:

```bash
curl -sSL https://raw.githubusercontent.com/sunfounder/pironman5/ups/install.sh | sudo bash -s -- --variant ups
```

## CLI Usage

```bash
pipower5 -a                  # Show all status
pipower5 -bv                 # Battery voltage
pipower5 -bp                 # Battery percentage
pipower5 --power-failure-simulation 60  # Battery runtime test (60s)
pipower5 --buzz-on           # Show buzzer event settings
pipower5 --buzzer-volume 8   # Set buzzer volume (0-10)
pipower5 send-email test     # Test email configuration
pipower5 doctor              # Hardware diagnostic
pipower5 doctor --fix        # Auto-repair
```

## Web Dashboard

After install, open `http://<ip>:34001` for the dashboard.

## Architecture

- **Kernel driver** (`/sys/class/pipower5/pipower5/`): sysfs interface for all sensors, buzzer, power failure test
- **Python library** (`pipower5`): wraps sysfs, provides CLI + email + config management
- **pm_auto addon** (`PiPower5Addon`): bridges driver to pironman5 event bus
- **Email**: kernel uevents → udev rules → `pipower5 send-email` via `systemd-run`

## Development

Clone and build:

```bash
git clone -b feature/native-driver https://github.com/sunfounder/pipower5.git
cd pipower5/driver && make && make install && sudo reboot
cd .. && sudo pip3 install -e .
```
