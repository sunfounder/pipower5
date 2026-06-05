
NAME = "PiPower 5"
ID = "pipower5"

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
    "pipower5_buzzer_volume": 3,
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
        "battery_activated": "A4,50:p,100:B4,50",
        "low_battery": "A4,50:p,100:A4,50",
        "power_disconnected": "D5,50:p,100:G4,50",
        "power_restored": "G4,50:p,100:D5,50",
        "power_insufficient": "B4,50:p,100:B4,50:p,100:B4,100",
        "battery_critical_shutdown": "C6,50:p,60:C6,50:p,60:C6,100",
        "battery_voltage_critical_shutdown": "C6,50:p,60:C6,50:p,60:C6,100:p,60:C6,100",
    },
    "send_email_to": "",
    "smtp_email": "",
    "smtp_password": "",
    "smtp_server": "",
    "smtp_port": 465,
    "smtp_security": "ssl",
}

