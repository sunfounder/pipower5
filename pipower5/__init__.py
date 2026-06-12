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

    from .version import __version__
    from .pipower5 import PiPower5, Event, PowerSource

    from importlib.resources import files as resource_files
    import json
    import sys
    import os

    SYSTEM_DEFAULT_CONFIG = {
        "enable_history": True,
        "debug_level": "INFO",
        "data_interval": 1,
        "database_retention_days": 30,
        "temperature_unit": "C",
        "power-failure-simulation": True,
        "shutdown_percentage": 10,
        "send_email_on": [
            "battery_activated",
            "low_battery",
            "power_disconnected",
            "power_restored",
            "power_insufficient",
            "battery_critical_shutdown",
            "battery_voltage_critical_shutdown",
        ],
        "pipower5_buzzer_volume": 50,
        "pipower5_buzz_on": [
            "battery_activated",
            "low_battery",
            "power_disconnected",
            "power_restored",
            "power_insufficient",
            "battery_critical_shutdown",
            "battery_voltage_critical_shutdown",
        ],
        "pipower5_buzz_sequence": {
            "battery_activated": "A4,50:p,100:B4,50",
            "low_battery": "A4,50:p,100:A4,50",
            "power_disconnected": "D5,50:p,100:G4,50",
            "power_restored": "G4,50:p,100:D5,50",
            "power_insufficient": "B4,50:p,100:B4,50:p,100:B4,100",
            "battery_critical_shutdown": "C6,50:p,60:C6,50:p,60:C6,100",
            "battery_voltage_critical_shutdown": "C6,50:p,60:C6,50:p,60:C6,100:p,60:C6,100",
        },
        "send_email_to": "",
        "smtp_email": "",
        "smtp_password": "",
        "smtp_server": "",
        "smtp_port": 465,
        "smtp_security": "ssl",
    }

    TRUE_LIST = ['true', 'True', 'TRUE', '1', 'on', 'On', 'ON']
    FALSE_LIST = ['false', 'False', 'FALSE', '0', 'off', 'Off', 'OFF']
    AVAILABLE_EVENTS = [i.value for i in Event]

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

    args, extra = parser.parse_known_args()

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
        if len(extra) < 1:
            print("Usage: pipower5 send-email <event>")
            print("Events: battery_activated low_battery power_disconnected power_restored power_insufficient")
            print("        battery_critical_shutdown battery_voltage_critical_shutdown")
            quit()
        event = extra[0]

        # Load config: try pironman5 first, then pipower5 standalone
        pironman5_config = "/opt/pironman5/config.json"
        if os.path.exists(pironman5_config):
            with open(pironman5_config, 'r') as f:
                cfg = json.load(f).get('system', {})
        elif os.path.exists(config_path):
            cfg = current_config.get('system', {})
        else:
            cfg = SYSTEM_DEFAULT_CONFIG

        from .email_sender import EmailSender
        sender = EmailSender(cfg)
        bat_pct = pipower5.read_battery_percentage()
        bat_cur = pipower5.read_battery_current()
        is_plugged = pipower5.read_is_input_plugged_in()
        is_charging = pipower5.read_is_charging()
        data = {
            'device_name': 'PiPower5',
            'battery_percentage': bat_pct,
            'battery_voltage': f"{pipower5.read_battery_voltage() / 1000:.1f}V",
            'shutdown_percentage': pipower5.read_shutdown_percentage(),
            'battery_current_output': bat_cur,
            'estimated_time': 'N/A',
            'switch_time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'input_status': 'Plugged In' if is_plugged else 'Unplugged',
            'charging_status': 'Charging' if is_charging else ('Not Charging' if is_plugged else 'N/A (on battery)'),
        }
        result = sender.send_preset_email(event, data)
        if result is True:
            print(f"Email sent for: {event}")
        else:
            print(f"Failed to send email: {result}")
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
                new_sys_config['shutdown_percentage'] = int(args.shutdown_percentage)
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
        test_time = 60
        if args.power_failure_simulation != None:
            try:
                test_time = int(args.power_failure_simulation)
                test_time = max(10, min(test_time, 600))
            except ValueError:
                pass
        pipower5.power_failure_simulation(test_time)
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

    # ── Also sync to pironman5 config if running under pironman5 ──────
    def _sync_to_pironman5_config(patches):
        """If pironman5 config exists, apply the same patches to it."""
        pironman5_config = "/opt/pironman5/config.json"
        if not os.path.exists(pironman5_config):
            return
        try:
            with open(pironman5_config, 'r') as f:
                pm5 = json.load(f)
            if 'system' not in pm5:
                pm5['system'] = {}
            for k, v in patches.items():
                pm5['system'][k] = v
            with open(pironman5_config, 'w') as f:
                json.dump(pm5, f, indent=4)
        except Exception as e:
            print(f"  [notice] Could not sync to pironman5 config: {e}")

    if len(new_sys_config) > 0 or len(new_peripheral_config) > 0:
        new_config = {
            'system': new_sys_config,
            'peripherals': new_peripheral_config
        }

        update_config_file(new_config, config_path)
        _sync_to_pironman5_config(new_sys_config)
