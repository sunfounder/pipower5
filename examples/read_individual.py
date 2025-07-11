#!/usr/bin/env python3
from pipower5 import PiPower5
import time

pipower5 = PiPower5()

def main():
    print(f"Firmware Version: {pipower5.read_firmware_version()}")
    time.sleep(2)

    while True:
        print(f"Input voltage: {pipower5.read_input_voltage()} mV")
        print(f"Raspberry Pi voltage: {pipower5.read_output_voltage()} mV")
        print(f"Battery voltage: {pipower5.read_battery_voltage()} mV")
        print(f"Battery percentage: {pipower5.read_battery_percentage()} %")
        power_source = pipower5.read_power_source()
        print(f"Power source: {power_source} - {'Battery' if power_source == pipower5.BATTERY else 'External'}")
        print(f"Input plugged in: {pipower5.read_is_input_plugged_in()}")
        print(f"Charging: {pipower5.read_is_charging()}")

        print('')
        print(f"Internal data:")
        shutdown_request = pipower5.read_shutdown_request()
        shutdown_request_str = 'None'
        if shutdown_request == pipower5.SHUTDOWN_REQUEST_NONE:
            shutdown_request_str = 'None'
        elif shutdown_request == pipower5.SHUTDOWN_REQUEST_LOW_BATTERY:
            shutdown_request_str = 'Low battery'
        elif shutdown_request == pipower5.SHUTDOWN_REQUEST_BUTTON:
            shutdown_request_str = 'Button'
        else:
            shutdown_request_str = 'Unknown'
        print(f"Shutdown request: {shutdown_request} - {shutdown_request_str}")
        print(f'Board id: {pipower5.read_board_id()}')
        print(f"read_always_on on: {pipower5.read_default_on()}")
        print(f"Shutdown percentage: {pipower5.read_shutdown_percentage()} %")


        print('')
        time.sleep(1)

if __name__ == '__main__':
    main()
