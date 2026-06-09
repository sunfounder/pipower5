.. note::

    Hello, welcome to the SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasts Community on Facebook! Dive deeper into Raspberry Pi, Arduino, and ESP32 with fellow enthusiasts.

    **Why Join?**

    - **Expert Support**: Solve post-sale issues and technical challenges with help from our community and team.
    - **Learn & Share**: Exchange tips and tutorials to enhance your skills.
    - **Exclusive Previews**: Get early access to new product announcements and sneak peeks.
    - **Special Discounts**: Enjoy exclusive discounts on our newest products.
    - **Festive Promotions and Giveaways**: Take part in giveaways and holiday promotions.

    👉 Ready to explore and create with us? Click [|link_sf_facebook|] and join today!

.. _troubleshooting:

Troubleshooting
===============

This page helps you diagnose PiPower 5 issues using the onboard LEDs, buzzer, and software tools. Start with the quick reference tables below, then follow the symptom-based guides for detailed steps.

.. contents:: Table of Contents
   :local:
   :depth: 2


----
LED & Buzzer Quick Reference
----------------------------

Before diving into specific symptoms, use these tables to interpret what the board is telling you.

Power & Status LEDs
+++++++++++++++++++

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - LED
     - State
     - What It Means
   * - **PWR LED** (green)
     - ON
     - Output power is active — the board is supplying 5V to your device.
   * -
     - OFF
     - Output is off. Press the power button once to turn it on.
   * - **BAT LED** (yellow)
     - ON
     - Battery is currently supplying power. If external power is connected, this indicates insufficient input power.
   * -
     - OFF
     - Battery is in standby — external power is sufficient.
   * - **Reverse Battery LEDs** (2× red)
     - ON (both)
     - Battery polarity is reversed! Disconnect immediately and correct the wiring.

Battery Level LEDs
++++++++++++++++++

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - LED Pattern
     - Meaning
   * - 4 LEDs lit
     - Battery > 80%
   * - 3 LEDs lit
     - Battery 60% – 80%
   * - 2 LEDs lit
     - Battery 40% – 60%
   * - 1 LED lit
     - Battery 20% – 40%
   * - First LED flashing
     - Battery < 20% — charge soon
   * - LEDs cycling sequentially
     - Charging in progress
   * - Middle two LEDs flashing
     - Waiting for shutdown signal from Raspberry Pi
   * - All LEDs off
     - Board unpowered or in sleep mode

.. note::

   Battery LEDs remain active during charging even when the board is in the off state. They turn off only when charging is complete.

Buzzer Signals
++++++++++++++

If the buzzer is enabled, these sounds indicate specific events:

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Event
     - Typical Sound
     - What It Means
   * - ``battery_activated``
     - Two ascending tones
     - Battery has taken over power supply (external power lost or insufficient).
   * - ``low_battery``
     - Two repeated tones of same pitch
     - Battery level has fallen below the configured shutdown percentage. Charge immediately.
   * - ``power_disconnected``
     - High tone → low tone
     - External power was disconnected. System is now running on battery.
   * - ``power_restored``
     - Low tone → high tone
     - External power was restored. Battery is no longer discharging.
   * - ``power_insufficient``
     - Three rapid tones of same pitch
     - External power is connected but too weak. Battery is supplementing. Check your power adapter.
   * - ``battery_critical_shutdown``
     - Three rapid descending tones
     - Battery capacity critically low. System will shut down.
   * - ``battery_voltage_critical_shutdown``
     - Four rapid descending tones
     - Battery voltage critically low (failsafe). System will shut down immediately.

.. tip::

   If you never hear buzzer sounds, the buzzer may be disabled or its volume set to 0. Run ``pipower5 -bzv`` to check the current volume, or test with ``pipower5 -bzt low_battery``.


----
Symptom-Based Diagnosis
-----------------------

"No Power" — All LEDs Off, No Output
+++++++++++++++++++++++++++++++++++++

**What you see**: PWR LED off, battery LEDs off, connected device shows no power.

**Check these, in order:**

1. **Is the battery installed?**
   PiPower 5 cannot operate without a battery. Ensure the battery connector (XH2.54 3P) is firmly seated. See :ref:`battery_connector`.

2. **Is the battery completely drained?**
   A deeply discharged battery (< 2.5V per cell) enters trickle-charge mode and may not power the board for several minutes.

   - Connect external power and wait 10–15 minutes.
   - If battery LEDs remain off after 15 minutes, the battery may be defective.

3. **Is external power connected correctly?**
   - Use a USB-C PD power supply (5V–15V) or DC power via the screw terminals.
   - Ensure the USB-C cable supports power delivery — some data-only cables will not work.
   - Try a different power adapter and cable.

4. **Press the power button once.**
   PiPower 5 requires a button press to activate output, unless the Default ON jumper is set.

5. **Check the Default ON jumper.** See :ref:`cap_onoff`.
   - Jumper on **ON**: Output activates automatically when external power is connected.
   - Jumper on **OFF**: You must press the power button each time.

6. **Check for reverse battery installation.**
   If both red LEDs near the battery connector are lit, the battery polarity is reversed. Power off immediately, disconnect the battery, and reconnect with correct polarity. See :ref:`battery_connector`.


"BAT LED Always On" — External Power Seems Insufficient
++++++++++++++++++++++++++++++++++++++++++++++++++++++++

**What you see**: External power is connected, but the BAT LED remains lit. The battery is discharging despite external power being present.

**What this means**: The external power supply cannot meet the total power demand. The battery is supplementing the shortfall.

**Check these, in order:**

1. **Is your power adapter powerful enough?**
   The formula is: *Adapter wattage ≥ Raspberry Pi power (~20–25W) + Charging power (set via DIP switch)*.

   - Raspberry Pi 5 under load can draw > 25W.
   - If charging power is set to 20W (both DIP switches ON), you need a **45W+** adapter.
   - For a 30W adapter, reduce charging power to 10W or 5W.

2. **Check the DIP switch (charging power selector).**
   See the charging power table in :ref:`power_input`. Lower the charging power if your adapter is underpowered.

3. **Try a different USB-C cable.**
   Not all cables support USB PD at higher wattages. Use the cable that came with your power adapter.

4. **Check the adapter's PD profile.**
   Some adapters advertise high wattage but only on specific voltage/current combinations. PiPower 5 requires a PD-compliant supply. Non-PD adapters (e.g., fixed 5V-only) may not provide enough current.

5. **For screw terminal input**, ensure input voltage is ≥ 9V for optimal performance. See :ref:`power_input` for the voltage-to-current limits.


"PWR LED Off" — Device Not Receiving Power
+++++++++++++++++++++++++++++++++++++++++++

**What you see**: Battery LEDs are on (board has power), but PWR LED is off and the connected device won't boot.

**Check these:**

1. **Press the power button once.**
   The board has power but output is not enabled.

2. **Is the GPIO header properly seated?**
   If using a Raspberry Pi, remove and re-seat the PiPower 5 HAT. Check for bent pins or debris in the header.

3. **Try an alternative output.**
   Connect a device to the USB-A port or the 2x4P header. If these work, the issue is with the GPIO passthrough.


"Device Keeps Shutting Down Unexpectedly"
+++++++++++++++++++++++++++++++++++++++++

**What you see**: Raspberry Pi or connected device shuts down without warning.

**Check these:**

1. **Check the shutdown percentage.**
   Run ``pipower5 -sp``. If it is set high (e.g., 50% or more), the board will trigger a shutdown early. Set a lower value if needed:

   .. code-block:: shell

      pipower5 -sp 10
      sudo systemctl restart pipower5.service

2. **Check if the battery is actually discharging.**
   Run ``pipower5 -a`` and look at:
   - ``source``: Should be "0 - External" when external power is connected.
   - ``battery current``: Negative = charging, positive = discharging.

3. **For Raspberry Pi 5 with high-power peripherals (SSD, HATs)**:
   Consider setting ``pipower5 -sp 100`` to trigger immediate safe shutdown when external power is lost. See :ref:`pipower5_tool`.

4. **Check the power adapter.**
   If ``power_insufficient`` events are triggered (buzzer or log), the adapter is too weak. Upgrade to a higher-wattage supply or lower the charging power DIP switch.


"Battery Not Charging"
++++++++++++++++++++++

**What you see**: External power connected, but battery LEDs do not show the charging animation (sequential cycling).

**Check these:**

1. **Is the battery already full?**
   4 solid LEDs = battery > 80%. The charging circuit may have stopped because the battery is full or in the constant-voltage taper phase.

2. **Check charging status via software.**
   Run ``pipower5 -ichg``. If it returns ``False``, the board reports it is not charging. Check ``pipower5 -bp`` for the current battery percentage.

3. **Over-temperature protection active.**
   If the board has been under heavy load in a warm environment, the charging chip may have exceeded 125°C and halted charging. Let the board cool down and try again.

4. **Input voltage too low via screw terminals.**
   If using screw terminals with voltage ≤ 6.5V, the charging current is limited. Use ≥ 9V for reliable charging.

5. **Check the battery health.**
   A battery that never reaches full charge or charges very slowly may have degraded cells. Try a different compatible battery (7.4V 2-cell Li-ion, XH2.54 3P).


"I2C Communication Fails" — `pipower5` Command Returns Errors
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

**What you see**: Running ``pipower5 -a`` produces an error or no data.

**Check these:**

1. **Is I2C enabled on the Raspberry Pi?**
   Run ``sudo raspi-config`` → Interface Options → I2C → Enable.

2. **Is the I2C device detected?**

   .. code-block:: shell

      sudo i2cdetect -y 1

   PiPower 5 should appear at address ``0x5a``. If no device shows up:

   - Reseat the HAT on the GPIO header.
   - Check that ``i2c-dev`` is loaded: ``lsmod | grep i2c``.
   - Verify ``dtparam=i2c_arm=on`` is in ``/boot/firmware/config.txt``.

3. **Is the `pipower5` service running?**

   .. code-block:: shell

      sudo systemctl status pipower5.service

   If inactive, start it: ``sudo systemctl start pipower5.service``.

4. **Multiple I2C devices conflict?**
   PiPower 5 uses I2C address ``0x5a``. Check that no other HAT or device is using this address. See :ref:`pin_header`.

5. **Reboot.**
   Sometimes a cold restart of both the Raspberry Pi and PiPower 5 resolves I2C bus issues. Power off completely, wait 10 seconds, then power on.


"Buzzer Silent" — No Sound on Events
+++++++++++++++++++++++++++++++++++++

**What you see**: Events occur (power disconnect, low battery, etc.) but no buzzer sound.

**Check these:**

1. **Check buzzer volume.**

   .. code-block:: shell

      pipower5 -bzv

   If it returns 0, the buzzer is muted. Set a volume (1–10):

   .. code-block:: shell

      pipower5 -bzv 5
      sudo systemctl restart pipower5.service

2. **Check which events have buzzer enabled.**

   .. code-block:: shell

      pipower5 -bzo

   Ensure the event you expect is in the list. To add an event:

   .. code-block:: shell

      pipower5 -bzo low_battery,power_disconnected

3. **Test the buzzer directly.**

   .. code-block:: shell

      pipower5 -bzt low_battery

   If you hear sound, the buzzer hardware is working — the issue is with event configuration.


"Raspberry Pi Shows Low Voltage Warning"
++++++++++++++++++++++++++++++++++++++++

**What you see**: The Raspberry Pi desktop or ``dmesg`` shows under-voltage warnings.

**This is expected behavior in some cases:**

- When powering a Raspberry Pi from the PiPower 5 USB-A port (instead of the GPIO header), the Pi may report a non-PD power supply warning. This can be safely ignored.
- If using the GPIO header and still seeing warnings, the PiPower 5 output may be under heavy load. Check the total current draw of your setup.

**Check these:**

1. Run ``pipower5 -a`` and check ``Output: voltage``. It should be stable around 5.2–5.3V. If it drops below 5.0V under load, total current draw may exceed the 5A limit.

2. Disconnect non-essential USB peripherals and re-test.

3. If the issue persists, the DC-DC converter may be faulty. Contact support.


----
Software Diagnostic Commands
----------------------------

The ``pipower5`` CLI tool is your primary diagnostic interface. Here are the most useful commands:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Command
     - What It Tells You
   * - ``pipower5 -a``
     - Complete status snapshot: input/output voltage, battery state, charging status, shutdown request, button state.
   * - ``pipower5 -bp``
     - Battery percentage.
   * - ``pipower5 -ichg``
     - Whether the battery is currently charging (``True`` / ``False``).
   * - ``pipower5 -ii``
     - Whether external power is connected.
   * - ``pipower5 -sp``
     - Current shutdown percentage threshold.
   * - ``pipower5 -sr``
     - Current shutdown request status (0 = None, 1 = Low Battery, 2 = Button).
   * - ``pipower5 -pb``
     - Current power button state.
   * - ``pipower5 -bzv``
     - Current buzzer volume.
   * - ``pipower5 -fv``
     - Firmware version (verify you're on the latest).
   * - ``pipower5 -c``
     - Full configuration dump.
   * - ``pipower5 -pfs 60``
     - Run a 60-second power failure simulation to test battery runtime.
   * - ``sudo systemctl status pipower5.service``
     - Check if the PiPower 5 background service is running.
   * - ``cat /opt/pipower5/log``
     - View service logs for error messages.

.. tip::

   For a quick health check, run ``pipower5 -a`` and verify:

   - ``shutdown request`` is ``0 - NONE`` (no pending shutdown).
   - ``battery percentage`` is above your ``shutdown percentage``.
   - ``Output: voltage`` is between 5.1V and 5.4V.


----
Still Having Issues?
--------------------

If none of the above resolves your problem, collect the following information before contacting support:

1. **System information**:

   .. code-block:: shell

      pipower5 -a
      pipower5 -fv
      pipower5 -c

2. **Service logs**:

   .. code-block:: shell

      cat /opt/pipower5/log
      sudo journalctl -u pipower5.service --no-pager -n 100

3. **Hardware details**:
   - Raspberry Pi model
   - Power adapter model and rated wattage
   - Battery type and age
   - PiPower 5 DIP switch settings
   - SDSIG and Default ON jumper positions

