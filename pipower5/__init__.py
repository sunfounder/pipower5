
def main():
    import time
    from spc.spc import SPC
    import argparse
    from .constants import PERIPHERALS
    from .version import __version__
    from .utils import is_included
    from importlib.resources import files as resource_files
    import json
    import sys
    from os import path

    TRUE_LIST = ['true', 'True', 'TRUE', '1', 'on', 'On', 'ON']
    FALSE_LIST = ['false', 'False', 'FALSE', '0', 'off', 'Off', 'OFF']

    __package_name__ = __name__.split('.')[0]
    CONFIG_PATH = str(resource_files(__package_name__).joinpath('config.json'))
    PIP_PATH = "/opt/pipower5/venv/bin/pip"

    current_config = None
    debug_level = 'INFO'
    new_sys_config = {}
    new_peripheral_config = {}

    spc = SPC()
    parser = argparse.ArgumentParser(description='PiPower 5')
    parser.add_argument("command",
                        choices=["start", "restart", "stop"],
                        nargs="?",
                        help="Command")
    parser.add_argument("-v", "--version", action="store_true", help="Show version")
    parser.add_argument("-c", "--config", action="store_true", help="Show config")
    parser.add_argument("-dl", "--debug-level", choices=['debug', 'info', 'warning', 'error', 'critical'], help="Debug level")
    parser.add_argument("--background", nargs='?', default='', help="Run in background")
    parser.add_argument("-rd", "--remove-dashboard", action="store_true", help="Remove dashboard")

    parser.add_argument('-sp', '--shutdown-percentage', nargs='?', default='', help='Set shutdown percentage, leave empty to read')
    parser.add_argument('-iv', '--input-voltage', action='store_true', help='Read input voltage')
    parser.add_argument('-ov', '--output-voltage', action='store_true', help='Read output voltage')
    parser.add_argument('-oc', '--output-current', action='store_true', help='Read output current')
    parser.add_argument('-bv', '--battery-voltage', action='store_true', help='Read battery voltage')
    parser.add_argument('-bc', '--battery-current', action='store_true', help='Read battery current')
    parser.add_argument('-bp', '--battery-percentage', action='store_true', help='Read battery percentage')
    parser.add_argument('-bs', '--battery-source', action='store_true', help='Read battery source')
    parser.add_argument('-ii', '--is-input-plugged_in', action='store_true', help='Read is input plugged in')
    parser.add_argument('-ichg', '--is-charging', action='store_true', help='Read is charging')
    parser.add_argument('-do', '--default-on', action='store_true', help='Read default on')
    parser.add_argument('-sr', '--shutdown-request', action='store_true', help='Read shutdown request')
    parser.add_argument('-cc', '--charging-current', action='store_true', help='Max charging current')
    parser.add_argument('-a', '--all', action='store_true', help='Show all status')
    parser.add_argument('-fv', '--firmware', action='store_true', help='pipower5 firmware version')

    if is_included(PERIPHERALS, "temperature_unit"):
        parser.add_argument("-u", "--temperature-unit", choices=["C", "F"], nargs='?', default='', help="Temperature unit")
    parser.add_argument('-ef', '--enable-pwm-fan', nargs='?', default='', help='Enable PWM fan, if you have one connected')

    args = parser.parse_args()

    if not len(sys.argv) > 1:
        parser.print_help()
        quit()

    if not path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'w') as f:
            json.dump({'system': {}}, f, indent=4)
    else:
        with open(CONFIG_PATH, 'r') as f:
            current_config = json.load(f)

    if args.config:
        print(json.dumps(current_config, indent=4))
        quit()

    if args.debug_level != None:
        debug_level = args.debug_level.upper()

    if args.command == "restart":
        print("This is a placeholder for pipower5 binary help, you should run pipower5 instead")
        quit()

    if args.command == "stop":
        import os
        from .pipower5 import PiPower5
        os.system('kill -9 $(pgrep -f "pipower5 start")')
        os.system('kill -9 $(pgrep -f "pipower5-service start")')
        pipower5 = PiPower5()
        pipower5.stop()
        quit()

    if args.version:
        print(__version__)
        quit()

    if args.background != '':
        print("This is a placeholder for pipower5 binary help, you should run pipower5 instead")
        quit()
    
    if args.remove_dashboard:
        import os
        print("Remove Dashboard")
        os.system(f'{PIP_PATH} uninstall pm_dashboard -y')
        while True:
            yesno = input("Do you want to uninstall influxdb? (y/n) ")
            if yesno.lower() == 'y':
                os.system(f'apt-get purge influxdb -y')
                break
            elif yesno.lower() == 'n':
                break
            else:
                print("Invalid input, please enter y or n")
        print("Dashboard removed, restart pipower5 to apply changes: sudo systemctl restart pipower5.service")
        quit()

    if is_included(PERIPHERALS, "temperature_unit"):
        if args.temperature_unit != '':
            if args.temperature_unit == None:
                print(f"Temperature unit: {current_config['system']['temperature_unit']}")
            else:
                if args.temperature_unit not in ['C', 'F']:
                    print(f"Invalid value for Temperature unit, it should be C or F")
                    quit()
                new_sys_config['temperature_unit'] = args.temperature_unit
                print(f"Set Temperature unit: {args.temperature_unit}")

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
        print(f"Default on: {'on' if spc.read_default_on() else 'off'}")
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
        print(f"Max charging current: {spc.i2c.read_byte_data(149)*100} mA")
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
        print(f"Max charging current: {spc.i2c.read_byte_data(149)*100} mA")
        print(f"Default on: {'on' if spc.read_default_on() else 'off'}")
        print(f"Shutdown percentage: {spc.read_shutdown_percentage()} %")
    if args.firmware:
        print(f"Pipower5 firmware version: {spc.read_firmware_version()}")

    if args.enable_pwm_fan != '':
        if args.enable_pwm_fan == None:
            enabled = "enabled" if current_config['peripherals']['pwm_fan'] else 'disabled'
            print(f"PWM Fan {enabled}")
        else:
            if args.enable_pwm_fan in TRUE_LIST:
                new_peripheral_config['peripherals']['pwm_fan'] = True
                print(f"Set PWM Fan enabled")
            elif args.enable_pwm_fan in FALSE_LIST:
                new_peripheral_config['peripherals']['pwm_fan'] = False
                print(f"Set PWM Fan disabled")
            else:
                print(f"Invalid value for PWM Fan, it should be true or false")
                quit()

    if len(new_sys_config) > 0:
        new_config = {
            'system': new_sys_config,
             'peripherals': current_config['peripherals']
        }
        
        from .pipower5 import PiPower5
        PiPower5.update_config_file(new_config)

    if args.command == "start":
        from .pipower5 import PiPower5
        pipower5 = PiPower5()
        pipower5.set_debug_level(debug_level)
        pipower5.start()
