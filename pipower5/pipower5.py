import json
import time
import os
from importlib.resources import files as resource_files

from .logger import create_get_child_logger
from .utils import merge_dict, log_error
from .version import __version__ as pipower5_version
from .constants import NAME, ID, PERIPHERALS, SYSTEM_DEFAULT_CONFIG

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
    def __init__(self):
        self.log = get_child_logger('main')
        self.config = {
            'system': SYSTEM_DEFAULT_CONFIG,
        }
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                config = json.load(f)
            merge_dict(self.config, config)
        with open(CONFIG_PATH, 'w') as f:
            json.dump(self.config, f, indent=4)

        self.update_extra_peripherals()

        device_info = {
            'name': NAME,
            'id': ID,
            'peripherals': PERIPHERALS,
            'version': pipower5_version,
        }

        self.log.debug(f"PiPower 5 version: {pipower5_version}")
        if PMDashboard is not None:
            self.log.debug(f"PM_Dashboard version: {pm_dashboard_version}")
        if PMDashboard is None:
            self.pm_dashboard = None
            self.log.warning('PM Dashboard not found skipping')
        else:
            self.pm_dashboard = PMDashboard(device_info=device_info,
                                            database=ID,
                                            spc_enabled=True if 'spc' in PERIPHERALS else False,
                                            config=self.config,
                                            get_logger=get_child_logger)
            self.pm_dashboard.set_on_config_changed(self.update_config)
        self.shutdown_service = ShutdownService(get_logger=get_child_logger)

    @log_error
    def update_extra_peripherals(self):
        if 'peripherals' not in self.config:
            return
        for peripheral in self.config['peripherals']:
            if self.config['peripherals'][peripheral]:
                if peripheral == 'pwm_fan':
                    PERIPHERALS.append("pwm_fan_speed")

    @log_error
    def set_debug_level(self, level):
        self.log.setLevel(level)
        if self.pm_dashboard:
            self.pm_dashboard.set_debug_level(level)

    @log_error
    def update_config(self, config):
        self.shutdown_service.update_config(config['system'])
        merge_dict(self.config, config)
        with open(CONFIG_PATH, 'w') as f:
            json.dump(self.config, f, indent=4)

    @log_error
    @staticmethod
    def update_config_file(config):
        current = None
        with open(CONFIG_PATH, 'r') as f:
            current = json.load(f)
        merge_dict(current, config)
        with open(CONFIG_PATH, 'w') as f:
            json.dump(current, f, indent=4)

    @log_error
    def start(self):
        self.shutdown_service.start()
        if self.pm_dashboard:
            self.pm_dashboard.start()
            self.log.info('PmDashboard started')
        while True:
            time.sleep(1)

    @log_error
    def stop(self):
        self.shutdown_service.stop()
        if self.pm_dashboard:
            self.pm_dashboard.stop()
