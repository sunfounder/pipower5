Arduino
===================================

Se si utilizza il PiPower 5 per alimentare la scheda Arduino, è possibile collegare Arduino alla porta di uscita Type A del PiPower 5 o utilizzare due cavi jumper. Collegare l'interfaccia I2C della scheda utilizzando un ponticello.

.. If no operation is required before powering off, directly connect the **SDSIG** jumper cap to the GND. If operations are necessary before shutdown, remove the jumper cap and connect the intermediate wire to an IO port on the Arduino to notify PiPower 5 that it can safely power off.

Forniamo una libreria che consente di monitorare le tensioni di ingresso e uscita, la tensione e la percentuale della batteria, la fonte di alimentazione, lo stato di carica e altri dati interni.

#. Nell'IDE Arduino, aprire il **Gestore librerie**, cercare ``SunFounderPowerControl``, quindi scaricare e installare.

   .. image:: img/install_arduino_lib.png
      :width: 100%

#. Dopo l'installazione, accedere a **File** -> **Esempi** -> **SunFounderPowerControl** -> **PiPower 5**, dove si troveranno quattro esempi.

   .. image:: img/arduino_lib_example.png
      :width: 100%

   * ``read_all`` : Utilizzare questo esempio se si desidera leggere tutti i dati in una volta ed elaborarli individualmente.
   * ``read_individual`` : Se si desidera leggere solo dati specifici, questo esempio fornisce istruzioni per il recupero individuale dei dati.
   * ``set_shutdown_percentage`` : Questo esempio spiega come impostare una percentuale di batteria per lo spegnimento. Questa funzione invia un segnale di spegnimento all'host quando la batteria non è in carica e scende al di sotto della percentuale impostata. Dopo lo spegnimento dell'host, si spegnerà solo dopo aver ricevuto un segnale di spegnimento. Tipicamente utilizzato con SBC come Raspberry Pi. Per i microcontrollori, rimuovere il ponticello **SDSIG** e collegare il filo intermedio a un pin. Dopo uno spegnimento sicuro a seguito della ricezione del segnale di spegnimento, portare questo pin a livello alto per spegnere PiPower 5.
   * ``shutdown_when_request`` : Questo esempio mostra come gestire le operazioni dopo aver ricevuto un segnale di spegnimento. Rimuovere il ponticello **SDSIG** e collegare il filo intermedio a un pin.

#. Scegliere uno degli esempi e caricarlo sulla scheda.

   .. note::

      Su alcune schede in cui l'I2C può essere modificato, se è necessario cambiare i pin I2C, modificare il codice ``Wire.begin()``.

Documentazione API della libreria Arduino: https://github.com/sunfounder/arduino_spc?tab=readme-ov-file#api

