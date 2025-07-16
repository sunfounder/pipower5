import time
import json
from enum import IntEnum
from spc.spc import SPC

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

    def __init__(self):
        super().__init__()

    def get_max_charge_current(self):
        return self.i2c.read_byte_data(self.REG_CHARGE_MAX_CURRENT)*100

    def disable_input(self):
        time_out = 5 # seconds
        st = time.time()
        while time.time() - st < time_out:
            self.i2c.write_block_data(self.ADV_CMD_START, [self.ADV_CMD_VBUS_EN, 0, self.ADV_CMD_END])
            if self.read_input_voltage() == 0:
                break
            time.sleep(0.5)
        else:
            raise Exception(f'Failed to disable VBUS after {time_out} seconds')

    def enable_input(self):
        time_out = 5 # seconds
        st = time.time()
        while time.time() - st < time_out:
            self.i2c.write_block_data(self.ADV_CMD_START, [self.ADV_CMD_VBUS_EN, 1, self.ADV_CMD_END])
            if self.read_input_voltage() > 0:
                break
        else:
            raise Exception(f'Failed to enable VBUS after {time_out} seconds')

    def power_failure_simulation(self, test_time):
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
                if every_delay > 0:
                    time.sleep(every_delay)
        finally:
            print() # newline
            print('enable Input ... ', end='')
            self.enable_input()
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
        #
        with open('/opt/pipower5/blackout_simulation.json', 'w') as f:
            json.dump(result, f, indent=4)
        #
        return result
    
    def read_power_btn(self):
        '''
        Read power button state.

        Returns:
            ButtonState: Power button state.
        '''
        val = self.i2c.read_byte_data(self.REG_PWR_BTN_STATE)
        self.i2c.write_byte_data(self.REG_WRITE_POWER_BTN_STATE, 0) # reset state

        return ButtonState(val)

    def read_shutdown_request(self):
        '''
        Read shutdown request.

        Returns:
            ShutdownRequest: Shutdown request.
        '''
        val = super().read_shutdown_request()
        return ShutdownRequest(val)
