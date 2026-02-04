#!/bin/bash
set -euo pipefail
trap 'echo "Error occurred. Exiting..." >&2; exit 1' ERR

# Check if argument exists before accessing $1
if [ $# -ge 1 ] && [ "$1" == "--uninstall" ]; then
    echo "Uninstalling PiPower 5 driver"
    sudo modprobe -r pipower5 2>/dev/null || true
    sudo rm -f /lib/modules/$(uname -r)/kernel/drivers/misc/pipower5.ko
    sudo rm -f /etc/modules-load.d/pipower5.conf
    sudo depmod -a
    echo "PiPower5 driver uninstalled"
    exit 0
fi

echo "Installing PiPower 5 driver..."

# Install prerequisites
sudo apt update
sudo apt install -y linux-headers-$(uname -r)

# Build the module using our simplified Makefile
echo "Building driver..."
make

# Copy the module to the appropriate location
echo "Installing module..."
sudo cp pipower5.ko /lib/modules/$(uname -r)/kernel/drivers/misc/

# Update module dependencies
sudo depmod -a

# Copy auto-load configuration
sudo cp pipower5.conf /etc/modules-load.d/

# Load the module
sudo modprobe pipower5

echo "PiPower5 driver installed and loaded successfully!"
echo "To verify the module is loaded, run: lsmod | grep pipower5"
echo "To check power supply info: ls /sys/class/power_supply/"