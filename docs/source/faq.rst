.. note::

    Hallo, willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauchen Sie tiefer in Raspberry Pi, Arduino und ESP32 mit gleichgesinnten Enthusiasten ein.

    **Warum beitreten?**

    - **Experten-Support**: Lösen Sie Probleme nach dem Kauf und technische Herausforderungen mit Hilfe unserer Community und unseres Teams.
    - **Lernen & Teilen**: Tauschen Sie Tipps und Tutorials aus, um Ihre Fähigkeiten zu verbessern.
    - **Exklusive Vorschauen**: Erhalten Sie frühzeitigen Zugang zu neuen Produktankündigungen und Vorab-Einblicken.
    - **Spezielle Rabatte**: Genießen Sie exklusive Rabatte auf unsere neuesten Produkte.
    - **Festliche Aktionen und Gewinnspiele**: Nehmen Sie an Gewinnspielen und Feiertagsaktionen teil.

    👉 Bereit, mit uns zu entdecken und zu gestalten? Klicken Sie [|link_sf_facebook|] und treten Sie noch heute bei!

.. _faq:

FAQ
===

So installieren Sie PiPower 5 neu
----------------------------------

Wenn PiPower 5 nicht richtig funktioniert und Sie eine saubere Neuinstallation durchführen möchten, befolgen Sie diese Schritte:

**1. Deinstallieren Sie die aktuelle Installation:**

.. code-block:: shell

   cd ~/pipower5
   sudo python3 install.py --uninstall

**2. Neuinstallation aus dem Quellcode:**

.. code-block:: shell

   git clone https://github.com/sunfounder/pipower5
   cd pipower5
   sudo python3 install.py

**3. Starten Sie den Raspberry Pi neu, wenn Sie dazu aufgefordert werden.**

Überprüfen Sie nach dem Neustart die Installation:

.. code-block:: shell

   pipower5 -a
   sudo systemctl status pipower5.service

.. tip::

   Wenn das Verzeichnis ``~/pipower5`` von der ursprünglichen Installation nicht mehr existiert, überspringen Sie den Deinstallationsschritt und gehen Sie direkt zum Neuinstallationsschritt.


Dashboard zeigt „Database Required" oder keine Daten
-----------------------------------------------------

**Was Sie sehen**: Das Web-Dashboard öffnet sich normal in Ihrem Browser, aber alle Datenfelder sind leer oder zeigen „database required".

**Was das normalerweise bedeutet**: Dies ist selten ein Hardware-Problem. In den meisten Fällen hat das InfluxDB-Backend ein Konfigurationsproblem — eine beschädigte Datenbank, einen fehlenden Bucket oder ein abgelaufenes Token.

**Überprüfen Sie Folgendes, in dieser Reihenfolge:**

1. **Überprüfen Sie, ob der PiPower 5-Dienst läuft:**

   .. code-block:: shell

      sudo systemctl status pipower5

   Wenn der Dienst nicht aktiv ist, starten Sie ihn:

   .. code-block:: shell

      sudo systemctl start pipower5

2. **Überprüfen Sie, ob der InfluxDB-Bucket existiert:**

   .. code-block:: shell

      sudo influx bucket list

   Suchen Sie in der Ausgabe nach einem Bucket namens ``pipower5``. Falls dieser fehlt, muss die Datenbank neu erstellt werden.

3. **Überprüfen Sie die Dienstprotokolle auf Fehler:**

   .. code-block:: shell

      journalctl -u pipower5 -n 50

   Achten Sie auf Fehlermeldungen im Zusammenhang mit InfluxDB, wie z.B.:

   - ``unauthorized`` oder ``token`` — deutet auf ein Problem mit dem Authentifizierungstoken hin.
   - ``bucket not found`` — der Datenbank-Bucket fehlt.
   - ``connection refused`` — InfluxDB läuft nicht.

4. **Wenn InfluxDB selbst ausgefallen ist**, starten Sie es neu:

   .. code-block:: shell

      sudo systemctl restart influxdb
      sudo systemctl restart pipower5

.. note::

   Wenn InfluxDB manuell installiert oder von einer älteren Version migriert wurde, können sich Konfigurationspfade oder Authentifizierungstoken geändert haben. In diesem Fall wird eine saubere Neuinstallation von PiPower 5 (siehe oben) auch das InfluxDB-Setup neu initialisieren.
