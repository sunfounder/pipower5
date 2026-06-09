.. note::

    Hallo, willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauchen Sie tiefer in Raspberry Pi, Arduino und ESP32 mit gleichgesinnten Enthusiasten ein.

    **Warum beitreten?**

    - **Experten-Support**: Lösen Sie Probleme nach dem Kauf und technische Herausforderungen mit Hilfe unserer Community und unseres Teams.
    - **Lernen & Teilen**: Tauschen Sie Tipps und Tutorials aus, um Ihre Fähigkeiten zu verbessern.
    - **Exklusive Vorschauen**: Erhalten Sie frühzeitigen Zugang zu neuen Produktankündigungen und Vorab-Einblicken.
    - **Spezielle Rabatte**: Genießen Sie exklusive Rabatte auf unsere neuesten Produkte.
    - **Festliche Aktionen und Gewinnspiele**: Nehmen Sie an Gewinnspielen und Feiertagsaktionen teil.

    👉 Bereit, mit uns zu entdecken und zu gestalten? Klicken Sie [|link_sf_facebook|] und treten Sie noch heute bei!

SunFounder PiPower5 - Schützen Sie Ihr Gerät & Ihre Daten
================================================================================

.. * |link_PiPower_5_buy|

.. Thank you for choosing our |link_PiPower_5|.

Vielen Dank, dass Sie sich für unseren PiPower5 entschieden haben.


.. .. note::
..     This document is available in the following languages.

..         * |link_german_tutorials|
..         * |link_jp_tutorials|
..         * |link_en_tutorials|

..     Please click on the respective links to access the document in your preferred language.

.. todo: new pic

.. image:: img/PP.0.A.JPG
    :width: 400
    :align: center

PiPower 5 ist eine vielseitige USV-Lösung, die für die nahtlose Integration mit Raspberry Pi-Geräten entwickelt wurde. Sie verfügt über robustes Pfadmanagement für die Stromversorgung, Lade- und Entladefunktionen für zwei Lithium-Akkus sowie grundlegende Schutzfunktionen gegen Verpolung, Überladung und Tiefentladung.

Mit einer Ausgangsleistung von bis zu 5V/5A gewährleistet PiPower 5 eine stabile Leistung für eine Vielzahl von Geräten. Die HAT+-Konfiguration garantiert Kompatibilität mit dem Raspberry Pi 5, während zusätzliche Ausgänge, einschließlich eines USB-A-Anschlusses und eines 4x2P-Headers, Unterstützung für verschiedene Einplatinencomputer (SBCs) und Mikrocontroller-Plattformen wie Arduino, Pico und ESP32 bieten.

Ein integrierter Mikrocontroller verwaltet effizient die Stromversorgungsoperationen und ermöglicht die Echtzeitüberwachung wichtiger Parameter über I2C-Kommunikation. Zu diesen Parametern gehören Eingangsspannung, Ausgangsspannung, Akkuspannung, Akkukapazität, Status der externen Stromverbindung, Ladestatus und die aktuelle Stromquelle (Akku oder USB).

Durch die Kombination aus fortschrittlichem Akkumanagement und breiter Kompatibilität ist PiPower 5 ein unverzichtbares Werkzeug für Technikbegeisterte und Profis, die ihre Hardware-Umgebungen optimieren möchten.

**Funktionen**

* **Eingang**: 5-15V, 45W, USB Type-C PD, DC5.5-2.1
* **Ausgang**: 5V/5A über Raspberry Pi GPIO, USB Type-A und 2x4P 2,54mm Stiftleisten
* **Ladeleistung**: Bis zu 20W
* **Akku-Spezifikationen**: 7,4V 2 Zellen 18650 Li-Ion, XH2.54 3P Anschluss
* **Konfigurierbare Einstellungen über Jumper**:

  * Default-On-Jumper: Legen Sie fest, ob das Gerät beim Anschließen der Stromversorgung automatisch eingeschaltet wird.
  * Shutdown-Signal-Jumper: Aktivieren Sie die Erkennung des Ausschaltzustands des Geräts.
  * Externer Power-Button-Pin-Header: Schließen Sie einen externen Netzschalter für manuelle Stromsteuerung an.

* **Integrierte Anzeigen und Tasten**:

  * Akkustatus-Anzeige
  * Eingangsquellen-Anzeige
  * Power-Taste
  * Akku-Verpolungsanzeige
  * Ausgangsstrom-Anzeige

* **Integrierter Mikrocontroller**: 32-bit ARM Cortex-M23, mit I2C-Kommunikation

* **I2C-Kommunikationsschnittstellen**:

  * Raspberry Pi GPIO
  * SH1.0 4P (kompatibel mit Qwiic und STEMMA QT)
  * 1x4P 2,54mm Stiftleiste


.. **Table of Contents**

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Erste Schritte

   About PiPower 5 <self>
   assembly
   quick_guide

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Hardware-Übersicht

   pipower_hat
   battery

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Software-Konfiguration

   pipower5_software
   update_firmware
   use_with_python


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Anhang

   compatible_sbc
   troubleshooting
   faq


**Urheberrechtshinweis**

Alle Inhalte, einschließlich aber nicht beschränkt auf Texte, Bilder und Code in diesem Handbuch, sind Eigentum der SunFounder Company. Sie dürfen diese nur für persönliche Studien, Untersuchungen, Vergnügen oder andere nicht-kommerzielle oder gemeinnützige Zwecke verwenden, unter Einhaltung der entsprechenden Vorschriften und Urheberrechtsgesetze, ohne die gesetzlichen Rechte des Autors und der relevanten Rechteinhaber zu verletzen. Für jede Einzelperson oder Organisation, die diese ohne Genehmigung für kommerzielle Gewinne nutzt, behält sich das Unternehmen das Recht vor, rechtliche Schritte einzuleiten.
