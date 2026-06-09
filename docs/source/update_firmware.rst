PiPower5-Firmware mit Raspberry Pi aktualisieren
===================================================================

Diese Anleitung erklärt, wie Sie die Firmware von **PiPower5** auf einem Raspberry Pi aktualisieren.

**1. Laden Sie** ``pipower5_update_tools`` **herunter und installieren Sie die Abhängigkeiten**

.. code-block:: shell

   git clone https://github.com/sunfounder/pipower5_update_tools.git --depth 1

   sudo pip3 install blessed --break
   sudo pip3 install smbus2 --break

**2. Auf Updates prüfen**

.. code-block:: shell

   cd pipower5_update_tools
   git pull

**3. Update-Tool ausführen**

.. code-block:: shell

   python3 run.py

**4. Dienst bei Aufforderung stoppen**

Beim Ausführen von ``pipower5_update_tools`` werden Sie möglicherweise aufgefordert, ``pipower5.service`` zu stoppen. Drücken Sie ``Y``, um den Dienst zu stoppen.

.. image:: img/upd_frw_1.png

**5. Wählen Sie** ``Update Firmware``

Wählen Sie **Update Firmware**. Der Raspberry Pi sendet einen Befehl, der PiPower5 in den **BOOT-Modus** versetzt.

.. image:: img/upd_frw_2.png

**6. BOOT-Modus überprüfen**

Sobald der BOOT-Modus erfolgreich aktiviert ist, blinken die **zwei mittleren LEDs** auf dem PiPower5 abwechselnd, was anzeigt, dass der BOOT-Modus aktiv ist.

.. image:: img/upd_frw_3.png

**7. Firmware-Datei auswählen**

Wählen Sie eine Firmware-Datei im ``.bin``-Format und drücken Sie ``Enter``, um mit dem Schreiben zu beginnen.

.. image:: img/upd_frw_4.png

**8. Update abschließen**

Wählen Sie nach Abschluss des Flash-Vorgangs **Restart**.
PiPower5 startet neu und führt die neue Firmware aus.

.. image:: img/upd_frw_5.png

----------------------------------------------------------------

**Werks-Firmware wiederherstellen**

Wenn Sie zur Werks-Firmware zurückkehren müssen, verwenden Sie die Option **Restore Factory Firmware** in ``pipower5_update_tools``.
Dadurch wird die in der Werkpartition gespeicherte Firmware neu geladen und die ursprüngliche Version wiederhergestellt.

.. image:: img/upd_frw_6.png


----------------------------------------------------------------

**BOOT-Modus erzwingen**

Wenn Sie nicht normal in den BOOT-Modus wechseln können, können Sie ihn erzwingen:

1. Schalten Sie PiPower5 aus.
2. Schließen Sie den **Boot 1-Pin** kurz.
3. Schalten Sie das Gerät ein.

PiPower5 startet direkt im BOOT-Modus.

.. image:: img/upd_frw_7.png

Um den BOOT-Modus zu verlassen, halten Sie die Power-Taste zwei Sekunden lang gedrückt.
PiPower5 startet dann im normalen Modus neu.

.. image:: img/upd_frw_8.png

----------------------------------------------------------------

**Fehlerbehebung**


Hier sind einige häufig auftretende Probleme während des Update-Vorgangs und deren Lösungen:

- **Gerät nicht erkannt**

  - Versuchen Sie, sowohl den Raspberry Pi als auch PiPower5 neu zu starten und führen Sie das Update-Tool erneut aus.

- **BOOT-Modus konnte nicht aktiviert werden**

  - Stellen Sie sicher, dass ``pipower5.service`` vor dem Update gestoppt ist.
  - Wenn der automatische BOOT-Modus fehlschlägt, verwenden Sie die Methode **BOOT-Modus erzwingen** (Kurzschließen des Boot 1-Pins).

- **Update-Vorgang hängt oder Flash-Vorgang fehlgeschlagen**

  - Überprüfen Sie, ob die Firmware-Datei im ``.bin``-Format vorliegt.
  - Führen Sie das Update-Tool erneut aus und versuchen Sie es noch einmal.
  - Verwenden Sie eine stabile Stromversorgung, um Unterbrechungen während des Flash-Vorgangs zu vermeiden.

- **Firmware-Update abgeschlossen, aber Gerät funktioniert nicht richtig**

  - Stellen Sie die Werks-Firmware mit dem integrierten Tool wieder her.
  - Wenn das Problem weiterhin besteht, überprüfen Sie, ob die Firmware-Datei mit Ihrer PiPower5-Version übereinstimmt.
