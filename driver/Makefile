# PiPower5 Linux Driver Makefile
# Supports DKMS for automatic rebuild on kernel updates

KDIR ?= /lib/modules/$(shell uname -r)/build
PWD := $(shell pwd)

# Extract version from pipower5.h
DRIVER_VERSION := $(shell grep 'PIPOWER5_DRIVER_VERSION' include/pipower5.h | head -1 | sed 's/.*"\(.*\)".*/\1/')

# Module definition - Combine all source files into a single module
obj-m += pipower5.o
pipower5-objs := \
	src/pipower5_main.o \
	src/pipower5_i2c.o \
	src/pipower5_sysfs.o \
	src/pipower5_power.o \
	src/pipower5_button.o \
	src/pipower5_shutdown.o

# Compilation flags
EXTRA_CFLAGS := -I$(PWD)/include

# Device Tree Compiler and overlay file settings
DTC := dtc
DTBO_NAME := sunfounder-pipower5.dtbo
DTOVERLAY_NAME := sunfounder-pipower5

# Automatically detect the correct overlay directory path
OVERLAY_DIRS := \
	/boot/firmware/overlays \
	/boot/overlays \
	/lib/firmware \
	/boot/dtb/overlays

OVERLAY_DIR := $(firstword $(wildcard $(OVERLAY_DIRS)))

# DKMS source destination
DKMS_SRC := /usr/src/pipower5-$(DRIVER_VERSION)

# config.txt path
CONFIG_TXT := $(firstword $(wildcard /boot/firmware/config.txt /boot/config.txt))

# Check that kernel build directory is usable
check_kdir = \
	(if [ ! -f "$(KDIR)/Makefile" ]; then \
		echo "  Kernel headers not found, installing..."; \
		sudo apt install -y linux-headers-$$(uname -r) 2>/dev/null \
		|| sudo apt install -y raspberrypi-kernel-headers 2>/dev/null \
		|| true; \
		if [ ! -f "$(KDIR)/Makefile" ]; then \
			echo "" >&2; \
			echo "ERROR: Failed to install kernel headers." >&2; \
			echo "Try: sudo apt install linux-headers-$$(uname -r)" >&2; \
			echo "  or: sudo apt install raspberrypi-kernel-headers" >&2; \
			exit 1; \
		fi; \
		echo "  Kernel headers installed."; \
	fi)

# ── Build targets ──────────────────────────────────────────────────────────

all: module dtbo

module:
	@echo "Building PiPower5 driver v$(DRIVER_VERSION)..."
	@$(check_kdir)
	$(MAKE) -C $(KDIR) M=$(PWD) EXTRA_CFLAGS="$(EXTRA_CFLAGS)" modules
	@echo "Module build completed."

dtbo:
	@echo "Compiling device tree overlay..."
	$(DTC) -@ -I dts -O dtb -o $(DTBO_NAME) sunfounder-pipower5-overlay.dts
	@echo "Device tree overlay compiled."

clean:
	@echo "Cleaning build files..."
	@if [ -f "$(KDIR)/Makefile" ]; then \
		$(MAKE) -C $(KDIR) M=$(PWD) clean; \
	fi
	rm -f $(DTBO_NAME)
	rm -f Module.symvers modules.order
	@echo "Clean completed."

# ── Install targets ────────────────────────────────────────────────────────

modules_install:
	@echo "Installing kernel module..."
	@$(check_kdir)
	$(MAKE) -C $(KDIR) M=$(PWD) modules_install
	depmod -a
	@echo "Module installed."

install-overlay:
	@echo "Installing device tree overlay to $(OVERLAY_DIR)/"
	@if [ ! -d "$(OVERLAY_DIR)" ]; then \
		echo "Error: Overlay directory $(OVERLAY_DIR) does not exist."; \
		exit 1; \
	fi
	@cp -f $(DTBO_NAME) $(OVERLAY_DIR)/ || { echo "Error: Permission denied. Run with sudo."; exit 1; }

# Add dtoverlay line to config.txt
install-config:
	@if [ -z "$(CONFIG_TXT)" ]; then \
		echo "Error: config.txt not found."; exit 1; \
	fi
	@if grep -q '^dtoverlay=$(DTOVERLAY_NAME)' $(CONFIG_TXT) 2>/dev/null; then \
		echo "dtoverlay=$(DTOVERLAY_NAME) already in config.txt"; \
	elif grep -q '^# *dtoverlay=$(DTOVERLAY_NAME)' $(CONFIG_TXT) 2>/dev/null; then \
		echo "Uncommenting dtoverlay=$(DTOVERLAY_NAME) in config.txt..."; \
		sudo sed -i 's/^# *dtoverlay=$(DTOVERLAY_NAME).*/dtoverlay=$(DTOVERLAY_NAME)/' $(CONFIG_TXT); \
	else \
		echo "Adding dtoverlay=$(DTOVERLAY_NAME) to config.txt..."; \
		echo "dtoverlay=$(DTOVERLAY_NAME)" | sudo tee -a $(CONFIG_TXT) > /dev/null; \
	fi

# Remove dtoverlay line from config.txt
remove-config:
	@if [ -f "$(CONFIG_TXT)" ]; then \
		sudo sed -i '/^dtoverlay=$(DTOVERLAY_NAME)/d' $(CONFIG_TXT) 2>/dev/null || true; \
	fi

# DKMS install
dkms_install:
	@echo "Installing PiPower5 driver via DKMS (v$(DRIVER_VERSION))..."
	@# Check if DKMS is installed
	@if ! command -v dkms >/dev/null 2>&1; then \
		echo "DKMS not found. Installing dkms..."; \
		sudo apt-get update && sudo apt-get install -y dkms || { \
			echo "Error: Failed to install DKMS."; exit 1; \
		}; \
	fi
	@# Clean up old non-DKMS module files
	@sudo rm -f /lib/modules/$(shell uname -r)/extra/pipower5.ko* /lib/modules/$(shell uname -r)/updates/pipower5.ko* 2>/dev/null || true
	@# Remove previous DKMS registrations
	-@for ver in $$(dkms status pipower5 2>/dev/null | sed -n 's/^pipower5\/\([^,]*\).*/\1/p' | sort -u); do \
		sudo dkms remove -m pipower5 -v $$ver --all 2>/dev/null || true; \
	done
	@# Copy source files
	@echo "Copying source to $(DKMS_SRC)..."
	@sudo mkdir -p $(DKMS_SRC)/src $(DKMS_SRC)/include
	@sudo cp -f Makefile dkms.conf $(DKMS_SRC)/
	@sudo cp -f include/*.h $(DKMS_SRC)/include/
	@sudo cp -f src/*.c $(DKMS_SRC)/src/
	@# Update dkms.conf version
	@sudo sed -i 's/^PACKAGE_VERSION=.*/PACKAGE_VERSION="$(DRIVER_VERSION)"/' $(DKMS_SRC)/dkms.conf
	@# Register, build, install
	@sudo dkms add -m pipower5 -v $(DRIVER_VERSION)
	@sudo dkms build -m pipower5 -v $(DRIVER_VERSION)
	@sudo dkms install -m pipower5 -v $(DRIVER_VERSION)
	@echo "DKMS installation completed. Driver will auto-rebuild on kernel updates."

dkms_uninstall:
	@echo "Removing PiPower5 driver from DKMS..."
	@if command -v dkms >/dev/null 2>&1; then \
		sudo dkms remove -m pipower5 -v $(DRIVER_VERSION) --all || echo "DKMS module not found."; \
		sudo rm -rf $(DKMS_SRC); \
	fi
	@echo "DKMS uninstall completed."

# Full install: DKMS + overlay + config.txt + load module
install: module dtbo
	@echo "Installing PiPower5 driver..."
	@# Unload if loaded
	-@sudo rmmod pipower5 2>/dev/null || true
	@# Install DKMS if not present, then use DKMS
	@if ! command -v dkms >/dev/null 2>&1; then \
		echo "DKMS not found. Installing DKMS..."; \
		sudo apt-get update -qq && sudo apt-get install -y dkms || { \
			echo "Failed to install DKMS, falling back to traditional install."; \
			$(MAKE) modules_install; \
		}; \
	fi
	@if command -v dkms >/dev/null 2>&1; then \
		$(MAKE) dkms_install; \
	else \
		$(MAKE) modules_install; \
	fi
	@$(MAKE) install-overlay
	@$(MAKE) install-config
	@echo "Loading pipower5 module..."
	@sudo modprobe pipower5 || echo "Warning: Failed to load module. A reboot may be needed."
	@echo "Installation completed."
	@echo ""
	@echo "Check status with: make status"

# Full uninstall: remove module, DKMS, overlay, config.txt
uninstall:
	@echo "Uninstalling PiPower5 driver..."
	@# Unload module
	@if lsmod | grep -q pipower5; then \
		echo "Unloading pipower5 module..."; \
		sudo rmmod pipower5 || echo "Warning: Failed to unload module."; \
	fi
	@# DKMS uninstall
	-@$(MAKE) dkms_uninstall
	@# Remove from traditional locations (including old pipower5_driver)
	@sudo rm -f /lib/modules/$(shell uname -r)/extra/pipower5.ko* /lib/modules/$(shell uname -r)/updates/pipower5.ko* 2>/dev/null || true
	@sudo rm -f /lib/modules/$(shell uname -r)/kernel/drivers/misc/pipower5_driver.ko* 2>/dev/null || true
	@sudo rm -f /etc/modules-load.d/pipower5_driver.conf 2>/dev/null || true
	@# Remove dtbo
	@if [ -d "$(OVERLAY_DIR)" ]; then \
		sudo rm -f $(OVERLAY_DIR)/$(DTBO_NAME); \
	fi
	@# Remove config.txt entry
	@$(MAKE) remove-config
	depmod -a || true
	@echo "Uninstall completed. Reboot to fully remove."

# ── Utility targets ────────────────────────────────────────────────────────

load:
	@sudo modprobe pipower5 || echo "Failed to load module."

unload:
	@sudo rmmod pipower5 2>/dev/null || echo "Module not loaded."

# Diagnostic status check (like 'doctor')
status:
	@echo "=== PiPower5 Driver Status ==="
	@echo ""
	@# Module file (check multiple locations, including DKMS .ko.xz)
	@KO_PATH=$$(find /lib/modules/$(shell uname -r) -name 'pipower5.ko*' 2>/dev/null | head -1); \
	if [ -n "$$KO_PATH" ]; then \
		echo "Module file      : INSTALLED ($$KO_PATH)"; \
	else \
		echo "Module file      : MISSING (run 'sudo make install')"; \
	fi
	@# DKMS registration
	@if command -v dkms >/dev/null 2>&1; then \
		if dkms status pipower5 2>/dev/null | grep -q pipower5; then \
			echo "DKMS status      : $(shell dkms status pipower5 2>/dev/null | head -1)"; \
		else \
			echo "DKMS status      : not registered"; \
		fi; \
	else \
		echo "DKMS status      : DKMS not installed"; \
	fi
	@# Module loaded
	@if lsmod | grep -q pipower5; then \
		echo "Module loaded    : YES"; \
	else \
		echo "Module loaded    : NO"; \
	fi
	@# sysfs interface
	@if [ -d /sys/class/pipower5/pipower5 ]; then \
		echo "sysfs interface  : EXISTS (/sys/class/pipower5/pipower5)"; \
	else \
		echo "sysfs interface  : MISSING"; \
	fi
	@# device tree overlay
	@if [ -f "$(OVERLAY_DIR)/$(DTBO_NAME)" ]; then \
		echo "Device tree blob : INSTALLED ($(OVERLAY_DIR)/$(DTBO_NAME))"; \
	else \
		echo "Device tree blob : MISSING"; \
	fi
	@# config.txt
	@if [ -f "$(CONFIG_TXT)" ] && grep -q '^dtoverlay=$(DTOVERLAY_NAME)' $(CONFIG_TXT) 2>/dev/null; then \
		echo "config.txt       : OK (dtoverlay=$(DTOVERLAY_NAME))"; \
	else \
		echo "config.txt       : MISSING (add: dtoverlay=$(DTOVERLAY_NAME))"; \
	fi
	@# power supply
	@if [ -d /sys/class/power_supply/pipower5 ]; then \
		echo "power_supply     : REGISTERED (/sys/class/power_supply/pipower5)"; \
	else \
		echo "power_supply     : MISSING"; \
	fi
	@echo ""

help:
	@echo "PiPower5 Driver Makefile v$(DRIVER_VERSION)"
	@echo ""
	@echo "Build:"
	@echo "  make all            - Build module + device tree overlay"
	@echo "  make module         - Build kernel module only"
	@echo "  make dtbo           - Build device tree overlay only"
	@echo "  make clean          - Remove build artifacts"
	@echo ""
	@echo "Install:"
	@echo "  make install        - Full install (DKMS + overlay + config.txt)"
	@echo "  make dkms_install   - Install via DKMS (survives kernel updates)"
	@echo "  make uninstall      - Full uninstall"
	@echo ""
	@echo "Utility:"
	@echo "  make status         - Diagnostic health check"
	@echo "  make load           - Load the module"
	@echo "  make unload         - Unload the module"
	@echo ""

.PHONY: all module dtbo clean modules_install install-overlay install-config remove-config \
        dkms_install dkms_uninstall install uninstall load unload status help