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
