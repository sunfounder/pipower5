# Simplified Makefile for PiPower5 driver
# This Makefile simplifies the compilation and installation process

# Module name
MODULE_NAME := pipower5

# Build directory
BUILD_DIR := build

# Device tree overlay file
DT_OVERLAY_SRC := sunfounder-pipower5-overlay.dts
DT_OVERLAY_DST := $(BUILD_DIR)/sunfounder-pipower5.dtbo

# Object files
obj-m := $(MODULE_NAME).o
$(MODULE_NAME)-objs := src/pipower5_main.o src/pipower5_i2c.o src/pipower5_sysfs.o src/pipower5_power.o src/pipower5_button.o src/pipower5_shutdown.o

# Kernel build directory
KDIR := /lib/modules/$(shell uname -r)/build

# Current directory
PWD := $(shell pwd)

# Extra compiler flags to include header directory
EXTRA_CFLAGS := -I$(PWD)/include

# Default target
all: prepare module dtbo

# Prepare build directory
prepare:
	@echo "Preparing build directory..."
	@mkdir -p $(BUILD_DIR)
	@echo "Build directory prepared."

# Build the kernel module
module:
	@echo "Compiling $(MODULE_NAME) kernel module..."
	$(MAKE) -C $(KDIR) M=$(PWD) EXTRA_CFLAGS="$(EXTRA_CFLAGS)" modules
	@mv $(MODULE_NAME).ko $(BUILD_DIR)/
	@mv $(MODULE_NAME).mod $(BUILD_DIR)/
	@mv $(MODULE_NAME).mod.c $(BUILD_DIR)/
	@mv $(MODULE_NAME).o $(BUILD_DIR)/
	@mv .$(MODULE_NAME).ko.cmd $(BUILD_DIR)/
	@mv .$(MODULE_NAME).mod.cmd $(BUILD_DIR)/
	@mv .$(MODULE_NAME).o.cmd $(BUILD_DIR)/
	@mv .module-common.o $(BUILD_DIR)/
	@mv ..module-common.o.cmd $(BUILD_DIR)/
	@mv modules.order $(BUILD_DIR)/
	@mv .modules.order.cmd $(BUILD_DIR)/
	@mv Module.symvers $(BUILD_DIR)/
	@mv .Module.symvers.cmd $(BUILD_DIR)/
	@echo "Compilation completed."

# Build the device tree overlay
dtbo:
	@echo "Compiling device tree overlay..."
	dtc -@ -I dts -O dtb -o $(DT_OVERLAY_DST) $(DT_OVERLAY_SRC)
	@echo "Device tree overlay compiled."

# Clean build files
clean:
	@echo "Cleaning build files..."
	$(MAKE) -C $(KDIR) M=$(PWD) clean
	@rm -rf $(BUILD_DIR)
	@echo "Clean completed."

# Install the module
install: module dtbo
	@echo "Installing $(MODULE_NAME) module..."
	sudo cp $(BUILD_DIR)/$(MODULE_NAME).ko /lib/modules/$(shell uname -r)/kernel/drivers/misc/
	sudo cp $(DT_OVERLAY_DST) /boot/firmware/overlays/
	sudo depmod -a
	sudo modprobe $(MODULE_NAME)
	@echo "Module installed and loaded."

# Uninstall the module
uninstall:
	@echo "Uninstalling $(MODULE_NAME) module..."
	sudo modprobe -r $(MODULE_NAME) 2>/dev/null || true
	sudo rm -f /lib/modules/$(shell uname -r)/kernel/drivers/misc/$(MODULE_NAME).ko
	sudo rm -f /boot/firmware/overlays/$(notdir $(DT_OVERLAY_DST))
	sudo depmod -a
	@echo "Module uninstalled."

# Load the module
load:
	@echo "Loading $(MODULE_NAME) module..."
	sudo modprobe $(MODULE_NAME)
	@echo "Module loaded."

# Unload the module
unload:
	@echo "Unloading $(MODULE_NAME) module..."
	sudo modprobe -r $(MODULE_NAME)
	@echo "Module unloaded."

# Check if module is loaded
status:
	@echo "Checking $(MODULE_NAME) module status..."
	@if lsmod | grep -q $(MODULE_NAME); then \
		echo "$(MODULE_NAME) module is loaded."; \
	else \
		echo "$(MODULE_NAME) module is not loaded."; \
	fi

# Show help
help:
	@echo "$(MODULE_NAME) Driver Makefile"
	@echo ""
	@echo "Usage:"
	@echo "  make all       - Compile the module and device tree overlay (default)"
	@echo "  make module    - Compile the module"
	@echo "  make dtbo      - Compile the device tree overlay"
	@echo "  make clean     - Remove compiled files"
	@echo "  make install   - Compile and install the module and device tree overlay"
	@echo "  make uninstall - Remove the module and device tree overlay"
	@echo "  make load      - Load the module"
	@echo "  make unload    - Unload the module"
	@echo "  make status    - Check if module is loaded"
	@echo "  make help      - Show this help message"
	@echo ""

.PHONY: all prepare module dtbo clean install uninstall load unload status help