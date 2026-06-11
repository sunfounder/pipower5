#!/bin/bash
# Quick button press test — polls power_button_state every 200ms
# Usage: bash test/btn_test.sh
# Press the power button. Press q+Enter to skip.

SYSFS=/sys/class/pipower5/pipower5

if [ ! -f "$SYSFS/power_button_state" ]; then
  echo "Driver not loaded. Run: sudo make install"
  echo "  or: sudo modprobe pipower5"
  exit 1
fi

echo "Press the power button ONCE within 10 seconds."
echo "Type q + Enter to skip..."
echo "Polling every 200ms..."

FOUND=0
for i in $(seq 1 50); do
  STATE=$(cat "$SYSFS/power_button_state" 2>/dev/null || echo 0)
  if [ "$STATE" != "0" ]; then
    echo ""
    echo ">>> DETECTED: state=$STATE"
    case $STATE in
      1) echo "    CLICK" ;;
      2) echo "    DOUBLE CLICK" ;;
      3) echo "    LONG PRESS 2s" ;;
      5) echo "    LONG PRESS 5s" ;;
      *) echo "    UNKNOWN" ;;
    esac
    FOUND=1
    break
  fi
  read -t 0.2 -r ans 2>/dev/null
  [ "$ans" = "q" ] && { echo "Skipped."; exit 0; }
done

if [ "$FOUND" = "1" ]; then
  echo "PASS: button press detected"
  exit 0
else
  echo ""
  echo "FAIL: no press detected"
  echo "Check: sudo dmesg | grep BUTTON | tail -5"
  exit 1
fi
