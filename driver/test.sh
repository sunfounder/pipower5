

echo "=== Testing PiPower5 Driver Interface ==="
echo "Input: "
echo "  Voltage: $(cat /sys/class/pipower5/pipower5/input_voltage) mV"
echo "  Current: $(cat /sys/class/pipower5/pipower5/input_current) mA"
echo "  Plugged In: $(cat /sys/class/pipower5/pipower5/is_input_plugged_in)"
echo "Output: "
echo "  Voltage: $(cat /sys/class/pipower5/pipower5/output_voltage) mV"
echo "  Current: $(cat /sys/class/pipower5/pipower5/output_current) mA"
echo "  Source: $(cat /sys/class/pipower5/pipower5/power_source)"
echo "Battery: "
echo "  Voltage: $(cat /sys/class/pipower5/pipower5/battery_voltage) mV"
echo "  Current: $(cat /sys/class/pipower5/pipower5/battery_current) mA"
echo "  Percentage: $(cat /sys/class/pipower5/pipower5/battery_percentage) %"
echo "  Charging Status: $(cat /sys/class/pipower5/pipower5/is_charging)"
echo "Others: "
echo "  Shutdown Percentage: $(cat /sys/class/pipower5/pipower5/shutdown_percentage)"
echo "  Shutdown Request: $(cat /sys/class/pipower5/pipower5/shutdown_request)"
echo "  Max Charge Current: $(cat /sys/class/pipower5/pipower5/charge_current_max)00 mA"
echo "  Battery Internal Resistor: $(cat /sys/class/pipower5/pipower5/battery_internal_resistor) mΩ"
echo "  Board ID: $(cat /sys/class/pipower5/pipower5/board_id)"
echo "  Buzzewr Volume: $(cat /sys/class/pipower5/pipower5/buzzer_volume)"
echo "  Default On: $(cat /sys/class/pipower5/pipower5/default_on)"
echo "  Firmware Version: $(cat /sys/class/pipower5/pipower5/firmware_version)"
echo "  Driver Version: $(cat /sys/class/pipower5/pipower5/driver_version)"

upower -i /org/freedesktop/UPower/devices/battery_pipower5

# Test power button
 echo "\n=== Testing Power Button ==="
 echo "Looking for power button input device..."
 BUTTON_DEVICE=$(grep -l "pipower5-power-button" /proc/bus/input/devices | sed 's/.*Handlers=.*event\([0-9]*\).*/\1/')
 if [ -n "$BUTTON_DEVICE" ]; then
   echo "Found power button device: /dev/input/event$BUTTON_DEVICE"
   echo "Testing power button events (press and release the power button)..."
   echo "Press Ctrl+C to exit."
   sudo evtest /dev/input/event$BUTTON_DEVICE | grep -E "(Event|KEY_POWER)"
 else
   echo "Power button device not found."
 fi