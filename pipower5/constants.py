
NAME = "PiPower 5"
ID = "pipower5"
PERIPHERALS = [
    "storage",
    "cpu",
    "network",
    "memory",
    "history",
    "log",
    "cpu_temperature",
    "gpu_temperature",
    "temperature_unit",
    "clear_history",
    "delete_log_file",
    "data_interval",
    "debug_level",
    "ip_address",
    "mac_address",
    "restart_service",

    "pwm_fan_speed",

    "pipower5",
    "input_voltage",
    "input_current",
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
    "power-failure-simulation",
    "send_email",
    "pipower5_buzzer",
]

SYSTEM_DEFAULT_CONFIG = {
    "enable_history": True,
    "debug_level": "INFO",
    "data_interval": 1,
    "database_retention_days": 30,
    "temperature_unit": "C",
    "power-failure-simulation": True,
    "shutdown_percentage": 10,
    "send_email_on": [
        "battery_activated",
        "low_battery",
        "power_disconnected",
        "power_restored",
        "power_insufficient",
        "battery_critical_shutdown",
        "battery_voltage_critical_shutdown",
    ],
    "pipower5_buzzer_volume": 5,
    "pipower5_buzz_on": [
        "battery_activated",
        "low_battery",
        "power_disconnected",
        "power_restored",
        "power_insufficient",
        "battery_critical_shutdown",
        "battery_voltage_critical_shutdown",
    ],
    "pipower5_buzz_sequence": {
        "battery_activated": [
            ["A4", 200],  # 中等音调起始
            ["pause", 100],
            ["B4", 200]   # 小幅上升，体现激活状态
        ],
        "low_battery": [
            ["A4", 250],  # 中等音调
            ["pause", 150],
            ["A4", 250],  # 重复提醒
        ],
        "power_disconnected": [
            ["D5", 150],
            ["G4", 150],
        ],
        "power_restored": [
            ["G4", 150],
            ["D5", 150],
        ],
        "power_insufficient": [
            ["B4", 200],
            ["pause", 100],
            ["B4", 200],
            ["pause", 100],
            ["B4", 300] 
        ],
        "battery_critical_shutdown": [
            ["C6", 120],
            ["pause", 60],
            ["C6", 120],
            ["pause", 60],
            ["C6", 400],
        ],
        "battery_voltage_critical_shutdown": [
            ["C6", 120],
            ["pause", 60],
            ["C6", 120],
            ["pause", 60],
            ["C6", 400],
            ["pause", 60],
            ["C6", 400],
        ]
    },
    "send_email_to": "",
    "smtp_email": "",
    "smtp_password": "",
    "smtp_server": "",
    "smtp_port": 465,
    "smtp_security": "ssl",
}

