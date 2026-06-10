Aggiornamento del firmware di PiPower5 con Raspberry Pi
===================================================================

Questa guida spiega come aggiornare il firmware di **PiPower5** su un Raspberry Pi.

**1. Scaricare** ``pipower5_update_tools`` **e installare le dipendenze**

.. code-block:: shell

   git clone https://github.com/sunfounder/pipower5_update_tools.git --depth 1

   sudo pip3 install blessed --break
   sudo pip3 install smbus2 --break

**2. Verificare la presenza di aggiornamenti**

.. code-block:: shell

   cd pipower5_update_tools
   git pull

**3. Eseguire lo strumento di aggiornamento**

.. code-block:: shell

   python3 run.py

**4. Arrestare il servizio se richiesto**

Durante l'esecuzione di ``pipower5_update_tools``, potrebbe essere richiesto di arrestare ``pipower5.service``. Premere ``Y`` per arrestare il servizio.

.. image:: img/upd_frw_1.png

**5. Selezionare** ``Update Firmware``

Scegliere **Update Firmware**. Il Raspberry Pi invierà un comando che porta PiPower5 in **modalità BOOT**.

.. image:: img/upd_frw_2.png

**6. Verificare la modalità BOOT**

Una volta entrati con successo in modalità BOOT, i **due LED centrali** su PiPower5 lampeggeranno alternativamente, indicando che la modalità BOOT è attiva.

.. image:: img/upd_frw_3.png

**7. Scegliere il file firmware**

Selezionare un file firmware in formato ``.bin`` e premere ``Invio`` per avviare la scrittura.

.. image:: img/upd_frw_4.png

**8. Completare l'aggiornamento**

Dopo il completamento del flashing, selezionare **Restart**.
PiPower5 si riavvierà e inizierà a eseguire il nuovo firmware.

.. image:: img/upd_frw_5.png

----------------------------------------------------------------

**Ripristinare il firmware di fabbrica**

Se è necessario tornare al firmware di fabbrica, utilizzare l'opzione **Restore Factory Firmware** in ``pipower5_update_tools``.
Questo ricaricherà il firmware memorizzato nella partizione di fabbrica e ripristinerà la versione originale.

.. image:: img/upd_frw_6.png


----------------------------------------------------------------

**Forzare la modalità BOOT**

Se non si riesce ad entrare normalmente in modalità BOOT, è possibile forzarla:

1. Spegnere PiPower5.
2. Cortocircuitare il **pin Boot 1**.
3. Accendere il dispositivo.

PiPower5 si avvierà direttamente in modalità BOOT.

.. image:: img/upd_frw_7.png

Per uscire dalla modalità BOOT, tenere premuto il pulsante di accensione per due secondi.
PiPower5 si riavvierà quindi in modalità normale.

.. image:: img/upd_frw_8.png

----------------------------------------------------------------

**Risoluzione dei problemi**


Ecco alcuni problemi comuni che si possono incontrare durante il processo di aggiornamento e le relative soluzioni:

- **Dispositivo non rilevato**

  - Provare a riavviare sia il Raspberry Pi che PiPower5, quindi eseguire nuovamente lo strumento di aggiornamento.

- **Impossibile entrare in modalità BOOT**

  - Assicurarsi che ``pipower5.service`` sia arrestato prima dell'aggiornamento.
  - Se la modalità BOOT automatica fallisce, utilizzare il metodo **Forzare la modalità BOOT** (cortocircuitare il pin Boot 1).

- **Processo di aggiornamento bloccato o flashing fallito**

  - Verificare che il file firmware sia in formato ``.bin``.
  - Eseguire nuovamente lo strumento di aggiornamento e riprovare.
  - Utilizzare un'alimentazione stabile per evitare interruzioni durante il flashing.

- **Aggiornamento del firmware completato, ma il dispositivo non funziona correttamente**

  - Ripristinare il firmware di fabbrica utilizzando lo strumento integrato.
  - Se il problema persiste, verificare che il file firmware corrisponda alla propria versione di PiPower5.
