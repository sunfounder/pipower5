import time
import json
from enum import IntEnum, StrEnum
from .note import NOTES, get_note_freq
from .device import check_pipower5_connected, DEVICE_PATH
import threading

I2C_ADDR = 0x5C
I2C_BUS = 1

# Internal register addresses (for operations not exposed via sysfs)
REG_WRITE_BUZZER_FEQ_L = 13
REG_WRITE_BUZZER_FEQ_H = 14
REG_READ_BATTERY_1_VOLTAGE = 0x50   # V50 board variant
REG_READ_BATTERY_2_VOLTAGE = 0x52   # V50 board variant
REG_PWR_BTN_STATE = 154
REG_WRITE_POWER_BTN_STATE = 12
REG_CHARGE_MAX_CURRENT = 155

ADV_CMD_START = 0xAC
ADV_CMD_END = 0xAE
ADV_CMD_OK = 0xE0
ADV_CMD_ERR = 0xEF
ADV_CMD_RST = 0x00
ADV_CMD_VBUS_EN = 0x01
ADV_CMD_BAT_EN = 0x02
ADV_CMD_OUPUT_EN = 0x03
ADV_CMD_ENTER_IAP = 0x04

BAT_MAX_CAPACITY = 2000 # mAh

PAUSE_ACTIONS = ['pause', 'PAUSE', 'Pause', 'P', 'p']

class PowerSource(IntEnum):
    EXTERNAL = 0
    BATTERY = 1

class ButtonState(IntEnum):
    RELEASED = 0
    CLICK = 1
    DOUBLE_CLICK = 2
    LONG_PRESS_2S = 3
    LONG_PRESS_2S_RELEASED = 4
    LONG_PRESS_5S = 5
    LONG_PRESS_5S_RELEASED = 6

class ShutdownRequest(IntEnum):
    NONE = 0
    LOW_BATTERY = 1
    BUTTON = 2
    LOW_VOLTAGE = 3

class Event(StrEnum):
    BATTERY_ACTIVATED = 'battery_activated'
    LOW_BATTERY = 'low_battery'
    POWER_DISCONNECTED = 'power_disconnected'
    POWER_RESTORED = 'power_restored'
    POWER_INSUFFICIENT = 'power_insufficient'
    BATTERY_CRITICAL_SHUTDOWN = 'battery_critical_shutdown'
    BATTERY_VOLTAGE_CRITICAL_SHUTDOWN = 'battery_voltage_critical_shutdown'

class PiPower5():
    BAT_MAX_CAPACITY = BAT_MAX_CAPACITY

    def __init__(self):
        check_pipower5_connected()
        from smbus2 import SMBus
        self._i2c = SMBus(I2C_BUS)
        self.buzzer_sequence_queue = []
        self.buzzer_thread = None
        self.buzzer_stop = False

    # ==================== SysFS Helpers ====================

    def _read_sysfs(self, name):
        with open(f"{DEVICE_PATH}/{name}", "r") as f:
            return f.read().strip()

    def _read_sysfs_int(self, name):
        return int(self._read_sysfs(name))

    def _write_sysfs(self, name, value):
        with open(f"{DEVICE_PATH}/{name}", "w") as f:
            f.write(str(value))

    # ==================== Sensor Reads (sysfs) ====================

    def read_input_voltage(self):
        return self._read_sysfs_int("input_voltage")
    def read_input_current(self):
        return self._read_sysfs_int("input_current")
    def read_input_power(self):
        return self._read_sysfs_int("input_power")
    def read_output_voltage(self):
        return self._read_sysfs_int("output_voltage")
    def read_output_current(self):
        return self._read_sysfs_int("output_current")
    def read_output_power(self):
        return self._read_sysfs_int("output_power")
    def read_battery_voltage(self):
        return self._read_sysfs_int("battery_voltage")
    def read_battery_current(self):
        return self._read_sysfs_int("battery_current")
    def read_battery_power(self):
        return self._read_sysfs_int("battery_power")
    def read_battery_percentage(self):
        return self._read_sysfs_int("battery_percentage")
    def read_is_input_plugged_in(self):
        return bool(self._read_sysfs_int("is_input_plugged_in"))
    def read_is_charging(self):
        return bool(self._read_sysfs_int("is_charging"))
    def read_power_source(self):
        return PowerSource(self._read_sysfs_int("power_source"))
    def read_shutdown_request(self):
        return ShutdownRequest(self._read_sysfs_int("shutdown_request"))
    def read_shutdown_percentage(self):
        return self._read_sysfs_int("shutdown_percentage")
    def read_firmware_version(self):
        return self._read_sysfs("firmware_version")
    def read_default_on(self):
        return bool(self._read_sysfs_int("default_on"))
    def get_max_charge_current(self):
        return self._read_sysfs_int("charge_current_max") * 100
    def read_buzzer_volume(self):
        return self._read_sysfs_int("buzzer_volume")
    def get_buzzer_volume(self):
        return self.read_buzzer_volume()
    def read_power_btn(self):
        '''
        Read power button state. Reads from register 154 via sysfs,
        then writes 0 to register 12 to reset.
        '''
        val = self._read_sysfs_int("power_button_state")
        self._i2c.write_byte_data(I2C_ADDR, REG_WRITE_POWER_BTN_STATE, 0)
        return ButtonState(val)
    def read_battery_1_voltage(self):
        '''V50 board: battery 1 voltage (mV)'''
        return self._i2c.read_word_data(I2C_ADDR, REG_READ_BATTERY_1_VOLTAGE)
    def read_battery_2_voltage(self):
        '''V50 board: battery 2 voltage (mV)'''
        return self._i2c.read_word_data(I2C_ADDR, REG_READ_BATTERY_2_VOLTAGE)

    def read_all(self):
        '''Read all sensor data in one call.'''
        return {
            'input_voltage': self.read_input_voltage(),
            'input_current': self.read_input_current(),
            'output_voltage': self.read_output_voltage(),
            'output_current': self.read_output_current(),
            'battery_voltage': self.read_battery_voltage(),
            'battery_current': self.read_battery_current(),
            'battery_percentage': self.read_battery_percentage(),
            'power_source': self.read_power_source(),
            'is_input_plugged_in': self.read_is_input_plugged_in(),
            'is_charging': self.read_is_charging(),
        }

    # ==================== Write Operations (sysfs + I2C) ====================

    def write_shutdown_percentage(self, value):
        self._write_sysfs("shutdown_percentage", value)

    def set_buzzer_volume(self, volume):
        self._write_sysfs("buzzer_volume", volume)

    def write_buzzer_volume(self, volume):
        self._write_sysfs("buzzer_volume", volume)

    def write_buzzer_freq(self, freq):
        '''Write 16-bit buzzer frequency to registers 13 (low) and 14 (high).'''
        freq = int(freq)
        self._i2c.write_byte_data(I2C_ADDR, REG_WRITE_BUZZER_FEQ_L, freq & 0xFF)
        self._i2c.write_byte_data(I2C_ADDR, REG_WRITE_BUZZER_FEQ_H, (freq >> 8) & 0xFF)



    def disable_input(self):
        time_out = 5 # seconds
        st = time.time()
        while time.time() - st < time_out:
            self._i2c.write_i2c_block_data(I2C_ADDR, ADV_CMD_START, [ADV_CMD_VBUS_EN, 0, ADV_CMD_END])
            status = self._i2c.read_byte(I2C_ADDR)
            if status == ADV_CMD_OK:
                return True
            # !!! Don't add delay, otherwise status maybe error casued multiple process read data at the same time !!!
        else:
            return False

    def enable_input(self):
        time_out = 5 # seconds
        st = time.time()
        while time.time() - st < time_out:
            self._i2c.write_i2c_block_data(I2C_ADDR, ADV_CMD_START, [ADV_CMD_VBUS_EN, 1, ADV_CMD_END])
            status = self._i2c.read_byte(I2C_ADDR)
            if status == ADV_CMD_OK:
                return True
            # !!! Don't add delay, otherwise status maybe error casued multiple process read data at the same time !!!
        else:
            return False

    def power_failure_simulation(self, test_time):
        import signal, os
        # --- Protect VBUS when the program terminates. ---
        def signal_handler(signum, frame):
            if signum == signal.SIGINT:
                print('\nCancelled by user.')
            print('enable input ... ', end='')
            if self.enable_input():
                print('OK')
            else:
                print('Failed')

            print('exit')
            quit()

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGABRT, signal_handler)
    
        # --- clear the report ---
        file_path = '/opt/pipower5/blackout_simulation'
        with open(file_path + '.json', 'w') as f:
            # pass
            json.dump({}, f, indent=4)
        with open(file_path + ".lock", "w") as lock_file:
            lock_file.write("writing")

        # --- checkout power status ---
        battery_percentage =  self.read_battery_percentage()
        is_input_plugged_in = self.read_is_input_plugged_in()

        # Temporary set shutdown percentage
        origin_shutdown_percentage = self.read_shutdown_percentage()
        self.write_shutdown_percentage(10)

        print(f'battery: {battery_percentage}%, input: {"plugged in" if is_input_plugged_in else "unplugged"}')

        warn_emoji = '\U000026A0'
        if battery_percentage < 80:
            print(f'{warn_emoji} Battery must be greater than 80%')
            return None
        if not is_input_plugged_in:
            print(f'{warn_emoji} Input must be plugged in')
            return None

        # --- variables ---
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
        print('disable input ... ', end='')
        self.disable_input()
        print('OK')

        # -----------------
        simulation_start = time.time()
        mah_used = 0.0
        mah_interval_start = None
        try:
            while True:
                #
                count += 1
                every_start = time.time()
                dt = every_start - simulation_start
                if dt > test_time:
                    break
                # print(f'\r{dt:.0f}/{test_time}s', end='')
                #
                data_buffer = self.read_all()

                bat_voltage = data_buffer['battery_voltage']
                bat_current = -data_buffer['battery_current'] # negative value
                bat_power = bat_voltage * bat_current / 1000 / 1000 # W
                
                if mah_interval_start is None:
                    mah_interval_start = time.time()
                else:
                    duration = (time.time() - mah_interval_start) / 3600.0
                    mah = bat_current * duration
                    mah_used += mah
                    mah_interval_start = time.time()

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

                every_delay = interval - (time.time() - every_start)
                print(f'\r{dt:.0f}/{test_time}s, {bat_voltage/1000:.2f} V, {bat_current/1000:.2f} A, {bat_power:.2f} W', end='', flush=True)
                if every_delay > 0:
                    time.sleep(every_delay)
        finally:
            print() # newline
            print('enable Input ... ', end='')
            self.enable_input()
            # reset shutdown percentage
            self.write_shutdown_percentage(origin_shutdown_percentage)
            print('OK')

        # -----------------
        bat_mah_used = round(mah_used, 3)
        bat_percent_used = round(bat_voltage_avg / (self.BAT_MAX_CAPACITY*0.8) * 100, 3)
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
            'bat_mah_used': bat_mah_used,
            'bat_percent_used': bat_percent_used,
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
        # --- save result ---
        with open('/opt/pipower5/blackout_simulation.json', 'w') as f:
            json.dump(result, f, indent=4)
        os.remove(file_path + ".lock")        
        #
        return result


    def _buzz_action(self, action):
        if action in PAUSE_ACTIONS:
            self.write_buzzer_freq(0)
        elif isinstance(action, str):
            if action is not None and action in NOTES:
                freq = get_note_freq(action)
                freq = int(freq)
                self.write_buzzer_freq(freq)
            else:
                raise ValueError(f"Invalid note: {action}")
        elif isinstance(action, int):
            if action > 0 and action < 65535:
                self.write_buzzer_freq(action)
            else:
                raise ValueError(f"Invalid frequency: {action}")
        else:
            raise ValueError(f"Invalid action: {action}")

    def _buzz_sequence(self, sequence):
        '''
        Buzz according to the sequence, every value is a list of [action, duration]
        Actions:
        - Tone note string like 'C5', 'D3', 'C#1'
        - Frequency integer like 440, 880
        - Pause string like 'pause', 'PAUSE', 'Pause', 'P', 'p', 'stop', 'STOP'
        Duration:
        - Integer like 1000, 2000 in milisecond

        Args:
            sequence (list): A list of [action, duration]
        '''
        for action, duration in sequence:
            if self.buzzer_stop:
                break
            self._buzz_action(action)
            time.sleep(duration / 1000)
        self.write_buzzer_freq(0)

    def _buzz_sequence_loop(self):
        while not self.buzzer_stop:
            if len(self.buzzer_sequence_queue) > 0:
                sequence = self.buzzer_sequence_queue.pop(0)
                self._buzz_sequence(sequence)
                time.sleep(1)
            else:
                break
        self.buzzer_thread = None

    def buzz_sequence(self, sequence: [str,list]):
        '''
        Buzz according to the sequence, every value is a list of [action, duration]
        Actions:
        - Tone note string like 'C5', 'D3', 'C#1'
        - Frequency integer like 440, 880
        - Pause string like 'pause', 'PAUSE', 'Pause', 'P', 'p', 'stop', 'STOP'
        Duration:
        - Integer like 1000, 2000 in milisecond

        Args:
            sequence (str|list): A list of [[action, duration], [action, duration]] or a string of action,duration:action,duration.
        '''
        self.buzzer_stop = False
        if isinstance(sequence, str):
            sequence = [item.split(',') for item in sequence.split(':')]
            sequence = [[action.strip(), int(duration.strip())] for action, duration in sequence]

        self.buzzer_sequence_queue.append(sequence)
        if self.buzzer_thread is None or not self.buzzer_thread.is_alive():
            self.buzzer_thread = threading.Thread(target=self._buzz_sequence_loop)
            self.buzzer_thread.start()
        
