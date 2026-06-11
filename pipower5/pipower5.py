import json
from enum import IntEnum, StrEnum
from .device import check_pipower5_connected, DEVICE_PATH
from .note import get_note_freq

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
    read_buzzer_volume       = lambda self: self._read_sysfs_int("buzzer_volume")
    get_buzzer_volume        = read_buzzer_volume
    read_power_btn           = lambda self: ButtonState(self._read_sysfs_int("power_button_state"))
    # backward compat: old code expects this, kernel driver handles it internally now
    read_shutdown_request    = lambda self: ShutdownRequest.NONE

    # ---- Write operations ----

    write_shutdown_percentage = lambda self, v: self._write_sysfs("shutdown_percentage", v)
    set_buzzer_volume         = lambda self, v: self._write_sysfs("buzzer_volume", v)
    write_buzzer_volume       = set_buzzer_volume

    # ---- Backward compatibility stubs ----

    def buzz_sequence(self, sequence):
        """Play buzzer by event name or raw sequence via kernel sysfs.
        Event:  buzz_sequence('power_disconnected')
        Raw:    buzz_sequence('440,200;0,100;523,200')
        Old list format also supported for backward compat.
        """
        if isinstance(sequence, list):
            # Old format: [[note_or_freq, dur_ms], ...]
            parts = []
            for n in sequence:
                note, dur = n[0], n[1]
                if str(note).lower() in ('pause', 'p'):
                    parts.append(f"0,{dur}")
                elif isinstance(note, str) and note[0] in 'ABCDEFG':
                    freq = int(get_note_freq(note))
                    parts.append(f"{freq},{dur}")
                else:
                    parts.append(f"{note},{dur}")
            s = ";".join(parts)
        elif isinstance(sequence, str):
            # Write directly: event name or raw sequence
            s = sequence
        else:
            raise TypeError(f"Expected str or list, got {type(sequence)}")
        self._write_sysfs("buzzer_play", s)

    def power_failure_simulation(self, test_time=60):
        """Simulate power outage by disabling VBUS via kernel driver.
        Measures battery drain over <test_time> seconds and returns stats.
        """
        import signal, time

        if test_time < 10:
            test_time = 10
        if test_time > 600:
            test_time = 600

        bat_pct = self.read_battery_percentage()
        plugged = self.read_is_input_plugged_in()

        if bat_pct < 80:
            print("Battery must be >80%% for simulation (currently %d%%)" % bat_pct)
            return None
        if not plugged:
            print("Input must be plugged in for simulation")
            return None

        orig_shutdown = self.read_shutdown_percentage()
        self.write_shutdown_percentage(10)

        # ensure VBUS is re-enabled on exit
        def cleanup(sig=None, frame=None):
            self._write_sysfs("vbus_enable", "1")
            self.write_shutdown_percentage(orig_shutdown)
            if sig:
                print("\nCancelled by user, VBUS re-enabled.")
                import sys; sys.exit(0)

        for s in (signal.SIGINT, signal.SIGTERM, signal.SIGABRT):
            signal.signal(s, cleanup)

        print(f"Disabling VBUS for {test_time}s (battery: {bat_pct}%)...")
        self._write_sysfs("vbus_enable", "0")

        count = 0
        interval = 0.5
        bat_v_sum, bat_c_sum, bat_p_sum = 0.0, 0.0, 0.0
        bat_v_max, bat_c_max, bat_p_max = 0.0, 0.0, 0.0
        out_v_sum, out_c_sum, out_p_sum = 0.0, 0.0, 0.0
        out_v_max, out_c_max, out_p_max = 0.0, 0.0, 0.0
        mah_used = 0.0
        last_ts = time.time()

        t0 = time.time()
        try:
            while time.time() - t0 < test_time:
                data = self.read_all()
                bv = data["battery_voltage"]
                bc = -data["battery_current"]
                bp = bv * bc / 1e6
                ov = data["output_voltage"]
                oc = data["output_current"]
                op = ov * oc / 1e6

                dt = time.time() - last_ts
                mah_used += bc * dt / 3600.0
                last_ts = time.time()

                bat_v_sum += bv; bat_c_sum += bc; bat_p_sum += bp
                out_v_sum += ov; out_c_sum += oc; out_p_sum += op
                bat_v_max = max(bat_v_max, bv)
                bat_c_max = max(bat_c_max, bc)
                bat_p_max = max(bat_p_max, bp)
                out_v_max = max(out_v_max, ov)
                out_c_max = max(out_c_max, oc)
                out_p_max = max(out_p_max, op)
                count += 1

                elapsed = time.time() - t0
                bar = int(elapsed / test_time * 20)
                print(f"\r[{elapsed:.0f}s] {'#'*bar}{'.'*(20-bar)} {bv/1000:.2f}V {bc/1000:.2f}A {bp:.2f}W", end="", flush=True)
                time.sleep(max(0, interval - (time.time() - t0 - elapsed)))
        finally:
            cleanup()

        avg = lambda s, n: round(s / n, 3) if n else 0
        bat_pct_end = self.read_battery_percentage()
        available_pct = bat_pct_end - orig_shutdown
        if available_pct < 0:
            available_pct = 0
        avail_cap = available_pct * self.BAT_MAX_CAPACITY / 100 * 0.9
        avail_time = int(avail_cap / 1000 / max(avg(bat_c_sum, count) / 1000, 0.001) * 3600)

        result = {
            "bat_mah_used": round(mah_used, 3),
            "bat_percent_used": round(bat_pct - bat_pct_end, 1),
            "bat_voltage_avg": avg(bat_v_sum / 1000, count),
            "bat_current_avg": avg(bat_c_sum / 1000, count),
            "bat_power_avg": avg(bat_p_sum, count),
            "bat_voltage_max": round(bat_v_max / 1000, 3),
            "bat_current_max": round(bat_c_max / 1000, 3),
            "bat_power_max": round(bat_p_max, 3),
            "output_voltage_avg": avg(out_v_sum / 1000, count),
            "output_current_avg": avg(out_c_sum / 1000, count),
            "output_power_avg": avg(out_p_sum, count),
            "output_voltage_max": round(out_v_max / 1000, 3),
            "output_current_max": round(out_c_max / 1000, 3),
            "output_power_max": round(out_p_max, 3),
            "battery_percentage": bat_pct_end,
            "shutdown_percentage": orig_shutdown,
            "available_time": avail_time,
            "available_time_str": f"{avail_time // 3600}h {(avail_time % 3600) // 60}m",
            "available_bat_capacity": int(avail_cap),
        }
        print(f"\n\nResults: {mah_used:.1f}mAh used, {bat_pct_end}% remaining, ~{result['available_time_str']} runtime")
        return result
    set_buzzer_volume         = lambda self, v: self._write_sysfs("buzzer_volume", v)
    write_buzzer_volume       = set_buzzer_volume

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
