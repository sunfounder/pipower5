#!/bin/bash

echo "Make driver"
make
sudo cp pipower5_driver.ko /lib/modules/$(uname -r)/kernel/drivers/misc/
echo "Install driver"
sudo depmod -a
sudo cp pipower5_driver.conf /etc/modules-load.d/
sudo modprobe pipower5_driver

echo "Install python script"
sudo cp pipower5_driver.py /usr/local/bin

echo "Install service"
sudo cp pipower5_driver.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable pipower5_driver.service
sudo systemctl start pipower5_driver.service

echo "Done"
