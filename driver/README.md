# PiPower 5 Battery driver

Register PiPower 5 to UPower

## File explanation
- `pipower5.conf`: Auto enable pipower5 driver on boot
- `src/pipower5_main.c`: Main driver implementation
- `src/pipower5_i2c.c`: I2C communication functions
- `src/pipower5_sysfs.c`: SysFS interface
- `src/pipower5_power.c`: UPower integration
- `include/pipower5.h`: Header file with definitions
- `install.sh`: Install script to install pipower5 driver
- `Makefile`: Makefile to build pipower5 driver

## Compilation and Installation

### Quick Build
```bash
make
```

### Build and Install
```bash
make install
```

### Available Make Targets
- `make` or `make all` - Compile the module
- `make module` - Compile the module
- `make clean` - Remove compiled files
- `make install` - Compile and install the module
- `make uninstall` - Remove the module
- `make load` - Load the module
- `make unload` - Unload the module
- `make status` - Check if module is loaded
- `make help` - Show help message

### Manual Installation
```bash
# Compile
make

# Install
sudo cp pipower5.ko /lib/modules/$(uname -r)/kernel/drivers/misc/
sudo depmod -a
sudo modprobe pipower5
```

### Auto-load at Boot
After installation, the module will be loaded automatically at boot time.