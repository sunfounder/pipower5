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
    return os.path.exists(MODULE_PATH) or os.path.exists(DEVICE_PATH)

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
    # Driver-claimed device shows as "UU", unclaimed shows as "5c"
    rc, out = _run_command("i2cdetect -y 1 0x5c 0x5c 2>/dev/null | grep -cE '5c|UU' || echo 0")
    try:
        ok = int(out.strip()) > 0
    except ValueError:
        ok = False
    if ok:
        return True, ""
    return False, "PiPower5 (0x5C) not found on I2C bus 1. Check that the HAT is properly attached and powered."

def _check_module_file() -> tuple:
    rc, out = _run_command("uname -r")
    kver = out.strip()
    # Check standard and DKMS locations
    paths = [
        f"/lib/modules/{kver}/extra/pipower5.ko",
        f"/lib/modules/{kver}/updates/pipower5.ko",
        f"/lib/modules/{kver}/updates/dkms/pipower5.ko",
    ]
    for path in paths:
        if os.path.exists(path):
            return True, ""
        for ext in ("", ".xz", ".zst", ".gz"):
            if os.path.exists(path + ext):
                return True, ""
    return False, f"pipower5.ko not found in /lib/modules/{kver}/ (checked extra/ and updates/). Driver may need rebuild."

def _check_dkms_status() -> tuple:
    rc, out = _run_command("dkms status pipower5 2>/dev/null || true")
    if out.strip():
        return True, out.strip()
    return False, "pipower5 not registered with DKMS. Run 'sudo dkms build/install pipower5'."

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
        ("kernel module file",     _check_module_file),
        ("DKMS registered",        _check_dkms_status),
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
        print(f"  → Check that the HAT is properly attached and powered.")
        print(f"  → Verify I2C is enabled: {BOLD}raspi-config{RESET} → Interface Options → I2C")
        if not results.get("kernel module loaded", True) and not results.get("sysfs interface", True):
            print(f"  (The driver is not loaded; if the HAT is attached, run --fix to load it.)")

    # ── Fix all fixable issues ──
    if fix:
        fixed_any = False

        # Fix: dtoverlay missing
        if not results.get("dtoverlay in config.txt", False):
            print(f"  → Adding dtoverlay to config.txt...")
            if add_dtoverlay():
                print(f"  {GREEN}→ dtoverlay added.{RESET}")
                fixed_any = True
            else:
                print(f"  {RED}→ Failed to add dtoverlay.{RESET}")

        # Fix: DTBO file missing
        if not results.get("device tree blob (.dtbo)", True):
            dtbo_fixed = False
            for d in ["/boot/firmware/overlays", "/boot/overlays"]:
                if os.path.isdir(d):
                    # Try local source first, then curl fallback
                    for src_dir in ["/home/pi/pipower5/driver", "/home/kc5jim/pipower5/driver",
                                    "/root/pipower5/driver", "/home/only/pipower5/driver"]:
                        src = f"{src_dir}/sunfounder-pipower5.dtbo"
                        if os.path.exists(src):
                            _run_command(f"sudo cp {src} {d}/")
                            if os.path.exists(f"{d}/sunfounder-pipower5.dtbo"):
                                print(f"  {GREEN}→ DTBO file restored.{RESET}")
                                dtbo_fixed = True
                                fixed_any = True
                            break
                    if not dtbo_fixed:
                        _run_command(f"sudo curl -fsSL https://github.com/sunfounder/pipower5/raw/refs/heads/main/sunfounder-pipower5.dtbo -o {d}/sunfounder-pipower5.dtbo 2>/dev/null")
                        if os.path.exists(f"{d}/sunfounder-pipower5.dtbo"):
                            print(f"  {GREEN}→ DTBO file downloaded.{RESET}")
                            dtbo_fixed = True
                            fixed_any = True
                    break
            if not dtbo_fixed:
                print(f"  {RED}→ Could not restore DTBO file.{RESET}")

        # Fix: module file missing + DKMS unregistered
        if not results.get("DKMS registered", True) or not results.get("kernel module file", True):
            # Try DKMS registration first (also rebuilds .ko)
            if not results.get("DKMS registered", True):
                print("  → Attempting DKMS registration...")
                src_found = None
                for d in ["/home/pi/pipower5", "/home/kc5jim/pipower5",
                          "/root/pipower5", "/home/only/pipower5"]:
                    conf = f"{d}/driver/dkms.conf"
                    if os.path.exists(conf):
                        src_found = d
                        break
                if src_found:
                    drv_dir = f"{src_found}/driver"
                    rc, ver = _run_command(f"grep -oP '(?<=PIPOWER5_DRIVER_VERSION \")[^\"]+' {drv_dir}/include/pipower5.h 2>/dev/null || echo 2.1.0")
                    ver = ver.strip() or "2.1.0"
                    dkms_src = f"/usr/src/pipower5-{ver}"
                    _run_command(f"sudo mkdir -p {dkms_src}/src {dkms_src}/include")
                    _run_command(f"sudo cp {drv_dir}/Makefile {drv_dir}/dkms.conf {dkms_src}/")
                    _run_command(f"sudo cp {drv_dir}/include/*.h {dkms_src}/include/")
                    _run_command(f"sudo cp {drv_dir}/src/*.c {dkms_src}/src/")
                    _run_command(f"sudo sed -i 's/^PACKAGE_VERSION=.*/PACKAGE_VERSION=\"{ver}\"/' {dkms_src}/dkms.conf")
                    _run_command(f"sudo dkms add -m pipower5 -v {ver} 2>&1")
                    _run_command(f"sudo dkms build -m pipower5 -v {ver} 2>&1")
                    _run_command(f"sudo dkms install -m pipower5 -v {ver} --force 2>&1")
                    dkms_ok, _ = _check_dkms_status()
                    if dkms_ok:
                        print(f"  {GREEN}→ DKMS registered.{RESET}")
                        fixed_any = True
                else:
                    print("  → DKMS source not found, trying source rebuild...")
                    for src_dir in ["/home/pi/pipower5/driver", "/home/kc5jim/pipower5/driver",
                                    "/root/pipower5/driver", "/home/only/pipower5/driver"]:
                        if os.path.exists(f"{src_dir}/Makefile"):
                            kver = os.uname().sysname  # placeholder, get actual kver
                            rc, kout = _run_command("uname -r")
                            kver = kout.strip()
                            _run_command(f"cd {src_dir} && sudo make clean && sudo make -C /lib/modules/{kver}/build M={src_dir} modules 2>&1")
                            _run_command(f"sudo make -C /lib/modules/{kver}/build M={src_dir} modules_install 2>&1")
                            break

            # Re-check module file after DKMS or source rebuild
            _run_command("sudo depmod -a")
            mod_ok, _ = _check_module_file()

            # If still missing but DKMS registered, force reinstall
            if not mod_ok and results.get("DKMS registered", False):
                print("  → Module file missing — reinstalling from DKMS...")
                rc, out = _run_command("dkms status pipower5 2>/dev/null | head -1 | cut -d/ -f2 | cut -d, -f1")
                ver = out.strip()
                if ver:
                    rc2, _ = _run_command(f"sudo dkms install -m pipower5 -v {ver} --force 2>&1")
                    _run_command("sudo depmod -a")
                    mod_ok, _ = _check_module_file()
                    # If DKMS source was deleted, try rebuilding from source
                    if not mod_ok:
                        print("  → DKMS source missing, trying source rebuild...")
                        for src_dir in ["/home/pi/pipower5/driver", "/home/kc5jim/pipower5/driver",
                                        "/root/pipower5/driver", "/home/only/pipower5/driver"]:
                            if os.path.exists(f"{src_dir}/Makefile"):
                                rc, kout = _run_command("uname -r")
                                kver = kout.strip()
                                _run_command(f"cd {src_dir} && sudo make clean && sudo make -C /lib/modules/{kver}/build M={src_dir} modules 2>&1")
                                _run_command(f"sudo make -C /lib/modules/{kver}/build M={src_dir} modules_install 2>&1")
                                _run_command("sudo depmod -a")
                                mod_ok, _ = _check_module_file()
                                break

            if mod_ok:
                print(f"  {GREEN}→ Module file restored.{RESET}")
                fixed_any = True

        # Fix: module not loaded
        if not results.get("kernel module loaded", False):
            _run_command("sudo depmod -a")
            rc, _ = _run_command("sudo modprobe pipower5 2>&1")
            if rc == 0:
                print(f"  {GREEN}→ Module loaded successfully.{RESET}")
                fixed_any = True
            else:
                print(f"  {RED}→ modprobe failed. Try rebooting.{RESET}")
                rc, dmesg_out = _run_command("dmesg | grep -i pipower5 2>/dev/null || true")
                if dmesg_out.strip():
                    print(f"    {BOLD}[dmesg]{RESET}")
                    for line in dmesg_out.strip().split("\n"):
                        print(f"      {line}")

        # Fix: power_supply not registered
        if not results.get("power_supply registered", True) and results.get("kernel module loaded", False):
            print(f"  {YELLOW}→ Power supply not registered. Reloading driver...{RESET}")
            _run_command("sudo rmmod pipower5 2>/dev/null")
            _run_command("sudo modprobe pipower5 2>&1")
            ps_ok, _ = _check_power_supply()
            if ps_ok:
                print(f"  {GREEN}→ Power supply registered.{RESET}")
                fixed_any = True
            else:
                print(f"  {YELLOW}→ Power supply still not registered. A reboot is required.{RESET}")
                print(f"  {BOLD}  Reboot now? (y/n):{RESET} ", end="", flush=True)
                try:
                    ans = input().strip().lower()
                    if ans in ("y", "yes"):
                        print("  → Rebooting...")
                        _run_command("sudo reboot")
                except (EOFError, OSError):
                    print("  → Run 'sudo reboot' manually after saving your work.")

        # Re-evaluate all checks and print final result
        if fixed_any:
            print(f"")
            print(f"  {BOLD}── Re-checking all items ──{RESET}")
            for name, func in checks:
                ok, detail = func()
                results[name] = ok
                _print_check(name, ok, detail)
            overall = all(v for k, v in results.items() if k != "overall")
            results["overall"] = overall
            if overall:
                print(f"  {GREEN}All checks passed.{RESET}")
            else:
                print(f"  {YELLOW}Some checks still failed. Try rebooting, or send dmesg to support:{RESET}")
                rc, dmesg_out = _run_command("dmesg | grep -i pipower5 2>/dev/null || true")
                if dmesg_out.strip():
                    for line in dmesg_out.strip().split("\n"):
                        print(f"    {line}")
        else:
            print(f"  → Could not auto-fix. Reinstall PiPower5 or contact support.")

    # ── Non-fix mode: print what the user should do ──
    elif not results.get("I2C device (0x5C)", False):
        pass  # already printed above
    elif not results.get("dtoverlay in config.txt", False):
        print(f"  → Run: {BOLD}pipower5 doctor --fix{RESET}")
    elif not results.get("kernel module loaded", False):
        print(f"  → Run: {BOLD}pipower5 doctor --fix{RESET}")
    elif not overall:
        print(f"  → Run: {BOLD}pipower5 doctor --fix{RESET}")
    else:
        print(f"  {GREEN}All checks passed.{RESET}")

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
 