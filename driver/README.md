# PiPower 5 Battery driver

Register PiPower 5 to UPower

## File explanation
- `pipower5_driver.conf`: Auto enable pipower5 driver on boot
- `pipower5_driver.py`: Update battery status and information
- `pipower5_driver.service`: Systemd service file to run pipower5 driver in background
- `pipower5_driver.c`: Linux kernel module to communicate with pipower5
- `install.sh`: Install script to install pipower5 driver
- `Makefile`: Makefile to build pipower5 driver
