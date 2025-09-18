.. _pipower_5_tool:

PiPower 5 Tool
===============================

The |link_pipower_tool| is the companion software for PiPower 5. 

PiPower 5 sends a shutdown signal in the following scenarios, and the PiPower 5 Tool is responsible for processing these signals:

- The power button is held for two seconds and then released.
- The external power supply is disconnected, and the battery level reaches the configured shutdown percentage.

You can also use this tool to retrieve various information from PiPower 5, such as voltage, current, and more.


Install the PiPower 5 Tool
----------------------------------------------------

1. Download the library from GitHub:

   .. code-block:: shell
       
       git clone https://github.com/sunfounder/pipower5

2. Navigate to the directory:
   
   .. code-block:: shell
   
       cd pipower5

3. Run the installation script:

   .. code-block:: shell
   
       sudo python3 install.py

   This command also installs a :ref:`web dashboard <web_dashboard>` that runs on port 34001 of your device. The dashboard provides access to PiPower and Raspberry Pi device information. If you do not need the web dashboard, use this command instead:
   
   .. code-block:: shell
   
       sudo python install.py --disable-dashboard
   
   After installation, you will be prompted to restart the system. Enter ``Y`` and press **Enter** to reboot. Once rebooted, the PiPower 5 safe shutdown service will start automatically.
   
   .. image:: img/pi_install_pipower.png
     :width: 90%
     :align: center

After that, if the power button is pressed for 2 seconds or the battery power is low, PiPower 5 will notify the Raspberry Pi to shut down and disconnect the power.


Basic Command Usage
------------------------------------------------------

When the Raspberry Pi is not connected to an external power supply and the battery voltage drops below the configured shutdown percentage, PiPower 5 sends a "low battery" shutdown request via I²C. A Raspberry Pi with the PiPower 5 Tool installed can process this request, execute the shutdown command, and allow PiPower 5 to disconnect the power, preventing unexpected data loss caused by sudden power outages.

After installing the ``pipower5`` library, the Raspberry Pi will automatically manage safe shutdowns.


Power-Off After Raspberry Pi Shutdown
++++++++++++++++++++++++++++++++++++++

PiPower5 can detect when the Raspberry Pi has shut down and automatically cut power afterwards.

- Press and hold the PiPower button for 2 seconds (or when the battery is low) → Raspberry Pi shuts down → PiPower5 powers off.  
- Double-press the Raspberry Pi’s power button → Raspberry Pi shuts down → PiPower5 powers off.  
- Shut down from the Raspberry Pi desktop menu → PiPower5 powers off.  
- When the battery level drops below the configured shutdown percentage, PiPower5 notifies the Raspberry Pi to shut down. After shutdown, PiPower5 cuts power.  

.. note::  
   To use this feature, ensure that the **SDSIG jumper** on PiPower5 is connected to **PI3V3**.

Run the following command:

.. code-block:: shell

   sudo raspi-config

Navigate to:  
**6 Advanced Options → A11 Shutdown Behaviour → B1 Full power off**  
(*Switch off Pi power management (PMIC) outputs on Pi4 / Pi5 - recommended*).

Reboot when prompted after exiting `raspi-config`.



Configure Shutdown Percentage
++++++++++++++++++++++++++++++++++++++

To set the shutdown percentage, use the following command:

.. code-block:: shell

    pipower5 -sp [PERCENTAGE]

Example:

Set the shutdown percentage to 30%:

.. code-block:: shell

    pipower5 -sp 30

When the battery level drops below 30%, PiPower 5 will notify the Raspberry Pi to shut down and disconnect the power.

.. tip::

   If you are using high-power peripherals (>3A), the battery may not be able to provide power for a long time, consider setting the shutdown percentage to 100%. This ensures immediate shutdown when external power is disconnected, protecting the Raspberry Pi and its data.





Retrieving Data with PiPower5
++++++++++++++++++++++++++++++++++++++++

You can use the ``pipower5`` command to view the current information. The detailed command parameters are as follows:

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


Example:

.. image:: img/pipower5_tool.png
  :width: 70%

.. _web_dashboard:



Battery Shutdown Percentage
---------------------------------------------

When running only on battery power and the battery voltage drops below the configured **Shutdown Percentage**, PiPower5 sends a **LOW BATTERY Shutdown Request** via I²C.  

- The host system can read this Shutdown Request signal.  
- When LOW BATTERY is detected, the system can safely shut down.  
- After shutdown, PiPower5 pulls the **SDSIG** pin high and cuts power.  

This ensures a controlled shutdown sequence on low battery. On Raspberry Pi, installing the **pipower5 library** automatically sets up the required service for safe shutdown.  

You can configure the shutdown percentage via:

- CLI command:  

  .. code-block:: shell

     pipower5 -sp [value]

- Or from the **Dashboard settings page**.

.. note::  
   On Raspberry Pi 5, if the power draw is high (e.g., >3A), the battery cannot sustain long-term operation. In this case, it is recommended to set the Shutdown Percentage to **100%**, so the Raspberry Pi shuts down immediately when external power is lost, protecting both the device and your data.


Web Dashboard
------------------------------------------------------

When installing the PiPower command-line tool, a Web Dashboard is also included, accessible via port 34001 on your device.

If you prefer not to use the Web Dashboard, you can remove it with the following command:

.. code-block:: shell

   sudo pipower5 --remove-dashboard

The Web Dashboard allows you to view various PiPower 5 and raspberry pi data, including:

.. image:: img/web_dashboard.png
   :width: 100%
   :align: center

.. image:: img/web_dashboard_2.png
   :width: 100%
   :align: center

.. raw:: html

   <br/>

Additionally, you can configure the **Shutdown Percentage** through the dashboard.

Example:

Set the shutdown percentage to 10%:

.. image:: img/web_dashboard_3.png
   :width: 100%
   :align: center

.. raw:: html

   <br/>

When the battery level drops below 10%, PiPower 5 will notify the Raspberry Pi to shut down and disconnect the power.


Event Notifications
-------------------------------

PiPower5 supports event-driven notifications, which can be configured to trigger either **buzzer alerts** or **email alerts**. Below is a detailed explanation of each event:

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

PiPower5 supports buzzer notifications, allowing audible alerts for specific events.

1. Configure buzzer events via **Dashboard** or **CLI**. When an event occurs, the buzzer plays the corresponding sound.  
2. Adjust buzzer volume from **1–10**.  
3. Preview event sounds to recognize them easily.  
4. Advanced: Create **custom sound effects**.  

   Steps:  
   (1) Open the configuration file:  

   .. code-block:: shell

      /opt/pipower5/venv/lib/python3.11/site-packages/pipower5/config.json

   (2) Locate the **pipower5_buzz_sequence** section.  
   (3) Each effect is a list entry in the format: `[action, duration]`.  
   (4) **Action** can be:  

       - A musical note (e.g., `"A4"`, `"D3"`, `"C#4"`).  
       - A frequency (integer).  
       - `"pause"` (silence).  

   (5) **Duration** is the length in milliseconds (ms).  



Email Alerts
+++++++++++++++++++++++++++++++++++++++++++++++++

PiPower5 software can also send **email notifications** for specific events.

1. You need an SMTP server. Most email providers support this.  

   - For Gmail, simply create an **App Password** (no extra SMTP activation required).  
   - For other providers, enable SMTP and generate a dedicated SMTP password (separate from your account password).  

2. Gather the following information:  

   (1) **SMTP server address** (e.g., `smtp.gmail.com`).  
   (2) **SMTP port** (e.g., `465`, `25` depending on encryption).  
   (3) **Encryption type** (None / SSL / TLS).  
   (4) **SMTP account** (usually your email address).  
   (5) **SMTP password** (App password or dedicated SMTP password).  

3. Enter this information via **Dashboard** or **CLI**.  
4. Configure the recipient email address.  

   - PiPower5 uses the SMTP server to log into your account and send notifications.  
   - You can use the same email as both sender and recipient (sending mail to yourself is valid).  

5. After setup, run the **test command** to verify connection with the SMTP server.
