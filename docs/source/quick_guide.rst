Guida rapida
===============================

Questa guida ti aiuta a iniziare rapidamente con PiPower 5 dopo l'assemblaggio hardware.

Caricare la batteria
----------------------------------------------------

Prima del primo utilizzo, caricare completamente la batteria.

Raccomandazioni:

- Utilizzare un adattatore di alimentazione USB-C di alta qualità
- Per Raspberry Pi 5 si consiglia un alimentatore da 5V 5A
- Si consigliano adattatori di potenza superiore quando si utilizzano SSD o altre periferiche ad alta potenza

Durante la carica:

- Utilizzare un alimentatore USB-C di alta qualità per caricare PiPower 5.

  .. image:: img/power_input.png
     :width: 50%
     :align: center

- Durante la carica, i LED indicatori della batteria si accendono progressivamente in sequenza.

  .. image:: img/battery_indicator.png
     :width: 50%
     :align: center

  Lo stato della batteria è indicato dal numero di LED accesi:

  * **4 LED accesi**: Batteria > 80%
  * **3 LED accesi**: 60% < Batteria < 80%
  * **2 LED accesi**: 40% < Batteria < 60%
  * **1 LED acceso**: 20% < Batteria < 40%
  * **Primo LED lampeggiante**: Batteria < 20%
  * **I LED si accendono progressivamente in ciclo**: Ricarica in corso
  * **Due LED centrali lampeggianti**: In attesa del segnale di spegnimento
  * **Tutti i LED spenti**: Dispositivo spento o in modalità sospensione
  * Durante la carica, l'indicatore rimane acceso **anche a dispositivo spento** fino al completamento della carica.

Accensione
----------------------------------------------------

Per i dispositivi Raspberry Pi, non è richiesto alcun cablaggio di alimentazione aggiuntivo. PiPower 5 fornisce alimentazione direttamente attraverso il connettore GPIO.

Per altri dispositivi, è possibile alimentarli utilizzando:

- La porta di uscita USB-A
- I pin 5V/GND accanto alla porta USB-A

.. image:: img/power_output.png
   :width: 50%
   :align: center

Premere una volta il pulsante di accensione per accendere PiPower 5. Quando è acceso:

- Il **LED PWR** si accende
- Il dispositivo collegato inizia a ricevere alimentazione da PiPower 5

.. image:: img/pwr_led.png
   :width: 50%
   :align: center

.. include:: /pipower5_software.rst
    :start-after: start_install_pipower5
    :end-before: end_install_pipower5

Aprire il pannello di controllo Web
----------------------------------------------------

Dopo l'installazione, aprire il pannello di controllo nel browser:

.. code-block:: text

   http://<indirizzo-ip-raspberry-pi>:34001

Il pannello di controllo consente di:

- Visualizzare la percentuale della batteria
- Monitorare lo stato di carica
- Controllare tensione e corrente
- Configurare la percentuale di spegnimento
- Gestire le notifiche

.. image:: img/web_dashboard.png
   :width: 100%
   :align: center


Spegnimento sicuro
----------------------------------------------------

.. include:: /pipower5_software.rst
    :start-after: start_power_off_after_shutdown
    :end-before: end_power_off_after_shutdown

.. note::

   Per funzionalità avanzate e opzioni di configurazione dettagliate, tra cui:

   - Comandi di monitoraggio dell'alimentazione
   - Impostazioni di notifica
   - Avvisi acustici (buzzer)
   - Avvisi email
   - Configurazione avanzata

   Consultare:

   * :ref:`pipower5_tool`
