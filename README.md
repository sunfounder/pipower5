# PiPower 5

UPS HAT for Raspberry Pi 5.

## Installation

### Option 1: One-liner

Install PiPower 5 standalone:

```bash
curl -sSL https://raw.githubusercontent.com/sunfounder/sunfounder-installer-scripts/main/pironman5/install.sh | sudo bash -s -- --variant pipower5
```

Or install as Pironman 5 UPS bundle:

```bash
curl -sSL https://raw.githubusercontent.com/sunfounder/sunfounder-installer-scripts/main/pironman5/install.sh | sudo bash -s -- --variant ups
```

If Pironman 5 is already installed, add PiPower 5 as a plugin:

```bash
pironman5 plugin install pipower5
```

### Option 2: Manual install

**Step 1: Install kernel driver**

```bash
cd driver
sudo bash install.sh
sudo reboot
```

**Step 2: Install Python library**

```bash
sudo pip3 install git+https://github.com/sunfounder/pipower5.git@feature/native-driver
```

## Usage

```bash
pipower5 -a              # Show all status
pipower5 -bv             # Battery voltage
pipower5 -bp             # Battery percentage
pipower5 doctor          # Hardware diagnostic
pipower5 doctor --fix    # Auto-repair
pipower5 uninstall       # Remove driver and package
```

## Development

Clone and install in editable mode:

```bash
git clone https://github.com/sunfounder/pipower5.git
cd pipower5
sudo pip3 install -e .
```

Build and install driver from source:

```bash
cd driver
sudo bash install.sh
sudo reboot
```

Debug with journal:

```bash
journalctl -xefu pipower5.service
# or if installed via pironman5:
journalctl -xefu pironman5.service
```

## Power-off signal for Pi 3B+ / Pi Zero

Edit `/boot/firmware/config.txt`:

```
dtoverlay=gpio-poweroff,gpio_pin=26,active_low=1
gpio=26=op,dh
```

