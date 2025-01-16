#!/usr/bin/env python3
from spc.spc import SPC
import time

spc = SPC()

def main():
    print(f"Firmware Version: {spc.read_firmware_version()}")
    time.sleep(2)

    while True:
        print(f"Input voltage: {spc.read_input_voltage()} mV")
        print(f"Raspberry Pi voltage: {spc.read_output_voltage()} mV")
        print(f"Battery voltage: {spc.read_battery_voltage()} mV")
        print(f"Battery percentage: {spc.read_battery_percentage()} %")
        power_source = spc.read_power_source()
        print(f"Power source: {power_source} - {'Battery' if power_source == spc.BATTERY else 'External'}")
        print(f"Input plugged in: {spc.read_is_input_plugged_in()}")
        print(f"Charging: {spc.read_is_charging()}")

        print('')
        print(f"Internal data:")
        shutdown_request = spc.read_shutdown_request()
        shutdown_request_str = 'None'
        if shutdown_request == spc.SHUTDOWN_REQUEST_NONE:
            shutdown_request_str = 'None'
        elif shutdown_request == spc.SHUTDOWN_REQUEST_LOW_BATTERY:
            shutdown_request_str = 'Low battery'
        elif shutdown_request == spc.SHUTDOWN_REQUEST_BUTTON:
            shutdown_request_str = 'Button'
        else:
            shutdown_request_str = 'Unknown'
        print(f"Shutdown request: {shutdown_request} - {shutdown_request_str}")
        print(f'Board id: {spc.read_board_id()}')
        print(f"read_always_on on: {spc.read_default_on()}")
        print(f"Shutdown percentage: {spc.read_shutdown_percentage()} %")

        print('')
        time.sleep(1)

if __name__ == '__main__':
    main()
