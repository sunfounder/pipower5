import time
import os
import threading
from spc.spc import SPC
from .utils import log_error

class ShutdownService():
    @log_error
    def __init__(self, get_logger=None):
        self.spc = SPC()
        if get_logger is None:
            import logging
            get_logger = logging.getLogger
        self.log = get_logger(__name__)

        self.interval = 1
        self.thread = None
        self.running = False

        self.last_shutdown_request = None
        self.last_is_input_plugged_in = None

    @log_error
    def update_config(self, config):
        if 'shutdown_percentage' in config:
            self.spc.write_shutdown_percentage(config['shutdown_percentage'])

    @log_error
    def loop(self):
        while self.running:
            shutdown_request = self.spc.read_shutdown_request()
            is_input_plugged_in = self.spc.read_is_input_plugged_in()
            if shutdown_request != self.last_shutdown_request:
                if shutdown_request == self.spc.SHUTDOWN_REQUEST_NONE:
                    continue
                elif shutdown_request == self.spc.SHUTDOWN_REQUEST_BUTTON:
                    self.log.info("Shutdown request: Button")
                    os.system("sudo shutdown -h now")
                elif shutdown_request == self.spc.SHUTDOWN_REQUEST_LOW_BATTERY:
                    self.log.info("Shutdown request: Low battery")
                    os.system("sudo shutdown -h now")
                self.last_shutdown_request = shutdown_request
            if is_input_plugged_in != self.last_is_input_plugged_in:
                if is_input_plugged_in:
                    self.log.info("Input plugged in")
                else:
                    self.log.info("Input unplugged")
                self.last_is_input_plugged_in = is_input_plugged_in
            time.sleep(self.interval)
    
    @log_error
    def start(self):
        if self.running:
            self.log.warning("Already running")
            return
        self.running = True
        self.thread = threading.Thread(target=self.loop)
        self.thread.start()
        self.log.info("Shutdown service started")

    @log_error
    def stop(self):
        if self.running:
            self.thread.join()
        self.running = False
        self.log.info("Shutdown service stoped")
