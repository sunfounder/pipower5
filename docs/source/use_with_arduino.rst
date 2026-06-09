Arduino
===================================

Wenn Sie PiPower 5 zur Stromversorgung Ihres Arduino-Boards verwenden, können Sie das Arduino an den USB-Typ-A-Ausgang von PiPower 5 anschließen oder zwei Jumper-Kabel verwenden. Verbinden Sie die I2C-Schnittstelle des Boards über einen Jumper.

.. If no operation is required before powering off, directly connect the **SDSIG** jumper cap to the GND. If operations are necessary before shutdown, remove the jumper cap and connect the intermediate wire to an IO port on the Arduino to notify PiPower 5 that it can safely power off.

Wir stellen eine Bibliothek zur Verfügung, mit der Sie Eingangs- und Ausgangsspannungen, Akkuspannung und -prozentsatz, Stromquelle, Ladestatus und andere interne Daten überwachen können.

#. Öffnen Sie in der Arduino IDE den **Bibliotheksverwalter**, suchen Sie nach ``SunFounderPowerControl`` und laden Sie die Bibliothek herunter und installieren Sie sie.

   .. image:: img/install_arduino_lib.png
      :width: 100%

#. Nach der Installation können Sie zu **Datei** -> **Beispiele** -> **SunFounderPowerControl** -> **PiPower 5** navigieren, wo Sie vier Beispiele finden.

   .. image:: img/arduino_lib_example.png
      :width: 100%

   * ``read_all``: Verwenden Sie dieses Beispiel, wenn Sie alle Daten auf einmal lesen und einzeln verarbeiten müssen.
   * ``read_individual``: Wenn Sie nur bestimmte Daten lesen müssen, bietet dieses Beispiel Anleitungen zum individuellen Datenabruf.
   * ``set_shutdown_percentage``: Dieses Beispiel zeigt, wie Sie einen Abschalt-Akkuprozentsatz einstellen können. Diese Funktion sendet ein Shutdown-Signal an den Host, wenn der Akku nicht geladen wird und unter den eingestellten Prozentsatz fällt. Nachdem der Host heruntergefahren ist, wird die Stromversorgung erst nach Erhalt eines Ausschaltsignals getrennt. Wird normalerweise mit SBCs wie Raspberry Pi verwendet. Entfernen Sie bei Mikrocontrollern die **SDSIG**-Jumper-Kappe und verbinden Sie das mittlere Kabel mit einem Pin. Nach dem sicheren Herunterfahren nach Erhalt des Shutdown-Signals ziehen Sie diesen Pin auf High, um PiPower 5 auszuschalten.
   * ``shutdown_when_request``: Dieses Beispiel zeigt, wie Sie Operationen nach Erhalt eines Shutdown-Signals behandeln. Entfernen Sie die **SDSIG**-Jumper-Kappe und verbinden Sie das mittlere Kabel mit einem Pin.

#. Wählen Sie eines der Beispiele aus und laden Sie es auf Ihr Board hoch.

   .. note::

      Bei einigen Boards, bei denen I2C geändert werden kann, müssen Sie den Code ``Wire.begin()`` ändern, wenn Sie die I2C-Pins ändern müssen.

Arduino-Bibliothek API-Dokumentation: https://github.com/sunfounder/arduino_spc?tab=readme-ov-file#api
