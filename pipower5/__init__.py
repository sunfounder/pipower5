from .version import __version__
from .pipower5 import PiPower5


def update_config_file(config, config_path):
    import json
    from .utils import merge_dict
    current = None
    with open(config_path, 'r') as f:
        current = json.load(f)
    current = merge_dict(current, config)
    with open(config_path, 'w') as f:
        json.dump(current, f, indent=4)

def main():
    import time
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

    pipower5 = PiPower5()
    parser = argparse.ArgumentParser(prog='pipower5', description='PiPower 5')
    parser.add_argument("command",
                        choices=["start", "restart", "stop"],
                        nargs="?",
                        help="Command")
    parser.add_argument("-v", "--version", action="store_true", help="Show version")
    parser.add_argument("-c", "--config", action="store_true", help="Show config")
    parser.add_argument("-drd", "--database-retention-days", nargs='?', default='', help="Database retention days")
    parser.add_argument("-dl", "--debug-level", nargs='?', default='', choices=['debug', 'info', 'warning', 'error', 'critical'], help="Debug level")
    parser.add_argument("-rd", "--remove-dashboard", action="store_true", help="Remove dashboard")
    parser.add_argument("-cp", "--config-path", nargs='?', default='', help="Config path")

    parser.add_argument('-sp', '--shutdown-percentage', nargs='?', default='', help='Set shutdown percentage, leave empty to read')
    parser.add_argument('-iv', '--input-voltage', action='store_true', help='Read input voltage')
    parser.add_argument('-ic', '--input-current', action='store_true', help='Read input current')
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
    parser.add_argument('-fv', '--firmware', action='store_true', help='PiPower5 firmware version')
    parser.add_argument('-pfs', '--power-failure-simulation', nargs='?', default='', help='Power failure simulation')

    if is_included(PERIPHERALS, "temperature_unit"):
        parser.add_argument("-u", "--temperature-unit", choices=["C", "F"], nargs='?', default='', help="Temperature unit")

    args = parser.parse_args()

    if not len(sys.argv) > 1:
        parser.print_help()
        quit()

    config_path = CONFIG_PATH
    if args.config_path != '':
        if args.config_path == None:
            print(f"Config path: {config_path}")
        else:
            config_path = args.config_path
    if not path.exists(config_path):
        with open(config_path, 'w') as f:
            json.dump({'system': {}}, f, indent=4)
    else:
        with open(config_path, 'r') as f:
            try:
                content = f.read()
                if content == '':
                    current_config = {'system': {}}
                current_config = json.loads(content)
            except json.JSONDecodeError:
                print(f"Invalid config file: {config_path}")
                quit()

    if args.config:
        print(json.dumps(current_config, indent=4))
        quit()

    # get or set debug level
    # ----------------------------------------
    if args.debug_level != '':
        if args.debug_level == None:
            print(f"Debug level: {current_config['system']['debug_level']}")
        else:
            if args.debug_level.lower() not in ['debug', 'info', 'warning', 'error', 'critical']:
                print(f"Invalid debug level, it should be one of: debug, info, warning, error, critical")
                quit()
            else:
                debug_level = args.debug_level.upper()
                new_sys_config['debug_level'] = debug_level
                print(f"Set debug level: {debug_level}")

    # Set database retention days
    # ----------------------------------------
    if args.database_retention_days != '':
        if args.database_retention_days == None:
            print(f"Database retention days: {current_config['system']['database_retention_days']}")
        else:
            try:
                database_retention_days = int(args.database_retention_days)
                new_sys_config['database_retention_days'] = database_retention_days
                print(f"Set database retention days: {database_retention_days}")
            except ValueError:
                print(f"Invalid value for database retention days, it should be a number")
                quit()

    if args.command == "restart":
        import os
        os.system('systemctl restart pipower5.service')
        quit()

    if args.command == "stop":
        import os
        os.system('kill -9 $(pgrep -f "pipower5 start")')
        os.system('kill -9 $(pgrep -f "pipower5-service start")')
        pipower5.stop()
        quit()

    if args.version:
        print(__version__)
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
            print(f"Shutdown battery percentage: {pipower5.read_shutdown_percentage()}%")
        else:
            if int(args.shutdown_percentage) < 10:
                print("Failed, shutdown battery percentage minimal is 10%")
            elif int(args.shutdown_percentage) > 100:
                print("Failed, shutdown battery percentage maximal is 100%")
            else:
                pipower5.write_shutdown_percentage(int(args.shutdown_percentage))
                time.sleep(0.5)
                if pipower5.read_shutdown_percentage() == int(args.shutdown_percentage):
                    print(f"Success, shutdown battery percentage: {pipower5.read_shutdown_percentage()}%")
    
    if args.input_voltage:
        print(f"Input voltage: {pipower5.read_input_voltage()} mV")
    if args.input_current:
        print(f"Input current: {pipower5.read_input_current()} mA")
    if args.output_voltage:
        print(f"Output voltage: {pipower5.read_output_voltage()} mV")
    if args.output_current:
        print(f"Output current: {pipower5.read_output_current()} mA")
    if args.battery_voltage:
        print(f"Battery voltage: {pipower5.read_battery_voltage()} mV")
    if args.battery_current:
        print(f"Battery current: {pipower5.read_battery_current()} mA")
    if args.battery_percentage:
        print(f"Battery percentage: {pipower5.read_battery_percentage()} %")
    if args.battery_source:
        power_source = pipower5.read_power_source()
        print(f"Power source: {power_source} ({'Battery' if power_source == pipower5.BATTERY else 'External'})")
    if args.is_input_plugged_in:
        print(f"Input plugged in: {pipower5.read_is_input_plugged_in()}")
    if args.is_charging:
        print(f"Charging: {pipower5.read_is_charging()}")
    if args.default_on:
        print(f"Default on: {'on' if pipower5.read_default_on() else 'off'}")
    if args.shutdown_request:
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
    if args.charging_current:
        print(f"Max charging current: {pipower5.get_max_charge_current()} mA")
    if args.all:
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
    if args.firmware:
        print(f"Pipower5 firmware version: {pipower5.read_firmware_version()}")

    if len(new_sys_config) > 0 or len(new_peripheral_config) > 0:
        new_config = {
            'system': new_sys_config,
            'peripherals': new_peripheral_config
        }
        
        update_config_file(new_config, config_path)

    if args.command == "start":
        pipower5 = PiPower5(config_path=config_path)
        pipower5.set_debug_level(debug_level)
        pipower5.start()

    if args.power_failure_simulation != '':
        test_time = 60 # seconds
        if args.power_failure_simulation != None:
            test_time = int(args.power_failure_simulation)
            if test_time < 10:
                print(f"Blackout simulation time should be at least 10 seconds")
                quit()
            elif test_time > 600:
                print(f"Blackout simulation time should be at most 600 seconds(10 minutes)")
                quit()

        print(f"Blackout simulation for {test_time} seconds")
        report = pipower5.power_failure_simulation(test_time)
        if report != None:
            print(f'report:')
            print(f'  battery mah used : {report["bat_mah_used"]:.3f} mAh')
            print(f'  battery percent used : {report["bat_percent_used"]:.3f} %')
            print(f'  average battery voltage : {report["bat_voltage_avg"]:.3f} V')
            print(f'  average battery current : {report["bat_current_avg"]:.3f} A')
            print(f'  average battery power : {report["bat_power_avg"]:.3f} W')
            print(f'  average output voltage : {report["output_voltage_avg"]:.3f} V')
            print(f'  average output current : {report["output_current_avg"]:.3f} A')
            print(f'  average output power : {report["output_power_avg"]:.3f} W')
            print(f'  ---')
            print(f'  max battery voltage : {report["bat_voltage_max"]:.3f} V')
            print(f'  max battery current : {report["bat_current_max"]:.3f}A')
            print(f'  max battery power : {report["bat_power_max"]:.2f} W')
            print(f'  max output voltage : {report["output_voltage_max"]:.3f} V')
            print(f'  max output current : {report["output_current_max"]:.3f} A')
            print(f'  max output power : {report["output_power_max"]:.3f} W')
            print(f'  ---')
            print(f'  battery precentage : {report["battery_percentage"]} %')
            print(f'  shutdown percentage : {report["shutdown_percentage"]} %')
            print(f'  available time: {report["available_time_str"]}')
            print(f'  available time: {report["available_time"]} s')
            print(f'  available_bat_capacity: {int(report["available_bat_capacity"])} mAh')


        