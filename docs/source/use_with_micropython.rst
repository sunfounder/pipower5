MicroPython
==========================================================

Wir stellen eine Bibliothek zur Verfügung, mit der Sie Eingangs- und Ausgangsspannungen, Akkuspannung und -prozentsatz, Stromquelle, Ladestatus und andere interne Daten überwachen können.

Wenn Sie PiPower 5 zur Stromversorgung Ihres Raspberry Pi Pico oder ESP32-Boards verwenden, können Sie das Board über den USB-Typ-A-Ausgang oder zwei Jumper-Kabel mit PiPower 5 verbinden.

Verwenden Sie zum Anschluss der I2C-Schnittstelle von PiPower 5 einen Jumper.

.. If no operations are needed before shutting down, connect the SDSIG jumper cap directly to the GND pin. If operations are required before shutdown, remove the jumper cap and connect the intermediate wire to an I/O pin on the Raspberry Pi Pico or ESP32 board. This setup notifies the PiPower 5 that the shutdown process is complete and it can safely power off.

#. Laden Sie die Bibliothek von GitHub herunter. Sie können sie schnell über den folgenden Link herunterladen oder besuchen: https://github.com/sunfounder/micropython_spc.

   * :download:`micropython_spc <https://github.com/sunfounder/micropython_spc/archive/refs/heads/main.zip>`

#. Laden Sie nach dem Herunterladen und Entpacken den Ordner ``spc`` auf Ihr Raspberry Pi Pico oder ESP32-Board hoch. Thonny wird für diesen Zweck empfohlen.

   .. image:: img/micropython_upload.png
       :width: 100%
       :align: center

   .. raw:: html

      <br/>

#. Nachdem die Bibliothek hochgeladen wurde, können Sie sie mit den Beispielen im Ordner ``micropython_spc-main/examples/pipower5`` testen:

   * ``pipower_5_read_all.py``: Verwenden Sie dieses Beispiel, wenn Sie alle Daten lesen müssen. Es zeigt, wie Sie alle verfügbaren Daten auf einmal lesen und einzeln verarbeiten können.

   * ``pipower_5_read_individual.py``: Dieses Beispiel bietet Anleitungen zum individuellen Lesen bestimmter Daten. Verwenden Sie es, wenn Sie nur auf bestimmte Daten zugreifen müssen.

   * ``pipower_5_set_shutdown_percentage.py``: Dieses Beispiel erklärt, wie Sie den Abschalt-Akkuprozentsatz einstellen. Wenn der Akku nicht geladen wird und sein Stand unter den angegebenen Prozentsatz fällt, sendet PiPower 5 ein Shutdown-Signal an den Host. Die Stromversorgung wird erst getrennt, nachdem der Host heruntergefahren ist und ein Ausschaltsignal zurückgesendet hat.

     * Für SBCs (z.B. Raspberry Pi): Keine zusätzliche Konfiguration erforderlich.
     * Für Mikrocontroller: Entfernen Sie die **SDSIG**-Jumper-Kappe und verbinden Sie das mittlere Kabel mit einem Pin. Nach Erhalt des Shutdown-Signals und sicherem Herunterfahren ziehen Sie diesen Pin auf High, um PiPower 5 zum Ausschalten zu veranlassen.

   * ``pipower_5_shutdown_when_request.py``: Dieses Beispiel zeigt, wie Sie Operationen nach Erhalt eines Shutdown-Signals behandeln. Sie müssen die **SDSIG**-Jumper-Kappe entfernen und das mittlere Kabel mit einem Pin verbinden.

Micropython-Bibliothek API-Dokumentation: https://github.com/sunfounder/micropython_spc?tab=readme-ov-file#api
