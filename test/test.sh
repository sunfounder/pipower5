#!/bin/bash
# pipower5 test suite

SYSFS=/sys/class/pipower5/pipower5
G='\033[32m'; R='\033[31m'; Y='\033[33m'; B='\033[1m'; N='\033[0m'
PASS=0; FAIL=0; SKIP=0
INT=0; [ "${1:-}" = "--full" ] && INT=1

_p() { printf '  \033[32mPASS\033[0m %s\n' "$1"; PASS=$((PASS+1)); }
_f() { printf '  \033[31mFAIL\033[0m %s - %s\n' "$1" "$2"; FAIL=$((FAIL+1)); }
_s() { printf '  \033[33mSKIP\033[0m %s - %s\n' "$1" "$2"; SKIP=$((SKIP+1)); }
_sec() { printf '\n\033[1m[%s]\033[0m %s\n' "$1" "$2"; }

if [ ! -d "$SYSFS" ]; then
  echo; echo -e "  ${R}Module NOT loaded - fix:${N}"
  echo "    cd ~/pipower5/driver && sudo make install"
  read -t 5 -r -p "  Continue? (y/N): " ans 2>/dev/null
  [ "$ans" != "y" ] && { echo "  Aborted."; exit 1; }
fi

#=== 1 ===
_sec 1 "Kernel"
lsmod | grep -q pipower5 && _p "module loaded" || _f "module loaded" "lsmod"
[ -d "$SYSFS" ] && _p "sysfs" || _f "sysfs" "not found"

#=== 2 - sysfs RO ===
_sec 2 "sysfs Read-Only"
for attr in input_voltage input_current input_power output_voltage output_current output_power \
            battery_voltage battery_current battery_power battery_percentage battery_capacity \
            power_source is_input_plugged_in is_charging firmware_version default_on board_id \
            charge_current_max driver_version power_button_state battery_internal_resistor events vbus_enable; do
  if   [ ! -f "$SYSFS/$attr" ]; then _f "$attr" "missing"
  elif val=$(cat "$SYSFS/$attr" 2>/dev/null) && [ -n "$val" ]; then _p "$attr = $val"
  else _f "$attr" "empty"; fi
done

#=== 3 - sysfs RW ===
_sec 3 "sysfs Read-Write"
_rw() {
  local a=$1 o=$2 t=$3
  [ ! -f "$SYSFS/$a" ] && { _f "$a" "missing"; return; }
  local before=$(cat "$SYSFS/$a" 2>/dev/null)
  echo "$t" > "$SYSFS/$a" 2>/dev/null || { _f "$a write" "perm"; return; }
  local after=$(cat "$SYSFS/$a" 2>/dev/null)
  echo "$o" > "$SYSFS/$a" 2>/dev/null || { _f "$a restore" "perm"; return; }
  local restored=$(cat "$SYSFS/$a" 2>/dev/null)
  _p "$a: $before -> $t -> $after -> $restored"
}
ov=$(cat $SYSFS/buzzer_volume 2>/dev/null || echo 3)
os=$(cat $SYSFS/shutdown_percentage 2>/dev/null || echo 10)
ob=$(cat $SYSFS/buzz_on 2>/dev/null || echo 0x7F)
_rw buzzer_volume "$ov" $(( (ov % 10) + 1 ))
_rw shutdown_percentage "$os" $(( (os % 90) + 10 ))
_rw buzz_on "$ob" "0x3F"
echo 0 > "$SYSFS/buzzer_play" 2>/dev/null && _p "buzzer_play stop" || _f "buzzer_play" "perm"
echo 0 > "$SYSFS/power_button_state" 2>/dev/null && _p "power_button_state reset" || _f "power_button_state" "perm"

#=== 4 - UPower ===
_sec 4 "UPower"
if command -v upower >/dev/null 2>&1; then
  U=$(upower -i /org/freedesktop/UPower/devices/battery_pipower5 2>/dev/null)
  for f in percentage state energy-full voltage technology vendor model; do
    echo "$U" | grep -qi "$f" && _p "UPower $f" || _f "UPower $f" "missing"
  done
else _s "UPower" "not installed"; fi

#=== 5 - Button ===
_sec 5 "Button"
BTN=$(grep -l pipower5-power-button /sys/class/input/*/name 2>/dev/null | head -1)
[ -n "$BTN" ] && _p "input: $(basename $(dirname $BTN))" || _f "input" "not found"

#=== 6 - dmesg ===
_sec 6 "dmesg"
N=$(dmesg 2>/dev/null | grep -ci pipower5 || echo 0)
[ "$N" -gt 0 ] && _p "dmesg: $N entries" || _f "dmesg" "empty"

#=== 7 - CLI commands ===
_sec 7 "CLI Commands"
for cmd in info status; do
  pipower5 "$cmd" >/dev/null 2>&1 && _p "pipower5 $cmd" || _f "pipower5 $cmd" "failed"
done
pipower5 --config >/dev/null 2>&1  && _p "pipower5 --config"  || _f "pipower5 --config" "failed"
pipower5 --version >/dev/null 2>&1 && _p "pipower5 --version" || _f "pipower5 --version" "failed"

#=== 8 - CLI --all ===
_sec 8 "CLI --all"
OUT=$(pipower5 --all 2>/dev/null)
for s in "Input:" "Output:" "Battery:" "Internal:" "Versions:"; do
  echo "$OUT" | grep -q "$s" && _p "--all: $s" || _f "--all: $s" "missing"
done

#=== 9 - CLI sensor flags ===
_sec 9 "CLI Sensor Flags"
for f in -iv -ic -ov -oc -bv -bc -bp -bs -ii -ichg -do -pb -cc -fv -dv -sp -bzv -bzo; do
  pipower5 "$f" >/dev/null 2>&1 && _p "$f" || _f "$f" "failed"
done
pipower5 --shutdown-percentage 10 >/dev/null 2>&1 && _p "--shutdown-percentage 10" || _f "--shutdown-percentage 10" "failed"
pipower5 --buzzer-volume 3       >/dev/null 2>&1 && _p "--buzzer-volume 3"       || _f "--buzzer-volume 3" "failed"
pipower5 --buzz-on 0x7F          >/dev/null 2>&1 && _p "--buzz-on 0x7F"          || _f "--buzz-on 0x7F" "failed"
pipower5 --buzzer-test 0         >/dev/null 2>&1 && _p "--buzzer-test 0 (stop)"   || _f "--buzzer-test 0" "failed"

#=== 10 - CLI email/SMTP ===
_sec 10 "CLI Email/SMTP"
for f in --send-email-on --send-email-to --smtp-server --smtp-port --smtp-email --smtp-password --smtp-security; do
  pipower5 "$f" 2>/dev/null | grep -q . && _p "$f (read)" || _s "$f" "no config"
done

#=== 11 - CLI other ===
_sec 11 "CLI Other"
pipower5 --temperature-unit >/dev/null 2>&1 && _p "--temperature-unit"      || _f "--temperature-unit" "failed"
pipower5 --debug-level info  >/dev/null 2>&1 && _p "--debug-level info"     || _f "--debug-level" "failed"

#=== 12 - CLI doctor ===
_sec 12 "CLI doctor"
pipower5 doctor 2>&1 | grep -qE 'Doctor|All checks|overall' \
  && _p "pipower5 doctor" || _f "pipower5 doctor" "failed"

#=== Interactive ===
if [ $INT -eq 1 ]; then
  echo; echo "=== Interactive Tests ==="
  echo; echo ">>> TEST 1: Buzzer"
  echo "    Playing 440Hz for 1s..."
  echo "440,1000" > "$SYSFS/buzzer_play" 2>/dev/null
  read -r -p "    Did you hear a beep? (y/n): " ans
  [ "$ans" = "y" ] && _p "buzzer: audible" || _f "buzzer: no sound" "check HW"

  echo; echo ">>> TEST 2: Button Press"
  echo "    Press power button ONCE within 10s."
  echo "    Type q + Enter to skip."
  echo "    Polling every 200ms..."
  FOUND=0
  for i in $(seq 1 50); do
    STATE=$(cat "$SYSFS/power_button_state" 2>/dev/null || echo 0)
    if [ "$STATE" != "0" ]; then
      _p "button: detected (state=$STATE)"
      FOUND=1; break
    fi
    read -t 0.2 -r ans 2>/dev/null
    [ "$ans" = "q" ] && break
  done
  [ "$FOUND" = "0" ] && _f "button: no press" "timeout/skipped"

  echo; echo ">>> TEST 3: Desktop Battery Icon"
  read -r -p "    Does taskbar show battery? (y/n): " ans
  [ "$ans" = "y" ] && _p "desktop: icon OK" || _f "desktop: icon missing" "check DE"

  echo; echo ">>> TEST 4: CLI --buzzer-test"
  pipower5 --buzzer-test 440 2>/dev/null &
  read -r -p "    Did you hear a tone? (y/n): " ans
  [ "$ans" = "y" ] && _p "CLI --buzzer-test OK" || _f "CLI --buzzer-test: no sound" "check HW"

  echo; echo "=== Interactive done ==="
fi

#=== Summary ===
echo
echo "========================================"
printf "  Results: %d passed, %d failed, %d skipped\n" $PASS $FAIL $SKIP
echo "========================================"
echo
exit $FAIL
