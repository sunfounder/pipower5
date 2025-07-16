
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
    "power-failure-simulation",
]

SYSTEM_DEFAULT_CONFIG = {
    'enable_history': True,
    'data_interval': 1,
    'database_retention_days': 30,
    'temperature_unit': 'C',
    'power-failure-simulation': True,
    'shutdown_percentage': 10,
    'send_email_on': [
        "battery_activated",
        "low_battery",
        "power_disconnected",
        "power_restored",
        "power_insufficient",
        "battery_critical_shutdown",
        "battery_voltage_critical_shutdown",
    ],
    "send_email_to": "",
    "smtp_email": "",
    "smtp_password": "",
    "smtp_server": "",
    "smtp_port": 465,
    "smtp_use_tls": False
}

CUSTOM_PERIPHERALS = {
    "pwm_fan": False
}
