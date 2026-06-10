.. note::

    Ciao, benvenuto nella community SunFounder degli appassionati di Raspberry Pi, Arduino e ESP32 su Facebook! Approfondisci Raspberry Pi, Arduino e ESP32 con altri appassionati.

    **Perché unirsi?**

    - **Supporto esperto**: Risolvi i problemi post-vendita e le sfide tecniche con l'aiuto della nostra community e del nostro team.
    - **Impara e condividi**: Scambia consigli e tutorial per migliorare le tue competenze.
    - **Anteprime esclusive**: Accedi in anteprima agli annunci di nuovi prodotti e alle anticipazioni.
    - **Sconti speciali**: Goditi sconti esclusivi sui nostri prodotti più recenti.
    - **Promozioni festive e omaggi**: Partecipa a concorsi e promozioni stagionali.

    👉 Pronto a esplorare e creare con noi? Clicca [|link_sf_facebook|] e unisciti oggi!

.. _troubleshooting:

Risoluzione dei problemi
=========================

Questa pagina aiuta a diagnosticare i problemi di PiPower 5 utilizzando i LED integrati, il buzzer e gli strumenti software. Inizia con le tabelle di riferimento rapido qui sotto, quindi segui le guide basate sui sintomi per i passaggi dettagliati.

.. contents:: Indice
   :local:
   :depth: 2


-----------------------------------
Riferimento rapido LED e buzzer
-----------------------------------

Prima di addentrarsi nei sintomi specifici, utilizza queste tabelle per interpretare ciò che la scheda ti sta comunicando.

LED di alimentazione e stato
+++++++++++++++++++++++++++++

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - LED
     - Stato
     - Significato
   * - **LED PWR** (verde)
     - ON
     - La potenza di uscita è attiva — la scheda sta fornendo 5V al tuo dispositivo.
   * -
     - OFF
     - L'uscita è disattivata. Premi una volta il pulsante di accensione per attivarla.
   * - **LED BAT** (giallo)
     - ON
     - La batteria sta attualmente fornendo alimentazione. Se l'alimentazione esterna è collegata, questo indica una potenza di ingresso insufficiente.
   * -
     - OFF
     - La batteria è in standby — l'alimentazione esterna è sufficiente.
   * - **LED batteria invertita** (2× rosso)
     - ON (entrambi)
     - La polarità della batteria è invertita! Scollegare immediatamente e correggere il cablaggio.

LED livello batteria
+++++++++++++++++++++

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Schema LED
     - Significato
   * - 4 LED accesi
     - Batteria > 80%
   * - 3 LED accesi
     - Batteria 60% – 80%
   * - 2 LED accesi
     - Batteria 40% – 60%
   * - 1 LED acceso
     - Batteria 20% – 40%
   * - Primo LED lampeggiante
     - Batteria < 20% — caricare presto
   * - LED a scorrimento sequenziale
     - Ricarica in corso
   * - Due LED centrali lampeggianti
     - In attesa del segnale di spegnimento dal Raspberry Pi
   * - Tutti i LED spenti
     - Scheda spenta o in modalità sospensione

.. note::

   I LED della batteria rimangono attivi durante la carica anche quando la scheda è spenta. Si spengono solo al completamento della carica.

Segnali del buzzer
+++++++++++++++++++

Se il buzzer è abilitato, questi suoni indicano eventi specifici:

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Evento
     - Suono tipico
     - Significato
   * - ``battery_activated``
     - Due toni ascendenti
     - La batteria ha preso il controllo dell'alimentazione (alimentazione esterna persa o insufficiente).
   * - ``low_battery``
     - Due toni ripetuti della stessa altezza
     - Il livello della batteria è sceso al di sotto della percentuale di spegnimento configurata. Caricare immediatamente.
   * - ``power_disconnected``
     - Tono alto → tono basso
     - L'alimentazione esterna è stata scollegata. Il sistema ora funziona a batteria.
   * - ``power_restored``
     - Tono basso → tono alto
     - L'alimentazione esterna è stata ripristinata. La batteria non si sta più scaricando.
   * - ``power_insufficient``
     - Tre toni rapidi della stessa altezza
     - L'alimentazione esterna è collegata ma troppo debole. La batteria sta supplementando. Verifica l'adattatore di alimentazione.
   * - ``battery_critical_shutdown``
     - Tre toni discendenti rapidi
     - Capacità della batteria criticamente bassa. Il sistema si spegnerà.
   * - ``battery_voltage_critical_shutdown``
     - Quattro toni discendenti rapidi
     - Tensione della batteria criticamente bassa (sicurezza). Il sistema si spegnerà immediatamente.

.. tip::

   Se non si sentono mai i suoni del buzzer, il buzzer potrebbe essere disabilitato o il suo volume impostato a 0. Eseguire ``pipower5 -bzv`` per controllare il volume corrente, o testare con ``pipower5 -bzt low_battery``.


---------------------------------
Diagnosi basata sui sintomi
---------------------------------

"Nessuna alimentazione" — Tutti i LED spenti, nessuna uscita
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

**Cosa si vede**: LED PWR spento, LED batteria spenti, il dispositivo collegato non mostra alimentazione.

**Verificare questi punti, nell'ordine:**

1. **La batteria è installata?**
   PiPower 5 non può funzionare senza batteria. Assicurarsi che il connettore della batteria (XH2.54 3P) sia saldamente inserito. Vedi :ref:`battery_connector`.

2. **La batteria è completamente scarica?**
   Una batteria profondamente scarica (< 2,5V per cella) entra in modalità di carica di mantenimento e potrebbe non alimentare la scheda per diversi minuti.

   - Collegare l'alimentazione esterna e attendere 10–15 minuti.
   - Se i LED della batteria rimangono spenti dopo 15 minuti, la batteria potrebbe essere difettosa.

3. **L'alimentazione esterna è collegata correttamente?**

     - Utilizzare un alimentatore USB-C PD (5V–15V) o alimentazione CC tramite i morsetti a vite.
     - Assicurarsi che il cavo USB-C supporti la fornitura di energia — alcuni cavi solo dati non funzioneranno.
     - Provare un altro adattatore di alimentazione e cavo.

4. **Premere una volta il pulsante di accensione.**
   PiPower 5 richiede la pressione del pulsante per attivare l'uscita, a meno che il ponticello Default ON non sia impostato.

5. **Controllare il ponticello Default ON.** Vedi :ref:`cap_onoff`.
   - Ponticello su **ON**: L'uscita si attiva automaticamente quando l'alimentazione esterna è collegata.
   - Ponticello su **OFF**: È necessario premere il pulsante di accensione ogni volta.

6. **Verificare l'installazione invertita della batteria.**
   Se entrambi i LED rossi vicino al connettore della batteria sono accesi, la polarità della batteria è invertita. Spegnere immediatamente, scollegare la batteria e ricollegare con la polarità corretta. Vedi :ref:`battery_connector`.


"LED BAT sempre acceso" — L'alimentazione esterna sembra insufficiente
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

**Cosa si vede**: L'alimentazione esterna è collegata, ma il LED BAT rimane acceso. La batteria si sta scaricando nonostante la presenza di alimentazione esterna.

**Cosa significa**: L'alimentatore esterno non riesce a soddisfare la domanda totale di potenza. La batteria sta colmando il deficit.

**Verificare questi punti, nell'ordine:**

1. **L'adattatore di alimentazione è sufficientemente potente?**
   La formula è: *Potenza adattatore ≥ Potenza Raspberry Pi (~20–25W) + Potenza di carica (impostata tramite DIP switch)*.

   - Raspberry Pi 5 sotto carico può assorbire > 25W.
   - Se la potenza di carica è impostata a 20W (entrambi i DIP switch su ON), è necessario un adattatore da **45W+**.
   - Per un adattatore da 30W, ridurre la potenza di carica a 10W o 5W.

2. **Controllare il DIP switch (selettore potenza di carica).**
   Consultare la tabella della potenza di carica in :ref:`power_input`. Ridurre la potenza di carica se l'adattatore è sottodimensionato.

3. **Provare un altro cavo USB-C.**
   Non tutti i cavi supportano USB PD a potenze elevate. Utilizzare il cavo fornito con l'adattatore di alimentazione.

4. **Verificare il profilo PD dell'adattatore.**
   Alcuni adattatori dichiarano potenze elevate ma solo su combinazioni specifiche di tensione/corrente. PiPower 5 richiede un'alimentazione conforme PD. Gli adattatori non-PD (es. solo 5V fisso) potrebbero non fornire corrente sufficiente.

5. **Per l'ingresso tramite morsetti a vite**, assicurarsi che la tensione di ingresso sia ≥ 9V per prestazioni ottimali. Vedi :ref:`power_input` per i limiti tensione-corrente.


"LED PWR spento" — Il dispositivo non riceve alimentazione
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

**Cosa si vede**: I LED della batteria sono accesi (la scheda è alimentata), ma il LED PWR è spento e il dispositivo collegato non si avvia.

**Verificare questi punti:**

1. **Premere una volta il pulsante di accensione.**
   La scheda è alimentata ma l'uscita non è abilitata.

2. **Il connettore GPIO è inserito correttamente?**
   Se si utilizza un Raspberry Pi, rimuovere e reinserire il HAT PiPower 5. Verificare l'assenza di pin piegati o detriti nel connettore.

3. **Provare un'uscita alternativa.**
   Collegare un dispositivo alla porta USB-A o al connettore 2x4P. Se questi funzionano, il problema è nel passthrough GPIO.


"Il dispositivo si spegne inaspettatamente"
++++++++++++++++++++++++++++++++++++++++++++

**Cosa si vede**: Il Raspberry Pi o il dispositivo collegato si spegne senza preavviso.

**Verificare questi punti:**

1. **Controllare la percentuale di spegnimento.**
   Eseguire ``pipower5 -sp``. Se è impostata alta (es. 50% o più), la scheda attiverà uno spegnimento precoce. Impostare un valore più basso se necessario:

   .. code-block:: shell

      pipower5 -sp 10
      sudo systemctl restart pipower5.service

2. **Verificare se la batteria si sta effettivamente scaricando.**

     Eseguire ``pipower5 -a`` e controllare:

     - ``source``: Dovrebbe essere "0 - External" quando l'alimentazione esterna è collegata.
     - ``battery current``: Negativo = carica, Positivo = scarica.

3. **Per Raspberry Pi 5 con periferiche ad alta potenza (SSD, HAT)**:
   Considerare di impostare ``pipower5 -sp 100`` per attivare lo spegnimento sicuro immediato quando l'alimentazione esterna viene persa. Vedi :ref:`pipower5_tool`.

4. **Verificare l'adattatore di alimentazione.**
   Se vengono attivati eventi ``power_insufficient`` (buzzer o log), l'adattatore è troppo debole. Passare a un alimentatore di potenza superiore o ridurre il DIP switch di potenza di carica.


"La batteria non si carica"
++++++++++++++++++++++++++++

**Cosa si vede**: Alimentazione esterna collegata, ma i LED della batteria non mostrano l'animazione di carica (scorrimento sequenziale).

**Verificare questi punti:**

1. **La batteria è già piena?**
   4 LED fissi = batteria > 80%. Il circuito di carica potrebbe essersi interrotto perché la batteria è piena o in fase di tensione costante.

2. **Verificare lo stato di carica via software.**
   Eseguire ``pipower5 -ichg``. Se restituisce ``False``, la scheda segnala che non è in carica. Controllare ``pipower5 -bp`` per la percentuale attuale della batteria.

3. **Protezione da sovratemperatura attiva.**
   Se la scheda è stata sottoposta a carico elevato in un ambiente caldo, il chip di carica potrebbe aver superato 125°C e interrotto la carica. Lasciar raffreddare la scheda e riprovare.

4. **Tensione di ingresso troppo bassa tramite morsetti a vite.**
   Se si utilizzano i morsetti a vite con tensione ≤ 6,5V, la corrente di carica è limitata. Utilizzare ≥ 9V per una carica affidabile.

5. **Verificare lo stato della batteria.**
   Una batteria che non raggiunge mai la carica completa o che si carica molto lentamente potrebbe avere celle degradate. Provare un'altra batteria compatibile (Li-ion 7.4V 2 celle, XH2.54 3P).


"Comunicazione I2C fallita" — Il comando `pipower5` restituisce errori
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

**Cosa si vede**: L'esecuzione di ``pipower5 -a`` produce un errore o nessun dato.

**Verificare questi punti:**

1. **L'I2C è abilitato sul Raspberry Pi?**
   Eseguire ``sudo raspi-config`` → Interface Options → I2C → Enable.

2. **Il dispositivo I2C viene rilevato?**

   .. code-block:: shell

      sudo i2cdetect -y 1

   PiPower 5 dovrebbe apparire all'indirizzo ``0x5a``. Se non appare alcun dispositivo:

   - Reinserire il HAT sul connettore GPIO.
   - Verificare che ``i2c-dev`` sia caricato: ``lsmod | grep i2c``.
   - Verificare che ``dtparam=i2c_arm=on`` sia in ``/boot/firmware/config.txt``.

3. **Il servizio `pipower5` è in esecuzione?**

   .. code-block:: shell

      sudo systemctl status pipower5.service

   Se inattivo, avviarlo: ``sudo systemctl start pipower5.service``.

4. **Conflitto tra più dispositivi I2C?**
   PiPower 5 utilizza l'indirizzo I2C ``0x5a``. Verificare che nessun altro HAT o dispositivo stia utilizzando questo indirizzo. Vedi :ref:`pin_header`.

5. **Riavviare.**
   A volte un riavvio a freddo sia del Raspberry Pi che di PiPower 5 risolve i problemi del bus I2C. Spegnere completamente, attendere 10 secondi, quindi riaccendere.


"Buzzer silenzioso" — Nessun suono durante gli eventi
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

**Cosa si vede**: Si verificano eventi (disconnessione alimentazione, batteria scarica, ecc.) ma nessun suono del buzzer.

**Verificare questi punti:**

1. **Controllare il volume del buzzer.**

   .. code-block:: shell

      pipower5 -bzv

   Se restituisce 0, il buzzer è in mute. Impostare un volume (1–10):

   .. code-block:: shell

      pipower5 -bzv 5
      sudo systemctl restart pipower5.service

2. **Verificare quali eventi hanno il buzzer abilitato.**

   .. code-block:: shell

      pipower5 -bzo

   Assicurarsi che l'evento previsto sia nell'elenco. Per aggiungere un evento:

   .. code-block:: shell

      pipower5 -bzo low_battery,power_disconnected

3. **Testare il buzzer direttamente.**

   .. code-block:: shell

      pipower5 -bzt low_battery

   Se si sente un suono, l'hardware del buzzer funziona — il problema è nella configurazione degli eventi.


"Il Raspberry Pi mostra un avviso di bassa tensione"
+++++++++++++++++++++++++++++++++++++++++++++++++++++

**Cosa si vede**: Il desktop del Raspberry Pi o ``dmesg`` mostra avvisi di sottotensione.

**Questo è un comportamento previsto in alcuni casi:**

- Quando si alimenta un Raspberry Pi dalla porta USB-A di PiPower 5 (invece del connettore GPIO), il Pi potrebbe segnalare un avviso di alimentazione non-PD. Questo può essere ignorato in sicurezza.
- Se si utilizza il connettore GPIO e si vedono ancora avvisi, l'uscita di PiPower 5 potrebbe essere sotto carico elevato. Verificare l'assorbimento totale di corrente della configurazione.

**Verificare questi punti:**

1. Eseguire ``pipower5 -a`` e controllare ``Output: voltage``. Dovrebbe essere stabile intorno a 5,2–5,3V. Se scende sotto 5,0V sotto carico, l'assorbimento totale di corrente potrebbe superare il limite di 5A.

2. Scollegare le periferiche USB non essenziali e ripetere il test.

3. Se il problema persiste, il convertitore DC-DC potrebbe essere difettoso. Contattare l'assistenza.


--------------------------------------
Comandi di diagnostica software
--------------------------------------

Lo strumento CLI ``pipower5`` è l'interfaccia diagnostica principale. Ecco i comandi più utili:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Comando
     - Cosa indica
   * - ``pipower5 -a``
     - Istantanea completa dello stato: tensione ingresso/uscita, stato batteria, stato carica, richiesta spegnimento, stato pulsante.
   * - ``pipower5 -bp``
     - Percentuale batteria.
   * - ``pipower5 -ichg``
     - Se la batteria è attualmente in carica (``True`` / ``False``).
   * - ``pipower5 -ii``
     - Se l'alimentazione esterna è collegata.
   * - ``pipower5 -sp``
     - Soglia attuale percentuale di spegnimento.
   * - ``pipower5 -sr``
     - Stato attuale richiesta spegnimento (0 = Nessuna, 1 = Batteria scarica, 2 = Pulsante).
   * - ``pipower5 -pb``
     - Stato attuale pulsante di accensione.
   * - ``pipower5 -bzv``
     - Volume attuale buzzer.
   * - ``pipower5 -fv``
     - Versione firmware (verificare di avere l'ultima versione).
   * - ``pipower5 -c``
     - Dump completo configurazione.
   * - ``pipower5 -pfs 60``
     - Esegue una simulazione di interruzione di corrente di 60 secondi per testare l'autonomia della batteria.
   * - ``sudo systemctl status pipower5.service``
     - Verifica se il servizio in background PiPower 5 è in esecuzione.
   * - ``cat /opt/pipower5/log``
     - Visualizza i log di servizio per i messaggi di errore.

.. tip::

   Per un controllo rapido dello stato, eseguire ``pipower5 -a`` e verificare:

   - ``shutdown request`` è ``0 - NONE`` (nessuno spegnimento in sospeso).
   - ``battery percentage`` è al di sopra del ``shutdown percentage``.
   - ``Output: voltage`` è tra 5,1V e 5,4V.


--------------------------------
Hai ancora problemi?
--------------------------------

Se nessuna delle soluzioni sopra risolve il problema, raccogliere le seguenti informazioni prima di contattare l'assistenza:

1. **Informazioni di sistema**:

   .. code-block:: shell

      pipower5 -a
      pipower5 -fv
      pipower5 -c

2. **Log di servizio**:

   .. code-block:: shell

      cat /opt/pipower5/log
      sudo journalctl -u pipower5.service --no-pager -n 100

3. **Dettagli hardware**:

     - Modello Raspberry Pi
     - Modello adattatore di alimentazione e potenza nominale
     - Tipo ed età della batteria
     - Impostazioni DIP switch di PiPower 5
     - Posizioni ponticelli SDSIG e Default ON

