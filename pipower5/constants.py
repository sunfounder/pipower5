
NAME = "PiPower 5"
ID = "pipower5"
PERIPHERALS = [
    "storage",
    "cpu",
    "network",
    "memory",
    "history",
    "log",
    "spc",
    "cpu_temperature",
    "gpu_temperature",
    "temperature_unit",
    "input_voltage",
    "is_input_plugged_in",
    "output_voltage",
    "output_current",
    "output_power",
    "power_source",
    "battery_voltage",
    "battery_current",
    "battery_percentage",
    "is_charging",
    "shutdown_percentage",
    "default_on",
    "data_interval",
]

SYSTEM_DEFAULT_CONFIG = {
    'temperature_unit': 'C',
    'interval': 1,
}

CUSTOM_PERIPHERALS = {
    "pwm_fan": False
}
