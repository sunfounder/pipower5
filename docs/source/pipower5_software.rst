.. _pipower5_tool:

Strumento PiPower 5
===============================

Lo strumento PiPower 5 è il software companion per PiPower 5.

Fornisce:

- Supporto per lo spegnimento sicuro
- Gestione della batteria e della ricarica
- Monitoraggio dell'alimentazione
- Accesso al pannello di controllo Web
- Notifiche di eventi

PiPower 5 può inviare richieste di spegnimento al Raspberry Pi nelle seguenti situazioni:

- Il pulsante PiPower viene tenuto premuto per 2 secondi
- Il livello della batteria scende al di sotto della percentuale di spegnimento configurata

Dopo il completamento dello spegnimento del Raspberry Pi, PiPower 5 può scollegare automaticamente l'alimentazione per prevenire il danneggiamento della scheda SD e problemi di perdita improvvisa di alimentazione.

.. start_install_pipower5

.. important::

   PiPower 5 requires a **64-bit** operating system. The ``pipower5`` service
   does not support 32-bit Raspberry Pi OS.

   To check your system architecture, run:

   .. code-block:: shell

      uname -m

   - ``aarch64`` → 64-bit (supported)
   - ``armv7l`` → 32-bit (not supported)

   If you are running a 32-bit OS, please reinstall with the 64-bit version of
   Raspberry Pi OS before proceeding.

Installare lo strumento ``pipower5``
----------------------------------------------------

Installare lo strumento PiPower 5:

1. Clonare il repository:

   .. code-block:: shell

      git clone https://github.com/sunfounder/pipower5

2. Entrare nella directory:

   .. code-block:: shell

      cd pipower5

3. Eseguire l'installatore:

   .. code-block:: shell

      sudo python3 install.py

4. Riavviare il Raspberry Pi quando richiesto.

.. end_install_pipower5

Riferimento dei comandi
---------------------------------------

Lo strumento ``pipower5`` fornisce accesso alle informazioni di stato e alle opzioni di configurazione di PiPower 5.

Ad esempio, il seguente comando visualizza lo stato corrente di PiPower 5:

.. code-block:: shell

   pipower5 -a

Esempio di output:

.. code-block::

   Input:
      voltage: 0 mV
      current: 0 mA
      power: 0.000 W
      plugged in: False
   Output:
      voltage: 5296 mV
      current: 452 mA
      power: 2.394 W
   Battery:
      voltage: 8028 mV
      current: -315 mA
      power: -2.529 W
      percentage: 91 %
      source: 1 - Battery
      charging: False

   Internal:
      shutdown request: 0 - NONE
      power button: 0 - RELEASED
      max charging current: 0 mA
      default on: on
      shutdown percentage: 10 %

È possibile personalizzare queste impostazioni in base alle proprie esigenze.

Utilizzare ``pipower5`` o ``pipower5 -h`` per le istruzioni.

.. code-block:: text


  usage: pipower5 [-h] [-v] [-c] [-drd [DATABASE_RETENTION_DAYS]]
                  [-dl [{debug,info,warning,error,critical}]] [-rd]
                  [-cp [CONFIG_PATH]] [-sp [SHUTDOWN_PERCENTAGE]] [-iv] [-ic]
                  [-ov] [-oc] [-bv] [-bc] [-bp] [-bs] [-ii] [-ichg] [-do] [-sr]
                  [-pb] [-cc] [-a] [-fv] [-pfs [POWER_FAILURE_SIMULATION]]
                  [-seo [SEND_EMAIL_ON]] [-set [SEND_EMAIL_TO]]
                  [-ss [SMTP_SERVER]] [-smp [SMTP_PORT]] [-se [SMTP_EMAIL]]
                  [-spw [SMTP_PASSWORD]] [-ssc [SMTP_SECURITY]] [-bzo [BUZZ_ON]]
                  [-bzv [BUZZER_VOLUME]] [-bzt [BUZZER_TEST]] [-u [{C,F}]]
                  [{start,stop}]

  PiPower 5

  positional arguments:
    {start,stop}          Command

  options:
    -h, --help            show this help message and exit
    -v, --version         Show version
    -c, --config          Show config
    -drd [DATABASE_RETENTION_DAYS], --database-retention-days [DATABASE_RETENTION_DAYS]
                          Database retention days
    -dl [{debug,info,warning,error,critical}], --debug-level [{debug,info,warning,error,critical}]
                          Debug level
    -rd, --remove-dashboard
                          Remove dashboard
    -cp [CONFIG_PATH], --config-path [CONFIG_PATH]
                          Config path
    -sp [SHUTDOWN_PERCENTAGE], --shutdown-percentage [SHUTDOWN_PERCENTAGE]
                          Set shutdown percentage, leave empty to read
    -iv, --input-voltage  Read input voltage
    -ic, --input-current  Read input current
    -ov, --output-voltage
                          Read output voltage
    -oc, --output-current
                          Read output current
    -bv, --battery-voltage
                          Read battery voltage
    -bc, --battery-current
                          Read battery current
    -bp, --battery-percentage
                          Read battery percentage
    -bs, --battery-source
                          Read battery source
    -ii, --is-input-plugged_in
                          Read is input plugged in
    -ichg, --is-charging  Read is charging
    -do, --default-on     Read default on
    -sr, --shutdown-request
                          Read shutdown request
    -pb, --power-btn      Read power button
    -cc, --charging-current
                          Max charging current
    -a, --all             Show all status
    -fv, --firmware       PiPower5 firmware version
    -pfs [POWER_FAILURE_SIMULATION], --power-failure-simulation [POWER_FAILURE_SIMULATION]
                          Power failure simulation
    -seo [SEND_EMAIL_ON], --send-email-on [SEND_EMAIL_ON]
                          Send email on: ['battery_activated', 'low_battery',
                          'power_disconnected', 'power_restored',
                          'power_insufficient', 'battery_critical_shutdown',
                          'battery_voltage_critical_shutdown']
    -set [SEND_EMAIL_TO], --send-email-to [SEND_EMAIL_TO]
                          Email address to send email to
    -ss [SMTP_SERVER], --smtp-server [SMTP_SERVER]
                          SMTP server
    -smp [SMTP_PORT], --smtp-port [SMTP_PORT]
                          SMTP port
    -se [SMTP_EMAIL], --smtp-email [SMTP_EMAIL]
                          SMTP email
    -spw [SMTP_PASSWORD], --smtp-password [SMTP_PASSWORD]
                          SMTP password
    -ssc [SMTP_SECURITY], --smtp-security [SMTP_SECURITY]
                          SMTP security, 'none', 'ssl' or 'tls'
    -bzo [BUZZ_ON], --buzz-on [BUZZ_ON]
                          Buzz on: ['battery_activated', 'low_battery',
                          'power_disconnected', 'power_restored',
                          'power_insufficient', 'battery_critical_shutdown',
                          'battery_voltage_critical_shutdown']
    -bzv [BUZZER_VOLUME], --buzzer-volume [BUZZER_VOLUME]
                          Buzz volume
    -bzt [BUZZER_TEST], --buzzer-test [BUZZER_TEST]
                          Test buzzer on selected event.
    -u [{C,F}], --temperature-unit [{C,F}]
                          Temperature unit

.. note::

   Ogni volta che si modifica lo stato di ``pipower5.service``, è necessario utilizzare il seguente comando per rendere effettive le modifiche di configurazione.

   .. code-block:: shell

      sudo systemctl restart pipower5.service

   Verificare lo stato del programma pipower5 utilizzando lo strumento systemctl.

   .. code-block:: shell

      sudo systemctl status pipower5.service

   In alternativa, ispezionare i file di log generati dal programma.

   .. code-block:: shell

      cat /opt/pipower5/log

Pannello di controllo Web
----------------------------------------------------

Lo strumento PiPower 5 include un pannello di controllo Web integrato per il monitoraggio e la configurazione.

Accedere al pannello di controllo dal browser:

.. code-block:: text

   http://<indirizzo-ip-raspberry-pi>:34001

Le funzionalità del pannello includono:

- Monitoraggio della percentuale della batteria
- Monitoraggio dello stato di carica
- Monitoraggio della tensione di ingresso e uscita
- Monitoraggio della corrente
- Configurazione della percentuale di spegnimento
- Gestione delle notifiche
- Informazioni sul dispositivo Raspberry Pi

.. image:: img/web_dashboard.png
   :width: 100%
   :align: center

.. image:: img/web_dashboard_2.png
   :width: 100%
   :align: center

È anche possibile configurare la percentuale di spegnimento direttamente dal pannello di controllo:

.. image:: img/web_dashboard_3.png
   :width: 100%
   :align: center

Se non si necessita del pannello di controllo, rimuoverlo con:

.. code-block:: shell

   pipower5 --remove-dashboard

Spegnimento sicuro
----------------------------------------------------

PiPower 5 supporta la protezione automatica con spegnimento sicuro per i sistemi Raspberry Pi.

Flusso di lavoro di spegnimento:

.. code-block:: text

   Spegnimento attivato
   -> Il Raspberry Pi esegue uno spegnimento sicuro
   -> PiPower 5 rileva il completamento dello spegnimento
   -> PiPower 5 scollega automaticamente l'alimentazione

Questo aiuta a prevenire:

- Il danneggiamento della scheda SD
- Danni al file system
- Problemi di perdita improvvisa di alimentazione


Spegnimento dopo l'arresto del Raspberry Pi
+++++++++++++++++++++++++++++++++++++++++++

.. start_power_off_after_shutdown

Per consentire a PiPower 5 di scollegare automaticamente l'alimentazione dopo lo spegnimento del Raspberry Pi, è necessaria una configurazione aggiuntiva.

1. Se si utilizza un **Raspberry Pi 4 o 5**:

   * Assicurarsi che il ponticello ``SDSIG`` su PiPower 5 sia collegato a ``PI3V3``.

     .. image:: img/safe_shutdown_3v3.png
        :width: 400

   * Aprire la configurazione del Raspberry Pi:

     .. code-block:: shell

        sudo raspi-config

   * Accedere a:

     .. code-block:: text

        6 Advanced Options
        -> A11 Shutdown Behaviour
        -> B1 Full power off Switch off Pi ...

   * Riavviare il Raspberry Pi quando richiesto.

2. Se si utilizza un **Raspberry Pi 3** o precedente:

   * Impostare il ponticello ``SDSIG`` su PiPower 5 su ``GPIO26``.

     .. image:: img/safe_shutdown_io26.png
        :width: 400

   * Aprire ``/boot/firmware/config.txt``:

     .. code-block:: shell

        sudo nano /boot/firmware/config.txt

   * Aggiungere le seguenti righe:

     .. code-block:: shell

        dtoverlay=gpio-poweroff,gpio_pin=26,active_low=1
        gpio=26=op,dh

   * Premere ``Ctrl+X``, poi ``Y``, e premere ``Invio`` per salvare il file e uscire.

   * Riavviare il Raspberry Pi.

     .. code-block:: shell

        sudo reboot

Dopo la configurazione, PiPower 5 può rilevare automaticamente lo spegnimento del Raspberry Pi e scollegare l'alimentazione in modo sicuro.

I metodi di spegnimento sicuro supportati includono:

- Tenere premuto il pulsante PiPower per 2 secondi
- Spegnere dal menu del desktop Raspberry Pi
- Eseguire ``sudo shutdown now``
- Spegnimento automatico quando il livello della batteria scende al di sotto della percentuale di spegnimento configurata

.. end_power_off_after_shutdown

Configurare la percentuale di spegnimento
++++++++++++++++++++++++++++++++++++++++++

È possibile configurare la percentuale della batteria che attiva lo spegnimento automatico.

Esempio:

.. code-block:: shell

   pipower5 -sp 30

Questo imposta la soglia di spegnimento al 30%.

Quindi utilizzare il seguente comando per rendere effettive le modifiche di configurazione.

.. code-block:: shell

   sudo systemctl restart pipower5.service

Quando il livello della batteria scende al di sotto del 30%, PiPower 5 chiederà al Raspberry Pi di spegnersi e scollegherà automaticamente l'alimentazione.


È anche possibile leggere la percentuale di spegnimento corrente:

.. code-block:: shell

   pipower5 -sp

.. tip::

   Per i sistemi Raspberry Pi 5 con elevato consumo energetico (>3A), si consiglia di impostare la percentuale di spegnimento al ``100%``.

   Questo garantisce che il Raspberry Pi si spenga immediatamente quando l'alimentazione esterna viene scollegata, aiutando a proteggere il sistema e i dispositivi di archiviazione.


Monitoraggio dell'alimentazione
----------------------------------------------------

PiPower 5 fornisce monitoraggio in tempo reale per:

- Percentuale della batteria
- Stato di carica
- Tensione di ingresso
- Tensione di uscita
- Corrente di ingresso
- Corrente di uscita
- Tensione della batteria
- Corrente della batteria

Comandi utili:

Visualizzare la percentuale della batteria:

.. code-block:: shell

   pipower5 -bp

Visualizzare lo stato di carica:

.. code-block:: shell

   pipower5 -ichg

Visualizzare la tensione di ingresso:

.. code-block:: shell

   pipower5 -iv

Visualizzare tutte le informazioni di stato:

.. code-block:: shell

   pipower5 -a

Per l'elenco completo dei comandi:

.. code-block:: shell

   pipower5 --help


Notifiche
----------------------------------------------------

PiPower5 supporta notifiche guidate dagli eventi tramite:

- Avvisi acustici (buzzer)
- Notifiche email

Gli eventi supportati includono:

- ``battery_activated``
- ``low_battery``
- ``power_disconnected``
- ``power_restored``
- ``power_insufficient``
- ``battery_critical_shutdown``
- ``battery_voltage_critical_shutdown``

.. note::

   Ogni volta che si modifica lo stato di ``pipower5.service``, è necessario utilizzare il seguente comando per rendere effettive le modifiche di configurazione.

   .. code-block:: shell

      sudo systemctl restart pipower5.service

Descrizioni degli eventi
+++++++++++++++++++++++++++++++++++++++++++++++++

1. ``battery_activated``

   Attivato quando la batteria inizia a fornire alimentazione. Questo si verifica tipicamente se la fonte di alimentazione esterna è scollegata o non è in grado di fornire potenza sufficiente.

   * **Condizione di ripristino**: Si ripristina automaticamente dopo la disconnessione dell'alimentazione esterna.

2. ``low_battery``

   Attivato quando il livello di carica della batteria scende al di sotto della **soglia di spegnimento configurata**.

   * **Ripetizione**: Se la batteria rimane al di sotto di questa soglia, l'evento viene attivato ogni 10 minuti.
   * **Condizione di ripristino**: Si ripristina quando la carica della batteria risale sopra la **soglia di spegnimento + 5%**.

3. ``power_disconnected``

   Attivato quando la fonte di alimentazione esterna viene scollegata.

   * **Condizione di ripristino**: Si ripristina quando l'alimentazione esterna viene ripristinata.

4. ``power_restored``

   Attivato quando la fonte di alimentazione esterna viene ripristinata.

   * **Condizione di ripristino**: Si ripristina se l'alimentazione esterna viene nuovamente scollegata.

5. ``power_insufficient``

   Si verifica quando l'alimentazione esterna è insufficiente, richiedendo alla batteria di fornire potenza supplementare.

   * **Azione consigliata**: Verificare la potenza nominale della fonte di alimentazione o controllare le impostazioni di potenza di carica configurate.
   * **Condizione di ripristino**: Si ripristina quando la fonte di alimentazione esterna viene scollegata.

6. ``battery_critical_shutdown``

   Attivato appena prima dello spegnimento del sistema a causa della **capacità della batteria criticamente bassa**.

7. ``battery_voltage_critical_shutdown``

   Attivato quando la **tensione della batteria** scende al di sotto della soglia critica, portando allo spegnimento.

   * **Nota**: Questo evento è raramente attivato nell'uso normale. In genere, l'evento ``low_battery`` avvia una sequenza di spegnimento prima che la tensione scenda così tanto. Questo funge da **meccanismo di spegnimento di sicurezza**.

Con questi eventi, PiPower5 fornisce sia avvisi proattivi (es. batteria scarica, potenza insufficiente) che salvaguardie critiche (es. attivatori di spegnimento), garantendo un funzionamento stabile e la protezione dei dati.



Avvisi acustici (Buzzer)
+++++++++++++++++++++++++++++++++++++++++++++++++

PiPower5 supporta notifiche acustiche per diversi eventi di sistema.

È possibile configurare gli avvisi acustici tramite il **pannello di controllo Web** o lo **strumento a riga di comando**.
Quando si verifica un evento configurato, PiPower5 riproduce il suono acustico corrispondente.

Le funzionalità includono:

- Notifiche acustiche basate sugli eventi
- Volume del buzzer regolabile (1–10)
- Anteprima del suono degli eventi
- Supporto per effetti sonori personalizzati

Gli utenti avanzati possono anche creare effetti sonori acustici personalizzati.

1. Aprire il file di configurazione:

   .. code-block:: shell

      /opt/pipower5/venv/lib/python3.11/site-packages/pipower5/config.json

2. Individuare la sezione ``pipower5_buzz_sequence``.

3. Ogni effetto sonoro è definito utilizzando il seguente formato:

   .. code-block:: text

      [action, duration]

   Dove:

   - ``action`` può essere:

     - Una nota musicale, come ``"A4"``, ``"D3"`` o ``"C#4"``
     - Un valore di frequenza (intero)
     - ``"pause"`` per il silenzio

   - ``duration`` è il tempo di riproduzione in millisecondi (ms)


Avvisi email
+++++++++++++++++++++++++++++++++++++++++++++++++

PiPower5 supporta notifiche email per eventi di sistema importanti, come:

- Batteria scarica
- Alimentazione scollegata
- Alimentazione ripristinata
- Eventi di spegnimento critico

Le notifiche email possono essere configurate tramite il **pannello di controllo Web** o lo **strumento a riga di comando**.

Per utilizzare gli avvisi email, è necessario un server SMTP. La maggior parte dei provider di posta elettronica supporta i servizi SMTP.

- Per Gmail, è sufficiente creare una **password per app**
- Per altri provider, abilitare l'accesso SMTP e generare una password SMTP dedicata se necessario

Prima della configurazione, preparare le seguenti informazioni:

- Indirizzo del server SMTP
  (Esempio: ``smtp.gmail.com``)

- Porta SMTP
  (Esempio: ``465`` o ``25``)

- Tipo di crittografia
  (``None`` / ``SSL`` / ``TLS``)

- Account SMTP
  (Solitamente il proprio indirizzo email)

- Password SMTP
  (Password per app o password SMTP)

Dopo aver inserito le informazioni SMTP, configurare l'indirizzo email del destinatario.

.. note::

   PiPower5 utilizza il server SMTP per accedere al proprio account email e inviare notifiche.

   È possibile utilizzare lo stesso indirizzo email sia come mittente che come destinatario.

Dopo la configurazione, utilizzare il comando di test per verificare la connessione SMTP e la consegna delle email.
