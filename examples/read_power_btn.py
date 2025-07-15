from pipower5 import PiPower5
import time

power = PiPower5()

while True:
    state = power.read_power_btn()
    print(f"Button state: {int(state)} {state.name}")
    time.sleep(0.1)