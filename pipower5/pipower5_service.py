import asyncio
import logging
from .pipower5 import PiPower5, ButtonState, ShutdownRequest
from .utils import log_error
from .email_sender import EmailSender, EmailModes
from .battery_device import BatteryDevice
import threading
from .utils import LazyCaller

class PiPower5Service():
    @log_error
    def __init__(self, config, device_name='PiPower5', log=None):
        self.device_name = device_name
        self._is_ready = False
        self.log = log or logging.getLogger(__name__)
        self.update_config(config, init=True)
        
        self.pipower5 = PiPower5()
        try:
            self.email_sender = EmailSender(config, log=self.log)
        except Exception as e:
            self.log.warning(f'Email sender init failed: {e}')
            self.email_sender = None

        self.device = BatteryDevice()

        self.shutdown_percentage = self.pipower5.read_shutdown_percentage()
        self.log.debug(f'PiPower5 shutdown percentage: {self.shutdown_percentage}')

        self.interval = 1
        self.task = None
        self.running = False
        self.loop = None
        self.loop_thread = None

        self.last_shutdown_request = None
        self.last_is_input_plugged_in = True

        self.__on_user_button_click__ = None
        self.__on_user_button_double_click__ = None
        self.__on_user_button_long_press__ = None
        self.__on_user_battery_critical_shutdown__ = None
        self.__on_user_button_shutdown__ = None
        self.__on_user_battery_critical_shutdown__ = None
        self.__on_user_low_battery__ = None
        self.__on_user_power_insufficient__ = None
        self.__on_user_battery_activated__ = None
        self.__on_user_power_restore__ = None
        self.__on_user_power_disconnected__ = None
        self.__on_data_changed__ = None

        self.on_low_battery = LazyCaller(self._on_low_battery, interval=10*60) # 10 minutes
        self.on_power_insufficient = LazyCaller(self._on_power_insufficient, interval=10*60) # 10 minutes
        self.on_battery_critical_shutdown = LazyCaller(self._on_battery_critical_shutdown, interval=10*60) # 10 minutes
        self.on_battery_voltage_critical_shutdown = LazyCaller(self._on_battery_voltage_critical_shutdown, interval=10*60) # 10 minutes
        self.on_power_restore = LazyCaller(self._on_power_restore, oneshot=True) # 10 minutes
        self.on_power_disconnected = LazyCaller(self._on_power_disconnected, oneshot=True) # 10 minutes

        self._is_ready = True

    @log_error
    def set_on_button_click(self, callback):
        '''
        Set callback for button click.

        Args:
            callback (function): Callback function.
        '''
        self.__on_user_button_click__ = callback

    @log_error
    def set_on_button_double_click(self, callback):
        '''
        Set callback for button double click.

        Args:
            callback (function): Callback function.
        '''
        self.__on_user_button_double_click__ = callback

    @log_error
    def set_on_button_long_press(self, callback):
        '''
        Set callback for button long press.

        Args:
            callback (function): Callback function.
        '''
        self.__on_user_button_long_press__ = callback

    @log_error
    def set_on_battery_critical_shutdown(self, callback):
        '''
        Set callback for low battery shutdown

        Args:
            callback (function): Callback function.
        '''
        self.__on_user_battery_critical_shutdown__ = callback

    @log_error
    def set_on_button_shutdown(self, callback):
        '''
        Set callback for button shutdown.

        Args:
            callback (function): Callback function.
        '''
        self.__on_user_button_shutdown__ = callback

    @log_error
    def set_on_battery_voltage_critical_shutdown(self, callback):
        '''
        Set callback for low voltage shutdown

        Args:
            callback (function): Callback function.
        '''
        self.__on_user_battery_critical_shutdown__ = callback

    @log_error
    def set_on_low_battery(self, callback):
        '''
        Set callback for low power.

        Args:
            callback (function): Callback function.
        '''
        self.__on_user_low_battery__ = callback

    @log_error
    def set_on_power_insufficient(self, callback):
        '''
        Set callback for power insufficient.

        Args:
            callback (function): Callback function.
        '''
        self.__on_user_power_insufficient__ = callback

    @log_error
    def set_on_battery_activated(self, callback):
        '''
        Set callback for battery activated.

        Args:
            callback (function): Callback function.
        '''
        self.__on_user_battery_activated__ = callback

    @log_error
    def set_on_power_restore(self, callback):
        '''
        Set callback for input plugged in.

        Args:
            callback (function): Callback function.
        '''
        self.__on_user_power_restore__ = callback

    @log_error
    def set_on_power_disconnected(self, callback):
        '''
        Set callback for input unplugged.

        Args:
            callback (function): Callback function.
        '''
        self.__on_user_power_disconnected__ = callback

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
        if not init and self.email_sender:
            email_patch = self.email_sender.update_config(config)
            patch.update(email_patch)
        return patch

    @log_error
    def is_ready(self):
        return self._is_ready

    @log_error
    def send_email(self, mode, data):
        if not self.email_sender:
            self.log.debug("Email sender not ready")
            return False
        if mode not in self.send_email_on:
            self.log.debug(f"Email {mode} not in send_email_on")
            return False
        
        status = self.email_sender.send_preset_email(mode, data)
        if status == True:
            self.log.debug(f"Email {mode} sent successfully")
            return True
        else:
            self.log.error(f"Failed to send email {mode}: {status}")
            return False

    @log_error
    def test_smtp(self):
        '''
        Test SMTP connection.

        Returns:
            bool: True if connection is successful, False otherwise.
        '''
        try:
            self.email_sender.connect()
            return True, None
        except Exception as e:
            self.log.warning(f"Failed to connect SMTP server: {e}")
            return False, str(e)

    @log_error
    def call(self, callback, data):
        if callback:
            callback(data)

    @log_error
    def _on_low_battery(self, data):
        self.log.info("Low Battery")
        if self.__on_user_low_battery__:
            self.__on_user_low_battery__("Low Battery")
        self.send_email(EmailModes.LOW_BATTERY, data)

    @log_error
    def _on_power_insufficient(self, data):
        self.log.info("Power Insufficient")
        if self.__on_user_power_insufficient__:
            self.__on_user_power_insufficient__("Power Insufficient")
        self.send_email(EmailModes.POWER_INSUFFICIENT, data)

    @log_error
    def _on_battery_critical_shutdown(self, data):
        self.log.info("Battery Critical Shutdown")
        if self.__on_user_battery_critical_shutdown__:
            self.__on_user_battery_critical_shutdown__("Battery Critical Shutdown")
        self.send_email(EmailModes.BATTERY_CRITICAL_SHUTDOWN, data)

    @log_error
    def _on_battery_voltage_critical_shutdown(self, data):
        self.log.info("Battery Voltage Critical Shutdown")
        if self.__on_user_battery_critical_shutdown__:
            self.__on_user_battery_critical_shutdown__("Battery Voltage Critical Shutdown")
        self.send_email(EmailModes.BATTERY_VOLTAGE_CRITICAL_SHUTDOWN, data)

    @log_error
    def _on_power_restore(self, data):
        self.log.info("Power Restore")
        if self.__on_user_power_restore__:
            self.__on_user_power_restore__("Power Restore")
        self.send_email(EmailModes.POWER_RESTORED, data)
        self.on_power_insufficient.reset()

    @log_error
    def _on_power_disconnected(self, data, shutdown_percentage):
        self.log.info("Power Disconnected")
        try:
            remain_percentage = data['battery_percentage'] - shutdown_percentage
            remain_mAh = self.pipower5.BAT_MAX_CAPACITY * remain_percentage / 100
            current = -data['battery_current']
            estimated_time = remain_mAh / current
            estimated_time = round(estimated_time, 2)
        except Exception as e:
            self.log.error(f"Failed to estimate time until shutdown: {e}")
            estimated_time = "Unknown"
        data['battery_current_output'] = current
        data['shutdown_percentage'] = shutdown_percentage
        data['estimated_time'] = estimated_time
        if self.__on_user_power_disconnected__:
            self.__on_user_power_disconnected__("Power Disconnected")
        self.send_email(EmailModes.POWER_DISCONNECTED, data)
        self.on_power_insufficient.reset()
        self.on_power_restore.reset()

    @log_error
    async def main(self):
        while self.running:
            data = self.pipower5.read_all()
            data['device_name'] = self.device_name
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
                self.call(self.__on_user_button_click__, button_state)
            elif button_state == ButtonState.DOUBLE_CLICK:
                self.log.debug(f'pipower5_button_double_click: {button_state}')
                self.call(self.__on_user_button_double_click__, button_state)
            elif button_state == ButtonState.LONG_PRESS_2S:
                self.log.debug(f'pipower5_button_long_click: {button_state}')
                self.call(self.__on_user_button_long_press__, button_state)

            # Check low battery
            if battery_percentage < shutdown_percentage:
                self.on_low_battery(data)
            elif battery_percentage > shutdown_percentage + 5:
                self.on_low_battery.reset()

            # Check shutdown request
            if shutdown_request != self.last_shutdown_request:
                if shutdown_request == ShutdownRequest.BUTTON:
                    self.log.info("Shutdown request: Button")
                    self.call(self.__on_user_button_shutdown__, data, shutdown_percentage)
                elif shutdown_request == ShutdownRequest.LOW_BATTERY:
                    self.on_battery_critical_shutdown(data)
                elif shutdown_request == ShutdownRequest.LOW_VOLTAGE:
                    self.on_battery_voltage_critical_shutdown(data)
                self.last_shutdown_request = shutdown_request

            if is_input_plugged_in:
                self.on_power_restore(data)
                # Check power insufficient
                if  power_source == 'battery' and is_input_plugged_in:
                    self.on_power_insufficient(data)
            else:
                self.on_power_disconnected(data)
            await asyncio.sleep(self.interval)

    @log_error
    def start(self):
        if self.running:
            self.log.warning("Already running")
            return
        
        self.running = True
        # 创建新的事件循环
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        # 在新线程中运行事件循环
        self.loop_thread = threading.Thread(target=self._run_loop, daemon=True)
        self.loop_thread.start()
        # 在事件循环中创建并运行任务
        self.loop.call_soon_threadsafe(self._start_loop_task)
        self.log.info("PiPower5 service started")

    def _run_loop(self):
        """在线程中运行事件循环"""
        try:
            self.loop.run_forever()
        except Exception as e:
            self.log.error(f"Event loop error: {e}")
        finally:
            self.loop.close()
            self.log.info("Event loop closed")

    def _start_loop_task(self):
        """在事件循环中创建并启动任务"""
        self.task = self.loop.create_task(self.main())

    @log_error
    def stop(self):
        if not self.running or self.task is None:
            self.log.warning("Service not running")
            return
            
        self.running = False
        
        # 如果任务已完成，直接返回
        if self.task.done():
            return
            
        # 取消任务
        self.loop.call_soon_threadsafe(self.task.cancel)
        
        # 停止事件循环
        self.loop.call_soon_threadsafe(self.loop.stop)
        
        # 等待线程结束
        if self.loop_thread and self.loop_thread.is_alive():
            self.loop_thread.join(timeout=2.0)
                
        self.log.info("PiPower5 service stopped")
