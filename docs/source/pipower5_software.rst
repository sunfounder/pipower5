.. _pipower5_tool:

PiPower 5 Tool
===============================

The PiPower 5 Tool is the companion software for PiPower 5.

It provides:

- Safe shutdown support
- Battery and charging management
- Power monitoring
- Web Dashboard access
- Event notifications

PiPower 5 can send shutdown requests to the Raspberry Pi in the following situations:

- The PiPower button is held for 2 seconds
- Battery level falls below the configured shutdown percentage

After the Raspberry Pi completes shutdown, PiPower 5 can automatically disconnect power to help prevent SD card corruption and unexpected power loss issues.

.. start_install_pipower5

Install ``pipower5`` Tool
----------------------------------------------------

Install the PiPower 5 Tool:

1. Clone the repository:

   .. code-block:: shell

      git clone https://github.com/sunfounder/pipower5

2. Enter the directory:

   .. code-block:: shell

      cd pipower5

3. Run the installer:

   .. code-block:: shell

      sudo python3 install.py

4. Reboot the Raspberry Pi when prompted.

.. end_install_pipower5

Command Reference
---------------------------------------

The ``pipower5`` tool provides access to PiPower 5 status information and configuration options.

For example, the following command displays the current PiPower 5 status:

.. code-block:: shell

   pipower5 -a

Example output:

.. code-block:: 

   Input:
      voltage: 0 mV
      current: 0 mA
      power: 0.000 W
      plugged in: False
   Output:
      voltage: 5296 mV
      current: 452 mA
      power: 2.394 W
   Battery:
      voltage: 8028 mV
      current: -315 mA
      power: -2.529 W
      percentage: 91 %
      source: 1 - Battery
      charging: False

   Internal:
      shutdown request: 0 - NONE
      power button: 0 - RELEASED
      max charging current: 0 mA
      default on: on
      shutdown percentage: 10 %

You can customize these settings to fit your needs.

Use ``pipower5`` or ``pipower5 -h`` for instructions.

.. code-block:: text


  usage: pipower5 [-h] [-v] [-c] [-drd [DATABASE_RETENTION_DAYS]]
                  [-dl [{debug,info,warning,error,critical}]] [-rd]
                  [-cp [CONFIG_PATH]] [-sp [SHUTDOWN_PERCENTAGE]] [-iv] [-ic]
                  [-ov] [-oc] [-bv] [-bc] [-bp] [-bs] [-ii] [-ichg] [-do] [-sr]
                  [-pb] [-cc] [-a] [-fv] [-pfs [POWER_FAILURE_SIMULATION]]
                  [-seo [SEND_EMAIL_ON]] [-set [SEND_EMAIL_TO]]
                  [-ss [SMTP_SERVER]] [-smp [SMTP_PORT]] [-se [SMTP_EMAIL]]
                  [-spw [SMTP_PASSWORD]] [-ssc [SMTP_SECURITY]] [-bzo [BUZZ_ON]]
                  [-bzv [BUZZER_VOLUME]] [-bzt [BUZZER_TEST]] [-u [{C,F}]]
                  [{start,stop}]

  PiPower 5

  positional arguments:
    {start,stop}          Command

  options:
    -h, --help            show this help message and exit
    -v, --version         Show version
    -c, --config          Show config
    -drd [DATABASE_RETENTION_DAYS], --database-retention-days [DATABASE_RETENTION_DAYS]
                          Database retention days
    -dl [{debug,info,warning,error,critical}], --debug-level [{debug,info,warning,error,critical}]
                          Debug level
    -rd, --remove-dashboard
                          Remove dashboard
    -cp [CONFIG_PATH], --config-path [CONFIG_PATH]
                          Config path
    -sp [SHUTDOWN_PERCENTAGE], --shutdown-percentage [SHUTDOWN_PERCENTAGE]
                          Set shutdown percentage, leave empty to read
    -iv, --input-voltage  Read input voltage
    -ic, --input-current  Read input current
    -ov, --output-voltage
                          Read output voltage
    -oc, --output-current
                          Read output current
    -bv, --battery-voltage
                          Read battery voltage
    -bc, --battery-current
                          Read battery current
    -bp, --battery-percentage
                          Read battery percentage
    -bs, --battery-source
                          Read battery source
    -ii, --is-input-plugged_in
                          Read is input plugged in
    -ichg, --is-charging  Read is charging
    -do, --default-on     Read default on
    -sr, --shutdown-request
                          Read shutdown request
    -pb, --power-btn      Read power button
    -cc, --charging-current
                          Max charging current
    -a, --all             Show all status
    -fv, --firmware       PiPower5 firmware version
    -pfs [POWER_FAILURE_SIMULATION], --power-failure-simulation [POWER_FAILURE_SIMULATION]
                          Power failure simulation
    -seo [SEND_EMAIL_ON], --send-email-on [SEND_EMAIL_ON]
                          Send email on: ['battery_activated', 'low_battery',
                          'power_disconnected', 'power_restored',
                          'power_insufficient', 'battery_critical_shutdown',
                          'battery_voltage_critical_shutdown']
    -set [SEND_EMAIL_TO], --send-email-to [SEND_EMAIL_TO]
                          Email address to send email to
    -ss [SMTP_SERVER], --smtp-server [SMTP_SERVER]
                          SMTP server
    -smp [SMTP_PORT], --smtp-port [SMTP_PORT]
                          SMTP port
    -se [SMTP_EMAIL], --smtp-email [SMTP_EMAIL]
                          SMTP email
    -spw [SMTP_PASSWORD], --smtp-password [SMTP_PASSWORD]
                          SMTP password
    -ssc [SMTP_SECURITY], --smtp-security [SMTP_SECURITY]
                          SMTP security, 'none', 'ssl' or 'tls'
    -bzo [BUZZ_ON], --buzz-on [BUZZ_ON]
                          Buzz on: ['battery_activated', 'low_battery',
                          'power_disconnected', 'power_restored',
                          'power_insufficient', 'battery_critical_shutdown',
                          'battery_voltage_critical_shutdown']
    -bzv [BUZZER_VOLUME], --buzzer-volume [BUZZER_VOLUME]
                          Buzz volume
    -bzt [BUZZER_TEST], --buzzer-test [BUZZER_TEST]
                          Test buzzer on selected event.
    -u [{C,F}], --temperature-unit [{C,F}]
                          Temperature unit

.. note::

   Each time you modify the status of ``pipower5.service``, you need to use the following command to make the configuration changes take effect.

   .. code-block:: shell

      sudo systemctl restart pipower5.service

   Verify the pipower5 program status using the systemctl tool.

   .. code-block:: shell

      sudo systemctl status pipower5.service

   Alternatively, inspect the program-generated log files.

   .. code-block:: shell

      cat /opt/pipower5/log

Web Dashboard
----------------------------------------------------

The PiPower 5 Tool includes a built-in Web Dashboard for monitoring and configuration.

Access the dashboard from your browser:

.. code-block:: text

   http://<raspberry-pi-ip>:34001

Dashboard features include:

- Battery percentage monitoring
- Charging status monitoring
- Input and output voltage monitoring
- Current monitoring
- Shutdown percentage configuration
- Notification management
- Raspberry Pi device information

.. image:: img/web_dashboard.png
   :width: 100%
   :align: center

.. image:: img/web_dashboard_2.png
   :width: 100%
   :align: center

You can also configure the shutdown percentage directly from the dashboard:

.. image:: img/web_dashboard_3.png
   :width: 100%
   :align: center

If you do not need the dashboard, remove it with:

.. code-block:: shell

   pipower5 --remove-dashboard

Safe Shutdown
----------------------------------------------------

PiPower 5 supports automatic safe shutdown protection for Raspberry Pi systems.

Shutdown workflow:

.. code-block:: text

   Shutdown triggered
   -> Raspberry Pi performs safe shutdown
   -> PiPower 5 detects shutdown completion
   -> PiPower 5 automatically cuts power

This helps prevent:

- SD card corruption
- File system damage
- Unexpected power loss issues


Power-Off After Raspberry Pi Shutdown
++++++++++++++++++++++++++++++++++++++

.. start_power_off_after_shutdown

To allow PiPower 5 to automatically cut power after the Raspberry Pi shuts down, some additional configuration is required.

1. If you are using a **Raspberry Pi 4 or 5**:

   * Ensure the ``SDSIG`` jumper on PiPower 5 is connected to ``PI3V3``.

     .. image:: img/safe_shutdown_3v3.png
        :width: 400

   * Open Raspberry Pi Configuration:

     .. code-block:: shell
  
        sudo raspi-config

   * Navigate to:

     .. code-block:: text
  
        6 Advanced Options
        -> A11/A12 Shutdown Behaviour
        -> B1 Full power off Switch off Pi ...

   * Reboot the Raspberry Pi when prompted.

2. If you are using a **Raspberry Pi 3** or earlier:

   * Set the ``SDSIG`` jumper on PiPower 5 to ``GPIO26``.

     .. image:: img/safe_shutdown_io26.png
        :width: 400
        
   * Open ``/boot/firmware/config.txt``:

     .. code-block:: shell
  
        sudo nano /boot/firmware/config.txt

   * Add the following lines:

     .. code-block:: shell
  
        dtoverlay=gpio-poweroff,gpio_pin=26,active_low=1
        gpio=26=op,dh

   * Press ``Ctrl+X``, then ``Y``, and press ``Enter`` to save the file and exit.
   
   * Reboot the Raspberry Pi.

     .. code-block:: shell
  
        sudo reboot

After configuration, PiPower 5 can automatically detect Raspberry Pi shutdown and safely disconnect power.

Supported safe shutdown methods include:

- Hold the PiPower button for 2 seconds
- Shut down from the Raspberry Pi desktop menu
- Run ``sudo shutdown now``
- Automatic shutdown when battery level falls below the configured shutdown percentage

.. end_power_off_after_shutdown

Configure Shutdown Percentage
++++++++++++++++++++++++++++++++++++++

You can configure the battery percentage that triggers automatic shutdown.

Example:

.. code-block:: shell

   pipower5 -sp 30

This sets the shutdown threshold to 30%.

Then use the following command to make the configuration changes take effect.

.. code-block:: shell

   sudo systemctl restart pipower5.service

When the battery level falls below 30%, PiPower 5 will notify the Raspberry Pi to shut down and disconnect power automatically.


You can also read the current shutdown percentage:

.. code-block:: shell

   pipower5 -sp

.. tip::

   For Raspberry Pi 5 systems with high power consumption (>3A), it is recommended to set the shutdown percentage to ``100%``.

   This ensures the Raspberry Pi shuts down immediately when external power is disconnected, helping protect the system and storage devices.


Power Monitoring
----------------------------------------------------

PiPower 5 provides real-time monitoring for:

- Battery percentage
- Charging status
- Input voltage
- Output voltage
- Input current
- Output current
- Battery voltage
- Battery current

Useful commands:

Show battery percentage:

.. code-block:: shell

   pipower5 -bp

Show charging status:

.. code-block:: shell

   pipower5 -ichg

Show input voltage:

.. code-block:: shell

   pipower5 -iv

Show all status information:

.. code-block:: shell

   pipower5 -a

For the full command list:

.. code-block:: shell

   pipower5 --help


Notifications
----------------------------------------------------

PiPower5 supports event-driven notifications through:

- Buzzer alerts
- Email notifications

Supported events include:

- ``battery_activated``
- ``low_battery``
- ``power_disconnected``
- ``power_restored``
- ``power_insufficient``
- ``battery_critical_shutdown``
- ``battery_voltage_critical_shutdown``

.. note::

   Each time you modify the status of ``pipower5.service``, you need to use the following command to make the configuration changes take effect.

   .. code-block:: shell

      sudo systemctl restart pipower5.service

Event Descriptions
+++++++++++++++++++++++++++++++++++++++++++++++++

1. ``battery_activated``

   Triggered when the battery begins supplying power. This typically occurs if the external power source is disconnected or unable to provide sufficient power.

   * **Reset Condition**: Resets automatically after external power is disconnected.

2. ``low_battery``

   Activated when the battery charge level falls below the **configured shutdown threshold**.

   * **Repetition**: If the battery remains below this threshold, the event is triggered every 10 minutes.
   * **Reset Condition**: Resets once the battery charge rises above **shutdown threshold + 5%**.

3. ``power_disconnected``

   Triggered when the external power source is disconnected.

   * **Reset Condition**: Resets once the external power supply is restored.

4. ``power_restored``

   Triggered when the external power source is restored.

   * **Reset Condition**: Resets if the external power is disconnected again.

5. ``power_insufficient``

   Occurs when the external power supply is insufficient, requiring the battery to provide supplemental power.

   * **Recommended Action**: Check the rated output of the power source, or verify the configured charging power settings.
   * **Reset Condition**: Resets when the external power source is disconnected.

6. ``battery_critical_shutdown``

   Triggered just before the system shuts down due to **critically low battery capacity**.

7. ``battery_voltage_critical_shutdown``

   Triggered when the **battery voltage** drops below the critical threshold, leading to shutdown.

   * **Note**: This event is rarely triggered in normal use. Typically, the ``low_battery`` event will initiate a shutdown sequence before the voltage drops this far. This serves as a **failsafe shutdown mechanism**.

With these events, PiPower5 provides both proactive warnings (e.g., low battery, insufficient power) and critical safeguards (e.g., shutdown triggers), ensuring stable operation and data protection.



Buzzer Alerts
+++++++++++++++++++++++++++++++++++++++++++++++++

PiPower5 supports buzzer notifications for different system events.

You can configure buzzer alerts through the **Web Dashboard** or the **command-line tool**.  
When a configured event occurs, PiPower5 will play the corresponding buzzer sound.

Features include:

- Event-based buzzer notifications
- Adjustable buzzer volume (1–10)
- Event sound preview
- Custom sound effect support

Advanced users can also create custom buzzer sound effects.

1. Open the configuration file:

   .. code-block:: shell

      /opt/pipower5/venv/lib/python3.11/site-packages/pipower5/config.json

2. Locate the ``pipower5_buzz_sequence`` section.

3. Each sound effect is defined using the following format:

   .. code-block:: text

      [action, duration]

   Where:

   - ``action`` can be:

     - A musical note, such as ``"A4"``, ``"D3"``, or ``"C#4"``
     - A frequency value (integer)
     - ``"pause"`` for silence

   - ``duration`` is the playback time in milliseconds (ms)


Email Alerts
+++++++++++++++++++++++++++++++++++++++++++++++++

PiPower5 supports email notifications for important system events, such as:

- Low battery
- Power disconnected
- Power restored
- Critical shutdown events

Email notifications can be configured through the **Web Dashboard** or the **command-line tool**.

To use email alerts, an SMTP server is required. Most email providers support SMTP services.

- For Gmail, simply create an **App Password**
- For other providers, enable SMTP access and generate a dedicated SMTP password if required

Before configuration, prepare the following information:

- SMTP server address  
  (Example: ``smtp.gmail.com``)

- SMTP port  
  (Example: ``465`` or ``25``)

- Encryption type  
  (``None`` / ``SSL`` / ``TLS``)

- SMTP account  
  (Usually your email address)

- SMTP password  
  (App Password or SMTP password)

After entering the SMTP information, configure the recipient email address.

.. note::

   PiPower5 uses the SMTP server to log into your email account and send notifications.

   You may use the same email address as both the sender and recipient.

After setup, use the test command to verify the SMTP connection and email delivery.