.. _pipower5_tool:

PiPower 5 Tool
===============================

Das PiPower 5 Tool ist die Begleitsoftware für PiPower 5.

Es bietet:

- Unterstützung für sicheres Herunterfahren
- Akku- und Lade-Management
- Stromüberwachung
- Zugriff auf das Web-Dashboard
- Ereignis-Benachrichtigungen

PiPower 5 kann in folgenden Situationen Shutdown-Anforderungen an den Raspberry Pi senden:

- Die PiPower-Taste wird 2 Sekunden lang gedrückt gehalten
- Der Akkustand fällt unter den konfigurierten Abschalt-Prozentsatz

Nachdem der Raspberry Pi das Herunterfahren abgeschlossen hat, kann PiPower 5 automatisch die Stromversorgung trennen, um SD-Karten-Beschädigungen und unerwartete Stromausfall-Probleme zu vermeiden.

.. start_install_pipower5

``pipower5``-Tool installieren
----------------------------------------------------

Installieren Sie das PiPower 5 Tool:

1. Repository klonen:

   .. code-block:: shell

      git clone https://github.com/sunfounder/pipower5

2. In das Verzeichnis wechseln:

   .. code-block:: shell

      cd pipower5

3. Installationsprogramm ausführen:

   .. code-block:: shell

      sudo python3 install.py

4. Starten Sie den Raspberry Pi neu, wenn Sie dazu aufgefordert werden.

.. end_install_pipower5

Befehlsreferenz
---------------------------------------

Das ``pipower5``-Tool bietet Zugriff auf Statusinformationen und Konfigurationsoptionen von PiPower 5.

Der folgende Befehl zeigt beispielsweise den aktuellen PiPower 5-Status an:

.. code-block:: shell

   pipower5 -a

Beispielausgabe:

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

Sie können diese Einstellungen an Ihre Bedürfnisse anpassen.

Verwenden Sie ``pipower5`` oder ``pipower5 -h`` für Anweisungen.

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

   Jedes Mal, wenn Sie den Status von ``pipower5.service`` ändern, müssen Sie den folgenden Befehl verwenden, damit die Konfigurationsänderungen wirksam werden.

   .. code-block:: shell

      sudo systemctl restart pipower5.service

   Überprüfen Sie den Status des pipower5-Programms mit dem systemctl-Tool.

   .. code-block:: shell

      sudo systemctl status pipower5.service

   Alternativ können Sie die vom Programm generierten Protokolldateien einsehen.

   .. code-block:: shell

      cat /opt/pipower5/log

Web-Dashboard
----------------------------------------------------

Das PiPower 5 Tool enthält ein integriertes Web-Dashboard für Überwachung und Konfiguration.

Greifen Sie über Ihren Browser auf das Dashboard zu:

.. code-block:: text

   http://<raspberry-pi-ip>:34001

Dashboard-Funktionen umfassen:

- Überwachung des Akkustands in Prozent
- Überwachung des Ladestatus
- Überwachung der Eingangs- und Ausgangsspannung
- Stromüberwachung
- Konfiguration des Abschalt-Prozentsatzes
- Benachrichtigungsverwaltung
- Raspberry Pi-Geräteinformationen

.. image:: img/web_dashboard.png
   :width: 100%
   :align: center

.. image:: img/web_dashboard_2.png
   :width: 100%
   :align: center

Sie können den Abschalt-Prozentsatz auch direkt über das Dashboard konfigurieren:

.. image:: img/web_dashboard_3.png
   :width: 100%
   :align: center

Wenn Sie das Dashboard nicht benötigen, entfernen Sie es mit:

.. code-block:: shell

   pipower5 --remove-dashboard

Sicheres Herunterfahren
----------------------------------------------------

PiPower 5 unterstützt automatischen sicheren Shutdown-Schutz für Raspberry Pi-Systeme.

Shutdown-Ablauf:

.. code-block:: text

   Shutdown ausgelöst
   -> Raspberry Pi führt sicheres Herunterfahren durch
   -> PiPower 5 erkennt Abschluss des Herunterfahrens
   -> PiPower 5 trennt automatisch die Stromversorgung

Dies hilft zu verhindern:

- SD-Karten-Beschädigung
- Dateisystem-Schäden
- Unerwartete Stromausfall-Probleme


Ausschalten nach Raspberry Pi-Shutdown
+++++++++++++++++++++++++++++++++++++++

.. start_power_off_after_shutdown

Damit PiPower 5 nach dem Herunterfahren des Raspberry Pi automatisch die Stromversorgung trennt, ist eine zusätzliche Konfiguration erforderlich.

1. Wenn Sie einen **Raspberry Pi 4 oder 5** verwenden:

   * Stellen Sie sicher, dass der ``SDSIG``-Jumper auf PiPower 5 mit ``PI3V3`` verbunden ist.

     .. image:: img/safe_shutdown_3v3.png
        :width: 400

   * Öffnen Sie die Raspberry Pi-Konfiguration:

     .. code-block:: shell

        sudo raspi-config

   * Navigieren Sie zu:

     .. code-block:: text

        6 Advanced Options
        -> A11 Shutdown Behaviour
        -> B1 Full power off Switch off Pi ...

   * Starten Sie den Raspberry Pi neu, wenn Sie dazu aufgefordert werden.

2. Wenn Sie einen **Raspberry Pi 3** oder älter verwenden:

   * Setzen Sie den ``SDSIG``-Jumper auf PiPower 5 auf ``GPIO26``.

     .. image:: img/safe_shutdown_io26.png
        :width: 400

   * Öffnen Sie ``/boot/firmware/config.txt``:

     .. code-block:: shell

        sudo nano /boot/firmware/config.txt

   * Fügen Sie die folgenden Zeilen hinzu:

     .. code-block:: shell

        dtoverlay=gpio-poweroff,gpio_pin=26,active_low=1
        gpio=26=op,dh

   * Drücken Sie ``Strg+X``, dann ``Y`` und drücken Sie ``Enter``, um die Datei zu speichern und zu beenden.

   * Starten Sie den Raspberry Pi neu.

     .. code-block:: shell

        sudo reboot

Nach der Konfiguration kann PiPower 5 automatisch das Herunterfahren des Raspberry Pi erkennen und die Stromversorgung sicher trennen.

Unterstützte Methoden für sicheres Herunterfahren:

- Halten Sie die PiPower-Taste 2 Sekunden lang gedrückt
- Fahren Sie über das Raspberry Pi-Desktop-Menü herunter
- Führen Sie ``sudo shutdown now`` aus
- Automatisches Herunterfahren, wenn der Akkustand unter den konfigurierten Abschalt-Prozentsatz fällt

.. end_power_off_after_shutdown

Abschalt-Prozentsatz konfigurieren
+++++++++++++++++++++++++++++++++++++++

Sie können den Akku-Prozentsatz konfigurieren, der das automatische Herunterfahren auslöst.

Beispiel:

.. code-block:: shell

   pipower5 -sp 30

Dies setzt die Abschaltschwelle auf 30%.

Verwenden Sie dann den folgenden Befehl, damit die Konfigurationsänderungen wirksam werden.

.. code-block:: shell

   sudo systemctl restart pipower5.service

Wenn der Akkustand unter 30% fällt, benachrichtigt PiPower 5 den Raspberry Pi zum Herunterfahren und trennt automatisch die Stromversorgung.


Sie können auch den aktuellen Abschalt-Prozentsatz auslesen:

.. code-block:: shell

   pipower5 -sp

.. tip::

   Für Raspberry Pi 5-Systeme mit hohem Stromverbrauch (>3A) wird empfohlen, den Abschalt-Prozentsatz auf ``100%`` einzustellen.

   Dies stellt sicher, dass der Raspberry Pi sofort herunterfährt, wenn die externe Stromversorgung getrennt wird, und hilft, das System und die Speichergeräte zu schützen.


Stromüberwachung
----------------------------------------------------

PiPower 5 bietet Echtzeitüberwachung für:

- Akkustand in Prozent
- Ladestatus
- Eingangsspannung
- Ausgangsspannung
- Eingangsstrom
- Ausgangsstrom
- Akkuspannung
- Akkustrom

Nützliche Befehle:

Akkustand in Prozent anzeigen:

.. code-block:: shell

   pipower5 -bp

Ladestatus anzeigen:

.. code-block:: shell

   pipower5 -ichg

Eingangsspannung anzeigen:

.. code-block:: shell

   pipower5 -iv

Alle Statusinformationen anzeigen:

.. code-block:: shell

   pipower5 -a

Für die vollständige Befehlsliste:

.. code-block:: shell

   pipower5 --help


Benachrichtigungen
----------------------------------------------------

PiPower5 unterstützt ereignisgesteuerte Benachrichtigungen durch:

- Summer-Warnungen
- E-Mail-Benachrichtigungen

Unterstützte Ereignisse umfassen:

- ``battery_activated``
- ``low_battery``
- ``power_disconnected``
- ``power_restored``
- ``power_insufficient``
- ``battery_critical_shutdown``
- ``battery_voltage_critical_shutdown``

.. note::

   Jedes Mal, wenn Sie den Status von ``pipower5.service`` ändern, müssen Sie den folgenden Befehl verwenden, damit die Konfigurationsänderungen wirksam werden.

   .. code-block:: shell

      sudo systemctl restart pipower5.service

Ereignisbeschreibungen
+++++++++++++++++++++++++++++++++++++++++++++++++

1. ``battery_activated``

   Wird ausgelöst, wenn der Akku beginnt, Strom zu liefern. Dies tritt typischerweise auf, wenn die externe Stromquelle getrennt wird oder keine ausreichende Leistung liefern kann.

   * **Rücksetzbedingung**: Wird automatisch zurückgesetzt, nachdem die externe Stromversorgung getrennt wurde.

2. ``low_battery``

   Wird aktiviert, wenn der Akkuladestand unter die **konfigurierte Abschaltschwelle** fällt.

   * **Wiederholung**: Wenn der Akku unter dieser Schwelle bleibt, wird das Ereignis alle 10 Minuten ausgelöst.
   * **Rücksetzbedingung**: Wird zurückgesetzt, sobald die Akkuladung über **Abschaltschwelle + 5%** steigt.

3. ``power_disconnected``

   Wird ausgelöst, wenn die externe Stromquelle getrennt wird.

   * **Rücksetzbedingung**: Wird zurückgesetzt, sobald die externe Stromversorgung wiederhergestellt ist.

4. ``power_restored``

   Wird ausgelöst, wenn die externe Stromquelle wiederhergestellt wird.

   * **Rücksetzbedingung**: Wird zurückgesetzt, wenn die externe Stromversorgung erneut getrennt wird.

5. ``power_insufficient``

   Tritt auf, wenn die externe Stromversorgung unzureichend ist und der Akku zusätzliche Leistung liefern muss.

   * **Empfohlene Maßnahme**: Überprüfen Sie die Nennausgangsleistung der Stromquelle oder die konfigurierten Ladeleistungseinstellungen.
   * **Rücksetzbedingung**: Wird zurückgesetzt, wenn die externe Stromquelle getrennt wird.

6. ``battery_critical_shutdown``

   Wird unmittelbar vor dem Herunterfahren des Systems aufgrund **kritisch niedriger Akkukapazität** ausgelöst.

7. ``battery_voltage_critical_shutdown``

   Wird ausgelöst, wenn die **Akkuspannung** unter die kritische Schwelle fällt, was zum Herunterfahren führt.

   * **Hinweis**: Dieses Ereignis wird im normalen Gebrauch selten ausgelöst. Normalerweise leitet das ``low_battery``-Ereignis eine Shutdown-Sequenz ein, bevor die Spannung so weit abfällt. Dies dient als **zusätzlicher Sicherheitsmechanismus**.

Mit diesen Ereignissen bietet PiPower5 sowohl proaktive Warnungen (z.B. niedriger Akkustand, unzureichende Stromversorgung) als auch kritische Schutzfunktionen (z.B. Shutdown-Auslöser) und gewährleistet so stabilen Betrieb und Datenschutz.



Summer-Warnungen
+++++++++++++++++++++++++++++++++++++++++++++++++

PiPower5 unterstützt Summer-Benachrichtigungen für verschiedene Systemereignisse.

Sie können Summer-Warnungen über das **Web-Dashboard** oder das **Befehlszeilen-Tool** konfigurieren.
Wenn ein konfiguriertes Ereignis eintritt, gibt PiPower5 den entsprechenden Summton aus.

Funktionen umfassen:

- Ereignisbasierte Summer-Benachrichtigungen
- Einstellbare Summer-Lautstärke (1–10)
- Vorschau der Ereignistöne
- Unterstützung für benutzerdefinierte Soundeffekte

Fortgeschrittene Benutzer können auch eigene Summer-Soundeffekte erstellen.

1. Öffnen Sie die Konfigurationsdatei:

   .. code-block:: shell

      /opt/pipower5/venv/lib/python3.11/site-packages/pipower5/config.json

2. Suchen Sie den Abschnitt ``pipower5_buzz_sequence``.

3. Jeder Soundeffekt wird im folgenden Format definiert:

   .. code-block:: text

      [action, duration]

   Wobei:

   - ``action`` sein kann:

     - Eine Musiknote, wie ``"A4"``, ``"D3"`` oder ``"C#4"``
     - Ein Frequenzwert (Ganzzahl)
     - ``"pause"`` für Stille

   - ``duration`` die Wiedergabezeit in Millisekunden (ms) ist


E-Mail-Warnungen
+++++++++++++++++++++++++++++++++++++++++++++++++

PiPower5 unterstützt E-Mail-Benachrichtigungen für wichtige Systemereignisse, wie:

- Niedriger Akkustand
- Stromversorgung getrennt
- Stromversorgung wiederhergestellt
- Kritische Shutdown-Ereignisse

E-Mail-Benachrichtigungen können über das **Web-Dashboard** oder das **Befehlszeilen-Tool** konfiguriert werden.

Um E-Mail-Warnungen zu verwenden, ist ein SMTP-Server erforderlich. Die meisten E-Mail-Anbieter unterstützen SMTP-Dienste.

- Für Gmail erstellen Sie einfach ein **App-Passwort**
- Für andere Anbieter aktivieren Sie den SMTP-Zugriff und generieren Sie bei Bedarf ein eigenes SMTP-Passwort

Bereiten Sie vor der Konfiguration die folgenden Informationen vor:

- SMTP-Serveradresse
  (Beispiel: ``smtp.gmail.com``)

- SMTP-Port
  (Beispiel: ``465`` oder ``25``)

- Verschlüsselungstyp
  (``None`` / ``SSL`` / ``TLS``)

- SMTP-Konto
  (In der Regel Ihre E-Mail-Adresse)

- SMTP-Passwort
  (App-Passwort oder SMTP-Passwort)

Konfigurieren Sie nach Eingabe der SMTP-Informationen die Empfänger-E-Mail-Adresse.

.. note::

   PiPower5 verwendet den SMTP-Server, um sich in Ihr E-Mail-Konto einzuloggen und Benachrichtigungen zu senden.

   Sie können dieselbe E-Mail-Adresse sowohl als Absender als auch als Empfänger verwenden.

Verwenden Sie nach der Einrichtung den Testbefehl, um die SMTP-Verbindung und E-Mail-Zustellung zu überprüfen.
