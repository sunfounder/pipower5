from pipower5 import PiPower5
import time

power = PiPower5()

while True:
    print(power.read_power_btn())
    time.sleep(0.1)