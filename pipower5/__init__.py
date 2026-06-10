from .version import __version__

def update_config_file(config, config_path):
    import json
    current = None
    with open(config_path, 'r') as f:
        current = json.load(f)
    for key in config:
        if key in current:
            current[key].update(config[key])
        else:
            current[key] = config[key]
    with open(config_path, 'w') as f:
        json.dump(current, f, indent=4)

def main():
    import time
    import argparse

    from .constants import SYSTEM_DEFAULT_CONFIG
    from .version import __version__
    from .utils import get_varient_id_and_version
    from .pipower5 import PiPower5, Event, PowerSource

    from importlib.resources import files as resource_files
    import json
    import sys
    import os

    TRUE_LIST = ['true', 'True', 'TRUE', '1', 'on', 'On', 'ON']
    FALSE_LIST = ['false', 'False', 'FALSE', '0', 'off', 'Off', 'OFF']
    AVAILABLE_EVENTS = [i.value for i in Event]
    _, BOARD_VERSION = get_varient_id_and_version()

    __package_name__ = __name__.split('.')[0]
    _TEMPLATE_CONFIG = str(resource_files(__package_name__).joinpath('config.json'))
    _USER_CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "pipower5")
    _USER_CONFIG = os.path.join(_USER_CONFIG_DIR, "config.json")
    PIP_PATH = "/opt/pipower5/venv/bin/pip"

    current_config = None
    debug_level = 'INFO'
    new_sys_config = {}
    new_peripheral_config = {}

    pipower5 = PiPower5()
    parser = argparse.ArgumentParser(prog='pipower5', description='PiPower 5')
    parser.add_argument("command",
                        choices=["doctor", "uninstall", "info", "status", "send-email"],
                        nargs="?",
                        help="Command")
    parser.add_argument("--fix", action="store_true", help="Attempt auto-repair (with doctor)")
    parser.add_argument("-v", "--version", action="store_true", help="Show Python package version")
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
    if BOARD_VERSION == '50':
        parser.add_argument('-b1v', '--battery-1-voltage', action='store_true', help='Read battery 1 voltage')
        parser.add_argument('-b2v', '--battery-2-voltage', action='store_true', help='Read battery 2 voltage')
    parser.add_argument('-bc', '--battery-current', action='store_true', help='Read battery current')
    parser.add_argument('-bp', '--battery-percentage', action='store_true', help='Read battery percentage')
    parser.add_argument('-bs', '--battery-source', action='store_true', help='Read battery source')
    parser.add_argument('-ii', '--is-input-plugged_in', action='store_true', help='Read is input plugged in')
    parser.add_argument('-ichg', '--is-charging', action='store_true', help='Read is charging')
    parser.add_argument('-do', '--default-on', action='store_true', help='Read default on')
    parser.add_argument('-pb', '--power-btn', action='store_true', help='Read power button')
    parser.add_argument('-cc', '--charging-current', action='store_true', help='Max charging current')
    parser.add_argument('-a', '--all', action='store_true', help='Show all status')
    parser.add_argument('-fv', '--firmware', action='store_true', help='PiPower5 MCU firmware version')
    parser.add_argument('-dv', '--driver-version', action='store_true', help='PiPower5 kernel driver version')
    parser.add_argument('-pfs', '--power-failure-simulation', nargs='?', default='', help='Power failure simulation (seconds)')
    parser.add_argument("-seo", '--send-email-on', nargs='?', default='', help=f"Send email on events (comma-separated)")
    parser.add_argument("-set", '--send-email-to', nargs='?', default='', help="Email recipient address")
    parser.add_argument("-ss", '--smtp-server', nargs='?', default='', help="SMTP server")
    parser.add_argument("-smp", '--smtp-port', nargs='?', default='', help="SMTP port")
    parser.add_argument("-se", '--smtp-email', nargs='?', default='', help="SMTP email")
    parser.add_argument("-spw", '--smtp-password', nargs='?', default='', help="SMTP password")
    parser.add_argument("-ssc", '--smtp-security', nargs='?', default='', help="SMTP security: none, ssl, tls")
    parser.add_argument("-bzo", '--buzz-on', nargs='?', default='', help='Buzzer event bitmask (e.g. 0x7F), leave empty to read')
    parser.add_argument("-bzv", '--buzzer-volume', nargs='?', default='', help='Buzzer volume (0-10), leave empty to read')
    parser.add_argument("-bzt", '--buzzer-test', nargs='?', default='', help='Test buzzer: event name or frequency')

    parser.add_argument("-u", "--temperature-unit", choices=["C", "F"], nargs='?', default='', help="Temperature unit")

    args = parser.parse_args()

    if not len(sys.argv) > 1:
        parser.print_help()
        quit()

    current_config = {
        "system": SYSTEM_DEFAULT_CONFIG,
    }

    # Determine config path: --config-path override > ~/.config/pipower5/config.json
    config_path = _USER_CONFIG
    if args.config_path != '':
        if args.config_path == None:
            print(f"Config path: {config_path}")
        else:
            config_path = args.config_path

    # Ensure config directory exists
    config_dir = os.path.dirname(config_path)
    if config_dir and not os.path.isdir(config_dir):
        os.makedirs(config_dir, exist_ok=True)

    # Read config: user config > template (migrate from old location if needed)
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            current_config = json.load(f)
    elif os.path.exists(_TEMPLATE_CONFIG) and _TEMPLATE_CONFIG != config_path:
        # Copy from package template
        import shutil
        shutil.copy(_TEMPLATE_CONFIG, config_path)
        with open(config_path, 'r') as f:
            current_config = json.load(f)
    else:
        current_config = {'system': SYSTEM_DEFAULT_CONFIG,}
        with open(config_path, 'w') as f:
            json.dump(current_config, f, indent=4)
        

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

    if args.command == "doctor":
        from .device import doctor
        doctor(fix=args.fix)
        quit()

    if args.command in ("info", "status"):
        args.all = True  # alias for -a

    if args.command == "send-email":
        from .device import DEVICE_PATH
        event = args.event
        if not event:
            print("Usage: pipower5 send-email <event>")
            print("Events: low_battery power_disconnected power_restored battery_activated power_insufficient")
            quit()
        import subprocess, sys
        script = "/usr/local/bin/pipower5-send-mail"
        try:
            subprocess.run([sys.executable, script, event], check=True)
            print(f"Email sent for: {event}")
        except FileNotFoundError:
            print(f"Script not installed: {script}")
            print("Install with: sudo cp rules/pipower5-send-mail /usr/local/bin/")
        except Exception as e:
            print(f"Failed: {e}")
        quit()

    if args.command == "uninstall":
        from .device import uninstall
        uninstall()
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
    if BOARD_VERSION == '50':
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
        print(f"Power source: {power_source} ({'Battery' if power_source == PowerSource.BATTERY else 'External'})")
    if args.is_input_plugged_in:
        print(f"Input plugged in: {pipower5.read_is_input_plugged_in()}")
    if args.is_charging:
        print(f"Charging: {pipower5.read_is_charging()}")
    if args.default_on:
        print(f"Default on: {'on' if pipower5.read_default_on() else 'off'}")
    if args.power_btn:
        button_state = pipower5.read_power_btn()
        print(f"Power button: {int(button_state)} - {button_state.name}")
    if args.charging_current:
        print(f"Max charging current: {pipower5.get_max_charge_current()} mA")
    if args.all:
        data_buffer = pipower5.read_all()
        #
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
    source: {data_buffer['power_source']} - {'Battery' if data_buffer['power_source'] == PowerSource.BATTERY else 'External'}
    charging: {data_buffer['is_charging']}

Internal:
    power button: {int(button_state)} - {button_state.name}
    max charging current: {pipower5.get_max_charge_current()} mA
    default on: {'on' if pipower5.read_default_on() else 'off'}
    shutdown percentage: {pipower5.read_shutdown_percentage()} %

Versions:
    python:   {__version__}
    driver:   {pipower5.read_driver_version()}
    firmware: {pipower5.read_firmware_version()}
''')
    if args.firmware:
        print(f"PiPower5 MCU firmware version: {pipower5.read_firmware_version()}")
    if args.driver_version:
        print(f"PiPower5 kernel driver version: {pipower5.read_driver_version()}")

    # power failure simulation
    if args.power_failure_simulation != '':
        print("Power failure simulation requires kernel driver ADV_CMD support (not yet implemented).")
        print("Use 'pipower5 --all' to monitor battery drain manually.")
    # send email config
    if args.send_email_on != '':
        if args.send_email_on == None:
            print(f"Send email on: {current_config['system']['send_email_on']}")
        else:
            import json as _json
            email_cfg = _json.loads(_json.dumps(current_config['system']))
            email_cfg['send_email_on'] = args.send_email_on.split(',')
            new_sys_config['send_email_on'] = email_cfg['send_email_on']
            print(f"Set Send email on: {new_sys_config['send_email_on']}")
    if args.send_email_to != '':
        if args.send_email_to == None:
            print(f"Send email to: {current_config['system']['send_email_to']}")
        else:
            new_sys_config['send_email_to'] = args.send_email_to
            print(f"Set Send email to: {args.send_email_to}")
    if args.smtp_server != '':
        if args.smtp_server == None:
            print(f"SMTP server: {current_config['system']['smtp_server']}")
        else:
            new_sys_config['smtp_server'] = args.smtp_server
    if args.smtp_port != '':
        if args.smtp_port == None:
            print(f"SMTP port: {current_config['system']['smtp_port']}")
        else:
            new_sys_config['smtp_port'] = args.smtp_port
    if args.smtp_email != '':
        if args.smtp_email == None:
            print(f"SMTP email: {current_config['system']['smtp_email']}")
        else:
            new_sys_config['smtp_email'] = args.smtp_email
    if args.smtp_password != '':
        if args.smtp_password == None:
            print("SMTP password: ***")
        else:
            new_sys_config['smtp_password'] = args.smtp_password
    if args.smtp_security != '':
        if args.smtp_security == None:
            print(f"SMTP security: {current_config['system']['smtp_security']}")
        else:
            sec = args.smtp_security.lower()
            if sec not in ['none', 'tls', 'ssl']:
                print("Invalid SMTP security, use: none, tls, ssl")
                quit()
            new_sys_config['smtp_security'] = sec
    # buzzer
    if args.buzz_on != '':
        if args.buzz_on == None:
            try:
                with open(f"{DEVICE_PATH}/buzz_on", "r") as f:
                    print(f"Buzz on: {f.read().strip()}")
            except Exception:
                print("Buzz on: (cannot read sysfs)")
        else:
            pipower5._write_sysfs("buzz_on", args.buzz_on)
            print(f"Set buzz_on: {args.buzz_on} (persist via /etc/modprobe.d/pipower5.conf)")
    if args.buzzer_volume != '':
        if args.buzzer_volume == None:
            print(f"Buzzer volume: {pipower5.read_buzzer_volume()}")
        else:
            vol = int(args.buzzer_volume)
            pipower5.set_buzzer_volume(vol)
            print(f"Set buzzer volume: {vol}")
    if args.buzzer_test != '':
        if args.buzzer_test == None:
            print("Usage: --buzzer-test <frequency> (e.g. 440) or --buzzer-test <event_name>")
        else:
            from .device import DEVICE_PATH as _DP
            val = args.buzzer_test
            try:
                freq = int(val)
                pipower5._write_sysfs("buzzer_play", str(freq))
                print(f"Playing {freq}Hz for 5s...")
            except ValueError:
                print(f"Event '{val}' - buzzer auto-triggers on kernel events. Use frequency value to test manually.")

    if len(new_sys_config) > 0 or len(new_peripheral_config) > 0:
        new_config = {
            'system': new_sys_config,
            'peripherals': new_peripheral_config
        }
        
        update_config_file(new_config, config_path)
