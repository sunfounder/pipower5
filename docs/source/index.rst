.. note::

    Ciao, benvenuto nella community SunFounder degli appassionati di Raspberry Pi, Arduino e ESP32 su Facebook! Approfondisci Raspberry Pi, Arduino e ESP32 con altri appassionati.

    **Perché unirsi?**

    - **Supporto esperto**: Risolvi i problemi post-vendita e le sfide tecniche con l'aiuto della nostra community e del nostro team.
    - **Impara e condividi**: Scambia consigli e tutorial per migliorare le tue competenze.
    - **Anteprime esclusive**: Accedi in anteprima agli annunci di nuovi prodotti e alle anticipazioni.
    - **Sconti speciali**: Goditi sconti esclusivi sui nostri prodotti più recenti.
    - **Promozioni festive e omaggi**: Partecipa a concorsi e promozioni stagionali.

    👉 Pronto a esplorare e creare con noi? Clicca [|link_sf_facebook|] e unisciti oggi!

SunFounder PiPower5 - Proteggi il tuo dispositivo e i tuoi dati
================================================================================

.. * |link_PiPower_5_buy|

.. Thank you for choosing our |link_PiPower_5|.

Grazie per aver scelto il nostro PiPower5.


.. .. note::
..     This document is available in the following languages.

..         * |link_german_tutorials|
..         * |link_jp_tutorials|
..         * |link_en_tutorials|

..     Please click on the respective links to access the document in your preferred language.

.. todo: new pic

.. image:: img/PP.0.A.JPG
    :width: 400
    :align: center

PiPower 5 è una soluzione UPS versatile progettata per un'integrazione perfetta con i dispositivi Raspberry Pi. Dispone di una gestione robusta del percorso di alimentazione, capacità di carica e scarica di due batterie al litio e protezioni essenziali contro l'inversione di polarità, il sovraccarico e la scarica eccessiva.

Con un'uscita fino a 5V/5A, PiPower 5 garantisce prestazioni stabili per un'ampia gamma di dispositivi. La sua configurazione HAT+ garantisce la compatibilità con Raspberry Pi 5, mentre le uscite aggiuntive, tra cui una porta USB-A e un connettore 4x2P, forniscono supporto per vari computer a scheda singola (SBC) e piattaforme di microcontrollori, come Arduino, Pico e ESP32.

Un microcontrollore integrato gestisce in modo efficiente le operazioni di alimentazione e consente il monitoraggio in tempo reale dei parametri chiave tramite comunicazione I2C. Questi parametri includono la tensione di ingresso, la tensione di uscita, la tensione della batteria, la capacità della batteria, lo stato di connessione dell'alimentazione esterna, lo stato di carica e la fonte di alimentazione corrente (batteria o USB).

Combinando una gestione avanzata della batteria con un'ampia compatibilità, PiPower 5 è uno strumento essenziale per gli appassionati di tecnologia e i professionisti che desiderano ottimizzare le proprie configurazioni hardware.

**Caratteristiche**

* **Ingresso**: 5-15V, 45W, USB Type-C PD, DC5.5-2.1
* **Uscita**: 5V/5A tramite GPIO Raspberry Pi, USB Type-A e connettori a pin 2x4P 2.54mm
* **Potenza di carica**: Fino a 20W
* **Specifiche batteria**: 7.4V 2 celle Li-ion, connettore XH2.54 3P
* **Impostazioni configurabili tramite ponticelli**:

  * Ponticello Default On: Configura se il dispositivo si accende automaticamente quando è collegato all'alimentazione.
  * Ponticello Shutdown Signal: Abilita il rilevamento dello stato di spegnimento del dispositivo.
  * Connettore per pulsante di accensione esterno: Collega un pulsante di accensione esterno per il controllo manuale dell'alimentazione.

* **Indicatori e pulsanti integrati**:

  * Indicatore di stato della batteria
  * Indicatore della fonte di ingresso
  * Pulsante di accensione
  * Indicatore di connessione inversa della batteria
  * Indicatore di potenza in uscita

* **Microcontrollore integrato**: ARM Cortex-M23 a 32 bit, con supporto per comunicazione I2C

* **Interfacce di comunicazione I2C**:

  * GPIO Raspberry Pi
  * SH1.0 4P (compatibile con Qwiic e STEMMA QT)
  * Connettore a pin 1x4P 2.54mm


.. **Table of Contents**

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Per iniziare

   Informazioni su PiPower 5 <self>
   assembly
   quick_guide

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Panoramica hardware

   pipower_hat


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Configurazione software

   pipower5_software
   update_firmware
   use_with_python


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Appendice

   compatible_sbc
   troubleshooting
   faq


**Avviso di copyright**

Tutti i contenuti, inclusi a titolo esemplificativo ma non esaustivo testi, immagini e codice in questo manuale, sono di proprietà di SunFounder Company. È consentito utilizzarli solo per studio personale, ricerca, svago o altri scopi non commerciali o senza scopo di lucro, in conformità con le normative e le leggi sul copyright vigenti, senza violare i diritti legali dell'autore e degli aventi diritto. Per qualsiasi individuo o organizzazione che utilizzi questi contenuti a scopo di lucro commerciale senza autorizzazione, la Società si riserva il diritto di intraprendere azioni legali.

