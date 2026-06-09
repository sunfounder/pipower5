""" PiPower 5 device detection, config.txt management, and health checks.
"""

__all__ = [
    'NAME', 'ID', 'VENDOR',
    'DEVICE_PATH', 'DTOVERLAY_NAME',
    'is_connected', 'check_pipower5_connected',
    'add_dtoverlay', 'remove_dtoverlay', 'has_dtoverlay',
    'doctor', 'uninstall',
]

import os
import subprocess

NAME = "PiPower 5"
ID = "pipower5"
VENDOR = "SunFounder"

DEVICE_PATH = "/sys/class/pipower5/pipower5"
MODULE_PATH = "/sys/module/pipower5"
DTOVERLAY_NAME = "sunfounder-pipower5"
POWER_SUPPLY_PATH = "/sys/class/power_supply/pipower5"

GREEN  = "\033[32m"
RED    = "\033[31m"
YELLOW = "\033[33m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

# ── Detection ───────────────────────────────────────────────────────────────

def is_connected() -> bool:
    """Check if the pipower5 kernel module is loaded."""
    return os.path.exists(MODULE_PATH)

def check_pipower5_connected():
    """Raise IOError if PiPower 5 driver is not loaded."""
    if not is_connected():
        raise IOError("PiPower 5 driver not loaded. Run 'pipower5 doctor' to diagnose.")

# ── config.txt management ───────────────────────────────────────────────────

def _find_config_txt() -> str:
    """Locate the Raspberry Pi config.txt file."""
    for p in ["/boot/firmware/config.txt", "/boot/config.txt"]:
        if os.path.isfile(p):
            return p
    return "/boot/firmware/config.txt"

def _run_command(cmd: str, timeout: int = 10) -> tuple:
    """Run a shell command, return (returncode, stdout)."""
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True,
                           text=True, timeout=timeout)
        return r.returncode, r.stdout.strip()
    except subprocess.TimeoutExpired:
        return -1, ""
    except Exception:
        return -1, ""

def has_dtoverlay() -> bool:
    """Check if dtoverlay=sunfounder-pipower5 is active in config.txt."""
    config = _find_config_txt()
    if not os.path.isfile(config):
        return False
    try:
        with open(config, "r") as f:
            for line in f:
                s = line.strip()
                if f"dtoverlay={DTOVERLAY_NAME}" in s and not s.startswith("#"):
                    return True
    except Exception:
        pass
    return False

def add_dtoverlay() -> bool:
    """Ensure dtoverlay line is active in config.txt. Creates or uncomments it."""
    config = _find_config_txt()
    if not os.path.isfile(config):
        return False
    if has_dtoverlay():
        return True
    line = f"dtoverlay={DTOVERLAY_NAME}"
    # Uncomment if commented
    rc, has = _run_command(f"grep -q '^# *{line}' {config} 2>/dev/null && echo yes || echo no")
    if has == "yes":
        _run_command(f"sudo sed -i 's/^# *{line}.*/{line}/' {config}")
    else:
        _run_command(f"echo '{line}' | sudo tee -a {config} > /dev/null 2>&1")
    return has_dtoverlay()

def remove_dtoverlay() -> bool:
    """Remove dtoverlay line from config.txt."""
    config = _find_config_txt()
    if not os.path.isfile(config):
        return False
    if not has_dtoverlay():
        return True
    _run_command(f"sudo sed -i '/^dtoverlay={DTOVERLAY_NAME}/d' {config}")
    return not has_dtoverlay()

# ── Doctor ──────────────────────────────────────────────────────────────────

def _print_section(title: str):
    print(f"\n  {BOLD}{title}{RESET}")

def _print_check(name: str, ok: bool, detail: str = ""):
    mark = f"{GREEN}✓{RESET}" if ok else f"{RED}✗{RESET}"
    msg = f"    {mark} {name}"
    if detail and not ok:
        msg += f"  → {detail}"
    print(msg)

def _check_sysfs() -> tuple:
    ok = os.path.exists(DEVICE_PATH) or os.path.exists(MODULE_PATH)
    return ok, "" if ok else "Driver not loaded or device not present. Reboot or run 'sudo modprobe pipower5'."

def _check_module_loaded() -> tuple:
    rc, out = _run_command("lsmod | grep -q pipower5 && echo yes || echo no")
    ok = (out == "yes")
    return ok, "" if ok else "pipower5 module not loaded. Run 'sudo modprobe pipower5'."

def _check_dtoverlay_config() -> tuple:
    ok = has_dtoverlay()
    return ok, "" if ok else f"dtoverlay={DTOVERLAY_NAME} not in config.txt. Run 'pipower5 doctor --fix'."

def _check_dtbo_file() -> tuple:
    for d in ["/boot/firmware/overlays", "/boot/overlays"]:
        if os.path.isfile(f"{d}/{DTOVERLAY_NAME}.dtbo"):
            return True, ""
    return False, f"{DTOVERLAY_NAME}.dtbo not found in overlays dir."

def _check_power_supply() -> tuple:
    ok = os.path.isdir(POWER_SUPPLY_PATH)
    return ok, "" if ok else "Power supply not registered. Driver may need reload."

def _check_i2c_device() -> tuple:
    rc, out = _run_command("i2cdetect -y 1 0x5c 0x5c 2>/dev/null | grep -c 5c || echo 0")
    try:
        ok = int(out.strip()) > 0
    except ValueError:
        ok = False
    return ok, "" if ok else "PiPower5 (0x5C) not found on I2C bus 1."

def doctor(fix: bool = False) -> dict:
    """Run hardware/driver health checks.

    Args:
        fix: If True, attempt to auto-repair issues (add dtoverlay, modprobe).

    Returns:
        dict with overall status and per-check results.
    """
    results = {}

    print("")
    print("=" * 55)
    print(f"  {BOLD}PiPower 5 Doctor{RESET}")
    print("=" * 55)

    _print_section("Hardware & Driver")

    checks = [
        ("I2C device (0x5C)",      _check_i2c_device),
        ("sysfs interface",        _check_sysfs),
        ("kernel module loaded",   _check_module_loaded),
        ("power_supply registered",_check_power_supply),
        ("dtoverlay in config.txt",_check_dtoverlay_config),
        ("device tree blob (.dtbo)",_check_dtbo_file),
    ]

    for name, func in checks:
        ok, detail = func()
        results[name] = ok
        _print_check(name, ok, detail)

    # ── Summary ──
    overall = all(results.values())
    results["overall"] = overall

    print("")
    if not results.get("I2C device (0x5C)", False):
        print(f"  {RED}PiPower5 not detected on I2C bus.{RESET}")
        print(f"  → Ensure the HAT is properly attached and powered.")
    elif not results.get("dtoverlay in config.txt", False):
        print(f"  {YELLOW}dtoverlay not in config.txt{RESET}")
        if fix:
            print("  → Adding dtoverlay to config.txt...")
            if add_dtoverlay():
                print(f"  {GREEN}→ dtoverlay added. Reboot to take effect.{RESET}")
            else:
                print(f"  {RED}→ Failed to add dtoverlay.{RESET}")
        else:
            print(f"  → Run: {BOLD}pipower5 doctor --fix{RESET}")
    elif not results.get("kernel module loaded", False):
        print(f"  {YELLOW}Module not loaded{RESET}")
        if fix:
            print("  → Running modprobe pipower5...")
            _run_command("sudo modprobe pipower5 2>/dev/null")
        else:
            print(f"  → Run: {BOLD}pipower5 doctor --fix{RESET}")
    elif overall:
        print(f"  {GREEN}All checks passed.{RESET}")
    else:
        print(f"  {YELLOW}Some checks failed.{RESET}")
        print(f"  → Run: {BOLD}pipower5 doctor --fix{RESET}")

    print("")
    print("=" * 55)
    print("")

    return results

# ── Uninstall ───────────────────────────────────────────────────────────────

def uninstall() -> bool:
    """Uninstall PiPower5: remove module, DKMS, overlay, config.txt entry.

    Returns:
        bool: True if successful.
    """
    import platform

    print("")
    print("=" * 60)
    print(f"  {BOLD}PiPower 5 Uninstall{RESET}")
    print("=" * 60)
    print("")

    ok = True

    # 1. Unload module
    print("  [1/5] Unloading kernel module...")
    if os.path.exists("/sys/module/pipower5"):
        _run_command("sudo rmmod pipower5 2>&1")
        if os.path.exists("/sys/module/pipower5"):
            print(f"  {RED}[FAIL]{RESET} Could not unload pipower5")
            ok = False
        else:
            print(f"  {GREEN}[OK]{RESET} pipower5 module unloaded")
    else:
        print(f"  {GREEN}[OK]{RESET} pipower5 not loaded")

    # 2. DKMS uninstall
    print("  [2/5] Removing DKMS registration...")
    _, dkms_out = _run_command("dkms status pipower5 2>/dev/null || true")
    if dkms_out.strip():
        for line in dkms_out.strip().split("\n"):
            parts = line.split("/")
            if len(parts) > 1:
                ver = parts[1].split(",")[0].strip()
                _run_command(f"sudo dkms remove -m pipower5 -v {ver} --all 2>/dev/null")
        _, after = _run_command("dkms status pipower5 2>/dev/null || true")
        if not after.strip():
            print(f"  {GREEN}[OK]{RESET} DKMS registration removed")
        else:
            print(f"  {YELLOW}[!]{RESET} DKMS may still have entries: {after.strip()}")
    else:
        print(f"  {GREEN}[OK]{RESET} Not registered with DKMS")

    # Clean DKMS source
    _run_command("sudo rm -rf /usr/src/pipower5-* 2>/dev/null")

    # 3. Remove .ko files
    print("  [3/5] Removing module files...")
    _run_command("sudo rm -f /lib/modules/*/extra/pipower5.ko* /lib/modules/*/updates/pipower5.ko* 2>/dev/null")
    _run_command("sudo depmod -a 2>/dev/null")
    print(f"  {GREEN}[OK]{RESET} Module files removed")

    # 4. Remove dtbo and config.txt entry
    print("  [4/5] Removing device tree overlay and config...")
    for d in ["/boot/firmware/overlays", "/boot/overlays"]:
        _run_command(f"sudo rm -f {d}/{DTOVERLAY_NAME}.dtbo 2>/dev/null")
    remove_dtoverlay()
    print(f"  {GREEN}[OK]{RESET} Overlay and config cleaned")

    # 5. Python package
    print("  [5/5] Uninstalling Python package...")
    _run_command("sudo /opt/pipower5/venv/bin/pip3 uninstall pipower5 -y 2>/dev/null || sudo pip3 uninstall pipower5 -y 2>/dev/null || true")
    print(f"  {GREEN}[OK]{RESET} Python package removed")

    print("")
    if ok:
        print(f"  {GREEN}Uninstall completed. Reboot to fully remove.{RESET}")
    else:
        print(f"  {YELLOW}Uninstall completed with warnings.{RESET}")
    print("")
    print("=" * 60)
    print("")

    return ok
 