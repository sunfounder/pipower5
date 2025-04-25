#!/usr/bin/env python3
from pipower5 import PiPower5
import time

pipower5 = PiPower5()

def main():
    print(f"Firmware Version: {pipower5.read_firmware_version()}")
    time.sleep(2)

    while True:
        # Read the data before clearing the screen，to retain the last data when an error occurs.
        data_buffer = pipower5.read_all()
        
        print(f"Input voltage: {data_buffer['input_voltage']} mV")
        print(f"Output voltage: {data_buffer['output_voltage']} mV")
        print(f"Output current: {data_buffer['output_current']} mA")
        print(f"Battery voltage: {data_buffer['battery_voltage']} mV")
        print(f"Battery current: {data_buffer['battery_current']} mA")
        print(f"Battery percentage: {data_buffer['battery_percentage']} %")
        print(f"Power source: {data_buffer['power_source']} - {'Battery' if data_buffer['power_source'] == pipower5.BATTERY else 'External'}")
        print(f"Input plugged in: {data_buffer['is_input_plugged_in']}")
        print(f"Charging: {data_buffer['is_charging']}")
        print('')
        print(f"Internal data:")
        shutdown_request_str = 'None'
        if data_buffer['shutdown_request'] == pipower5.SHUTDOWN_REQUEST_NONE:
            shutdown_request_str = 'None'
        elif data_buffer['shutdown_request'] == pipower5.SHUTDOWN_REQUEST_LOW_BATTERY:
            shutdown_request_str = 'Low battery'
        elif data_buffer['shutdown_request'] == pipower5.SHUTDOWN_REQUEST_BUTTON:
            shutdown_request_str = 'Button'
        else:
            shutdown_request_str = 'Unknown'
        print(f"Shutdown request: {data_buffer['shutdown_request']} - {shutdown_request_str}")
        print(f"Max chargig current: {pipower5.i2c.read_byte_data(150)*100} mA")
        print(f'Board id: {pipower5.read_board_id()}')
        print(f"Default on: {pipower5.read_default_on()}")
        print(f"Shutdown percentage: {pipower5.read_shutdown_percentage()} %")

        print('')
        print('')
        time.sleep(1)

if __name__ == '__main__':
    main()
