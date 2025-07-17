import asyncio
import logging
from .pipower5 import PiPower5, ButtonState, ShutdownRequest
from .utils import log_error
from .email_sender import EmailSender, EmailModes
from .battery_device import BatteryDevice

class PiPower5Service():
    @log_error
    def __init__(self, config, log=None):
        self._is_ready = False
        self.log = log or logging.getLogger(__name__)
        self._is_ready = False
        
        self.pipower5 = PiPower5()
        try:
            self.email_sender = EmailSender(config)
        except Exception as e:
            self.log.error(f'Email sender init failed: {e}')
            self.email_sender = None

        self.device = BatteryDevice()

        self.shutdown_percentage = self.pipower5.read_shutdown_percentage()
        self.log.debug(f'PiPower5 shutdown percentage: {self.shutdown_percentage}')

        self.interval = 1
        self.task = None
        self.running = False

        self.last_shutdown_request = None
        self.last_is_input_plugged_in = None

        self.__on_button_click__ = None
        self.__on_button_double_click__ = None
        self.__on_button_long_press__ = None
        self.__on_low_battery_shutdown__ = None
        self.__on_button_shutdown__ = None
        self.__on_low_voltage_shutdown__ = None
        self.__on_low_power__ = None
        self.__on_power_insufficient__ = None
        self.__on_battery_activated__ = None
        self.__on_input_plugged_in__ = None
        self.__on_input_unplugged__ = None
        self.__on_data_changed__ = None

        self.update_config(config)

        self._is_ready = True

    @log_error
    def set_on_button_click(self, callback):
        '''
        Set callback for button click.

        Args:
            callback (function): Callback function.
        '''
        self.__on_button_click__ = callback

    @log_error
    def set_on_button_double_click(self, callback):
        '''
        Set callback for button double click.

        Args:
            callback (function): Callback function.
        '''
        self.__on_button_double_click__ = callback

    @log_error
    def set_on_button_long_press(self, callback):
        '''
        Set callback for button long press.

        Args:
            callback (function): Callback function.
        '''
        self.__on_button_long_press__ = callback

    @log_error
    def set_on_low_battery_shutdown(self, callback):
        '''
        Set callback for low battery shutdown

        Args:
            callback (function): Callback function.
        '''
        self.__on_low_battery_shutdown__ = callback

    @log_error
    def set_on_button_shutdown(self, callback):
        '''
        Set callback for button shutdown.

        Args:
            callback (function): Callback function.
        '''
        self.__on_button_shutdown__ = callback

    @log_error
    def set_on_low_voltage_shutdown(self, callback):
        '''
        Set callback for low voltage shutdown

        Args:
            callback (function): Callback function.
        '''
        self.__on_low_voltage_shutdown__ = callback

    @log_error
    def set_on_low_power(self, callback):
        '''
        Set callback for low power.

        Args:
            callback (function): Callback function.
        '''
        self.__on_low_power__ = callback

    @log_error
    def set_on_power_insufficient(self, callback):
        '''
        Set callback for power insufficient.

        Args:
            callback (function): Callback function.
        '''
        self.__on_power_insufficient__ = callback

    @log_error
    def set_on_battery_activated(self, callback):
        '''
        Set callback for battery activated.

        Args:
            callback (function): Callback function.
        '''
        self.__on_battery_activated__ = callback

    @log_error
    def set_on_input_plugged_in(self, callback):
        '''
        Set callback for input plugged in.

        Args:
            callback (function): Callback function.
        '''
        self.__on_input_plugged_in__ = callback

    @log_error
    def set_on_input_unplugged(self, callback):
        '''
        Set callback for input unplugged.

        Args:
            callback (function): Callback function.
        '''
        self.__on_input_unplugged__ = callback

    @log_error
    def set_on_data_changed(self, callback):
        '''
        Set callback for data changed.

        Args:
            callback (function): Callback function.
        '''
        self.__on_data_changed__ = callback

    @log_error
    def update_config(self, config, init=False):
        '''
        Update config.

        Args:
            config (Dict): New config dict.

        Returns:
            A dict of config patch to update the config file.
        '''
        patch = {}
        if "shutdown_percentage" in config:
            _percentage = config['shutdown_percentage']
            if not init:
                self.pipower5.write_shutdown_percentage(_percentage)
            patch['shutdown_percentage'] = _percentage
            self.log.debug(f'Set PiPower5 shutdown percentage: {_percentage}')
        if 'send_email_on' in config:
            _send_email_on = config['send_email_on']
            self.send_email_on = _send_email_on
            patch['send_email_on'] = _send_email_on
            self.log.debug(f'Set PiPower5 send email on: {_send_email_on}')
        return patch

    @log_error
    def is_ready(self):
        return self._is_ready

    @log_error
    def send_email(self, mode, data):
        if not self.email_sender:
            return "Email sender not ready"
        if mode not in self.send_email_on:
            return f"Email {mode} not in send_email_on"
        status = self.email_sender.send_preset_email(mode, data)
        if status == True:
            return f"Email {mode} sent successfully"
        else:
            return f"Failed to send email {mode}: {status}"

    @log_error
    def call(self, callback, data):
        if callback:
            callback(data)

    @log_error
    async def loop(self):
        while self.running:
            data = self.pipower5.read_all()
            self.call(self.__on_data_changed__, data)
            self.device.update_battery(data)

            battery_percentage = data['battery_percentage']
            is_input_plugged_in = data['is_input_plugged_in']
            power_source = data['power_source']
            shutdown_percentage = self.pipower5.read_shutdown_percentage()

            button_state = self.pipower5.read_power_btn()
            shutdown_request = self.pipower5.read_shutdown_request()

            # Check button state
            if button_state == ButtonState.CLICK:
                self.log.debug(f'pipower5_button_click: {button_state}')
                self.call(self.__on_button_click__, button_state)
            elif button_state == ButtonState.DOUBLE_CLICK:
                self.log.debug(f'pipower5_button_double_click: {button_state}')
                self.call(self.__on_button_double_click__, button_state)
            elif button_state == ButtonState.LONG_PRESS_2S:
                self.log.debug(f'pipower5_button_long_click: {button_state}')
                self.call(self.__on_button_long_press__, button_state)

            # Check low battery
            if battery_percentage < shutdown_percentage + 10:
                self.send_email(EmailModes.LOW_BATTERY, data)
                self.call(self.__on_low_battery_shutdown__, data)

            # Check power status
            if power_source == 'battery':
                if is_input_plugged_in:
                    self.send_email(EmailModes.POWER_INSUFFICIENT, data)
                    self.call(self.__on_power_insufficient__, data)
                self.send_email(EmailModes.BATTERY_ACTIVATED, data)
                self.call(self.__on_battery_activated__, data)
    
            # Check shutdown request
            if shutdown_request != self.last_shutdown_request:
                if shutdown_request == ShutdownRequest.BUTTON:
                    self.log.info("Shutdown request: Button")
                    self.call(self.__on_button_shutdown__, data)
                elif shutdown_request == ShutdownRequest.LOW_BATTERY:
                    self.log.info("Shutdown request: Low battery capacity")
                    self.call(self.__on_low_battery_shutdown__, data)
                    self.send_email(EmailModes.BATTERY_CRITICAL_SHUTDOWN, data)
                elif shutdown_request == ShutdownRequest.LOW_VOLTAGE:
                    self.log.info("Shutdown request: Low voltage")
                    self.call(self.__on_low_voltage_shutdown__, data)
                    self.send_email(EmailModes.BATTERY_VOLTAGE_CRITICAL_SHUTDOWN, data)
                self.last_shutdown_request = shutdown_request

            if is_input_plugged_in != self.last_is_input_plugged_in:
                if is_input_plugged_in:
                    self.log.info("Input plugged in")
                    self.send_email(EmailModes.POWER_RESTORED, data)
                    self.call(self.__on_input_plugged_in__, data)
                else:
                    self.log.info("Input unplugged")
                    self.send_email(EmailModes.POWER_DISCONNECTED, data)
                    self.call(self.__on_input_unplugged__, data)
                self.last_is_input_plugged_in = is_input_plugged_in
            await asyncio.sleep(self.interval)

    @log_error
    def start(self):
        if self.running:
            self.log.warning("Already running")
            return
        
        self.running = True
        # 获取当前事件循环
        loop = asyncio.get_running_loop()
        # 在事件循环中创建并运行任务
        self.task = loop.create_task(self.loop())
        self.log.info("Shutdown service started")

    @log_error
    def stop(self):
        if not self.running or self.task is None:
            self.log.warning("Service not running")
            return
            
        self.running = False
        
        # 如果任务已完成，直接返回
        if self.task.done():
            return
            
        # 取消任务并等待完成
        self.task.cancel()
        
        # 获取当前事件循环
        loop = asyncio.get_running_loop()
        
        # 如果在运行中，异步等待任务完成
        if loop.is_running():
            async def wait_for_task():
                try:
                    await self.task
                except asyncio.CancelledError:
                    pass
            loop.create_task(wait_for_task())
        else:
            # 如果事件循环未运行，同步等待
            try:
                loop.run_until_complete(self.task)
            except asyncio.CancelledError:
                pass
                
        self.log.info("Shutdown service stopped")
