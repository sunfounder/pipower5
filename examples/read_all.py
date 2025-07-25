#!/usr/bin/env python3
from pipower5.pipower5 import PiPower5, ShutdownRequest
import time

pipower5 = PiPower5()

def main():
    print(f"Firmware Version: {pipower5.read_firmware_version()}")
    time.sleep(2)

    while True:
        data_buffer = pipower5.read_all()

        shutdown_request = pipower5.read_shutdown_request()
        button_state = pipower5.read_power_btn()

        print(f'''
Input:
    voltage: {data_buffer['input_voltage']} mV
    current: {data_buffer['input_current']} mA
    power: {data_buffer['input_voltage'] * data_buffer['input_current'] * 0.000001:.3f} W
    plugged in: {data_buffer['is_input_plugged_in']}
Output: 
    voltage: {data_buffer['output_voltage']} mV
    current: {data_buffer['output_current']} mA
    power: {data_buffer['output_voltage'] * data_buffer['output_current'] * 0.000001:.3f} W
Battery:
    voltage: {data_buffer['battery_voltage']} mV
    current: {data_buffer['battery_current']} mA
    power: {data_buffer['battery_voltage'] * data_buffer['battery_current'] * 0.000001:.3f} W
    percentage: {data_buffer['battery_percentage']} %
    source: {data_buffer['power_source']} - {'Battery' if data_buffer['power_source'] == pipower5.BATTERY else 'External'}
    charging: {data_buffer['is_charging']}

Internal:
    shutdown request: {int(shutdown_request)} - {shutdown_request.name}
    button state: {int(button_state)} - {button_state.name}
    max charging current: {pipower5.get_max_charge_current()} mA
    default on: {'on' if pipower5.read_default_on() else 'off'}
    shutdown percentage: {pipower5.read_shutdown_percentage()} %
''')
        print('')
        print('')
        time.sleep(0.5)

if __name__ == '__main__':
    main()
