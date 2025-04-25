#!/usr/bin/env python3
from pipower5 import PiPower5
import time

pipower5 = PiPower5()

print(f"Board name: {pipower5.device.name}")
print(f"Firmware Version: {pipower5.read_firmware_version()}")
print(f"Set shutdown percentage example, shutdown percentage means if it's not charging, ")
print(f"and the battery percentage is less than the shutdown percentage, it will give a ")
print(f"shutdown request Low Battery, for device to safely shutdown.")
time.sleep(2)

def test(value):
    print(f"Current shutdown percentage: {pipower5.read_shutdown_percentage()}%")
    time.sleep(2)
    print(f"Setting shutdown percentage to {value}%")
    pipower5.write_shutdown_percentage(value)
    time.sleep(2) # Wait for the shutdown percentage to be updated
    current_shutdown_battery_percentage = pipower5.read_shutdown_percentage()
    print(f"Shutdown percentage: {current_shutdown_battery_percentage}%")
    if current_shutdown_battery_percentage == value:
        print("Success")
    else:
        print("Failed, shutdown percentage range is 10-100%")

test(20)
time.sleep(2)
test(10)
time.sleep(2)
test(0)
time.sleep(2)