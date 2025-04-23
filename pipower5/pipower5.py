import json
import time
import os
from importlib.resources import files as resource_files
import signal

from pm_auto.pm_auto import PMAuto
from pm_auto import __version__ as pm_auto_version
from .logger import create_get_child_logger
from .utils import merge_dict, log_error
from .version import __version__ as pipower5_version
from .constants import NAME, ID, PERIPHERALS, SYSTEM_DEFAULT_CONFIG, CUSTOM_PERIPHERALS

from .shutdown_service import ShutdownService

get_child_logger = create_get_child_logger('pipower5')
log = get_child_logger('main')
__package_name__ = __name__.split('.')[0]
CONFIG_PATH = str(resource_files(__package_name__).joinpath('config.json'))

PMDashboard = None
try:
    from pm_dashboard.pm_dashboard import PMDashboard
    from pm_dashboard.version import __version__ as pm_dashboard_version
except ImportError:
    pass

class PiPower5:

    REG_CHARGE_MAX_CURRENT = 155 # register address

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
        self.log = get_child_logger('main')
        self.config = {
            'system': SYSTEM_DEFAULT_CONFIG,
            "peripherals": CUSTOM_PERIPHERALS,
        }
        self.config_path = config_path
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                self.config = merge_dict(self.config, config)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)

        self.update_extra_peripherals()

        device_info = {
            'name': NAME,
            'id': ID,
            'peripherals': PERIPHERALS,
            'version': pipower5_version,
        }

        # 
        self.config['system']['shutdown_percentage'] = 10
        #

        self.log.debug(f"PiPower 5 version: {pipower5_version}")
        self.log.debug(f"Config: {self.config}")
        self.log.debug(f"Device info: {device_info}")
        self.log.debug(f"PM_Auto version: {pm_auto_version}")
        if PMDashboard is not None:
            self.log.debug(f"PM_Dashboard version: {pm_dashboard_version}")
        self.pm_auto = PMAuto(self.config['system'],
                              peripherals=PERIPHERALS,
                              get_logger=get_child_logger)
        if PMDashboard is None:
            self.pm_dashboard = None
            self.log.warning('PM Dashboard not found skipping')
        else:
            self.pm_dashboard = PMDashboard(device_info=device_info,
                                            database=ID,
                                            spc_enabled=True if 'spc' in PERIPHERALS else False,
                                            config=self.config,
                                            get_logger=get_child_logger)
            self.pm_auto.set_on_state_changed(self.pm_dashboard.update_status)
            self.pm_dashboard.set_on_config_changed(self.update_config)
        self.shutdown_service = ShutdownService(get_logger=get_child_logger)

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
        self.log.setLevel(level)
        self.pm_auto.set_debug_level(level)
        if self.pm_dashboard:
            self.pm_dashboard.set_debug_level(level)

    @log_error
    def update_config(self, config):
        self.pm_auto.update_config(config['system'])
        self.shutdown_service.update_config(config['system'])
        merge_dict(self.config, config)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)

    @log_error
    def start(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGABRT, self.signal_handler)
        self.shutdown_service.start()
        if self.pm_dashboard:
            self.pm_dashboard.start()
            self.log.info('PmDashboard started')
        while True:
            time.sleep(1)

    @log_error
    def stop(self):
        self.log.debug('Stopping PiPower5...')
        self.log.debug('Stop Shutdown service.')
        self.shutdown_service.stop()
        self.log.debug('Stop PM Auto.')
        self.pm_auto.stop()
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

    @staticmethod
    def get_max_charge_current(spc):
        return spc.i2c.read_byte_data(PiPower5.REG_CHARGE_MAX_CURRENT)*100
    
    @staticmethod
    def disable_vbus(spc):
        time_out = 5 # seconds
        st = time.time()
        while time.time() - st < time_out:
            spc.i2c.write_block_data(PiPower5.ADV_CMD_START, [PiPower5.ADV_CMD_VBUS_EN, 0, PiPower5.ADV_CMD_END])
            if spc.read_input_voltage() == 0:
                break
            time.sleep(0.5)
        else:
            raise Exception(f'Failed to disable VBUS after {time_out} seconds')

    @staticmethod
    def enable_vbus(spc):
        time_out = 5 # seconds
        st = time.time()
        while time.time() - st < time_out:
            spc.i2c.write_block_data(PiPower5.ADV_CMD_START, [PiPower5.ADV_CMD_VBUS_EN, 1, PiPower5.ADV_CMD_END])
            if spc.read_input_voltage() > 0:
                break
        else:
            raise Exception(f'Failed to enable VBUS after {time_out} seconds')

    @staticmethod
    def power_failure_simulation(spc, test_time):
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
        PiPower5.disable_vbus(spc)
        print('OK')

        # -----------------
        st = time.time()
        while time.time() - st < test_time:
            #
            count += 1
            print(f'\r{count*interval:.1f}/{test_time}s', end='')
            data_buffer = spc.read_all()
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
        PiPower5.enable_vbus(spc)
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
        shutdown_percentage = spc.read_shutdown_percentage()
        #
        data_buffer = spc.read_all()
        bat_prec = data_buffer['battery_percentage']
        #
        available_prec = bat_prec - shutdown_percentage
        if available_prec < 0:
            available_prec = 0
        available_capacity = available_prec * PiPower5.BAT_MAX_CAPACITY / 100
        available_capacity = available_capacity * 0.8 # 20% reserve
        #
        available_time = int(available_capacity / 1000 / bat_current_avg * 3600) # sec
        available_time_hour = int(available_time / 3600)
        available_time_min = int((available_time % 3600) / 60)
        available_time_sec = int((available_time % 3600) % 60)
        available_time_str = f"{available_time_hour}hour " if available_time_hour > 0 else ''
        available_time_str += f'{available_time_min} min {available_time_sec} sec'
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
