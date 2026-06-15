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
    @classmethod
    def _try_read_sysfs_int(cls, name, default=0):
        try:
            return int(cls._read_sysfs(name))
        except (FileNotFoundError, ValueError):
            return default

    read_shutdown_request    = lambda self: ShutdownRequest(
        self._try_read_sysfs_int("shutdown_request", 0))

    # ---- Write operations ----

    write_shutdown_percentage = lambda self, v: self._write_sysfs("shutdown_percentage", v)
    set_buzzer_volume         = lambda self, v: self._write_sysfs("buzzer_volume", v)

    BUZZ_EVENT_BIT = {
        "battery_activated":                 0x01,
        "low_battery":                       0x02,
        "power_disconnected":                0x04,
        "power_restored":                    0x08,
        "power_insufficient":                0x10,
        "battery_critical_shutdown":         0x20,
        "battery_voltage_critical_shutdown": 0x40,
    }

    @classmethod
    def _events_to_bitmask(cls, events):
        mask = 0
        for e in events:
            mask |= cls.BUZZ_EVENT_BIT.get(e, 0)
        return mask

    @classmethod
    def _bitmask_to_events(cls, mask):
        return [e for e, b in cls.BUZZ_EVENT_BIT.items() if mask & b]

    def set_buzz_on(self, events):
        """Write buzz_on bitmask to kernel driver. events is a list of event name strings.
        Kernel filters per-event by bit position."""
        mask = self._events_to_bitmask(events)
        self._write_sysfs("buzz_on", f"0x{mask:02X}")
        return mask

    def get_buzz_on(self):
        """Read current buzz_on bitmask from kernel. Returns int."""
        raw = self._read_sysfs("buzz_on")
        return int(raw, 16) if raw.startswith("0x") else int(raw)

    def test_smtp(self, config):
        """Test SMTP connection and send a test email. Returns (bool, message)."""
        try:
            from .email_sender import EmailSender
            sender = EmailSender(config)
            if not sender.is_ready():
                return False, "SMTP settings incomplete"
            sender.connect()
            # Send a test email with real hardware data
            import time
            bat_pct = self.read_battery_percentage()
            bat_cur = self.read_battery_current()
            is_plugged = self.read_is_input_plugged_in()
            is_charging = self.read_is_charging()
            test_data = {
                'device_name': 'PiPower5',
                'battery_percentage': f'{bat_pct}%',
                'battery_voltage': f'{self.read_battery_voltage() / 1000:.1f}V',
                'shutdown_percentage': f'{self.read_shutdown_percentage()}%',
                'battery_current_output': f'{bat_cur}mA',
                'estimated_time': 'N/A',
                'switch_time': time.strftime('%Y-%m-%d %H:%M:%S'),
                'input_status': 'Plugged In' if is_plugged else 'Unplugged',
                'charging_status': 'Charging' if is_charging else ('Not Charging' if is_plugged else 'N/A (on battery)'),
            }
            result = sender.send_preset_email('test', test_data)
            if result is not True:
                return False, f"Connection OK but send failed: {result}"
            return True, "Test email sent"
        except Exception as e:
            return False, str(e)

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
        Writes progress/results to /opt/pipower5/blackout_simulation.*
        for dashboard compatibility.
        """
        import json, time, os

        OUT_DIR = "/opt/pipower5"
        LOCK = f"{OUT_DIR}/blackout_simulation.lock"
        JSON = f"{OUT_DIR}/blackout_simulation.json"
        os.makedirs(OUT_DIR, exist_ok=True)

        # Write lock file to signal test in progress
        with open(LOCK, "w") as f:
            f.write(f"{test_time}")

        # Start the test via sysfs
        self._write_sysfs("power_failure_test", str(test_time))

        last_progress = -1
        while True:
            status = self._read_sysfs("power_failure_test")
            if status.startswith("done "):
                result = json.loads(status[5:])
                bat_v_avg = result["bat_voltage_avg"] / 1000.0
                bat_c_avg = result["bat_current_avg"] / 1000.0
                delta_mah = result["delta_mah"] / 1000.0
                est_runtime = result["estimated_runtime_s"]
                est_h = est_runtime // 3600
                est_m = (est_runtime % 3600) // 60

                print(f"\nResults: {delta_mah:.1f}mAh used, "
                      f"avg {bat_v_avg:.2f}V {bat_c_avg:.2f}A, "
                      f"~{est_h}h{est_m}m runtime")

                output = {
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
                # Write JSON for dashboard
                with open(JSON, "w") as f:
                    json.dump(output, f, indent=2)
                # Remove lock
                if os.path.exists(LOCK):
                    os.remove(LOCK)
                return output
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
                if os.path.exists(LOCK):
                    os.remove(LOCK)
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
