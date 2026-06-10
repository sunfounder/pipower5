MicroPython
==========================================================

Forniamo una libreria che consente di monitorare le tensioni di ingresso e uscita, la tensione e la percentuale della batteria, la fonte di alimentazione, lo stato di carica e altri dati interni.

Se si utilizza il PiPower 5 per alimentare la scheda Raspberry Pi Pico o ESP32, è possibile collegare la scheda al PiPower 5 tramite la porta di uscita Type-A o due cavi jumper.

Per collegare l'interfaccia I2C del PiPower 5, utilizzare un ponticello.

.. If no operations are needed before shutting down, connect the SDSIG jumper cap directly to the GND pin. If operations are required before shutdown, remove the jumper cap and connect the intermediate wire to an I/O pin on the Raspberry Pi Pico or ESP32 board. This setup notifies the PiPower 5 that the shutdown process is complete and it can safely power off.

#. Scaricare la libreria da GitHub. È possibile scaricarla rapidamente utilizzando il link sottostante o visitare: https://github.com/sunfounder/micropython_spc.

   * :download:`micropython_spc <https://github.com/sunfounder/micropython_spc/archive/refs/heads/main.zip>`

#. Dopo il download e l'estrazione, caricare la cartella ``spc`` sulla scheda Raspberry Pi Pico o ESP32. Si consiglia Thonny per questa operazione.

   .. image:: img/micropython_upload.png
       :width: 100%
       :align: center

   .. raw:: html

      <br/>

#. Una volta caricata la libreria, è possibile testarla utilizzando gli esempi forniti nella cartella ``micropython_spc-main/examples/pipower5``:

   * ``pipower_5_read_all.py`` : Utilizzare questo esempio se si desidera leggere tutti i dati. Mostra come leggere tutti i dati disponibili in una volta ed elaborarli individualmente.

   * ``pipower_5_read_individual.py`` : Questo esempio fornisce istruzioni per leggere singolarmente dati specifici. Utilizzarlo se si desidera accedere solo a determinati dati.

   * ``pipower_5_set_shutdown_percentage.py`` : Questo esempio spiega come impostare la percentuale di batteria per lo spegnimento. Quando la batteria non è in carica e il suo livello scende al di sotto della percentuale specificata, PiPower 5 invia un segnale di spegnimento all'host. Si spegne solo dopo che l'host ha completato lo spegnimento e inviato un segnale di spegnimento.

     * Per SBC (es. Raspberry Pi): Non è richiesta alcuna configurazione aggiuntiva.
     * Per microcontrollori: Rimuovere il ponticello **SDSIG** e collegare il filo intermedio a un pin. Dopo aver ricevuto il segnale di spegnimento ed eseguito uno spegnimento sicuro, portare questo pin a livello alto per indicare a PiPower 5 di spegnersi.

   * ``pipower_5_shutdown_when_request.py`` : Questo esempio mostra come gestire le operazioni dopo aver ricevuto un segnale di spegnimento. È necessario rimuovere il ponticello **SDSIG** e collegare il filo intermedio a un pin.

Documentazione API della libreria MicroPython: https://github.com/sunfounder/micropython_spc?tab=readme-ov-file#api
