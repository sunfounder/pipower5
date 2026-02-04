""" PiPower 5 device related functions
"""

__all__ = [
    'NAME',
    'ID',
    'UUID',
    'PRODUCT_ID',
    'PRODUCT_VER',
    'VENDOR',
    'is_installed',
    'is_connected',
    'check_pipower5_connected',
]

import os

HAT_DEVICE_TREE = "/proc/device-tree"

NAME = "PiPower 5"
""" Name of the board """

ID = "pipower5"
""" ID of the board """

UUID = "9daeea78-0000-0a2a-0033-582369ac3e02"
""" UUID of the board """

PRODUCT_ID = 0x0a2a
""" Product ID of the board """

PRODUCT_VER = 0x0033
""" Product version of the board """

VENDOR = "SunFounder"
""" Vendor of the board """ 


DEVICE_PATH = "/sys/class/pipower5/pipower5"

def is_installed() -> bool:
    """ Check if a PiPower 5 board is installed

    Returns:
        bool: True if installed, False otherwise
    """
    for file in os.listdir(HAT_DEVICE_TREE):
        if 'hat' in file:
            if os.path.exists(f"{HAT_DEVICE_TREE}/{file}/uuid") \
                and os.path.isfile(f"{HAT_DEVICE_TREE}/{file}/uuid"):
                with open(f"{HAT_DEVICE_TREE}/{file}/uuid", "r") as f:
                    uuid = f.read()[:-1] # [:-1] rm \x00
                    product_id = uuid.split("-")[2]
                    product_id = int(product_id, 16)
                    if product_id == PRODUCT_ID:
                        return True
    return False

def is_connected() -> bool:
    """ Check if PiPower 5 is connected

    Returns:
        bool: True if connected
    """
    return os.path.exists(DEVICE_PATH)

def check_pipower5_connected() -> bool:
    """ Check if PiPower 5 is ready

    Returns:
        bool: True if ready
    """
    if not is_installed():
        raise IOError("PiPower 5 not installed, make sure it is inserted on the Raspberry Pi.")
    
    if not is_connected():
        raise IOError("PiPower 5 not connected, check if PiPower 5 is powered on.")
 