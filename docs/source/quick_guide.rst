Kurzanleitung
===============================

Diese Anleitung hilft Ihnen, schnell mit PiPower 5 nach der Hardware-Montage zu starten.

Akku aufladen
----------------------------------------------------

Laden Sie den Akku vor der ersten Verwendung vollständig auf.

Empfehlungen:

- Verwenden Sie ein hochwertiges USB-C-Netzteil
- Ein 5V 5A-Netzteil wird für Raspberry Pi 5 empfohlen
- Netzteile mit höherer Leistung werden bei Verwendung von SSDs oder anderen Hochleistungs-Peripheriegeräten empfohlen

Während des Ladevorgangs:

- Verwenden Sie ein hochwertiges USB-C-Netzteil, um PiPower 5 aufzuladen.

  .. image:: img/power_input.png
     :width: 50%
     :align: center

- Während des Ladevorgangs leuchten die Akku-Status-LEDs nacheinander in Sequenz auf.

  .. image:: img/battery_indicator.png
     :width: 50%
     :align: center

  Der Akkustatus wird durch die Anzahl der leuchtenden LEDs angezeigt:

  * **4 LEDs leuchten**: Akku >80%
  * **3 LEDs leuchten**: 60%< Akku <80%
  * **2 LEDs leuchten**: 40%< Akku <60%
  * **1 LED leuchtet**: 20%< Akku <40%
  * **Erste LED blinkt**: Akku <20%
  * **LEDs leuchten nacheinander im Zyklus**: Ladevorgang läuft
  * **Mittlere zwei LEDs blinken**: Warten auf Shutdown-Signal
  * **Alle LEDs aus**: Keine Stromversorgung oder im Schlafmodus
  * Während des Ladevorgangs bleibt die Anzeige **auch im ausgeschalteten Zustand** aktiv, bis der Akku vollständig geladen ist.

Einschalten
----------------------------------------------------

Für Raspberry Pi-Geräte ist keine zusätzliche Stromverkabelung erforderlich. PiPower 5 versorgt das Gerät direkt über den GPIO-Header mit Strom.

Für andere Geräte können Sie diese versorgen über:

- Den USB-A-Ausgangsanschluss
- Die 5V/GND-Pins neben dem USB-A-Anschluss

.. image:: img/power_output.png
   :width: 50%
   :align: center

Drücken Sie einmal die Power-Taste, um PiPower 5 einzuschalten. Wenn eingeschaltet:

- Leuchtet die **PWR-LED** auf
- Beginnt das angeschlossene Gerät, Strom von PiPower 5 zu erhalten

.. image:: img/pwr_led.png
   :width: 50%
   :align: center

.. include:: /pipower5_software.rst
    :start-after: start_install_pipower5
    :end-before: end_install_pipower5

Web-Dashboard öffnen
----------------------------------------------------

Öffnen Sie nach der Installation das Dashboard in Ihrem Browser:

.. code-block:: text

   http://<raspberry-pi-ip>:34001

Das Dashboard ermöglicht Ihnen:

- Anzeige des Akkustands in Prozent
- Überwachung des Ladestatus
- Überprüfung von Spannung und Strom
- Konfiguration des Abschalt-Prozentsatzes
- Verwaltung von Benachrichtigungen

.. image:: img/web_dashboard.png
   :width: 100%
   :align: center


Sicheres Herunterfahren
----------------------------------------------------

.. include:: /pipower5_software.rst
    :start-after: start_power_off_after_shutdown
    :end-before: end_power_off_after_shutdown

.. note::

   Für erweiterte Funktionen und detaillierte Konfigurationsoptionen, einschließlich:

   - Befehle zur Stromüberwachung
   - Benachrichtigungseinstellungen
   - Summer-Warnungen
   - E-Mail-Warnungen
   - Erweiterte Konfiguration

   Siehe:

   * :ref:`pipower5_tool`
