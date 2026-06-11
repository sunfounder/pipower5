from enum import IntEnum, StrEnum
from .device import check_pipower5_connected, DEVICE_PATH

BAT_MAX_CAPACITY = 2000  # mAh


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
    BATTERY_ACTIVATED = "battery_activated"
    LOW_BATTERY = "low_battery"
    POWER_DISCONNECTED = "power_disconnected"
    POWER_RESTORED = "power_restored"
    POWER_INSUFFICIENT = "power_insufficient"
    BATTERY_CRITICAL_SHUTDOWN = "battery_critical_shutdown"
    BATTERY_VOLTAGE_CRITICAL_SHUTDOWN = "battery_voltage_critical_shutdown"


class PiPower5:
    """PiPower5 hardware interface -  reads sensors via sysfs, writes via sysfs."""

    BAT_MAX_CAPACITY = BAT_MAX_CAPACITY

    def __init__(self):
        check_pipower5_connected()

    # ---- SysFS helpers ----

    @staticmethod
    def _read_sysfs(name):
        with open(f"{DEVICE_PATH}/{name}", "r") as f:
            return f.read().strip()

    @classmethod
    def _read_sysfs_int(cls, name):
        return int(cls._read_sysfs(name))

    @staticmethod
    def _write_sysfs(name, value):
        with open(f"{DEVICE_PATH}/{name}", "w") as f:
            f.write(str(value))

    # ---- Sensor reads ----

    read_input_voltage       = lambda self: self._read_sysfs_int("input_voltage")
    read_input_current       = lambda self: self._read_sysfs_int("input_current")
    read_input_power         = lambda self: self._read_sysfs_int("input_power")
    read_output_voltage      = lambda self: self._read_sysfs_int("output_voltage")
    read_output_current      = lambda self: self._read_sysfs_int("output_current")
    read_output_power        = lambda self: self._read_sysfs_int("output_power")
    read_battery_voltage     = lambda self: self._read_sysfs_int("battery_voltage")
    read_battery_current     = lambda self: self._read_sysfs_int("battery_current")
    read_battery_percentage  = lambda self: self._read_sysfs_int("battery_percentage")
    read_battery_capacity    = lambda self: self._read_sysfs_int("battery_capacity")
    read_is_input_plugged_in = lambda self: bool(self._read_sysfs_int("is_input_plugged_in"))
    read_is_charging         = lambda self: bool(self._read_sysfs_int("is_charging"))
    read_power_source        = lambda self: PowerSource(self._read_sysfs_int("power_source"))
    read_shutdown_percentage = lambda self: self._read_sysfs_int("shutdown_percentage")
    read_firmware_version    = lambda self: self._read_sysfs("firmware_version")
    read_driver_version      = lambda self: self._read_sysfs("driver_version")
    read_default_on          = lambda self: bool(self._read_sysfs_int("default_on"))
    get_max_charge_current   = lambda self: self._read_sysfs_int("charge_current_max") * 100
    read_estimated_runtime   = lambda self: self._read_sysfs_int("estimated_runtime")
    read_buzzer_volume       = lambda self: self._read_sysfs_int("buzzer_volume")
    read_power_btn           = lambda self: ButtonState(self._read_sysfs_int("power_button_state"))
    read_shutdown_request    = lambda self: ShutdownRequest(self._read_sysfs_int("shutdown_request"))

    # ---- Write operations ----

    write_shutdown_percentage = lambda self, v: self._write_sysfs("shutdown_percentage", v)
    set_buzzer_volume         = lambda self, v: self._write_sysfs("buzzer_volume", v)

    # ---- Buzzer playback ----
    def buzz_sequence(self, sequence):
        """Play buzzer by event name via kernel driver sysfs.
        The kernel driver has built-in sequences for each event.
        """
        if not isinstance(sequence, str):
            raise TypeError(f"Expected str (event name), got {type(sequence)}")
        self._write_sysfs("buzzer_play", sequence)

    def power_failure_simulation(self, test_time=60):
        """Simulate power outage via kernel driver.
        The driver disables VBUS, samples at 1Hz, re-enables VBUS,
        and returns stats via sysfs. Python just polls for the result.
        """
        import json, time

        # Start the test via sysfs (kernel driver handles everything)
        self._write_sysfs("power_failure_test", str(test_time))

        last_progress = -1
        while True:
            status = self._read_sysfs("power_failure_test")
            if status.startswith("done "):
                result = json.loads(status[5:])
                # Convert driver units (mV, mA, mAh*1000) to human-readable
                n = result.get("samples", 1) or 1
                bat_v_avg = result["bat_voltage_avg"] / 1000.0
                bat_c_avg = result["bat_current_avg"] / 1000.0
                delta_mah = result["delta_mah"] / 1000.0
                est_runtime = result["estimated_runtime_s"]
                est_h = est_runtime // 3600
                est_m = (est_runtime % 3600) // 60

                print(f"\nResults: {delta_mah:.1f}mAh used, "
                      f"avg {bat_v_avg:.2f}V {bat_c_avg:.2f}A, "
                      f"~{est_h}h{est_m}m runtime")
                return {
                    "bat_mah_used": round(delta_mah, 3),
                    "bat_percent_used": result.get("bat_percent_used", 0),
                    "bat_voltage_avg": round(bat_v_avg, 3),
                    "bat_current_avg": round(bat_c_avg, 3),
                    "bat_power_avg": round(bat_v_avg * bat_c_avg, 3),
                    "bat_voltage_max": result["bat_voltage_max"] / 1000.0,
                    "bat_current_max": result["bat_current_max"] / 1000.0,
                    "bat_power_max": round(
                        result["bat_voltage_max"] * result["bat_current_max"] / 1e6, 3),
                    "output_voltage_avg": round(result["out_voltage_avg"] / 1000.0, 3),
                    "output_current_avg": round(result["out_current_avg"] / 1000.0, 3),
                    "output_power_avg": round(
                        result["out_voltage_avg"] * result["out_current_avg"] / 1e6, 3),
                    "output_voltage_max": result["out_voltage_max"] / 1000.0,
                    "output_current_max": result["out_current_max"] / 1000.0,
                    "output_power_max": round(
                        result["out_voltage_max"] * result["out_current_max"] / 1e6, 3),
                    "battery_percentage": self.read_battery_percentage(),
                    "shutdown_percentage": self.read_shutdown_percentage(),
                    "available_time": est_runtime,
                    "available_time_str": f"{est_h}h {est_m}m",
                    "available_bat_capacity": result.get("available_bat_capacity", 0),
                }
            elif status.startswith("running"):
                parts = status.split()
                elapsed = int(parts[1])
                total = int(parts[2])
                if elapsed != last_progress:
                    bar = int(elapsed / total * 20)
                    pct_bat = self.read_battery_percentage()
                    print(f"\r[{elapsed}s] {'#'*bar}{'.'*(20-bar)} "
                          f"bat:{pct_bat}%", end="", flush=True)
                    last_progress = elapsed
            elif status.startswith("idle"):
                print("Test was cancelled or did not start.")
                return None
            time.sleep(0.5)

    # ---- Aggregate read ----

    def read_all(self):
        return {
            "input_voltage": self.read_input_voltage(),
            "input_current": self.read_input_current(),
            "output_voltage": self.read_output_voltage(),
            "output_current": self.read_output_current(),
            "battery_voltage": self.read_battery_voltage(),
            "battery_current": self.read_battery_current(),
            "battery_percentage": self.read_battery_percentage(),
            "power_source": self.read_power_source(),
            "is_input_plugged_in": self.read_is_input_plugged_in(),
            "is_charging": self.read_is_charging(),
        }
