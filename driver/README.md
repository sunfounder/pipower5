# PiPower 5 Native Kernel Driver

Standalone I2C kernel driver for PiPower 5 that exposes battery status via
Linux power_supply subsystem (UPower), sysfs, and input events — **no Python
required for battery monitoring**.

## File structure

| File | Purpose |
|------|---------|
| `include/pipower5.h` | Register definitions, struct, function prototypes |
| `src/pipower5_main.c` | I2C driver framework, probe/remove, workqueue polling |
| `src/pipower5_i2c.c` | I2C register read/write (SMBus) |
| `src/pipower5_sysfs.c` | sysfs attributes (24 entries, read/write) |
| `src/pipower5_power.c` | power_supply / UPower registration |
| `src/pipower5_button.c` | Power button input device (`/dev/input/eventX`) |
| `src/pipower5_shutdown.c` | Shutdown handling (low battery / button) |
| `sunfounder-pipower5-overlay.dts` | Device tree overlay (I2C address 0x5C) |
| `dkms.conf` | DKMS configuration (auto-rebuild on kernel updates) |
| `Makefile` | Build, install, DKMS, uninstall, status targets |
| `install.sh` | Quick install / uninstall script |

## Quick Start

```bash
# Install driver (DKMS + overlay + config.txt)
sudo ./install.sh

# Or manually:
sudo make install

# Check status:
make status
pipower5 doctor
```

## Available Make Targets

| Target | Description |
|--------|-------------|
| `make all` | Build module + device tree overlay |
| `make install` | Full install (DKMS + overlay + config.txt + modprobe) |
| `make uninstall` | Full uninstall (module, DKMS, overlay, config.txt) |
| `make dkms_install` | Install via DKMS (survives kernel updates) |
| `make dkms_uninstall` | Remove from DKMS |
| `make status` | Diagnostic health check |
| `make load` / `make unload` | Load/unload module |
| `make clean` | Remove build artifacts |

## sysfs Interface

After loading, data is available at `/sys/class/pipower5/pipower5/`:

```bash
cat /sys/class/pipower5/pipower5/battery_percentage
cat /sys/class/pipower5/pipower5/battery_voltage
# ... (24 attributes total)
```

## Shutdown request handling

The MCU can ask the host to power off (`shutdown_request` register, also
exposed at `/sys/class/pipower5/pipower5/shutdown_request`) for low battery,
low input voltage or a button long-press. The driver only acts on such a
request when

1. the MCU reports the same non-zero value `shutdown_confirm` polls in a row
   (default 3), and
2. the matching condition is plausible — `battery_percentage` below
   `shutdown_percentage` for `low_battery`, `battery_voltage` below 6400 mV
   for `low_voltage`, or a real button event within the last 10 s for
   `button`.

A single corrupted I2C read can therefore no longer power the board off.
Battery voltage and percentage readings that are out of range, or that jump too
far between two polls, are discarded in favour of the previous value, so a bus
error cannot report 0% to UPower either.

### Module parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `auto_shutdown` | `1` | Honour MCU shutdown requests. `0` = never power off automatically |
| `shutdown_confirm` | `3` | Consecutive identical MCU shutdown requests required before acting |

```bash
# Disable automatic shutdown for this boot only
sudo modprobe -r pipower5
sudo modprobe pipower5 auto_shutdown=0

# Persist it
echo 'options pipower5 auto_shutdown=0' | sudo tee /etc/modprobe.d/pipower5.conf
```

## UPower / Desktop Integration

The driver registers as a native `power_supply` device. Desktop
environments and `upower` will show battery status automatically:

```bash
upower -i /org/freedesktop/UPower/devices/battery_pipower5
```

## config.txt

The driver uses `dtoverlay=` in config.txt instead of HAT EEPROM
auto-detection to avoid EEPROM conflicts:

```
dtoverlay=sunfounder-pipower5
```

The Makefile and `pipower5 doctor --fix` manage this automatically.