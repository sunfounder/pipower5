import os
import json
import signal
from importlib.resources import files as resource_files

from .pipower5_service import PiPower5Service

from .logger import Logger
from .utils import merge_dict, log_error, get_varient_id_and_version
from .version import __version__ as pipower5_version
from .constants import NAME, ID, PERIPHERALS, SYSTEM_DEFAULT_CONFIG, CUSTOM_PERIPHERALS

__package_name__ = __name__.split('.')[0]
CONFIG_PATH = str(resource_files(__package_name__).joinpath('config.json'))
_, BOARD_VERSION = get_varient_id_and_version()

class PiPower5Manager():

    def __init__(self, config_path=CONFIG_PATH):
        # --- init logger ---
        self.log = Logger('pipower5')
        self.log_level = 'INFO'

        # --- init config ---
        self.config = {
            'system': SYSTEM_DEFAULT_CONFIG,
            "peripherals": CUSTOM_PERIPHERALS,
        }
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
        

        # --- device_info ---
        self.device_info = {
            'name': NAME,
            'id': ID,
            'peripherals': PERIPHERALS,
            'version': pipower5_version,
        }

        self.pm_dashboard = None
        self.service = None

    def init_service(self):
        # --- import ---
        has_pm_dashboard = False
        try:
            from pm_dashboard.pm_dashboard import PMDashboard
            from pm_dashboard.version import __version__ as pm_dashboard_version
            has_pm_dashboard = True
        except ImportError:
            has_pm_dashboard = False

        # --- print ---
        self.log.info(f'PiPower5 {pipower5_version} started')
        self.log.info(f"Board version: {BOARD_VERSION}")
        self.log.debug(f"PiPower 5 version: {pipower5_version}")
        self.log.debug(f"Config: {self.config}")
        self.log.debug(f"Device info: {self.device_info}")
        if has_pm_dashboard:
            self.log.debug(f"PM_Dashboard version: {pm_dashboard_version}")

        # --- init pm_dashboard ---
        if not has_pm_dashboard:
            self.pm_dashboard = None
            self.log.warning('PM Dashboard not found skipping')
        else:
            self.pm_dashboard = PMDashboard(device_info=self.device_info,
                                            database=ID,
                                            spc_enabled=True if 'spc' in PERIPHERALS else False,
                                            config=self.config,
                                            log=self.log)
            self.pm_dashboard.set_on_config_changed(self.update_config)
            self.pm_dashboard.set_debug_level(self.log_level)
        # --- init service ---
        self.service = PiPower5Service(config=self.config, log=self.log)
        self.service.set_on_button_shutdown(self.handle_shutdown)
        self.service.set_on_low_battery_shutdown(self.handle_shutdown)
        self.service.set_on_low_voltage_shutdown(self.handle_shutdown)
            
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
        self.log_level = level
        if self.pm_dashboard:
            self.pm_dashboard.set_debug_level(level)

    @log_error
    def update_config(self, config):
        patch = self.service.update_config(config['system'])
        self.config.update(patch)
        try:
            os.chmod(self.config_path, 0o777)
        except:
            pass
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)

    @log_error
    def handle_shutdown(self):
        os.system(' hutdown -h now')

    @log_error
    def start(self):
        self.init_service()
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGABRT, self.signal_handler)
        self.service.start()
        if self.pm_dashboard:
            self.pm_dashboard.start()
            self.log.info('PmDashboard started')
        while True:
            signal.pause()

    @log_error
    def stop(self):
        self.log.debug('Stopping PiPower5...')
        if self.service:
            self.service.stop()
            self.log.debug('Stop Shutdown service.')
        if self.pm_dashboard:
            self.log.debug('Stop PM Dashboard.')
            self.pm_dashboard.stop()
        import threading
        for t in threading.enumerate():
            if t is not threading.main_thread():
                self.log.warning(f"Thread {t.name} is still alive")
        quit()

    @log_error
    def signal_handler(self, signum, frame):
        self.log.info(f'Received signal "{signal.strsignal(signum)}", cleaning up...')
        self.stop()
