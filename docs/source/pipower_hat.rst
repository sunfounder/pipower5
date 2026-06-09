PiPower 5 HAT
======================

.. interface:

Übersicht der Schnittstellen
-----------------------------

.. image:: img/pipower5_ov.png
  :width: 100%



1. **USB Type-C Stromeingang**

   - Externer Stromeingang zur gleichzeitigen Versorgung des Raspberry Pi und zum Laden des Akkus.
   - Unterstützt das **USB Power Delivery (PD)-Protokoll**, Eingangsbereich **5V–15V**.

2. **Stromeingangswahl (DIP-Schalter)**

   - Ermöglicht die Auswahl verschiedener Eingangsstromprofile für flexible Konfiguration.

3. **Default-ON-Jumper**

   - Legt fest, ob das System beim Anschließen der externen Stromversorgung automatisch eingeschaltet werden soll, während das Gerät ausgeschaltet ist.
   - ON = Automatisches Einschalten aktiviert, OFF = Manueller Start erforderlich.

4. **SDSIG (Shutdown-Signal)**

   - Bietet Shutdown-Erkennung für den Raspberry Pi.
   - Bei Brückung auf **PI3V3** funktioniert es mit Raspberry Pi 4 und Pi 5.
   - Bei Verbindung mit **Pin 26** unterstützt es Pi 3 und Pi Zero.
   - Nach korrekter Konfiguration trennt PiPower5 automatisch die Stromversorgung, sobald der Raspberry Pi herunterfährt.

5. **PWR-LED (Ausgangsstatus-Anzeige)**

   - Leuchtet, wenn der Systemausgang aktiv ist.

6. **BAT-LED (Akkustatus-Anzeige)**

   - Leuchtet, wenn das System über den Akku betrieben wird.
   - Eine Erinnerung zur Überwachung des Akkuverbrauchs bei Betrieb ohne externe Stromversorgung.

7. **Power-Taste**

   - **Einzelnes Drücken**: Ausgangsstrom aktivieren.
   - **Langes Drücken (2 Sekunden)**: Sendet eine sichere Shutdown-Anforderung über I²C.
   - **Langes Drücken (5 Sekunden)**: Erzwingt ein sofortiges Ausschalten (Hard-Shutdown).
   - **Anpassbar**: Einfach- und Doppelklick-Aktionen können per Software neu konfiguriert werden.

8. **Externer Power-Button-Anschluss (ZH1.5 2P)**

   - Ermöglicht den Anschluss einer externen physischen Power-Taste.

9. **Externer Power-Button-Header (2,54mm)**

   - Eine alternative lötbare Header-Option für den Anschluss einer externen Power-Taste.

10. **Akku-Status-LEDs**

    - Zeigen die verbleibende Akkukapazität und den Ladestatus an.
    - Hinweis: Auch bei ausgeschaltetem System bleiben die LEDs während des Ladevorgangs aktiv, bis der Akku vollständig geladen ist.

11. **I²C-Schnittstelle (SH1.0 4P)**

    - Kompatibel mit **Qwiic**- und **STEMMA QT**-Ökosystemen.
    - Wird für die Kommunikation mit dem integrierten Mikrocontroller und externen Peripheriegeräten verwendet.

12. **I²C-Schnittstelle (1x4P 2,54mm Header)**

    - Alternative I²C-Ausführung mit **3V3 Stromausgang**, konfigurierbar als Dauerstrom oder geschaltet.

13. **I²C-Stromauswahl-Jumper**

    - **PERM**: 3V3-Strom ist immer an, wenn externe Stromversorgung angeschlossen ist.
    - **SHUT (Standard)**: 3V3-Strom wird beim Herunterfahren des Systems automatisch abgeschaltet.

14. **USB Type-A Ausgangsanschluss**

    - Bietet **geregelten 5V-Ausgang**, geeignet zur Stromversorgung von Peripheriegeräten oder anderen Geräten.
    - Bei Stromversorgung eines Raspberry Pi kann eine Nicht-PD-Netzteil-Warnung auftreten, die bedenkenlos ignoriert werden kann.

15. **2x4P 2,54mm Stromausgangs-Header**

    - Zusätzlicher 5V-Ausgang für externe Module oder SBCs.

16. **Raspberry Pi GPIO-Header (Buchsenleiste)**

    - Direkte Schnittstelle für Raspberry Pi, die Strom, I²C und andere Signale durchleitet.
    - Vollständig kompatibel mit der Raspberry Pi-Pinbelegung.

17. **Raspberry Pi GPIO-Header (Stiftleisten-Breakout)**

    - Führt Raspberry Pi GPIO-Pins für das Stapeln von HATs oder externe Erweiterungen heraus.
    - **Hinweis**: I²C-Leitungen und Pin 26 sind bereits durch PiPower5-Funktionen belegt.
    - Sie können auch ein GPIO-Verlängerungskabel (von der Unterseite des Seitenteils) anschließen, um auf einem Breadboard zu experimentieren.

18. **Akku-Anschluss (XH2.54 3P)**

    - Akku-Anschlussschnittstelle.
    - Pin-Reihenfolge (von links nach rechts): Minus, Mittelpunkt (zwischen zwei Zellen), Plus.
    - Ausgelegt für **7,4V (2-Zellen) Li-Ion/LiPo-Akkus**.

19. **Verpolungs-Warn-LEDs**

    - Zwei rote LEDs leuchten auf, wenn der Akku verpolt angeschlossen ist, und warnen vor falscher Installation.

20. **Schraubklemmen für Akku & Eingangsstrom**

    - Alternative Anschlussmethode für externe Akkus und Stromquellen.
    - Unterstützt **5V–15V externen Eingang** (empfohlen: >9V).
    - Akku-Unterstützung: **Nur 2 x 3,7V Li-Ion / LiPo-Zellen** (NICHT kompatibel mit LiFePO₄-Akkus).


Technische Daten
-----------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 20 20

   * - Parameter
     - Minimum
     - Typisch
     - Maximum
     - Einheit
   * - Akku-Shutdown-Strom
     - \-
     - 60
     - \-
     - µA
   * - Akku-Ruhestrom
     - \-
     - 25
     - \-
     - mA
   * - DC-DC Ausgangsspannung
     - 5,1957
     - 5,2855
     - 5,3766
     - V
   * - DC-DC Übertemperaturschutz
     - \-
     - 150
     - \-
     - ℃
   * - Akku-Ladeleistung
     - \-
     - \-
     - 20
     - W
   * - Lade-Übertemperaturschutz
     - \-
     - 125
     - \-
     - ℃
   * - Balancier-Widerstand
     - \-
     - 60
     - \-
     - Ω
   * - Balancier-Aktivierungsspannung
     - \-
     - 4,2
     - \-
     - V


.. _power_input:

Stromeingang
-------------

.. image:: img/power_input.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

Bei Verwendung des Raspberry Pi 5 wird empfohlen, ein USB-PD-Netzteil oder ein DC-Netzteil mit einer Mindestausgangsleistung von 32W zu verwenden. Andernfalls kann der Akku in Zeiten hohen Stromverbrauchs möglicherweise nicht richtig geladen werden oder sogar seine Ladung aufgrund unzureichender Stromversorgung verlieren.

Sie können die **BAT-LED**-Anzeige überwachen, um den Akkustatus zu überprüfen. Wenn die externe Stromversorgung ausreichend ist, sollte die BAT-LED ausgeschaltet bleiben, was anzeigt, dass sich der Akku im Standby-Modus befindet und nicht entladen wird. Wenn die BAT-LED aufleuchtet, bedeutet dies, dass der Akku das Gerät mit Strom versorgt, möglicherweise aufgrund unzureichender oder getrennter externer Stromversorgung. Längeres Leuchten der BAT-LED kann zu übermäßiger Akkuentladung führen, wodurch der Akku bei Stromausfällen nicht mehr als unterbrechungsfreie Stromversorgung (USV) fungieren kann. Stellen Sie sicher, dass Sie eine Stromquelle verwenden, die den erforderlichen Spezifikationen entspricht, um solche Szenarien zu vermeiden.




.. image:: img/bat_led.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>


**Strompfad**

Der PiPower 5 integriert Strompfad-Management, das automatische Umschaltung der Stromquelle ermöglicht, um den Akkuverschleiß zu minimieren und eine unterbrechungsfreie Stromversorgung zu gewährleisten. Die wichtigsten Funktionen umfassen:

- Wenn eine externe Stromquelle angeschlossen ist, wird der 5V-Ausgang über eine Abwärtsschaltung von der externen Quelle versorgt. Der Ausgang kann über einen Schalter ausgeschaltet werden. Wenn die Bedingungen es zulassen, kann die externe Stromquelle den Akku gleichzeitig laden (siehe Abschnitt „Ladestrom" für Details).
- Bei Trennung der externen Stromquelle schaltet das System sofort über eine Abwärtsschaltung auf Akkustrom um. Dieser nahtlose Übergang stellt sicher, dass das System bei Stromunterbrechungen normal weiterarbeitet.

Sie können die BAT-LED-Anzeige überprüfen, um zu bestätigen, ob der Akku derzeit das System versorgt.




**Ladestrom**

Der Ladestrom unterliegt zwei Arten von Begrenzungen:

.. note::

   Der Ladestrom wird sowohl durch die „Ladebegrenzung der Schraubklemmen-Stromversorgung" als auch durch die „Ladeleistungs-Auswahlbegrenzung" bestimmt und durch den kleineren der beiden Werte begrenzt.

1. Ladebegrenzung der Schraubklemmen-Stromversorgung

   Bei Stromversorgung über den Schraubklemmen-Stromeingang wird der Ladestrom automatisch basierend auf der Eingangsspannung angepasst, wie unten dargestellt:

   .. list-table::
      :header-rows: 1

      * - Eingangsspannung (VBUS)
        - Maximaler Ladestrom
      * - 4,5 < VBUS ≤ 6,5V
        - 3A
      * - 6,5 < VBUS ≤ 9,5V
        - 2A
      * - 9,5 < VBUS ≤ 13,5V
        - 1,5A
      * - 13,5 < VBUS ≤ 16,5V
        - 2A

2. Ladeleistungs-Auswahlbegrenzung

   Ein 2-Positionen DIP-Schalter auf der Platine ermöglicht die Auswahl verschiedener Ladeleistungsstufen. Die entsprechende Zuweisung von Ladeleistung und Ausgangsleistung für jede Einstellung ist wie folgt:

   .. image:: img/power_selector.png
     :width: 50%
     :align: center

   .. list-table::
      :header-rows: 1

      * - Ladeauswahl 1
        - Ladeauswahl 2
        - Ladeleistung
      * - 0
        - 0
        - 5W
      * - 1
        - 0
        - 10W
      * - 0
        - 1
        - 15W
      * - 1
        - 1
        - 20W


**So wählen Sie die Ladeleistung**

Die Formel lautet:

*Kapazität der Stromversorgung = Benötigte Leistung des Raspberry Pi + Ladeleistung*

Wir empfehlen, den Strombedarf des Raspberry Pi mit **20W bis 25W** zu schätzen.

- Wenn Sie ein **30W-Netzteil** verwenden, stellen Sie die Ladeleistung auf **10W** oder **5W** ein.
- Wenn Sie ein **45W-Netzteil** verwenden, können Sie die Ladeleistung bedenkenlos auf **20W** einstellen.

Wenn Sie mit dem Strombedarf Ihres Raspberry Pi vertraut sind, können Sie eine höhere Ladeleistung einstellen, solange Sie genügend Spielraum für gelegentliche Stromspitzen lassen.

⚠️ Seien Sie vorsichtig: Unzureichende Stromversorgung kann dazu führen, dass der Raspberry Pi unerwartet herunterfährt.




**Ladevorgang**

- Wenn die Akkuspannung ``VBAT <= 2,5V`` beträgt, führt das System eine Erhaltungsladung mit niedrigem Strom von etwa 50 mA durch.
- Wenn ``2,5V < VBAT <= VTRKL``, wird die Erhaltungsladung fortgesetzt und der Akkuladestrom erhöht sich auf etwa 200 mA.
- Wenn ``VTRKL < VBAT < VCV``, schaltet das System auf Konstantstromladung um und liefert einen voreingestellten konstanten Strom an den Akku.
- Sobald ``VBAT = VCV`` und die Akkuspannung sich dem vollständig geladenen Niveau nähert, nimmt der Ladestrom allmählich ab und geht in Konstantspannungsladung über.
- Während der Konstantspannungsladung, wenn der Ladestrom unter ``ISTOP`` fällt und die Akkuspannung nahe der Konstantspannungsschwelle liegt, stoppt der Ladevorgang und der Akku geht in den vollständig geladenen Zustand über.
- Im vollständig geladenen Zustand überwacht das System kontinuierlich die Akkuspannung. Wenn die Spannung unter ``VRCH`` fällt, wird der Ladevorgang automatisch wieder aufgenommen.

**Schutzfunktionen**

Der PiPower 5 bietet umfassende Schutzfunktionen, einschließlich Eingangsunterspannungs- und Überspannungsschutz sowie Überhitzungsschutz für den Ladechip und den DC-DC-Wandler. Diese Funktionen gewährleisten einen stabilen und zuverlässigen Systembetrieb.

**Lade-Balancierung**

Der integrierte Lade-Balancier-Chip aktiviert einen 60Ω-Widerstand, um den Akku mit niedrigem Strom zu entladen, wenn er erkennt, dass die Spannung einer einzelnen Zelle 4,2V überschreitet. Diese Funktion hilft, das Spannungsgleichgewicht zwischen den Zellen aufrechtzuerhalten.

**Temperaturschutz**

Der Ladevorgang wird automatisch angehalten, wenn die interne Temperatur des Ladechips 125°C überschreitet. Ebenso deaktiviert der DC-DC-Chip den Ausgang, wenn seine interne Temperatur 150°C überschreitet.

.. _power_button:

Power-Taste
----------------

.. image:: img/power_button.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

Integrierte Power-Taste zur Steuerung der Stromversorgung der Platine:

* **Einzelnes Drücken**: Aktiviert den Ausgang.
* **2 Sekunden gedrückt halten, bis die mittleren beiden Akku-LEDs aufleuchten, dann loslassen**: Sendet eine Shutdown-Anforderung über I2C.
* **Mehr als 5 Sekunden gedrückt halten**: Schaltet den Ausgang direkt aus.


.. _battery_indicators:

Akkustatus-Anzeigen
--------------------------------

Vier integrierte LEDs zeigen den Akkustand und Ladestatus an.

.. note::

   Wenn das Gerät während des Herunterfahrens lädt, zeigt die Anzeige weiterhin den Ladestatus an, bis der Ladevorgang abgeschlossen ist.




.. image:: img/battery_indicator.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

* **4 LEDs leuchten**: Akku >80%
* **3 LEDs leuchten**: 60%< Akku <80%
* **2 LEDs leuchten**: 40%< Akku <60%
* **1 LED leuchtet**: 20%< Akku <40%
* **Erste LED blinkt**: Akku <20%
* **LEDs leuchten nacheinander im Zyklus**: Ladevorgang läuft
* **Mittlere zwei LEDs blinken**: Warten auf Shutdown-Signal
* **Alle LEDs aus**: Keine Stromversorgung oder im Schlafmodus

.. _battery_connector:

Akku-Anschluss
------------------------
VH3.96 2P Akku-Anschluss und Schraubklemmen-Akku-Anschluss.

.. image:: img/battery_pin.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

.. _cap_btn:

Externer Power-Button-Anschluss & Header
--------------------------------------------

.. image:: img/btn_jumper.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

Dieser Anschluss oder Header ist für den Anschluss einer externen Power-Taste vorgesehen. Schließen Sie einen Taster, wie z.B. einen taktilen Schalter oder einen Metallknopf im Vintage-Stil, an die Jumper-Pins an. Die beiden Leitungen der Taste können in beliebiger Richtung an die Pins des Jumpers angeschlossen werden, da keine Polarität erforderlich ist. Nach dem Anschluss können Sie die externe Taste genauso wie die integrierte Power-Taste verwenden.

.. _cap_sdsig:

SDSIG-Jumper
------------

.. image:: img/sdsig_jumper.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

Bietet Shutdown-Erkennung für den Raspberry Pi.

* Bei Brückung auf PI3V3 funktioniert es mit Raspberry Pi 4 und Pi 5.
* Bei Verbindung mit Pin 26 unterstützt es Pi 3 und Pi Zero.

Nach korrekter Konfiguration trennt PiPower5 automatisch die Stromversorgung, sobald der Raspberry Pi herunterfährt.

.. _cap_onoff:

Default-ON/OFF-Jumper
----------------------

.. image:: img/default_jumper.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

Dieser Jumper wird verwendet, um auszuwählen, ob der USB-Stromausgang nach einem Shutdown standardmäßig aktiviert ist. Verwenden Sie die Jumper-Kappe, um die mit ON oder OFF beschrifteten Pins zu verbinden und die Auswahl zu treffen.

* Wenn die Jumper-Kappe links positioniert und mit OFF verbunden ist, wird das Einstecken der USB-Stromversorgung nach einem Shutdown den Ausgang nicht aktivieren.
* Wenn die Jumper-Kappe rechts positioniert und mit ON verbunden ist, wird das Einstecken der USB-Stromversorgung nach einem Shutdown den Ausgang aktivieren.

Diese Funktion wird typischerweise für Geräte verwendet, die automatisch starten müssen, wie z.B. persönliche Server. Wenn beispielsweise ein Stromausfall auftritt, übernimmt PiPower 5 die Stromversorgung des Raspberry Pi und gewährleistet ein sicheres Herunterfahren. Sobald die Stromversorgung wiederhergestellt ist, schaltet PiPower 5 den Raspberry Pi automatisch ein, sodass kein manuelles Eingreifen erforderlich ist.

.. _pin_header:

Stiftleisten für Raspberry Pi
-----------------------------------

Die Stiftleiste ist für den direkten Anschluss an einen Raspberry Pi ausgelegt, einschließlich I2C-Kommunikation und Stromversorgung.




.. image:: img/pin_header.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

Der Header unterstützt das Stapeln zusätzlicher HATs. Beachten Sie jedoch, dass die I2C-Pins und Pin 26 bereits verbunden sind und möglicherweise sorgfältig verwaltet werden müssen, um Konflikte zu vermeiden.

.. list-table::
   :widths: 15 15
   :header-rows: 1

   * - Raspberry Pi
     - MCU auf der Platine
   * - SDA
     - SDA
   * - SCL
     - SCL
   * - GPIO26
     - SHUTDOWN
   * - ID_SD
     - ID_EEPROM SDA
   * - ID_SC
     - ID_EEPROM SCL

I2C-Kommunikation
-------------------------------

.. image:: img/i2c.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

I2C-Adresse: 0x5C

Der integrierte Mikrocontroller sammelt verschiedene Signale von der Platine und speichert sie in Registern. Diese Signale können über I2C mithilfe der folgenden Registertabellen abgerufen werden.

.. raw:: html

   <style>
       .custom-register-table {
           border-collapse: collapse;
           width: 100%;
           margin: 20px 0;
           font-size: 14px;
           text-align: left;
       }
       .custom-register-table th, .custom-register-table td {
           border: 1px solid #ddd;
           padding: 8px;
       }
       .custom-register-table th {
           background-color: #f4f4f4;
           font-weight: bold;
       }
       .custom-register-table tr:nth-child(even) {
           background-color: #f9f9f9;
       }
       .custom-register-table tr:hover {
           background-color: #f1f1f1;
       }
       .custom-register-table caption {
           font-size: 16px;
           font-weight: bold;
           margin-bottom: 10px;
           text-align: center;
       }
   </style>

   <table class="custom-register-table">
       <caption>Registertabelle</caption>
       <thead>
           <tr>
               <th>Name</th>
               <th>Adresse</th>
               <th>Datenlänge</th>
               <th>Datentyp</th>
               <th>Einheit</th>
               <th>Beschreibung</th>
           </tr>
       </thead>
       <tbody>
           <tr>
               <td>Eingangsspannung</td>
               <td>0</td>
               <td>2</td>
               <td>u16</td>
               <td>mV</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Eingangsstrom</td>
               <td>2</td>
               <td>2</td>
               <td>u16</td>
               <td>mA</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Ausgangsspannung</td>
               <td>4</td>
               <td>2</td>
               <td>u16</td>
               <td>mV</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Ausgangsstrom</td>
               <td>6</td>
               <td>2</td>
               <td>u16</td>
               <td>mA</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Akkuspannung</td>
               <td>8</td>
               <td>2</td>
               <td>u16</td>
               <td>mV</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Akkustrom</td>
               <td>10</td>
               <td>2</td>
               <td>i16</td>
               <td>mA</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Akkustand in Prozent</td>
               <td>12</td>
               <td>1</td>
               <td>u8</td>
               <td>%</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Akkukapazität</td>
               <td>13</td>
               <td>2</td>
               <td>u16</td>
               <td>mAh</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Stromquelle</td>
               <td>15</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>0: Akku liefert keinen Strom.<br> 1: Akku liefert Strom.</td>
           </tr>
           <tr>
               <td>USB-Verbindungsstatus</td>
               <td>16</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>0: USB nicht angeschlossen.<br> 1: USB angeschlossen.</td>
           </tr>
           <tr>
               <td>RESERVIERT</td>
               <td>17</td>
               <td>1</td>
               <td>-</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Ladestatus</td>
               <td>18</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>0: Lädt nicht.<br> 1: Lädt.</td>
           </tr>
           <tr>
               <td>Lüfterleistung</td>
               <td>19</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Lüfterleistungsstufe (0–100).</td>
           </tr>
           <tr>
               <td>Abschalt-Anforderung</td>
               <td>20</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>1: Ausgelöst durch niedrigen Akkustand.<br>2: Ausgelöst durch Drücken der Power-Taste.</td>
           </tr>
           <tr>
               <td>Firmware-Version (Major)</td>
               <td>128</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Firmware-Version (Minor)</td>
               <td>129</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Firmware-Version (Patch)</td>
               <td>130</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Reset-Code</td>
               <td>131</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>MCU-Reset-Ursachencode.</td>
           </tr>
           <tr>
               <td>RTC Jahr</td>
               <td>132</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RTC Monat</td>
               <td>133</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RTC Tag</td>
               <td>134</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RTC Stunde</td>
               <td>135</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RTC Minute</td>
               <td>136</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RTC Sekunde</td>
               <td>137</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RTC Sub-Sekunde</td>
               <td>138</td>
               <td>1</td>
               <td>u8</td>
               <td>1/128 s</td>
               <td>RTC Sub-Sekunde (1/128 Sekunde).</td>
           </tr>
           <tr>
               <td>Dauerbetrieb-Funktion</td>
               <td>139</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>0: Aktiviert.<br> 1: Deaktiviert.</td>
           </tr>
           <tr>
               <td>Platinen-ID</td>
               <td>140</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Platinen-Identifikation: <br> 0: Pironman U1.<br> 1: Pironman 4.<br> 2: PiPower 3.<br>4: PiPower 5.</td>
           </tr>
           <tr>
               <td>RESERVIERT</td>
               <td>141</td>
               <td>1</td>
               <td>-</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RESERVIERT</td>
               <td>142</td>
               <td>1</td>
               <td>-</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Abschalt-Prozentsatz</td>
               <td>143</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Aktueller Schwellenwert für Abschaltung bei niedrigem Akkustand (Prozentsatz).</td>
           </tr>
           <tr>
               <td>RESERVIERT</td>
               <td>144</td>
               <td>1</td>
               <td>-</td>
               <td>-</td>
               <td>-</td>
           </tr>
       </tbody>
   </table>


   <table class="custom-register-table">
       <caption>Register-Einstellungstabelle</caption>
       <thead>
           <tr>
               <th>Name</th>
               <th>Adresse</th>
               <th>Datenlänge</th>
               <th>Datentyp</th>
               <th>Einheit</th>
               <th>Beschreibung</th>
           </tr>
       </thead>
       <tbody>
           <tr>
               <td>Lüfterleistung</td>
               <td>0</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Lüftergeschwindigkeit einstellen (0–100).</td>
           </tr>
           <tr>
               <td>RTC Jahr</td>
               <td>1</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>RTC Jahr einstellen.</td>
           </tr>
           <tr>
               <td>RTC Monat</td>
               <td>2</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>RTC Monat einstellen.</td>
           </tr>
           <tr>
               <td>RTC Tag</td>
               <td>3</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>RTC Tag einstellen.</td>
           </tr>
           <tr>
               <td>RTC Stunde</td>
               <td>4</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>RTC Stunde einstellen.</td>
           </tr>
           <tr>
               <td>RTC Minute</td>
               <td>5</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>RTC Minute einstellen.</td>
           </tr>
           <tr>
               <td>RTC Sekunde</td>
               <td>6</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>RTC Sekunde einstellen.</td>
           </tr>
           <tr>
               <td>RTC Sub-Sekunde</td>
               <td>7</td>
               <td>1</td>
               <td>u8</td>
               <td>1/128 s</td>
               <td>RTC Sub-Sekunde einstellen.</td>
           </tr>
           <tr>
               <td>RTC-Einstellung</td>
               <td>8</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>RTC-Einstellung aktivieren: <br> 1: Aktiviert.</td>
           </tr>
           <tr>
               <td>Abschalt-Prozentsatz</td>
               <td>9</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Schwellenwert für Abschaltung bei niedrigem Akkustand einstellen (0–100).</td>
           </tr>
           <tr>
               <td>Ausschalt-Prozentsatz</td>
               <td>10</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Schwellenwert für Ausschalten bei niedrigem Akkustand einstellen (0–100).</td>
           </tr>
       </tbody>
   </table>
