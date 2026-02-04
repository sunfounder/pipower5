import os
import json
import signal
from importlib.resources import files as resource_files

from .pipower5_service import PiPower5Service
from .pipower5_system import PiPower5System

from .logger import Logger
from .utils import log_error, get_varient_id_and_version
from .version import __version__ as pipower5_version
from .constants import NAME, ID, PERIPHERALS, SYSTEM_DEFAULT_CONFIG

__package_name__ = __name__.split('.')[0]
CONFIG_PATH = str(resource_files(__package_name__).joinpath('config.json'))
_, BOARD_VERSION = get_varient_id_and_version()

DEFAULT_DEBUG_LEVEL = 'INFO' # 'DEBUG' | 'INFO' | 'WARNING' | 'ERROR' | 'CRITICAL'

class PiPower5Manager():

    def __init__(self, config_path=CONFIG_PATH):
        # --- init logger ---
        self.log = Logger('pipower5')
        self.log_level = 'INFO'

        # read config
        self.config_path = config_path
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {'system': SYSTEM_DEFAULT_CONFIG,}
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
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
        self.data = {}

    def init_service(self):
        # --- import ---
        has_pm_dashboard = False
        try:
            from pm_dashboard.pm_dashboard import PMDashboard
            from pm_dashboard.version import __version__ as pm_dashboard_version
            has_pm_dashboard = True
        except ImportError:
            has_pm_dashboard = False

        # Set debug level
        # -----------------------------------------
        _debug_level = self.config['system']['debug_level'].upper()
        if _debug_level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            self.log.warning(f"Invalid debug level '{_debug_level}', using default '{DEFAULT_DEBUG_LEVEL}'")
            _debug_level = DEFAULT_DEBUG_LEVEL
        self.set_debug_level(_debug_level)

        # LOG HEADER
        self.log.info(f"")
        self.log.info(f"{'#'*60}")
        self.log.debug(f"Config path: {CONFIG_PATH}")

        # --- print ---
        self.log.info(f'PiPower5 {pipower5_version} started')
        self.log.info(f"Board version: {BOARD_VERSION}")
        self.log.info(f"Config: {self.config}")
        self.log.info(f"Device info: {self.device_info}")
        if has_pm_dashboard:
            self.log.info(f"PM_Dashboard version: {pm_dashboard_version}")

        # --- init system ---
        self.system = PiPower5System(peripherals=PERIPHERALS, log=self.log)
        self.system.set_on_data_changed(self.handle_data_changed)

        # --- init service ---
        self.service = PiPower5Service(config=self.config['system'], log=self.log)
        self.service.set_on_data_changed(self.handle_data_changed)
        self.service.set_on_config_changed(self.update_config)
        self.service.set_on_button_shutdown(self.system.shutdown)
        self.service.set_on_battery_critical_shutdown(self.system.shutdown)
        self.service.set_on_battery_voltage_critical_shutdown(self.system.shutdown)

        # --- init pm_dashboard ---
        if not has_pm_dashboard:
            self.pm_dashboard = None
            self.log.warning('PM Dashboard not found skipping')
        else:
            self.pm_dashboard = PMDashboard(device_info=self.device_info,
                                            database=ID,
                                            config=self.config,
                                            log=self.log)
            self.pm_dashboard.set_read_data(self.read_data)
            self.pm_dashboard.set_read_config(self.read_config)
            self.pm_dashboard.set_on_config_changed(self.update_config)
            self.pm_dashboard.set_debug_level(self.log_level)
            self.pm_dashboard.set_test_smtp(self.service.test_smtp)
            self.pm_dashboard.set_on_restart_service(self.restart_service)
            self.pm_dashboard.set_play_pipower5_buzzer(self.play_pipower5_buzzer)

    @log_error
    def read_data(self):
        return self.data

    @log_error
    def read_config(self):
        return self.config

    @log_error
    def handle_data_changed(self, data) -> None:
        self.data.update(data)

    @log_error
    def play_pipower5_buzzer(self, event):
        self.service.buzz_event(event)

    @log_error
    def restart_service(self):
        self.log.info('Restarting PiPower5 service')
        os.system('sudo systemctl restart pipower5.service')

    @log_error
    def set_debug_level(self, level):
        self.log.setLevel(level)
        self.log_level = level
        if self.pm_dashboard:
            self.pm_dashboard.set_debug_level(level)

    @log_error
    def update_config(self, config):
        patch = {}
        if "temperature_unit" in config['system']:
            config['system']['temperature_unit'] = config['system']['temperature_unit'].upper()
            patch['temperature_unit'] = config['system']['temperature_unit']
        if "debug_level" in config['system']:
            config['system']['debug_level'] = config['system']['debug_level'].upper()
            self.set_debug_level(config['system']['debug_level'])
            patch['debug_level'] = config['system']['debug_level']
        
        service_patch = self.service.update_config(config['system'])
        patch.update(service_patch)

        if self.pm_dashboard:
            dashboard_patch = self.pm_dashboard.update_config(config['system'])
            patch.update(dashboard_patch)

        self.config["system"].update(patch)
        try:
            os.chmod(self.config_path, 0o777)
        except:
            pass
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)
        return self.config

    @log_error
    def start(self):
        self.init_service()
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGABRT, self.signal_handler)
        self.system.start()
        self.service.start()
        if self.pm_dashboard:
            self.pm_dashboard.start()
            self.log.info('PmDashboard started')
        while True:
            signal.pause()

    @log_error
    def stop(self):
        self.log.debug('Stopping PiPower5...')
        if self.system:
            self.system.stop()
            self.log.debug('Stop PiPower5 system.')
        if self.service:
            self.service.stop()
            self.log.debug('Stop PiPower5 service.')
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
