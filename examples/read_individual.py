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
        print(f"Shutdown request: {int(shutdown_request)} - {shutdown_request.name}")
        button_state = pipower5.read_power_btn()
        print(f"Button state: {int(button_state)} - {button_state.name}")
        print(f'Board id: {pipower5.read_board_id()}')
        print(f"read_always_on on: {pipower5.read_default_on()}")
        print(f"Shutdown percentage: {pipower5.read_shutdown_percentage()} %")

        print('')
        time.sleep(1)

if __name__ == '__main__':
    main()
