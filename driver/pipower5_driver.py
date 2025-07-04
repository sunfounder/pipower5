import os
import time
import random
import sys
import logging
import fcntl
import ctypes

from pipower5 import PiPower5

# Kernel constant definitions
_IOC_NONE = 0
_IOC_WRITE = 1
_IOC_READ = 2

# Correct bit shifting for ioctl commands
_IOC_NRBITS = 8
_IOC_TYPEBITS = 8
_IOC_SIZEBITS = 14
_IOC_DIRBITS = 2

_IOC_NRSHIFT = 0
_IOC_TYPESHIFT = _IOC_NRSHIFT + _IOC_NRBITS
_IOC_SIZESHIFT = _IOC_TYPESHIFT + _IOC_TYPEBITS
_IOC_DIRSHIFT = _IOC_SIZESHIFT + _IOC_SIZEBITS

def _IOC(direction, type_nr, number, size):
    return ((direction << _IOC_DIRSHIFT) |
            (ord(type_nr) << _IOC_TYPESHIFT) |
            (number << _IOC_NRSHIFT) |
            (size << _IOC_SIZESHIFT))

def _IOW(type_nr, number, size):
    return _IOC(_IOC_WRITE, type_nr, number, size)

def _IOR(type_nr, number, size):
    return _IOC(_IOC_READ, type_nr, number, size)

class PowerSupplyProperties(ctypes.Structure):
    _fields_ = [
        ('name', ctypes.c_char * 32),
        ('type', ctypes.c_int),
        ('technology', ctypes.c_int),
        ('status', ctypes.c_int),
        ('capacity', ctypes.c_int),
        ('capacity_level', ctypes.c_int),
        ('present', ctypes.c_int),
        ('online', ctypes.c_int),
        ('voltage_max_design', ctypes.c_long),
        ('voltage_min_design', ctypes.c_long),
        ('voltage_now', ctypes.c_long),
        ('current_now', ctypes.c_long),
        ('energy_full', ctypes.c_long),
        ('energy_now', ctypes.c_long),
        ('energy_full_design', ctypes.c_long),
        ('power_now', ctypes.c_long),
    ]

# Define ioctl commands
PIPOWER_5_REGISTER = _IOW('V', 0x10, ctypes.sizeof(PowerSupplyProperties))
PIPOWER_5_UNREGISTER = _IOW('V', 0x11, ctypes.sizeof(ctypes.c_int))
PIPOWER_5_UPDATE = _IOW('V', 0x12, ctypes.sizeof(PowerSupplyProperties))

# Other constant definitions
_POWER_SUPPLY_TYPE_BATTERY = 1
_POWER_SUPPLY_TYPE_USB = 2

class BatteryDriver:
    def __init__(self):
        self.logger = self.setup_logging()
        self.check_root()
        self.device_path = self.find_device()
        self.device_fd = self.open_device()
        self.props = PowerSupplyProperties()
        self.register_battery()
        self.pipower5 = PiPower5()
        
    def setup_logging(self):
        logger = logging.getLogger('pipower5')
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        return logger
    
    def check_root(self):
        if os.getuid() != 0:
            self.logger.error("Root privileges required to run this program")
            sys.exit(1)
            
    def find_device(self):
        # Possible device paths
        possible_paths = [
            "/dev/pipower5",
            "/dev/misc/pipower5"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                self.logger.info(f"Found virtual device interface: {path}")
                return path
                
        self.logger.error("Virtual battery device interface not found")
        self.logger.info("Please load the virtual battery kernel module: sudo modprobe pipower5")
        sys.exit(1)
        
    def open_device(self):
        try:
            fd = os.open(self.device_path, os.O_RDWR)
            self.logger.info(f"Device opened successfully: {self.device_path}")
            return fd
        except OSError as e:
            self.logger.error(f"Failed to open device {self.device_path}: {e}")
            sys.exit(1)
            
    def register_battery(self):
        # Initialize battery properties
        self.props.name = b"PiPower 5"
        self.props.type = _POWER_SUPPLY_TYPE_BATTERY
        self.props.present = 1
        self.props.online = 1
        self.props.technology = 2  # Li-ion
        self.props.capacity = 100
        self.props.capacity_level = 1  # Normal
        self.props.voltage_max_design = 8400000  # 8.4V
        self.props.voltage_min_design = 6200000  # 6.2V
        self.props.voltage_now = 8400000  # 8.4V
        self.props.current_now = 1500000  # 1.5A
        self.props.status = 1  # Discharging
        self.props.energy_full = 14800000  # 14.8Wh
        self.props.energy_now = 0  # 0
        self.props.energy_full_design = 14800000  # 14.8Wh
        self.props.power_now = 1500000  # 1.5W
        
        try:
            fcntl.ioctl(self.device_fd, PIPOWER_5_REGISTER, self.props)
            self.logger.info("Virtual battery registered successfully")
        except OSError as e:
            self.logger.exception(f"Battery registration failed: {e}")
            sys.exit(1)
                
    def unregister_battery(self):
        try:
            # Use any non-zero value to unregister
            unreg = ctypes.c_int(1)
            fcntl.ioctl(self.device_fd, PIPOWER_5_UNREGISTER, unreg)
            self.logger.info("Virtual battery unregistered")
        except OSError as e:
            self.logger.error(f"Failed to unregister battery: {e}")
                
    def update_battery(self):
        # Random status changes (original comment updated for clarity)
        data_buffer = self.pipower5.read_all()

        present = 1 if data_buffer['battery_percentage'] > 2 else 0
        capacity = int(data_buffer['battery_percentage'])
        
        status_code = 0
        if data_buffer['is_charging']:
            status_code = 1 # Charging
        elif data_buffer['battery_current'] > 20:
            status_code = 2 # Discharging
        elif data_buffer['battery_percentage'] == 100:
            status_code = 4 # Full
        else:
            status_code = 3 # Not Charging

        # Set capacity level based on capacity
        if data_buffer['battery_percentage'] > 90:
            capacity_level = 5  # Full
        elif data_buffer['battery_percentage'] > 80:
            capacity_level = 4  # High
        elif data_buffer['battery_percentage'] > 30:
            capacity_level = 3  # Normal
        elif data_buffer['battery_percentage'] > 10:
            capacity_level = 2  # Low
        else:
            capacity_level = 1  # Critical
        
        voltage_now = data_buffer['battery_voltage'] * 1000
        voltage_now = int(round(voltage_now))
        current_now = data_buffer['battery_current'] * 1000
        current_now = int(round(current_now))
        energy_now = data_buffer['battery_percentage'] * self.props.energy_full_design / 100
        energy_now = int(round(energy_now))
        power_now = data_buffer['battery_voltage'] * data_buffer['battery_current'] / 1000
        power_now = int(round(power_now))

        # Update properties
        self.props.present = present
        self.props.capacity = capacity
        self.props.online = int(data_buffer['is_input_plugged_in'])
        self.props.capacity_level = capacity_level
        self.props.status = status_code
        self.props.voltage_now = voltage_now
        self.props.current_now = current_now
        self.props.energy_now = energy_now
        self.props.power_now = power_now

        try:
            fcntl.ioctl(self.device_fd, PIPOWER_5_UPDATE, self.props)
        except OSError as e:
            self.logger.error(f"Failed to update battery status: {e}")
            
    def run(self):
        self.logger.info("Starting PiPower 5 battery service")
        
        try:
            while True:
                self.update_battery()
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.logger.info("Ctrl+C detected, stopping service")
        except Exception as e:
            self.logger.exception(f"Runtime error: {e}")
        finally:
            self.unregister_battery()
            os.close(self.device_fd)
            self.logger.info("Service stopped")

if __name__ == "__main__":
    
    try:
        battery = BatteryDriver()
        battery.run()
    except Exception as e:
        logging.error(f"Startup failed: {e}")
        sys.exit(1)