"""Unit tests for pipower5 doctor and CLI dispatch logic.

Uses unittest.mock to simulate driver states without real hardware.

Run from repo root:
    python -m pipower5.test.test_doctor

Or run directly:
    python pipower5/test/test_doctor.py
"""

import unittest
from unittest.mock import patch, MagicMock, DEFAULT
import sys
import os
import importlib.util

# ════════════════════════════════════════════════════════════════════════
#  Bootstrap: load the REAL pipower5 package from the inner directory
#  pipower5/pipower5/ (NOT the outer namespace-only shell)
# ════════════════════════════════════════════════════════════════════════

_HERE = os.path.dirname(os.path.abspath(__file__))
_INNER_PKG = os.path.normpath(os.path.join(_HERE, "..", "pipower5"))  # .../pipower5/pipower5


def _load_mod(name, path):
    """Load a module from a file path and register in sys.modules."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None:
        raise ImportError(f"No spec for {name} at {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# Load in dependency order: version → device → pipower5 → __init__
_ver  = _load_mod("pipower5.version",   os.path.join(_INNER_PKG, "version.py"))
_dev  = _load_mod("pipower5.device",    os.path.join(_INNER_PKG, "device.py"))
_p5   = _load_mod("pipower5.pipower5",  os.path.join(_INNER_PKG, "pipower5.py"))
_init = _load_mod("pipower5",           os.path.join(_INNER_PKG, "__init__.py"))

# Re-export symbols the tests need
import pipower5
import pipower5.device as device
from pipower5.device import doctor, is_connected, DEVICE_PATH, MODULE_PATH

# Help pytest / unittest discover find these as top-level names
__all__ = ["TestDoctor", "TestIsConnected", "TestMainDispatch"]


# ════════════════════════════════════════════════════════════════════════
#  Helper factories for mock side-effects
# ════════════════════════════════════════════════════════════════════════

def mock_run_cmd(i2c_found=True, module_loaded=True):
    """Return a callable that simulates device._run_command()."""
    def side_effect(cmd, timeout=10):
        if "i2cdetect" in cmd:
            return (0, "1" if i2c_found else "0")
        if "lsmod" in cmd:
            return (0, "yes" if module_loaded else "no")
        return (0, "")
    return side_effect


PATH_ALWAYS = {
    "/boot", "/boot/firmware", "/boot/firmware/overlays", "/boot/overlays",
}


def _path_set(sysfs=True, module=True, power_supply=True,
              dtbo=True, config_txt=True):
    s = set(PATH_ALWAYS)
    if sysfs:        s.add(DEVICE_PATH)
    if module:       s.add(MODULE_PATH)
    if power_supply: s.add("/sys/class/power_supply/pipower5")
    if dtbo:         s.add("/boot/firmware/overlays/sunfounder-pipower5.dtbo")
    if config_txt:   s.add("/boot/firmware/config.txt")
    return s


def mock_os_path(s: set):
    """Return a side_effect suitable for os.path.exists / isdir / isfile."""
    return lambda p: p in s


# ════════════════════════════════════════════════════════════════════════
#  TestDoctor
# ════════════════════════════════════════════════════════════════════════

class TestDoctor(unittest.TestCase):
    """Each test creates a specific driver state and checks doctor()."""

    def _doctor(self, *, config_txt_lines=None, **kwargs):
        """Run doctor() with mocked os.path and _run_command.

        Parameters (all bool, default True):
            sysfs, module, power_supply, dtbo, config_txt
            i2c, module_loaded

        config_txt_lines: list of lines to mock as config.txt content.
                          Default = ``["dtoverlay=sunfounder-pipower5\n"]``
        """
        ps = _path_set(
            sysfs=kwargs.get("sysfs", True),
            module=kwargs.get("module", True),
            power_supply=kwargs.get("power_supply", True),
            dtbo=kwargs.get("dtbo", True),
            config_txt=kwargs.get("config_txt", True),
        )
        path_side = mock_os_path(ps)
        cmd_side = mock_run_cmd(
            i2c_found=kwargs.get("i2c", True),
            module_loaded=kwargs.get("module_loaded", True),
        )

        # Config.txt content — default has dtoverlay, caller can override
        ctl = config_txt_lines
        if ctl is None:
            ctl = ["dtoverlay=sunfounder-pipower5\n"]

        mock_file = MagicMock()
        mock_file.__enter__.return_value = mock_file
        mock_file.__iter__.return_value = iter(ctl)

        with patch.object(os.path, "exists",  side_effect=path_side), \
             patch.object(os.path, "isfile",  side_effect=path_side), \
             patch.object(os.path, "isdir",   side_effect=path_side), \
             patch("pipower5.device._run_command", side_effect=cmd_side), \
             patch("builtins.open", return_value=mock_file), \
             patch("builtins.print"):
            return doctor(fix=kwargs.get("fix", False))

    # ── Happy path ────────────────────────────────────────────────────

    def test_all_pass(self):
        r = self._doctor()
        self.assertTrue(r["overall"])
        for key in ("I2C device (0x5C)", "sysfs interface",
                    "kernel module loaded", "power_supply registered",
                    "dtoverlay in config.txt", "device tree blob (.dtbo)"):
            with self.subTest(check=key):
                self.assertTrue(r[key])

    # ── Failures ──────────────────────────────────────────────────────

    def test_no_driver(self):
        r = self._doctor(sysfs=False, module=False, power_supply=False,
                         module_loaded=False)
        self.assertFalse(r["overall"])
        self.assertFalse(r["sysfs interface"])
        self.assertFalse(r["kernel module loaded"])
        self.assertFalse(r["power_supply registered"])

    def test_no_dtoverlay_config(self):
        r = self._doctor(config_txt_lines=[
            "# Config\n", "arm_64bit=1\n",
        ])
        self.assertFalse(r["dtoverlay in config.txt"])
        self.assertFalse(r["overall"])
        self.assertTrue(r["kernel module loaded"])
        self.assertTrue(r["device tree blob (.dtbo)"])

    def test_dtbo_missing(self):
        r = self._doctor(dtbo=False)
        self.assertFalse(r["device tree blob (.dtbo)"])
        self.assertFalse(r["overall"])
        self.assertTrue(r["dtoverlay in config.txt"])

    def test_i2c_missing(self):
        r = self._doctor(i2c=False)
        self.assertFalse(r["I2C device (0x5C)"])
        self.assertFalse(r["overall"])

    def test_config_txt_absent(self):
        r = self._doctor(config_txt=False, config_txt_lines=[])
        self.assertFalse(r["dtoverlay in config.txt"])
        self.assertFalse(r["overall"])

    # ── Edge cases ────────────────────────────────────────────────────

    def test_module_loaded_no_sysfs(self):
        """lsmod shows module but /sys paths are missing."""
        r = self._doctor(sysfs=False, module=True,
                         power_supply=False, module_loaded=True)
        self.assertTrue(r["kernel module loaded"])
        # sysfs interface checks DEVICE_PATH OR MODULE_PATH — module path exists
        self.assertTrue(r["sysfs interface"])
        self.assertFalse(r["power_supply registered"])
        self.assertFalse(r["overall"])

    def test_fix_no_dtoverlay(self):
        """"doctor --fix" runs without crash when dtoverlay missing."""
        r = self._doctor(fix=True, config_txt_lines=[
            "# Config\n", "arm_64bit=1\n",
        ])
        self.assertFalse(r["dtoverlay in config.txt"])


# ════════════════════════════════════════════════════════════════════════
#  TestIsConnected
# ════════════════════════════════════════════════════════════════════════

class TestIsConnected(unittest.TestCase):
    """Low-level is_connected() — the PiPower5() gate."""

    @patch.object(os.path, "exists", return_value=True)
    def test_true_when_module_exists(self, _):
        self.assertTrue(is_connected())

    @patch.object(os.path, "exists", return_value=False)
    def test_false_when_nothing_exists(self, _):
        self.assertFalse(is_connected())

    @patch.object(os.path, "exists")
    def test_true_when_only_sysfs(self, m):
        m.side_effect = lambda p: p == DEVICE_PATH
        self.assertTrue(is_connected())


# ════════════════════════════════════════════════════════════════════════
#  TestMainDispatch — entry-point routing
# ════════════════════════════════════════════════════════════════════════

class TestMainDispatch(unittest.TestCase):
    """CLI routing: commands that don't need HW must work without it.

    We use the *already-loaded* pipower5 module (from the inner package)
    instead of re-importing, which would hit the namespace-package trap.
    Patches target ``pipower5.device.*`` — since pipower5.device is
    already in sys.modules, the patch resolves correctly.
    """

    def setUp(self):
        self._argv = list(sys.argv)

    def tearDown(self):
        sys.argv = self._argv

    # ── doctor ─────────────────────────────────────────────────────────

    @patch("pipower5.device.doctor")
    def test_doctor(self, mock_doctor):
        """doctor runs even when driver not loaded."""
        sys.argv = ["pipower5", "doctor"]
        with patch("builtins.print"):
            with self.assertRaises(SystemExit):
                pipower5.main()
        mock_doctor.assert_called_once_with(fix=False)

    @patch("pipower5.device.doctor")
    def test_doctor_fix(self, mock_doctor):
        """doctor --fix passes fix=True."""
        sys.argv = ["pipower5", "doctor", "--fix"]
        with patch("builtins.print"):
            with self.assertRaises(SystemExit):
                pipower5.main()
        mock_doctor.assert_called_once_with(fix=True)

    # ── version ────────────────────────────────────────────────────────

    def test_version(self):
        """-v works without driver."""
        sys.argv = ["pipower5", "-v"]
        with patch("builtins.print") as p:
            with self.assertRaises(SystemExit):
                pipower5.main()
        calls = "".join(str(c) for c in p.call_args_list)
        self.assertIn("2.", calls)

    # ── config ─────────────────────────────────────────────────────────

    def test_config(self):
        """--config works without driver."""
        sys.argv = ["pipower5", "--config"]
        with patch("builtins.print"):
            with self.assertRaises(SystemExit):
                pipower5.main()

    # ── uninstall ──────────────────────────────────────────────────────

    @patch("pipower5.device.uninstall")
    def test_uninstall(self, mock_uninstall):
        """uninstall works without driver."""
        sys.argv = ["pipower5", "uninstall"]
        with patch("builtins.print"):
            with self.assertRaises(SystemExit):
                pipower5.main()
        mock_uninstall.assert_called_once()

    # ── status / info — legitimately crash without driver ──────────────

    def test_status_crashes_without_driver(self):
        """status crashes when driver not loaded (expected)."""
        sys.argv = ["pipower5", "status"]
        with patch("builtins.print"):
            with self.assertRaises(IOError):
                pipower5.main()

    def test_info_crashes_without_driver(self):
        """info crashes when driver not loaded (expected)."""
        sys.argv = ["pipower5", "info"]
        with patch("builtins.print"):
            with self.assertRaises(IOError):
                pipower5.main()


if __name__ == "__main__":
    unittest.main(verbosity=1)
