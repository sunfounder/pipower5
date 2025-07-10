import time
import os
import json
import signal
from importlib.resources import files as resource_files

from spc.spc import SPC

from .logger import create_get_child_logger
from .utils import merge_dict, log_error
from .version import __version__ as pipower5_version
from .constants import NAME, ID, PERIPHERALS, SYSTEM_DEFAULT_CONFIG, CUSTOM_PERIPHERALS

__package_name__ = __name__.split('.')[0]
CONFIG_PATH = str(resource_files(__package_name__).joinpath('config.json'))

get_child_logger = create_get_child_logger('pipower5')
DEFAULT_DEBUG_LEVEL = 'INFO' # 'DEBUG' | 'INFO' | 'WARNING' | 'ERROR' | 'CRITICAL'


class PiPower5(SPC):

    # register address
    REG_PWR_BTN_STATE= 154
    REG_CHARGE_MAX_CURRENT = 155

    REG_WRITE_POWER_BTN_STATE = 12

    BAT_MAX_CAPACITY = 2000 # mAh   

    ADV_CMD_START = 0xAC
    ADV_CMD_END = 0xAE
    ADV_CMD_OK = 0xE0
    ADV_CMD_ERR = 0xEF

    ADV_CMD_RST = 0x00
    ADV_CMD_VBUS_EN = 0x01
    ADV_CMD_BAT_EN = 0x02
    ADV_CMD_OUPUT_EN = 0x03
    ADV_CMD_ENTER_IAP = 0x04

    def __init__(self, config_path=CONFIG_PATH):
        # --- init SPC ---
        super().__init__()

        # --- init logger ---
        self.log = get_child_logger('main')

        # --- init config ---
        self.config = {
            'system': SYSTEM_DEFAULT_CONFIG,
            "peripherals": CUSTOM_PERIPHERALS,
        }
        self.config['system']['debug_level'] = DEFAULT_DEBUG_LEVEL

        # merge config
        self.config_path = config_path
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                self.config = merge_dict(self.config, config)
        try:
            os.chmod(self.config_path, 0o777)
        except:
            pass
        # read shutdown_percentage
        self.config['system']['shutdown_percentage'] = self.read_shutdown_percentage()
        #
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)

        # Set debug level
        # -----------------------------------------
        self._log_level = self.config['system']['debug_level'].upper()
        if self._log_level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            self.log.warning(f"Invalid debug level '{self._log_level}', using default '{DEFAULT_DEBUG_LEVEL}'")
            self._log_level = DEFAULT_DEBUG_LEVEL

        # --- device_info ---
        self.device_info = {
            'name': NAME,
            'id': ID,
            'peripherals': PERIPHERALS,
            'version': pipower5_version,
        }

        #
        self.pm_dashboard = None
        self.shutdown_service = None

    def init_services(self):
        # --- import ---
        has_pm_dashboard = False
        try:
            from pm_dashboard.pm_dashboard import PMDashboard
            from pm_dashboard.version import __version__ as pm_dashboard_version
            has_pm_dashboard = True
        except ImportError:
            has_pm_dashboard = False

        from .shutdown_service import ShutdownService

        # --- print ---
        # LOG HEADER
        self.log.info(f"")
        self.log.info(f"{'#'*60}")
        self.log.debug(f"Config path: {CONFIG_PATH}")
        #
        self.log.info(f'PiPower5 {pipower5_version} started')
        #
        _config_json = json.dumps(self.config, indent=4)
        self.log.info(f"Config:")
        for line in _config_json.splitlines():
            self.log.info(line)
        #
        _device_info_json = json.dumps(self.device_info, indent=4)
        self.log.debug(f"Device info:")
        for line in _device_info_json.splitlines():
            self.log.debug(line)
        #
        if has_pm_dashboard:
            self.log.info(f"PM_Dashboard version: {pm_dashboard_version}")

        # --- init pm_dashboard ---
        if not has_pm_dashboard:
            self.pm_dashboard = None
            self.log.warning('PM Dashboard not found skipping')
        else:
            self.pm_dashboard = PMDashboard(device_info=self.device_info,
                                            database=ID,
                                            spc_enabled=True if 'spc' in PERIPHERALS else False,
                                            config=self.config,
                                            get_logger=get_child_logger)
            self.pm_dashboard.set_on_config_changed(self.update_config)
        # --- init shutdown_service ---
        self.shutdown_service = ShutdownService(get_logger=get_child_logger)
        # --- set debug level ---
        self.set_debug_level(self._log_level)

    @log_error
    def update_extra_peripherals(self):
        if 'peripherals' not in self.config:
            return
        for peripheral in self.config['peripherals']:
            if peripheral == 'pwm_fan':
                if self.config['peripherals'][peripheral]:
                    PERIPHERALS.append("pwm_fan_speed")

    @log_error
    def set_debug_level(self, level):
        self._log_level = level

        self.log.setLevel(level)
        if self.pm_dashboard:
            self.pm_dashboard.set_debug_level(level)
        if self.shutdown_service:
            self.shutdown_service.set_debug_level(level)

    @log_error
    def update_config(self, config):
        self.shutdown_service.update_config(config['system'])
        merge_dict(self.config, config)
        try:
            os.chmod(self.config_path, 0o777)
        except:
            pass
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)


    @log_error
    def start(self):
        #
        self.init_services()
        #
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGABRT, self.signal_handler)
        #
        self.shutdown_service.start()
        #
        if self.pm_dashboard:
            self.pm_dashboard.start()
            self.log.info('PmDashboard started')
        while True:
            # time.sleep(1)
            signal.pause()

    @log_error
    def stop(self):
        self.log.debug('Stopping PiPower5...')
        if self.shutdown_service:
            self.shutdown_service.stop()
            self.log.debug('Stop Shutdown service.')
        if self.pm_dashboard:
            self.log.debug('Stop PM Dashboard.')
            self.pm_dashboard.stop()
        # Check if there's any thread still alive
        import threading
        for t in threading.enumerate():
            if t is not threading.main_thread():
                self.log.warning(f"Thread {t.name} is still alive")
        quit()

    @log_error
    def signal_handler(self, signum, frame):
        self.log.info(f'Received signal "{signal.strsignal(signum)}", cleaning up...')
        self.stop()

    def get_max_charge_current(self):
        return self.i2c.read_byte_data(self.REG_CHARGE_MAX_CURRENT)*100

    def disable_vbus(self):
        time_out = 5 # seconds
        st = time.time()
        while time.time() - st < time_out:
            self.i2c.write_block_data(self.ADV_CMD_START, [self.ADV_CMD_VBUS_EN, 0, self.ADV_CMD_END])
            if self.read_input_voltage() == 0:
                return True
            time.sleep(0.5)
        else:
            print(f'Failed to disable VBUS (timeout {time_out} s)')
            return False

    def enable_vbus(self):
        time_out = 5 # seconds
        st = time.time()
        while time.time() - st < time_out:
            self.i2c.write_block_data(self.ADV_CMD_START, [self.ADV_CMD_VBUS_EN, 1, self.ADV_CMD_END])
            if self.read_input_voltage() > 0:
               return True
        else:
            print(f'Failed to enable VBUS (timeout {time_out} s)')
            return False

    def power_failure_simulation(self, test_time):
        battery_percentage =  self.read_battery_percentage()
        is_input_plugged_in = self.read_is_input_plugged_in()

        print(f'battery: {battery_percentage}%, input: {"plugged in" if is_input_plugged_in else "unplugged"}')

        if battery_percentage < 80 or not is_input_plugged_in:
            warn_emoji = '\U000026A0'
            print(f'{warn_emoji} Battery must be greater than 80%')
            print(f'{warn_emoji} Input must be plugged in')
            return None

        if test_time < 10:
            test_time = 10
        if test_time > 600:
            test_time = 600

        count = 0
        interval = 0.5

        bat_voltage = 0
        bat_current = 0
        bat_power = 0
        bat_voltage_sum = 0
        bat_current_sum = 0
        bat_power_sum = 0
        bat_voltage_avg = 0
        bat_current_avg = 0
        bat_power_avg = 0
        bat_voltage_max = 0
        bat_current_max = 0
        bat_power_max = 0

        output_voltage = 0
        output_current = 0
        output_power = 0
        output_voltage_sum = 0
        output_current_sum = 0
        output_power_sum = 0
        output_voltage_avg = 0
        output_current_avg = 0
        output_power_avg = 0
        output_voltage_max = 0
        output_current_max = 0
        output_power_max = 0

        # -----------------
        print('disable VBUS ... ', end='')
        self.disable_vbus()
        print('OK')

        # -----------------
        st = time.time()
        while time.time() - st < test_time:
            #
            count += 1
            print(f'\r{count*interval:.1f}/{test_time}s', end='')
            data_buffer = self.read_all()
            #
            bat_voltage = data_buffer['battery_voltage']
            bat_current = -data_buffer['battery_current'] # negative value
            bat_power = bat_voltage * bat_current / 1000 / 1000 # W

            bat_voltage_sum += bat_voltage
            bat_current_sum += bat_current
            bat_power_sum += bat_power

            if bat_voltage > bat_voltage_max:
                bat_voltage_max = bat_voltage
            if bat_current > bat_current_max:
                bat_current_max = bat_current
            if bat_power > bat_power_max:
                bat_power_max = bat_power
            #
            output_voltage = data_buffer['output_voltage']
            output_current = data_buffer['output_current']
            output_power = output_voltage * output_current / 1000 / 1000 # W

            output_voltage_sum += output_voltage
            output_current_sum += output_current
            output_power_sum += output_power

            if output_voltage > output_voltage_max:
                output_voltage_max = output_voltage
            if output_current > output_current_max:
                output_current_max = output_current
            if output_power > output_power_max:
                output_power_max = output_power

            time.sleep(interval)

        # -----------------
        print() # newline
        print('enable VBUS ... ', end='')
        self.enable_vbus()
        print('OK')
        # -----------------
        bat_voltage_avg = round(bat_voltage_sum / count / 1000, 3)
        bat_current_avg = round(bat_current_sum / count / 1000, 3)
        bat_power_avg = round(bat_power_sum / count, 3)

        output_voltage_avg = round(output_voltage_sum / count / 1000, 3)
        output_current_avg = round(output_current_sum / count / 1000, 3)
        output_power_avg = round(output_power_sum / count, 3)

        bat_voltage_max = round(bat_voltage_max / 1000, 3)
        bat_current_max = round(bat_current_max / 1000, 3)
        bat_power_max = round(bat_power_max, 3)

        output_voltage_max = round(output_voltage_max / 1000, 3)
        output_current_max = round(output_current_max / 1000, 3)
        output_power_max = round(output_power_max, 3)
        #
        shutdown_percentage = self.read_shutdown_percentage()
        #
        data_buffer = self.read_all()
        bat_prec = data_buffer['battery_percentage']
        #
        available_prec = bat_prec - shutdown_percentage
        if available_prec < 0:
            available_prec = 0
        available_capacity = available_prec * self.BAT_MAX_CAPACITY / 100
        available_capacity = available_capacity * 0.9 # 20% reserve
        #
        available_time = int(available_capacity / 1000 / bat_current_avg * 3600) # sec
        available_time_hour = int(available_time / 3600)
        available_time_min = int((available_time % 3600) / 60)
        available_time_sec = int((available_time % 3600) % 60)
        available_time_str = f"{available_time_hour} hour " if available_time_hour > 0 else ''
        # available_time_str += f'{available_time_min} min {available_time_sec} sec'
        available_time_str += f'{available_time_min} min'

        #
        result =  {
            'bat_voltage_avg': bat_voltage_avg,
            'bat_current_avg': bat_current_avg,
            'bat_power_avg': bat_power_avg,
            'bat_voltage_max': bat_voltage_max,
            'bat_current_max': bat_current_max,
            'bat_power_max': bat_power_max,
            'output_voltage_avg': output_voltage_avg,
            'output_current_avg': output_current_avg,
            'output_power_avg': output_power_avg,
            'output_voltage_max': output_voltage_max,
            'output_current_max': output_current_max,
            'output_power_max': output_power_max,
            'available_bat_capacity': available_capacity,
            'battery_percentage': bat_prec,
            'shutdown_percentage': shutdown_percentage,
            'available_time': available_time,
            'available_time_str': available_time_str,
        }
        #
        with open('/opt/pipower5/blackout_simulation.json', 'w') as f:
            json.dump(result, f, indent=4)
        #
        return result
    
    def read_power_btn(self):
        key_map = {
            0: 'released',
            1: 'single_click',
            2: 'double_click',
            3: 'long_press_2s',
            4: 'long_press_2s_released',
            5: 'long_press_5s',
            6: 'long_press_5s_released',
        }
        val = self.i2c.read_byte_data(self.REG_PWR_BTN_STATE)
        self.i2c.write_byte_data(self.REG_WRITE_POWER_BTN_STATE, 0) # reset state

        if val in key_map:
            return key_map[val]
        else:
            return val
