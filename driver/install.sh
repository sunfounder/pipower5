#!/bin/bash
set -euo pipefail
trap 'echo "Error occurred. Exiting..." >&2; exit 1' ERR

# Check if argument exists before accessing $1
if [ $# -ge 1 ] && [ "$1" == "--uninstall" ]; then
    echo "Uninstalling PiPower 5 driver"
    sudo make uninstall
    echo "PiPower5 driver uninstalled"
    exit 0
fi

echo "Installing PiPower 5 driver..."

# Install prerequisites
sudo apt update
sudo apt install -y linux-headers-$(uname -r) dkms

# Build and install using Makefile (DKMS + overlay + config.txt)
echo "Building and installing driver..."
sudo make install

echo ""
echo "PiPower5 driver installed successfully!"
echo "  - Module is loaded via DKMS (auto-rebuilds on kernel updates)"
echo "  - Device tree overlay installed"
echo "  - dtoverlay added to config.txt"
echo ""
echo "After reboot, verify with: pipower5 doctor"