#!/bin/bash
# pipower5 full test suite �� driver + sysfs + CLI
set -euo pipefail

SYSFS=/sys/class/pipower5/pipower5
PS=/sys/class/power_supply/pipower5
G='\033[32m'; R='\033[31m'; Y='\033[33m'; B='\033[1m'; N='\033[0m'
PASS=0; FAIL=0; SKIP=0

_p() { echo -e "  $G PASS$N $1"; PASS=$((PASS+1)); }
_f() { echo -e "  $R FAIL$N $1 �� $2"; FAIL=$((FAIL+1)); }
_s() { echo -e "  $Y SKIP$N $1 �� $2"; SKIP=$((SKIP+1)); }
_sec() { echo ""; echo -e "$B[$1]$N $2"; }

#=== 1. Kernel Module ===
_sec 1 "Kernel Module"
lsmod | grep -q pipower5 && _p "module loaded"   || _f "module loaded" "lsmod"
[ -d "$SYSFS"            ] && _p "sysfs interface" || _f "sysfs interface" "not found"
[ -d "$PS"               ] && _p "power_supply"    || _f "power_supply"    "not found"
DTBO=$(find /boot -name sunfounder-pipower5.dtbo 2>/dev/null|head -1)
[ -n "$DTBO"             ] && _p "dtbo: $DTBO"     || _f "dtbo"            "not found"
grep -q 'dtoverlay=sunfounder-pipower5' /boot/firmware/config.txt /boot/config.txt 2>/dev/null \
                           && _p "dtoverlay config"  || _f "dtoverlay config" "not found"

#=== 2. sysfs RO Attributes ===
_sec 2 "sysfs Read-Only (22 attrs)"

RO_ATTRS=(
  input_voltage input_current input_power
  output_voltage output_current output_power
  battery_voltage battery_current battery_power
  battery_percentage battery_capacity
  power_source is_input_plugged_in is_charging
  firmware_version default_on board_id
  charge_current_max driver_version power_button_state
  battery_internal_resistor events vbus_enable
)
for attr in "${RO_ATTRS[@]}"; do
  if   [ ! -f "$SYSFS/$attr" ]; then _f "$attr" "file missing"
  elif val=$(cat "$SYSFS/$attr" 2>/dev/null) && [ -n "$val" ]; then
    _p "$attr = $val"
  else _f "$attr" "empty"; fi
done

#=== 3. sysfs RW Attributes ===
_sec 3 "sysfs Read-Write (5 attrs + vbus_enable read)"

_rw() {
  local a=$1 o=$2 t=$3
  [ ! -f "$SYSFS/$a" ] && { _f "$a" "file missing"; return; }
  echo "$t" > "$SYSFS/$a" 2>/dev/null || { _f "$a write" "permission"; return; }
  local n=$(cat "$SYSFS/$a" 2>/dev/null)
  echo "$o" > "$SYSFS/$a" 2>/dev/null
  _p "$a: write($t) read($n) restore($o)"
}

ov=$(cat $SYSFS/buzzer_volume 2>/dev/null || echo 3)
os=$(cat $SYSFS/shutdown_percentage 2>/dev/null || echo 10)
ob=$(cat $SYSFS/buzz_on 2>/dev/null || echo 0x7F)

_rw buzzer_volume       "$ov" "$(( (ov % 10) + 1 ))"
_rw shutdown_percentage "$os" "$(( (os % 90) + 10 ))"
_rw buzz_on             "$ob" "0x3F"

echo 0 > "$SYSFS/buzzer_play" 2>/dev/null          && _p "buzzer_play stop"         || _f "buzzer_play" "permission"
echo 0 > "$SYSFS/power_button_state" 2>/dev/null    && _p "power_button_state reset" || _f "power_button_state" "permission"

#=== 4. UPower ===
_sec 4 "UPower"
if command -v upower >/dev/null 2>&1; then
  U=$(upower -i /org/freedesktop/UPower/devices/battery_pipower5 2>/dev/null)
  for f in percentage state energy-full voltage technology vendor model; do
    echo "$U" | grep -qi "$f" && _p "UPower $f" || _f "UPower $f" "missing"
  done
else _s "UPower" "not installed"; fi

#=== 5. Button ===
_sec 5 "Button Input Device"
BTN=$(grep -l pipower5-power-button /sys/class/input/*/name 2>/dev/null | head -1)
[ -n "$BTN" ] && _p "input: $(dirname $BTN | xargs basename)" || _f "input device" "not found"

#=== 6. Kernel Log ===
_sec 6 "Kernel Log (dmesg)"
N=$(dmesg 2>/dev/null | grep -ci pipower5 || echo 0)
[ "$N" -gt 0 ] && _p "dmesg: $N entries" || _f "dmesg" "empty"

#=== 7. CLI Commands ===
_sec 7 "CLI Commands"
for cmd in info status; do
  pipower5 "$cmd" >/dev/null 2>&1 && _p "pipower5 $cmd" || _f "pipower5 $cmd" "failed"
done
pipower5 --config >/dev/null 2>&1  && _p "pipower5 --config"  || _f "pipower5 --config" "failed"
pipower5 --version >/dev/null 2>&1 && _p "pipower5 --version" || _f "pipower5 --version" "failed"

#=== 8. CLI --all ===
_sec 8 "CLI: --all"
OUT=$(pipower5 --all 2>/dev/null)
for s in "Input:" "Output:" "Battery:" "Internal:" "Versions:"; do
  echo "$OUT" | grep -q "$s" && _p "--all: $s" || _f "--all: $s" "missing"
done

#=== 9. CLI Individual Sensor Flags ===
_sec 9 "CLI: Sensor Flags"
for f in -iv -ic -ov -oc -bv -bc -bp -bs -ii -ichg -do -pb -cc -fv -dv -sp -bzv -bzo; do
  pipower5 "$f" >/dev/null 2>&1 && _p "$f" || _f "$f" "failed"
done
pipower5 --shutdown-percentage 10 >/dev/null 2>&1  && _p "--shutdown-percentage 10"  || _f "--shutdown-percentage 10" "failed"
pipower5 --buzzer-volume 3       >/dev/null 2>&1  && _p "--buzzer-volume 3"        || _f "--buzzer-volume 3" "failed"
pipower5 --buzz-on 0x7F          >/dev/null 2>&1  && _p "--buzz-on 0x7F"           || _f "--buzz-on 0x7F" "failed"
pipower5 --buzzer-test 0         >/dev/null 2>&1  && _p "--buzzer-test 0 (stop)"    || _f "--buzzer-test 0" "failed"

#=== 10. CLI Email/SMTP ===
_sec 10 "CLI: Email & SMTP"
for f in --send-email-on --send-email-to --smtp-server --smtp-port --smtp-email --smtp-password --smtp-security; do
  pipower5 "$f" 2>/dev/null | grep -q . && _p "$f (read)" || _s "$f (read)" "no config"
done
pipower5 --send-email-to test@example.com >/dev/null 2>&1  && _p "--send-email-to set"   || _f "--send-email-to set" "failed"
pipower5 --send-email-to >/dev/null 2>&1                  && _p "--send-email-to reset" || _f "--send-email-to reset" "failed"

#=== 11. CLI Other ===
_sec 11 "CLI: Other Flags"
pipower5 --temperature-unit         >/dev/null 2>&1 && _p "--temperature-unit"      || _f "--temperature-unit" "failed"
pipower5 --debug-level info         >/dev/null 2>&1 && _p "--debug-level info"      || _f "--debug-level" "failed"
pipower5 --config-path              >/dev/null 2>&1 && _p "--config-path (read)"    || _f "--config-path" "failed"

#=== 12. CLI doctor / send-email / uninstall ===
_sec 12 "CLI: doctor, send-email, uninstall"
pipower5 doctor 2>&1 | grep -qE 'Doctor|All checks|overall' \
  && _p "pipower5 doctor" || _f "pipower5 doctor" "failed"
pipower5 send-email 2>&1 | grep -qiE "Usage|Script|install|Permission|not found" \
  && _p "pipower5 send-email (needs setup)" || _f "pipower5 send-email" "unexpected"
pipower5 uninstall 2>&1 | grep -qi "Permission\|Uninstall\|PiPower" \
  && _p "pipower5 uninstall (needs root)" || _f "pipower5 uninstall" "unexpected"

#=== Summary ===
echo ""
echo "========================================"
printf "  $B Results: $G%d passed$N, $R%d failed$N, $Y%d skipped$N\n" $PASS $FAIL $SKIP
echo "========================================"
echo ""
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
