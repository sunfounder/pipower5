
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


def get_device_tree_path():
    """
    获取设备树路径。
    
    Returns:
        str: 设备树路径，如果不存在则返回None。
    """
    from os import path
    device_tree_path = '/proc/device-tree'
    if not path.exists(device_tree_path):
        device_tree_path = '/device-tree'
        if not path.exists(device_tree_path):
            return None
    return device_tree_path

def read_device_tree_file(file_path):
    from os import path
    if not path.exists(file_path):
        return None
    with open(file_path, "r") as f:
        result = f.read()[:-1]
        result = int(result, 16)
        return result

def get_part_number():
    """
    获取HAT设备的版本号。
    
    如果未发现HAT设备或发生错误，则返回错误码。
    
    Returns:
        str: HAT设备的PN号。
    """
    from os import listdir
    device_tree_path = get_device_tree_path()
    part_number = ""
    if device_tree_path is None:
        return
    hat_path = None
    for file in listdir(device_tree_path):
        if file.startswith('hat'):
            hat_path = f"{device_tree_path}/{file}"
            break
    if hat_path is None:
        return
    product_id_file = f"{hat_path}/product_id"
    product_ver_file = f"{hat_path}/product_ver"

    try:
        product_id = read_device_tree_file(product_id_file)
        product_ver = read_device_tree_file(product_ver_file)
        if product_id is None or product_ver is None:
            return
        part_number = f"{product_id:04d}V{product_ver:02d}"
    except Exception as e:
        # print(f"Error: {e}")
        pass
    
    return part_number

def get_varient_id_and_version():
    import os
    # Set Variant
    # Check environment variable PIRONMAN5_PART_NUMBER
    part_number = os.getenv('PIRONMAN5_PART_NUMBER', None)
    if part_number == None:
        # Get variant from hat info
        part_number = get_part_number()
    if part_number == None:
        part_number = "0306V10"
    # Set variant
    varient_id = part_number.split('V')[0]
    version_id = part_number.split('V')[1]
    return varient_id, version_id
