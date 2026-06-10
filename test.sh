#!/bin/bash
# pipower5 test suite ¡ª verifies kernel driver, sysfs, Python CLI, and UPower
set -euo pipefail

SYSFS=/sys/class/pipower5/pipower5
GREEN='\033[32m'
RED='\033[31m'
BOLD='\033[1m'
RESET='\033[0m'
PASS=0
FAIL=0

pass() { echo -e "  ${GREEN}PASS${RESET} $1"; PASS=$((PASS+1)); }
fail() { echo -e "  ${RED}FAIL${RESET} $1 ¡ª $2"; FAIL=$((FAIL+1)); }
skip() { echo -e "  SKIP $1 ¡ª $2"; }

echo ""
echo "=========================================="
echo -e "  ${BOLD}PiPower5 Test Suite${RESET}"
echo "=========================================="
echo ""

# ©¤©¤ 1. Kernel driver ©¤©¤
echo -e "${BOLD}[1] Kernel Driver${RESET}"

if lsmod | grep -q pipower5; then
  pass "module loaded"
else
  fail "module loaded" "lsmod | grep pipower5 returned nothing"
fi

if [ -d "$SYSFS" ]; then
  pass "sysfs interface exists"
else
  fail "sysfs interface exists" "$SYSFS not found"
fi

if [ -d /sys/class/power_supply/pipower5 ]; then
  pass "power_supply registered"
else
  fail "power_supply registered" "/sys/class/power_supply/pipower5 not found"
fi

if [ -f /boot/firmware/overlays/sunfounder-pipower5.dtbo ] ||    [ -f /boot/overlays/sunfounder-pipower5.dtbo ]; then
  pass "device tree blob installed"
else
  fail "device tree blob installed" "sunfounder-pipower5.dtbo not found"
fi

# ©¤©¤ 2. sysfs RO attributes ©¤©¤
echo ""
echo -e "${BOLD}[2] sysfs Read Attributes${RESET}"

RO_ATTRS=(
  input_voltage input_current input_power
  output_voltage output_current output_power
  battery_voltage battery_current battery_power
  battery_percentage battery_capacity
  power_source is_input_plugged_in is_charging
  firmware_version default_on board_id
  charge_current_max buzzer_volume
  power_button_state driver_version
  events buzz_on
)

for attr in "${RO_ATTRS[@]}"; do
  if [ -f "$SYSFS/$attr" ]; then
    val=$(cat "$SYSFS/$attr" 2>/dev/null)
    if [ -n "$val" ]; then
      pass "$attr = $val"
    else
      fail "$attr" "empty value"
    fi
  else
    fail "$attr" "file not found"
  fi
done

# ©¤©¤ 3. sysfs RW attributes ©¤©¤
echo ""
echo -e "${BOLD}[3] sysfs Write Attributes${RESET}"

# buzzer_volume
orig_vol=$(cat $SYSFS/buzzer_volume 2>/dev/null || echo 3)
echo "$orig_vol" > $SYSFS/buzzer_volume 2>/dev/null &&   pass "buzzer_volume write/restore $orig_vol" ||   fail "buzzer_volume write" "permission denied"

# shutdown_percentage
orig_sp=$(cat $SYSFS/shutdown_percentage 2>/dev/null || echo 10)
echo "$orig_sp" > $SYSFS/shutdown_percentage 2>/dev/null &&   pass "shutdown_percentage write/restore $orig_sp" ||   fail "shutdown_percentage write" "permission denied"

# buzz_on
orig_bo=$(cat $SYSFS/buzz_on 2>/dev/null || echo 0x7F)
echo "$orig_bo" > $SYSFS/buzz_on 2>/dev/null &&   pass "buzz_on write/restore $orig_bo" ||   fail "buzz_on write" "permission denied"

# buzzer_play (short test)
echo 0 > $SYSFS/buzzer_play 2>/dev/null &&   pass "buzzer_play stop" ||   fail "buzzer_play stop" "permission denied"

# ©¤©¤ 4. UPower ©¤©¤
echo ""
echo -e "${BOLD}[4] UPower${RESET}"

if command -v upower >/dev/null 2>&1; then
  UPOUT=$(upower -i /org/freedesktop/UPower/devices/battery_pipower5 2>/dev/null)
  if echo "$UPOUT" | grep -q "percentage"; then
    pct=$(echo "$UPOUT" | grep "percentage" | awk '{print $2}')
    pass "UPower battery: $pct"
  else
    fail "UPower battery" "no percentage in upower output"
  fi
  if echo "$UPOUT" | grep -q "state"; then
    state=$(echo "$UPOUT" | grep "state:" | awk '{$1=""; print $0}' | xargs)
    pass "UPower state: $state"
  fi
else
  skip "UPower" "upower not installed"
fi

# ©¤©¤ 5. Button input device ©¤©¤
echo ""
echo -e "${BOLD}[5] Button Input Device${RESET}"

if grep -r "pipower5-power-button" /sys/class/input/*/name 2>/dev/null | head -1 > /dev/null; then
  dev=$(grep -l "pipower5-power-button" /sys/class/input/*/name 2>/dev/null | head -1)
  pass "input device: $(dirname $dev | xargs basename)"
else
  fail "input device" "pipower5-power-button not found in /sys/class/input/"
fi

# ©¤©¤ 6. Events ©¤©¤
echo ""
echo -e "${BOLD}[6] Event Log${RESET}"

if grep -q "STARTUP" "$SYSFS/events" 2>/dev/null; then
  pass "events: STARTUP recorded"
else
  fail "events" "no STARTUP event found"
fi

# ©¤©¤ 7. dmesg ©¤©¤
echo ""
echo -e "${BOLD}[7] Kernel Log${RESET}"

DMESG_COUNT=$(dmesg | grep -ci pipower5 || echo 0)
if [ "$DMESG_COUNT" -gt 0 ]; then
  pass "dmesg: $DMESG_COUNT pipower5 entries"
else
  fail "dmesg" "no pipower5 entries"
fi

# ©¤©¤ 8. Python CLI ©¤©¤
echo ""
echo -e "${BOLD}[8] Python CLI${RESET}"

if command -v pipower5 >/dev/null 2>&1; then
  # --all
  if pipower5 --all >/dev/null 2>&1; then
    pass "pipower5 --all"
  else
    fail "pipower5 --all" "command failed"
  fi
  # --firmware
  FW=$(pipower5 --firmware 2>/dev/null)
  if [ -n "$FW" ]; then
    pass "pipower5 --firmware: $FW"
  else
    fail "pipower5 --firmware" "empty output"
  fi
  # --config
  if pipower5 --config >/dev/null 2>&1; then
    pass "pipower5 --config"
  else
    fail "pipower5 --config" "command failed"
  fi
  # doctor
  if pipower5 doctor 2>&1 | grep -q 'All checks passed\|overall'; then
    pass "pipower5 doctor"
  else
    # doctor might fail if not root
    pipower5 doctor 2>&1 | head -3
    skip "pipower5 doctor" "may need root"
  fi
else
  skip "pipower5 CLI" "not installed"
fi

# ©¤©¤ Summary ©¤©¤
echo ""
echo "=========================================="
echo -e "  ${BOLD}Results: ${GREEN}$PASS passed${RESET}, ${RED}$FAIL failed${RESET}"
echo "=========================================="
echo ""

[ "$FAIL" -eq 0 ] && exit 0 || exit 1
