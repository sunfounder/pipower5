.. note::

    Hallo, willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauchen Sie tiefer in Raspberry Pi, Arduino und ESP32 mit gleichgesinnten Enthusiasten ein.

    **Warum beitreten?**

    - **Experten-Support**: Lösen Sie Probleme nach dem Kauf und technische Herausforderungen mit Hilfe unserer Community und unseres Teams.
    - **Lernen & Teilen**: Tauschen Sie Tipps und Tutorials aus, um Ihre Fähigkeiten zu verbessern.
    - **Exklusive Vorschauen**: Erhalten Sie frühzeitigen Zugang zu neuen Produktankündigungen und Vorab-Einblicken.
    - **Spezielle Rabatte**: Genießen Sie exklusive Rabatte auf unsere neuesten Produkte.
    - **Festliche Aktionen und Gewinnspiele**: Nehmen Sie an Gewinnspielen und Feiertagsaktionen teil.

    👉 Bereit, mit uns zu entdecken und zu gestalten? Klicken Sie [|link_sf_facebook|] und treten Sie noch heute bei!

.. _troubleshooting:

Fehlerbehebung
===============

Diese Seite hilft Ihnen bei der Diagnose von PiPower 5-Problemen mithilfe der integrierten LEDs, des Summers und der Software-Tools. Beginnen Sie mit den folgenden Kurzreferenz-Tabellen und folgen Sie dann den symptombezogenen Anleitungen für detaillierte Schritte.

.. contents:: Inhaltsverzeichnis
   :local:
   :depth: 2


----------------------------
LED- & Summer-Kurzreferenz
----------------------------

Bevor Sie sich in spezifische Symptome vertiefen, verwenden Sie diese Tabellen, um zu interpretieren, was die Platine Ihnen mitteilt.

Betriebs- & Status-LEDs
+++++++++++++++++++++++++

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - LED
     - Zustand
     - Bedeutung
   * - **PWR-LED** (grün)
     - AN
     - Ausgangsstrom ist aktiv — die Platine liefert 5V an Ihr Gerät.
   * -
     - AUS
     - Ausgang ist aus. Drücken Sie einmal die Power-Taste, um ihn einzuschalten.
   * - **BAT-LED** (gelb)
     - AN
     - Akku versorgt derzeit das System. Wenn externe Stromversorgung angeschlossen ist, deutet dies auf unzureichende Eingangsleistung hin.
   * -
     - AUS
     - Akku ist im Standby — externe Stromversorgung ist ausreichend.
   * - **Verpolungs-LEDs** (2× rot)
     - AN (beide)
     - Akku-Polarität ist vertauscht! Sofort trennen und Verkabelung korrigieren.

Akku-Ladestand-LEDs
++++++++++++++++++++++

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - LED-Muster
     - Bedeutung
   * - 4 LEDs leuchten
     - Akku > 80%
   * - 3 LEDs leuchten
     - Akku 60% – 80%
   * - 2 LEDs leuchten
     - Akku 40% – 60%
   * - 1 LED leuchtet
     - Akku 20% – 40%
   * - Erste LED blinkt
     - Akku < 20% — bald aufladen
   * - LEDs laufen nacheinander durch
     - Ladevorgang läuft
   * - Mittlere zwei LEDs blinken
     - Warten auf Shutdown-Signal vom Raspberry Pi
   * - Alle LEDs aus
     - Platine ohne Strom oder im Schlafmodus

.. note::

   Die Akku-LEDs bleiben während des Ladevorgangs aktiv, auch wenn die Platine ausgeschaltet ist. Sie erlöschen erst, wenn der Ladevorgang abgeschlossen ist.

Summer-Signale
++++++++++++++++

Wenn der Summer aktiviert ist, zeigen diese Töne bestimmte Ereignisse an:

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Ereignis
     - Typischer Ton
     - Bedeutung
   * - ``battery_activated``
     - Zwei aufsteigende Töne
     - Der Akku hat die Stromversorgung übernommen (externe Stromversorgung verloren oder unzureichend).
   * - ``low_battery``
     - Zwei wiederholte Töne gleicher Tonhöhe
     - Der Akkustand ist unter den konfigurierten Abschalt-Prozentsatz gefallen. Sofort aufladen.
   * - ``power_disconnected``
     - Hoher Ton → tiefer Ton
     - Externe Stromversorgung wurde getrennt. System läuft jetzt über Akku.
   * - ``power_restored``
     - Tiefer Ton → hoher Ton
     - Externe Stromversorgung wurde wiederhergestellt. Akku wird nicht mehr entladen.
   * - ``power_insufficient``
     - Drei schnelle Töne gleicher Tonhöhe
     - Externe Stromversorgung ist angeschlossen, aber zu schwach. Akku unterstützt zusätzlich. Überprüfen Sie Ihr Netzteil.
   * - ``battery_critical_shutdown``
     - Drei schnelle absteigende Töne
     - Akkukapazität kritisch niedrig. System wird herunterfahren.
   * - ``battery_voltage_critical_shutdown``
     - Vier schnelle absteigende Töne
     - Akkuspannung kritisch niedrig (Sicherheitsmechanismus). System wird sofort herunterfahren.

.. tip::

   Wenn Sie nie Summer-Töne hören, ist der Summer möglicherweise deaktiviert oder seine Lautstärke auf 0 gesetzt. Führen Sie ``pipower5 -bzv`` aus, um die aktuelle Lautstärke zu überprüfen, oder testen Sie mit ``pipower5 -bzt low_battery``.


-------------------------
Symptombasierte Diagnose
-------------------------

„Keine Stromversorgung" — Alle LEDs aus, kein Ausgang
++++++++++++++++++++++++++++++++++++++++++++++++++++++

**Was Sie sehen**: PWR-LED aus, Akku-LEDs aus, angeschlossenes Gerät zeigt keine Stromversorgung.

**Überprüfen Sie Folgendes, in dieser Reihenfolge:**

1. **Ist der Akku installiert?**
   PiPower 5 kann ohne Akku nicht betrieben werden. Stellen Sie sicher, dass der Akku-Anschluss (XH2.54 3P) fest sitzt. Siehe :ref:`battery_connector`.

2. **Ist der Akku vollständig entladen?**
   Ein tiefentladener Akku (< 2,5V pro Zelle) wechselt in den Erhaltungslade-Modus und kann die Platine möglicherweise mehrere Minuten lang nicht mit Strom versorgen.

   - Schließen Sie die externe Stromversorgung an und warten Sie 10–15 Minuten.
   - Wenn die Akku-LEDs nach 15 Minuten immer noch aus sind, ist der Akku möglicherweise defekt.

3. **Ist die externe Stromversorgung korrekt angeschlossen?**
   - Verwenden Sie ein USB-C PD-Netzteil (5V–15V) oder Gleichstrom über die Schraubklemmen.
   - Stellen Sie sicher, dass das USB-C-Kabel Power Delivery unterstützt — reine Datenkabel funktionieren nicht.
   - Versuchen Sie ein anderes Netzteil und Kabel.

4. **Drücken Sie einmal die Power-Taste.**
   PiPower 5 erfordert einen Tastendruck, um den Ausgang zu aktivieren, es sei denn, der Default-ON-Jumper ist gesetzt.

5. **Überprüfen Sie den Default-ON-Jumper.** Siehe :ref:`cap_onoff`.
   - Jumper auf **ON**: Ausgang wird automatisch aktiviert, wenn externe Stromversorgung angeschlossen ist.
   - Jumper auf **OFF**: Sie müssen jedes Mal die Power-Taste drücken.

6. **Auf verpolten Akku prüfen.**
   Wenn beide roten LEDs in der Nähe des Akku-Anschlusses leuchten, ist die Akku-Polarität vertauscht. Schalten Sie sofort aus, trennen Sie den Akku und schließen Sie ihn mit korrekter Polarität wieder an. Siehe :ref:`battery_connector`.


„BAT-LED immer an" — Externe Stromversorgung scheint unzureichend
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

**Was Sie sehen**: Externe Stromversorgung ist angeschlossen, aber die BAT-LED bleibt an. Der Akku entlädt sich trotz vorhandener externer Stromversorgung.

**Was das bedeutet**: Die externe Stromversorgung kann den Gesamtstrombedarf nicht decken. Der Akku gleicht die Unterdeckung aus.

**Überprüfen Sie Folgendes, in dieser Reihenfolge:**

1. **Ist Ihr Netzteil leistungsstark genug?**
   Die Formel lautet: *Netzteil-Wattzahl ≥ Raspberry Pi-Leistung (~20–25W) + Ladeleistung (über DIP-Schalter eingestellt)*.

   - Raspberry Pi 5 kann unter Last > 25W ziehen.
   - Wenn die Ladeleistung auf 20W eingestellt ist (beide DIP-Schalter ON), benötigen Sie ein **45W+**-Netzteil.
   - Reduzieren Sie bei einem 30W-Netzteil die Ladeleistung auf 10W oder 5W.

2. **Überprüfen Sie den DIP-Schalter (Ladeleistungswahl).**
   Siehe Ladeleistungstabelle in :ref:`power_input`. Reduzieren Sie die Ladeleistung, wenn Ihr Netzteil zu schwach ist.

3. **Versuchen Sie ein anderes USB-C-Kabel.**
   Nicht alle Kabel unterstützen USB PD mit höheren Wattzahlen. Verwenden Sie das Kabel, das mit Ihrem Netzteil geliefert wurde.

4. **Überprüfen Sie das PD-Profil des Netzteils.**
   Einige Netzteile geben hohe Wattzahlen an, aber nur bei bestimmten Spannungs-/Stromkombinationen. PiPower 5 benötigt eine PD-konforme Stromversorgung. Nicht-PD-Netzteile (z.B. nur 5V fest) liefern möglicherweise nicht genügend Strom.

5. **Bei Schraubklemmen-Eingang** stellen Sie sicher, dass die Eingangsspannung ≥ 9V für optimale Leistung beträgt. Siehe :ref:`power_input` für die spannungsabhängigen Strombegrenzungen.


„PWR-LED aus" — Gerät erhält keinen Strom
+++++++++++++++++++++++++++++++++++++++++++

**Was Sie sehen**: Akku-LEDs sind an (Platine hat Strom), aber PWR-LED ist aus und das angeschlossene Gerät startet nicht.

**Überprüfen Sie Folgendes:**

1. **Drücken Sie einmal die Power-Taste.**
   Die Platine hat Strom, aber der Ausgang ist nicht aktiviert.

2. **Ist der GPIO-Header richtig aufgesteckt?**
   Wenn Sie einen Raspberry Pi verwenden, entfernen Sie das PiPower 5 HAT und stecken Sie es erneut auf. Überprüfen Sie auf verbogene Pins oder Schmutz im Header.

3. **Versuchen Sie einen alternativen Ausgang.**
   Schließen Sie ein Gerät an den USB-A-Anschluss oder den 2x4P-Header an. Wenn diese funktionieren, liegt das Problem an der GPIO-Durchleitung.


„Gerät schaltet sich unerwartet immer wieder aus"
+++++++++++++++++++++++++++++++++++++++++++++++++

**Was Sie sehen**: Raspberry Pi oder angeschlossenes Gerät schaltet sich ohne Vorwarnung ab.

**Überprüfen Sie Folgendes:**

1. **Überprüfen Sie den Abschalt-Prozentsatz.**
   Führen Sie ``pipower5 -sp`` aus. Wenn dieser hoch eingestellt ist (z.B. 50% oder mehr), löst die Platine frühzeitig eine Abschaltung aus. Setzen Sie bei Bedarf einen niedrigeren Wert:

   .. code-block:: shell

      pipower5 -sp 10
      sudo systemctl restart pipower5.service

2. **Überprüfen Sie, ob sich der Akku tatsächlich entlädt.**
   Führen Sie ``pipower5 -a`` aus und achten Sie auf:
   - ``source``: Sollte "0 - External" sein, wenn externe Stromversorgung angeschlossen ist.
   - ``battery current``: Negativ = Laden, positiv = Entladen.

3. **Für Raspberry Pi 5 mit Hochleistungs-Peripherie (SSD, HATs)**:
   Erwägen Sie ``pipower5 -sp 100`` zu setzen, um ein sofortiges sicheres Herunterfahren auszulösen, wenn die externe Stromversorgung ausfällt. Siehe :ref:`pipower5_tool`.

4. **Überprüfen Sie das Netzteil.**
   Wenn ``power_insufficient``-Ereignisse ausgelöst werden (Summer oder Protokoll), ist das Netzteil zu schwach. Rüsten Sie auf ein Netzteil mit höherer Wattzahl auf oder reduzieren Sie die Ladeleistung über den DIP-Schalter.


„Akku lädt nicht"
++++++++++++++++++

**Was Sie sehen**: Externe Stromversorgung ist angeschlossen, aber die Akku-LEDs zeigen nicht die Ladeanimation (sequenzielles Durchlaufen).

**Überprüfen Sie Folgendes:**

1. **Ist der Akku bereits voll?**
   4 dauerhaft leuchtende LEDs = Akku > 80%. Der Ladekreislauf hat möglicherweise gestoppt, weil der Akku voll ist oder sich in der Konstantspannungs-Erhaltungsphase befindet.

2. **Ladestatus per Software überprüfen.**
   Führen Sie ``pipower5 -ichg`` aus. Wenn es ``False`` zurückgibt, meldet die Platine, dass nicht geladen wird. Überprüfen Sie ``pipower5 -bp`` für den aktuellen Akkustand.

3. **Übertemperaturschutz aktiv.**
   Wenn die Platine unter hoher Last in einer warmen Umgebung betrieben wurde, hat der Ladechip möglicherweise 125°C überschritten und den Ladevorgang angehalten. Lassen Sie die Platine abkühlen und versuchen Sie es erneut.

4. **Eingangsspannung über Schraubklemmen zu niedrig.**
   Bei Verwendung von Schraubklemmen mit einer Spannung ≤ 6,5V ist der Ladestrom begrenzt. Verwenden Sie ≥ 9V für zuverlässiges Laden.

5. **Akkuzustand überprüfen.**
   Ein Akku, der nie vollständig geladen wird oder sehr langsam lädt, hat möglicherweise degradierte Zellen. Versuchen Sie einen anderen kompatiblen Akku (7,4V 2-Zellen Li-Ion, XH2.54 3P).


„I2C-Kommunikation fehlgeschlagen" — ``pipower5``-Befehl gibt Fehler zurück
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

**Was Sie sehen**: Die Ausführung von ``pipower5 -a`` erzeugt einen Fehler oder keine Daten.

**Überprüfen Sie Folgendes:**

1. **Ist I2C auf dem Raspberry Pi aktiviert?**
   Führen Sie ``sudo raspi-config`` aus → Interface Options → I2C → Enable.

2. **Wird das I2C-Gerät erkannt?**

   .. code-block:: shell

      sudo i2cdetect -y 1

   PiPower 5 sollte an der Adresse ``0x5a`` erscheinen. Wenn kein Gerät angezeigt wird:

   - Setzen Sie das HAT erneut auf den GPIO-Header.
   - Überprüfen Sie, ob ``i2c-dev`` geladen ist: ``lsmod | grep i2c``.
   - Überprüfen Sie, ob ``dtparam=i2c_arm=on`` in ``/boot/firmware/config.txt`` vorhanden ist.

3. **Läuft der ``pipower5``-Dienst?**

   .. code-block:: shell

      sudo systemctl status pipower5.service

   Wenn inaktiv, starten Sie ihn: ``sudo systemctl start pipower5.service``.

4. **Konflikt zwischen mehreren I2C-Geräten?**
   PiPower 5 verwendet die I2C-Adresse ``0x5a``. Stellen Sie sicher, dass kein anderes HAT oder Gerät diese Adresse verwendet. Siehe :ref:`pin_header`.

5. **Neustart.**
   Manchmal löst ein Kaltstart sowohl des Raspberry Pi als auch des PiPower 5 I2C-Bus-Probleme. Schalten Sie vollständig aus, warten Sie 10 Sekunden und schalten Sie dann ein.


„Summer stumm" — Kein Ton bei Ereignissen
++++++++++++++++++++++++++++++++++++++++++

**Was Sie sehen**: Ereignisse treten auf (Stromtrennung, niedriger Akkustand usw.), aber kein Summton.

**Überprüfen Sie Folgendes:**

1. **Summer-Lautstärke überprüfen.**

   .. code-block:: shell

      pipower5 -bzv

   Wenn 0 zurückgegeben wird, ist der Summer stummgeschaltet. Stellen Sie eine Lautstärke ein (1–10):

   .. code-block:: shell

      pipower5 -bzv 5
      sudo systemctl restart pipower5.service

2. **Überprüfen Sie, für welche Ereignisse der Summer aktiviert ist.**

   .. code-block:: shell

      pipower5 -bzo

   Stellen Sie sicher, dass das erwartete Ereignis in der Liste ist. Um ein Ereignis hinzuzufügen:

   .. code-block:: shell

      pipower5 -bzo low_battery,power_disconnected

3. **Testen Sie den Summer direkt.**

   .. code-block:: shell

      pipower5 -bzt low_battery

   Wenn Sie einen Ton hören, funktioniert die Summer-Hardware — das Problem liegt bei der Ereigniskonfiguration.


„Raspberry Pi zeigt Unterspannungswarnung"
++++++++++++++++++++++++++++++++++++++++++++

**Was Sie sehen**: Der Raspberry Pi-Desktop oder ``dmesg`` zeigt Unterspannungswarnungen an.

**Dies ist in einigen Fällen erwartetes Verhalten:**

- Bei der Stromversorgung eines Raspberry Pi über den PiPower 5 USB-A-Anschluss (anstelle des GPIO-Headers) kann der Pi eine Nicht-PD-Netzteil-Warnung melden. Diese kann bedenkenlos ignoriert werden.
- Wenn Sie den GPIO-Header verwenden und weiterhin Warnungen sehen, ist der PiPower 5-Ausgang möglicherweise stark belastet. Überprüfen Sie die Gesamtstromaufnahme Ihres Setups.

**Überprüfen Sie Folgendes:**

1. Führen Sie ``pipower5 -a`` aus und überprüfen Sie ``Output: voltage``. Sie sollte stabil bei etwa 5,2–5,3V liegen. Wenn sie unter Last unter 5,0V fällt, überschreitet die Gesamtstromaufnahme möglicherweise die 5A-Grenze.

2. Trennen Sie nicht benötigte USB-Peripheriegeräte und testen Sie erneut.

3. Wenn das Problem weiterhin besteht, ist der DC-DC-Wandler möglicherweise defekt. Kontaktieren Sie den Support.


----------------------------
Software-Diagnosebefehle
----------------------------

Das ``pipower5``-CLI-Tool ist Ihre primäre Diagnoseschnittstelle. Hier sind die nützlichsten Befehle:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Befehl
     - Was er Ihnen sagt
   * - ``pipower5 -a``
     - Vollständige Statusübersicht: Eingangs-/Ausgangsspannung, Akkustatus, Ladestatus, Abschalt-Anforderung, Tastenstatus.
   * - ``pipower5 -bp``
     - Akkustand in Prozent.
   * - ``pipower5 -ichg``
     - Ob der Akku derzeit lädt (``True`` / ``False``).
   * - ``pipower5 -ii``
     - Ob externe Stromversorgung angeschlossen ist.
   * - ``pipower5 -sp``
     - Aktueller Schwellenwert für Abschalt-Prozentsatz.
   * - ``pipower5 -sr``
     - Aktueller Status der Abschalt-Anforderung (0 = Keine, 1 = Niedriger Akkustand, 2 = Taste).
   * - ``pipower5 -pb``
     - Aktueller Status der Power-Taste.
   * - ``pipower5 -bzv``
     - Aktuelle Summer-Lautstärke.
   * - ``pipower5 -fv``
     - Firmware-Version (überprüfen Sie, ob Sie die neueste Version haben).
   * - ``pipower5 -c``
     - Vollständige Konfigurationsausgabe.
   * - ``pipower5 -pfs 60``
     - Führen Sie eine 60-sekündige Stromausfallsimulation durch, um die Akkulaufzeit zu testen.
   * - ``sudo systemctl status pipower5.service``
     - Überprüfen Sie, ob der PiPower 5-Hintergrunddienst läuft.
   * - ``cat /opt/pipower5/log``
     - Dienstprotokolle auf Fehlermeldungen prüfen.

.. tip::

   Für eine schnelle Gesundheitsprüfung führen Sie ``pipower5 -a`` aus und überprüfen Sie:

   - ``shutdown request`` ist ``0 - NONE`` (keine ausstehende Abschaltung).
   - ``battery percentage`` liegt über Ihrem ``shutdown percentage``.
   - ``Output: voltage`` liegt zwischen 5,1V und 5,4V.


--------------
Noch Probleme?
--------------

Wenn nichts davon Ihr Problem löst, sammeln Sie die folgenden Informationen, bevor Sie den Support kontaktieren:

1. **Systeminformationen**:

   .. code-block:: shell

      pipower5 -a
      pipower5 -fv
      pipower5 -c

2. **Dienstprotokolle**:

   .. code-block:: shell

      cat /opt/pipower5/log
      sudo journalctl -u pipower5.service --no-pager -n 100

3. **Hardware-Details**:
   - Raspberry Pi-Modell
   - Netzteil-Modell und Nennwattzahl
   - Akku-Typ und Alter
   - PiPower 5 DIP-Schalter-Einstellungen
   - SDSIG- und Default-ON-Jumper-Positionen
