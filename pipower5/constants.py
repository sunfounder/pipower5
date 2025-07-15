
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
    'temperature_unit': 'C',
    'data_interval': 1,
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
    "smtp_receiver": "381039379@qq.com",
    "smtp_sender": "381039379@qq.com",
    "smtp_password": "bjwkbepuzepebieb",
    "smtp_server": "smtp.qq.com",
    "smtp_port": 465,
    "smtp_use_tls": False  # 465端口使用SSL，不需要TLS
}

CUSTOM_PERIPHERALS = {
    "pwm_fan": False
}
