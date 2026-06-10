.. note::

    Ciao, benvenuto nella community SunFounder degli appassionati di Raspberry Pi, Arduino e ESP32 su Facebook! Approfondisci Raspberry Pi, Arduino e ESP32 con altri appassionati.

    **Perché unirsi?**

    - **Supporto esperto**: Risolvi i problemi post-vendita e le sfide tecniche con l'aiuto della nostra community e del nostro team.
    - **Impara e condividi**: Scambia consigli e tutorial per migliorare le tue competenze.
    - **Anteprime esclusive**: Accedi in anteprima agli annunci di nuovi prodotti e alle anticipazioni.
    - **Sconti speciali**: Goditi sconti esclusivi sui nostri prodotti più recenti.
    - **Promozioni festive e omaggi**: Partecipa a concorsi e promozioni stagionali.

    👉 Pronto a esplorare e creare con noi? Clicca [|link_sf_facebook|] e unisciti oggi!

.. _faq:

FAQ
===

Come reinstallare PiPower 5
----------------------------

Se PiPower 5 non funziona correttamente e si desidera eseguire una reinstallazione pulita, seguire questi passaggi:

**1. Disinstallare l'installazione corrente:**

.. code-block:: shell

   cd ~/pipower5
   sudo python3 install.py --uninstall

**2. Reinstallare dal sorgente:**

.. code-block:: shell

   git clone https://github.com/sunfounder/pipower5
   cd pipower5
   sudo python3 install.py

**3. Riavviare il Raspberry Pi quando richiesto.**

Dopo il riavvio, verificare l'installazione:

.. code-block:: shell

   pipower5 -a
   sudo systemctl status pipower5.service

.. tip::

   Se la directory ``~/pipower5`` non esiste più dall'installazione originale, saltare il passaggio di disinstallazione e passare direttamente alla reinstallazione.


Il pannello mostra "Database Required" o nessun dato
------------------------------------------------------

**Cosa si vede**: Il pannello di controllo Web si apre normalmente nel browser, ma tutti i pannelli dati sono vuoti o mostrano "database required".

**Cosa significa di solito**: Raramente è un problema hardware. Nella maggior parte dei casi, il backend InfluxDB ha un problema di configurazione — un database corrotto, un bucket mancante o un token scaduto.

**Verificare questi punti, nell'ordine:**

1. **Verificare che il servizio PiPower 5 sia in esecuzione:**

   .. code-block:: shell

      sudo systemctl status pipower5

   Se il servizio non è attivo, avviarlo:

   .. code-block:: shell

      sudo systemctl start pipower5

2. **Verificare se il bucket InfluxDB esiste:**

   .. code-block:: shell

      sudo influx bucket list

   Cercare un bucket denominato ``pipower5`` nell'output. Se manca, il database deve essere ricreato.

3. **Controllare i log del servizio per errori:**

   .. code-block:: shell

      journalctl -u pipower5 -n 50

   Cercare messaggi di errore relativi a InfluxDB, come:

   - ``unauthorized`` o ``token`` — indica un problema con il token di autenticazione.
   - ``bucket not found`` — il bucket del database è mancante.
   - ``connection refused`` — InfluxDB non è in esecuzione.

4. **Se InfluxDB stesso è spento**, riavviarlo:

   .. code-block:: shell

      sudo systemctl restart influxdb
      sudo systemctl restart pipower5

.. note::

   Se InfluxDB è stato installato manualmente o migrato da una versione precedente, i percorsi di configurazione o i token di autenticazione potrebbero essere cambiati. In tal caso, una reinstallazione pulita di PiPower 5 (vedi sopra) reinizializzerà anche la configurazione di InfluxDB.
