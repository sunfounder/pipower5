Quick User Guide
===============================

This guide helps you quickly get started with PiPower 5 after hardware assembly.

Charge the Battery
----------------------------------------------------

Before first use, fully charge the battery.

Recommendations:

- Use a high-quality USB-C power adapter
- A 5V 5A power supply is recommended for Raspberry Pi 5
- Higher-power adapters are recommended when using SSDs or other high-power peripherals

While Charging:

- Use a high-quality USB-C power supply to charge PiPower 5.

  .. image:: img/power_input.png
     :width: 50%
     :align: center

- During charging, the battery indicator LEDs light up progressively in sequence. 

  .. image:: img/battery_indicator.png
     :width: 50%
     :align: center

  Battery status is indicated by the number of lit LEDs:
  
  * **4 LEDs lit**: Battery >80%
  * **3 LEDs lit**: 60%< Battery <80%
  * **2 LEDs lit**: 40%< Battery <60%
  * **1 LED lit**: 20%< Battery <40%
  * **First LED flashing**: Battery <20%
  * **LEDs incrementally light up in a cycle**: Charging
  * **Middle two LEDs flashing**: Waiting for shutdown signal
  * **All LEDs off**: Unpowered or in sleep mode
  * During charging, the indicator remains lit **even in the off state** until fully charged.
  
Power On
----------------------------------------------------

For Raspberry Pi devices, no additional power wiring is required. PiPower 5 supplies power directly through the GPIO header.

For other devices, you can power them using:

- The USB-A output port
- The 5V/GND pins next to the USB-A port

.. image:: img/power_output.png
   :width: 50%
   :align: center

Press the power button once to turn on PiPower 5. When powered on:

- The **PWR LED** lights up
- The connected device begins receiving power from PiPower 5

.. image:: img/pwr_led.png
   :width: 50%
   :align: center

.. include:: /pipower5_software.rst
    :start-after: start_install_pipower5
    :end-before: end_install_pipower5

Open the Web Dashboard
----------------------------------------------------

After installation, open the dashboard in your browser:

.. code-block:: text

   http://<raspberry-pi-ip>:34001

The dashboard allows you to:

- View battery percentage
- Monitor charging status
- Check voltage and current
- Configure shutdown percentage
- Manage notifications

.. image:: img/web_dashboard.png
   :width: 100%
   :align: center


Safe Shutdown
----------------------------------------------------

.. include:: /pipower5_software.rst
    :start-after: start_power_off_after_shutdown
    :end-before: end_power_off_after_shutdown

.. note::

   For advanced features and detailed configuration options, including:

   - Power monitoring commands
   - Notification settings
   - Buzzer alerts
   - Email alerts
   - Advanced configuration

   Please refer to:

   * :ref:`pipower5_tool`