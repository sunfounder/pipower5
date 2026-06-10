import json
from enum import IntEnum, StrEnum
from .device import check_pipower5_connected, DEVICE_PATH

BAT_MAX_CAPACITY = 2000  # mAh


class PowerSource(IntEnum):
    EXTERNAL = 0
    BATTERY = 1


class ButtonState(IntEnum):
    RELEASED = 0
    CLICK = 1
    DOUBLE_CLICK = 2
    LONG_PRESS_2S = 3
    LONG_PRESS_2S_RELEASED = 4
    LONG_PRESS_5S = 5
    LONG_PRESS_5S_RELEASED = 6


class ShutdownRequest(IntEnum):
    NONE = 0
    LOW_BATTERY = 1
    BUTTON = 2
    LOW_VOLTAGE = 3


class Event(StrEnum):
    BATTERY_ACTIVATED = "battery_activated"
    LOW_BATTERY = "low_battery"
    POWER_DISCONNECTED = "power_disconnected"
    POWER_RESTORED = "power_restored"
    POWER_INSUFFICIENT = "power_insufficient"
    BATTERY_CRITICAL_SHUTDOWN = "battery_critical_shutdown"
    BATTERY_VOLTAGE_CRITICAL_SHUTDOWN = "battery_voltage_critical_shutdown"


class PiPower5:
    """PiPower5 hardware interface -  reads sensors via sysfs, writes via sysfs."""

    BAT_MAX_CAPACITY = BAT_MAX_CAPACITY

    def __init__(self):
        check_pipower5_connected()

    # ---- SysFS helpers ----

    @staticmethod
    def _read_sysfs(name):
        with open(f"{DEVICE_PATH}/{name}", "r") as f:
            return f.read().strip()

    @classmethod
    def _read_sysfs_int(cls, name):
        return int(cls._read_sysfs(name))

    @staticmethod
    def _write_sysfs(name, value):
        with open(f"{DEVICE_PATH}/{name}", "w") as f:
            f.write(str(value))

    # ---- Sensor reads ----

    read_input_voltage       = lambda self: self._read_sysfs_int("input_voltage")
    read_input_current       = lambda self: self._read_sysfs_int("input_current")
    read_input_power         = lambda self: self._read_sysfs_int("input_power")
    read_output_voltage      = lambda self: self._read_sysfs_int("output_voltage")
    read_output_current      = lambda self: self._read_sysfs_int("output_current")
    read_output_power        = lambda self: self._read_sysfs_int("output_power")
    read_battery_voltage     = lambda self: self._read_sysfs_int("battery_voltage")
    read_battery_current     = lambda self: self._read_sysfs_int("battery_current")
    read_battery_percentage  = lambda self: self._read_sysfs_int("battery_percentage")
    read_battery_capacity    = lambda self: self._read_sysfs_int("battery_capacity")
    read_is_input_plugged_in = lambda self: bool(self._read_sysfs_int("is_input_plugged_in"))
    read_is_charging         = lambda self: bool(self._read_sysfs_int("is_charging"))
    read_power_source        = lambda self: PowerSource(self._read_sysfs_int("power_source"))
    read_shutdown_percentage = lambda self: self._read_sysfs_int("shutdown_percentage")
    read_firmware_version    = lambda self: self._read_sysfs("firmware_version")
    read_default_on          = lambda self: bool(self._read_sysfs_int("default_on"))
    get_max_charge_current   = lambda self: self._read_sysfs_int("charge_current_max") * 100
    read_buzzer_volume       = lambda self: self._read_sysfs_int("buzzer_volume")
    get_buzzer_volume        = read_buzzer_volume
    read_power_btn           = lambda self: ButtonState(self._read_sysfs_int("power_button_state"))

    # ---- Write operations ----

    write_shutdown_percentage = lambda self, v: self._write_sysfs("shutdown_percentage", v)
    set_buzzer_volume         = lambda self, v: self._write_sysfs("buzzer_volume", v)
    write_buzzer_volume       = set_buzzer_volume

    # ---- Aggregate read ----

    def read_all(self):
        return {
            "input_voltage": self.read_input_voltage(),
            "input_current": self.read_input_current(),
            "output_voltage": self.read_output_voltage(),
            "output_current": self.read_output_current(),
            "battery_voltage": self.read_battery_voltage(),
            "battery_current": self.read_battery_current(),
            "battery_percentage": self.read_battery_percentage(),
            "power_source": self.read_power_source(),
            "is_input_plugged_in": self.read_is_input_plugged_in(),
            "is_charging": self.read_is_charging(),
        }
