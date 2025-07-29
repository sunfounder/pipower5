#!/bin/bash
set -euo pipefail
trap 'echo "Error occurred. Exiting..." >&2; exit 1' ERR

# Check if argument exists before accessing \$1
if [ $# -ge 1 ] && [ "$1" == "--uninstall" ]; then
    echo "Uninstalling PiPower 5 driver"
    rm -rf /lib/modules/$(uname -r)/kernel/drivers/misc/pipower5_driver.ko
    rm -rf /etc/modules-load.d/pipower5_driver.conf
    exit 0
fi

apt-get update
apt-get install linux-headers-$(uname -r) -y

echo "Make driver"
make
sudo cp pipower5_driver.ko /lib/modules/$(uname -r)/kernel/drivers/misc/
echo "Install driver"
sudo depmod -a
sudo cp pipower5_driver.conf /etc/modules-load.d/
sudo modprobe pipower5_driver

echo "Done"
