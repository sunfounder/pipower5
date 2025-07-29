import os
import sys
import logging
import fcntl
import ctypes

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
        ('charge_full', ctypes.c_long),
        ('charge_full_design', ctypes.c_long),
        ('charge_now', ctypes.c_long),
        ('temp', ctypes.c_long),
        ('temp_ambient', ctypes.c_long),
        ('time_to_full', ctypes.c_long),
        ('time_to_empty', ctypes.c_long),
        ('cycle_count', ctypes.c_int),
    ]

# Define ioctl commands
PIPOWER_5_REGISTER = _IOW('V', 0x10, ctypes.sizeof(PowerSupplyProperties))
PIPOWER_5_UNREGISTER = _IOW('V', 0x11, ctypes.sizeof(ctypes.c_int))
PIPOWER_5_UPDATE = _IOW('V', 0x12, ctypes.sizeof(PowerSupplyProperties))

# Other constant definitions
POWER_SUPPLY_TYPE_UNKNOWN = 0
POWER_SUPPLY_TYPE_BATTERY = 1
POWER_SUPPLY_TYPE_UPS = 2
POWER_SUPPLY_TYPE_MAINS = 3
POWER_SUPPLY_TYPE_USB = 4
POWER_SUPPLY_TYPE_USB_DCP = 5
POWER_SUPPLY_TYPE_USB_CDP = 6
POWER_SUPPLY_TYPE_USB_ACA = 7

class BatteryDevice:
    def __init__(self, log=None):
        self.log = log or logging.getLogger('BatteryDevice')
        self.device_path = self.find_device()
        self.device_fd = self.open_device()
        self.props = PowerSupplyProperties()
        self.register_battery()
        
    def find_device(self):
        # Possible device paths
        possible_paths = [
            "/dev/pipower5",
            "/dev/misc/pipower5"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                self.log.info(f"Found virtual device interface: {path}")
                return path
                
        self.log.error("Virtual battery device interface not found")
        self.log.info("Please load the virtual battery kernel module: sudo modprobe pipower5")
        
    def open_device(self):
        try:
            fd = os.open(self.device_path, os.O_RDWR)
            self.log.info(f"Device opened successfully: {self.device_path}")
            return fd
        except OSError as e:
            self.log.error(f"Failed to open device {self.device_path}: {e}")
            
    def register_battery(self):
        # Initialize battery properties
        self.props.name = b"PiPower 5"
        self.props.type = POWER_SUPPLY_TYPE_UPS
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
        # On Ubuntu energy_full is in mAh
        # self.props.energy_full = 14800000  # 14800mAh
        self.props.energy_full = 2000000  # 2000mAh
        self.props.energy_now = 0  # 0
        # On Ubuntu Power now is in fact the current
        # self.props.energy_full_design = 14800000  # 14800mAh
        self.props.energy_full_design = 2000000  # 2000mAh
        self.props.power_now = 1500000  # 1.5W
        self.props.charge_full = 2000000  # 2000mAh
        self.props.charge_full_design = 2000000  # 2000mAh
        self.props.charge_now = 0  # 0
        self.props.temp = 0  # 0
        self.props.temp_ambient = 0  # 0
        self.props.time_to_full = 0  # 0
        self.props.time_to_empty = 0  # 0
        self.props.cycle_count = 0  # 0
        
        
        try:
            fcntl.ioctl(self.device_fd, PIPOWER_5_REGISTER, self.props)
            self.log.info("Battery device registered successfully")
        except OSError as e:
            self.log.exception(f"Battery device registration failed: {e}")
            sys.exit(1)
                
    def unregister_battery(self):
        try:
            # Use any non-zero value to unregister
            unreg = ctypes.c_int(1)
            fcntl.ioctl(self.device_fd, PIPOWER_5_UNREGISTER, unreg)
            self.log.info("Virtual battery unregistered")
        except OSError as e:
            self.log.error(f"Failed to unregister battery: {e}")
                
    def update_battery(self, data):
        present = 1 if data['battery_percentage'] > 2 else 0
        capacity = int(data['battery_percentage'])
        
        status_code = 0
        if data['is_charging']:
            status_code = 1 # Charging
        elif data['battery_current'] > 20:
            status_code = 2 # Discharging
        elif data['battery_percentage'] == 100:
            status_code = 4 # Full
        else:
            status_code = 3 # Not Charging

        # Set capacity level based on capacity
        if data['battery_percentage'] > 90:
            capacity_level = 5  # Full
        elif data['battery_percentage'] > 80:
            capacity_level = 4  # High
        elif data['battery_percentage'] > 30:
            capacity_level = 3  # Normal
        elif data['battery_percentage'] > 10:
            capacity_level = 2  # Low
        else:
            capacity_level = 1  # Critical
        
        voltage_now = data['battery_voltage'] * 1000
        voltage_now = int(round(voltage_now))
        current_now = data['battery_current'] * 1000
        current_now = int(round(current_now))
        energy_now = data['battery_percentage'] * self.props.energy_full_design / 100
        energy_now = int(round(energy_now))
        # On Ubuntu Power now is in fact the current
        # power_now = data['battery_voltage'] * data['battery_current']
        power_now = data['battery_current'] * 1000
        power_now = int(round(power_now))
        charge_now = data['battery_percentage'] * self.props.charge_full_design / 100
        charge_now = int(round(charge_now))

        # Update properties
        self.props.present = present
        self.props.capacity = capacity
        self.props.online = int(data['is_input_plugged_in'])
        self.props.capacity_level = capacity_level
        self.props.status = status_code
        self.props.voltage_now = voltage_now
        self.props.current_now = current_now
        self.props.energy_now = energy_now
        self.props.power_now = power_now

        try:
            fcntl.ioctl(self.device_fd, PIPOWER_5_UPDATE, self.props)
        except OSError as e:
            self.log.error(f"Failed to update battery status: {e}")
