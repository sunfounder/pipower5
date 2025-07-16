from .version import __version__

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
    from .pipower5 import PiPower5
    import argparse
    from .constants import PERIPHERALS
    from .version import __version__
    from .utils import is_included
    from importlib.resources import files as resource_files
    from pipower5.email_sender import EmailModes
    import json
    import sys
    from os import path

    TRUE_LIST = ['true', 'True', 'TRUE', '1', 'on', 'On', 'ON']
    FALSE_LIST = ['false', 'False', 'FALSE', '0', 'off', 'Off', 'OFF']
    AVAILABLE_EMAIL_MODES = [i.value for i in EmailModes]

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
    parser.add_argument("-dl", "--debug-level", choices=['debug', 'info', 'warning', 'error', 'critical'], help="Debug level")
    parser.add_argument("--background", nargs='?', default='', help="Run in background")
    parser.add_argument("-rd", "--remove-dashboard", action="store_true", help="Remove dashboard")
    parser.add_argument("-cp", "--config-path", nargs='?', default='', help="Config path")

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
    parser.add_argument('-pb', '--power-btn', action='store_true', help='Read power button')
    parser.add_argument('-cc', '--charging-current', action='store_true', help='Max charging current')
    parser.add_argument('-a', '--all', action='store_true', help='Show all status')
    parser.add_argument('-fv', '--firmware', action='store_true', help='PiPower5 firmware version')
    parser.add_argument('-pfs', '--power-failure-simulation', nargs='?', default='', help='Power failure simulation')
    parser.add_argument("-seo", '--send-email-on', nargs='?', default=[], help=f"Send email on: {AVAILABLE_EMAIL_MODES}")
    parser.add_argument("-set", '--send-email-to', nargs='?', default='', help="Email address to send email to")
    parser.add_argument("-ss", '--smtp-server', nargs='?', default='', help="SMTP server")
    parser.add_argument("-sp", '--smtp-port', nargs='?', default='', help="SMTP port")
    parser.add_argument("-se", '--smtp-email', nargs='?', default='', help="SMTP email")
    parser.add_argument("-spw", '--smtp-password', nargs='?', default='', help="SMTP password")
    parser.add_argument("-ssu", '--smtp-use-tls', nargs='?', default='', help="SMTP use tls")

    if is_included(PERIPHERALS, "temperature_unit"):
        parser.add_argument("-u", "--temperature-unit", choices=["C", "F"], nargs='?', default='', help="Temperature unit")
    parser.add_argument('-ef', '--enable-pwm-fan', nargs='?', default='', help='Enable PWM fan, if you have one connected')

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

    if args.debug_level != None:
        debug_level = args.debug_level.upper()

    if args.command == "restart":
        print("This is a placeholder for pipower5 binary help, you should run pipower5 instead")
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
    if args.output_voltage:
        print(f"Output voltage: {pipower5.read_output_voltage()} mV")
    if args.output_current:
        print(f"Output current: {pipower5.read_output_current()} mA")
    if args.battery_voltage:
        print(f"Battery voltage: {pipower5.read_battery_voltage()} mV")
    if args.battery_1_voltage:
        print(f"Battery 1 voltage: {pipower5.read_battery_1_voltage()} mV")
    if args.battery_2_voltage:
        print(f"Battery 2 voltage: {pipower5.read_battery_2_voltage()} mV")
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
        print(f"Shutdown request: {int(shutdown_request)} - {shutdown_request.name}")
    if args.power_btn:
        button_state = pipower5.read_power_btn()
        print(f"Power button: {int(button_state)} - {button_state.name}")
    if args.charging_current:
        print(f"Max charging current: {pipower5.get_max_charge_current()} mA")
    if args.all:
        data_buffer = pipower5.read_all()
        #
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
    power button: {int(button_state)} - {button_state.name}
    max charging current: {PiPower5.get_max_charge_current(pipower5)} mA
    default on: {'on' if pipower5.read_default_on() else 'off'}
    shutdown percentage: {pipower5.read_shutdown_percentage()} %
''')
    if args.firmware:
        print(f"Pipower5 firmware version: {pipower5.read_firmware_version()}")

    if args.enable_pwm_fan != '':
        if args.enable_pwm_fan == None:
            if 'peripherals' not in current_config:
                enabled = "disabled"
            else:
                enabled = "enabled" if current_config['peripherals']['pwm_fan'] else 'disabled'
            print(f"PWM Fan {enabled}")
        else:
            if args.enable_pwm_fan in TRUE_LIST:
                new_peripheral_config['pwm_fan'] = True
                print(f"Set PWM Fan enabled")
            elif args.enable_pwm_fan in FALSE_LIST:
                new_peripheral_config['pwm_fan'] = False
                print(f"Set PWM Fan disabled")
            else:
                print(f"Invalid value for PWM Fan, it should be true or false")
                quit()

    if len(new_sys_config) > 0 or len(new_peripheral_config) > 0:
        new_config = {
            'system': new_sys_config,
            'peripherals': new_peripheral_config
        }
        
        update_config_file(new_config, config_path)

    if args.command == "start":
        pipower5 = PiPower5Manager(config_path=config_path)
        pipower5.set_debug_level(debug_level)
        pipower5.start()

    # send email on
    if args.send_email_on != []:
        if args.send_email_on == None:
            send_email_on = [f' - {mode}' for mode in current_config['system']['send_email_on']]
            send_email_on = '\n'.join(send_email_on)
            print("Send email on:")
            print(send_email_on)
        else:
            send_email_on = [p.replace(',', '') for p in args.send_email_on]
            for mode in send_email_on:
                if mode not in AVAILABLE_EMAIL_MODES:
                    print(f"Invalid value for Send email on: '{mode}', it should be {', '.join(AVAILABLE_EMAIL_MODES)}")
                    quit()
            new_sys_config['send_email_on'] = send_email_on
            print(f"Set Send email on: {send_email_on}")
    # send email to
    if args.send_email_to != '':
        if args.send_email_to == None:
            print(f"Send email to: {current_config['system']['send_email_to']}")
        else:
            new_sys_config['send_email_to'] = args.send_email_to
            print(f"Set Send email to: {args.send_email_to}")
    # SMTP server
    if args.smtp_server != '':
        if args.smtp_server == None:
            print(f"SMTP server: {current_config['system']['smtp_server']}")
        else:
            new_sys_config['smtp_server'] = args.smtp_server
            print(f"Set SMTP server: {args.smtp_server}")
    # SMTP port
    if args.smtp_port != '':
        if args.smtp_port == None:
            print(f"SMTP port: {current_config['system']['smtp_port']}")
        else:
            new_sys_config['smtp_port'] = args.smtp_port
            print(f"Set SMTP port: {args.smtp_port}")
    # SMTP user
    if args.smtp_email != '':
        if args.smtp_email == None:
            print(f"SMTP user: {current_config['system']['smtp_email']}")
        else:
            new_sys_config['smtp_email'] = args.smtp_email
            print(f"Set SMTP user: {args.smtp_email}")
    # SMTP password
    if args.smtp_password != '':
        if args.smtp_password == None:
            print(f"SMTP password: {current_config['system']['smtp_password']}")
        else:
            new_sys_config['smtp_password'] = args.smtp_password
            print(f"Set SMTP password: {args.smtp_password}")
    # SMTP use TLS
    if args.smtp_use_tls != '':
        if args.smtp_use_tls == None:
            print(f"SMTP use TLS: {current_config['system']['smtp_use_tls']}")
        else:
            if args.smtp_use_tls in TRUE_LIST:
                args.smtp_use_tls = True
            elif args.smtp_use_tls in FALSE_LIST:
                args.smtp_use_tls = False
            else:
                print(f"Invalid value for SMTP use TLS, it should be in {', '.join(TRUE_LIST + FALSE_LIST)}")
                quit()
            print(f"Set SMTP use TLS: {args.smtp_use_tls}")

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
        print(f'report:')
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


        