#!/usr/bin/env python3
from pipower5 import PiPower5
import time

pipower5 = PiPower5()

def main():
    print(f"Firmware Version: {pipower5.read_firmware_version()}")
    time.sleep(2)

    while True:
        data_buffer = pipower5.read_all()
        #
        shutdown_request_str = 'None'
        if data_buffer['shutdown_request'] == pipower5.SHUTDOWN_REQUEST_NONE:
            shutdown_request_str = 'None'
        elif data_buffer['shutdown_request'] == pipower5.SHUTDOWN_REQUEST_LOW_BATTERY:
            shutdown_request_str = 'Low battery'
        elif data_buffer['shutdown_request'] == pipower5.SHUTDOWN_REQUEST_BUTTON:
            shutdown_request_str = 'Button'
        else:
            shutdown_request_str = 'Unknown'
        #
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
    shutdown request: {data_buffer['shutdown_request']} - {shutdown_request_str}
    max charging current: {pipower5.get_max_charge_current()} mA
    default on: {'on' if pipower5.read_default_on() else 'off'}
    shutdown percentage: {pipower5.read_shutdown_percentage()} %
''')
        print('')
        print('')
        time.sleep(1)

if __name__ == '__main__':
    main()
