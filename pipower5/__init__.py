from .version import __version__

def main():
    from spc.spc import SPC
    import argparse
    import time
    import sys

    spc = SPC()
    parser = argparse.ArgumentParser(description='PiPower 5')
    parser.add_argument('command', nargs='?', help='Command')
    parser.add_argument('-sp', '--shutdown-percentage', nargs='?', default='', help='Set shutdown percentage, leave empty to read')
    parser.add_argument('-iv', '--input-voltage', action='store_true', help='Read input voltage')
    parser.add_argument('-ov', '--output-voltage', action='store_true', help='Read output voltage')
    parser.add_argument('-oc', '--output-current', action='store_true', help='Read output current')
    parser.add_argument('-bv', '--battery-voltage', action='store_true', help='Read battery voltage')
    parser.add_argument('-bc', '--battery-current', action='store_true', help='Read battery current')
    parser.add_argument('-bp', '--battery-percentage', action='store_true', help='Read battery percentage')
    parser.add_argument('-bs', '--battery-source', action='store_true', help='Read battery source')
    parser.add_argument('-ii', '--is-input-plugged_in', action='store_true', help='Read is input plugged in')
    parser.add_argument('-ic', '--is-charging', action='store_true', help='Read is charging')
    parser.add_argument('-do', '--default-on', action='store_true', help='Read default on')
    parser.add_argument('-sr', '--shutdown-request', action='store_true', help='Read shutdown request')
    parser.add_argument('-cc', '--charging-current', action='store_true', help='Max charging current')
    parser.add_argument('-bi', '--board-id', action='store_true', help='Read board id')
    parser.add_argument('-a', '--all', action='store_true', help='All')

    args = parser.parse_args()

    if not len(sys.argv) > 1:
        parser.print_help()

    if args.command == 'start':
        import os
        from pipower5.logger import Logger

        log = Logger('pipower5')
        log.info('Starting PiPower 5 service')
        last_shutdown_request = None
        last_is_input_plugged_in = None
        last_is_charging = None
        while True:
            shutdown_request = spc.read_shutdown_request()
            is_input_plugged_in = spc.read_is_input_plugged_in()
            is_charging = spc.read_is_charging()
            if shutdown_request != last_shutdown_request:
                if shutdown_request == spc.SHUTDOWN_REQUEST_NONE:
                    continue
                elif shutdown_request == spc.SHUTDOWN_REQUEST_BUTTON:
                    log.info("Shutdown request: Button")
                    os.system("sudo shutdown -h now")
                elif shutdown_request == spc.SHUTDOWN_REQUEST_LOW_BATTERY:
                    log.info("Shutdown request: Low battery")
                    os.system("sudo shutdown -h now")
                last_shutdown_request = shutdown_request
            if is_input_plugged_in != last_is_input_plugged_in:
                if is_input_plugged_in:
                    log.info("Input plugged in")
                else:
                    log.info("Input unplugged")
                last_is_input_plugged_in = is_input_plugged_in
            if is_charging != last_is_charging:
                if is_charging:
                    log.info("Charging")
                else:
                    log.info("Not charging")
                last_is_charging = is_charging
            time.sleep(1)
            
    if args.command == "stop":
        import os
        from pipower5.logger import Logger
        log = Logger('PiPower 5')
        log.info('Stopping PiPower 5 service')
        os.system('kill -9 $(pgrep -f "pipower5 start")')
        os.system('kill -9 $(pgrep -f "pipower5-service start")')

    if args.shutdown_percentage != '':
        if args.shutdown_percentage == None:
            print(f"Shutdown battery percentage: {spc.read_shutdown_percentage()}%")
        else:
            if int(args.shutdown_percentage) < 10:
                print("Failed, shutdown battery percentage minimal is 10%")
            elif int(args.shutdown_percentage) > 100:
                print("Failed, shutdown battery percentage maximal is 100%")
            else:
                spc.write_shutdown_percentage(int(args.shutdown_percentage))
                time.sleep(0.5)
                if spc.read_shutdown_percentage() == int(args.shutdown_percentage):
                    print(f"Success, shutdown battery percentage: {spc.read_shutdown_percentage()}%")
    if args.input_voltage:
        print(f"Input voltage: {spc.read_input_voltage()} mV")
    if args.output_voltage:
        print(f"Output voltage: {spc.read_output_voltage()} mV")
    if args.output_current:
        print(f"Output current: {spc.read_output_current()} mA")
    if args.battery_voltage:
        print(f"Battery voltage: {spc.read_battery_voltage()} mV")
    if args.battery_current:
        print(f"Battery current: {spc.read_battery_current()} mV")
    if args.battery_percentage:
        print(f"Battery percentage: {spc.read_battery_percentage()} %")
    if args.battery_source:
        power_source = spc.read_power_source()
        print(f"Power source: {power_source} ({'Battery' if power_source == spc.BATTERY else 'External'})")
    if args.is_input_plugged_in:
        print(f"Input plugged in: {spc.read_is_input_plugged_in()}")
    if args.is_charging:
        print(f"Charging: {spc.read_is_charging()}")
    if args.default_on:
        print(f"Default on: {spc.read_default_on()}")
    if args.shutdown_request:
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
    if args.charging_current:
        print(f"Max chargig current: {spc.i2c.read_byte_data(150)*100} mA")
    if args.board_id:
        print(f"Board id: {spc.read_board_id()}")
    if args.all:
        data_buffer = spc.read_all()
        print(f"Input voltage: {data_buffer['input_voltage']} mV")
        print(f"Output voltage: {data_buffer['output_voltage']} mV")
        print(f"Output current: {data_buffer['output_current']} mA")
        print(f"Battery voltage: {data_buffer['battery_voltage']} mV")
        print(f"Battery current: {data_buffer['battery_current']} mA")
        print(f"Battery percentage: {data_buffer['battery_percentage']} %")
        print(f"Power source: {data_buffer['power_source']} - {'Battery' if data_buffer['power_source'] == spc.BATTERY else 'External'}")
        print(f"Input plugged in: {data_buffer['is_input_plugged_in']}")
        print(f"Charging: {data_buffer['is_charging']}")
        print('')
        print(f"Internal data:")
        shutdown_request_str = 'None'
        if data_buffer['shutdown_request'] == spc.SHUTDOWN_REQUEST_NONE:
            shutdown_request_str = 'None'
        elif data_buffer['shutdown_request'] == spc.SHUTDOWN_REQUEST_LOW_BATTERY:
            shutdown_request_str = 'Low battery'
        elif data_buffer['shutdown_request'] == spc.SHUTDOWN_REQUEST_BUTTON:
            shutdown_request_str = 'Button'
        else:
            shutdown_request_str = 'Unknown'
        print(f"Shutdown request: {data_buffer['shutdown_request']} - {shutdown_request_str}")
        print(f"Max chargig current: {spc.i2c.read_byte_data(150)*100} mA")
        print(f'Board id: {spc.read_board_id()}')
        print(f"Default on: {spc.read_default_on()}")
        print(f"Shutdown percentage: {spc.read_shutdown_percentage()} %")
