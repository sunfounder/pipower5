
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
    "pwm_fan_speed",
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
    "power-failure-simulation",
]

SYSTEM_DEFAULT_CONFIG = {
    'enable_history': True,
    'temperature_unit': 'C',
    'data_interval': 1,
    'database_retention_days': 30,
    'power-failure-simulation': True,
    'shutdown_percentage': 10,
}

CUSTOM_PERIPHERALS = {}
