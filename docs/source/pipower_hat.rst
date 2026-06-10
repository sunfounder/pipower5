PiPower 5 HAT
======================

.. interface:

Panoramica dell'interfaccia
----------------------------

.. image:: img/pipower5_ov.png
  :width: 100%



1. **Ingresso alimentazione USB Type-C**

   - Ingresso di alimentazione esterna per alimentare il Raspberry Pi e caricare la batteria contemporaneamente.
   - Supporta il protocollo **USB Power Delivery (PD)**, intervallo di ingresso **5V–15V**.

2. **Selettore ingresso alimentazione (DIP Switch)**

   - Consente la selezione di diversi profili di potenza in ingresso per una configurazione flessibile.

3. **Ponticello Default ON**

   - Definisce se il sistema deve accendersi automaticamente quando l'alimentazione esterna è collegata mentre il dispositivo è spento.
   - ON = Accensione automatica abilitata, OFF = Avvio manuale richiesto.

4. **SDSIG (Segnale di spegnimento)**

   - Fornisce il rilevamento dello spegnimento per Raspberry Pi.
   - Quando collegato a **PI3V3**, funziona con Raspberry Pi 4 e Pi 5.
   - Quando cortocircuitato al **Pin 26**, supporta Pi 3 e Pi Zero.
   - Dopo una corretta configurazione, PiPower5 scollegherà automaticamente l'alimentazione una volta spento il Raspberry Pi.

5. **LED PWR (Indicatore di stato uscita)**

   - Si accende quando l'uscita del sistema è attiva.

6. **LED BAT (Indicatore di stato batteria)**

   - Si accende quando il sistema è alimentato dalla batteria.
   - Un promemoria per monitorare il consumo della batteria quando si opera senza alimentazione esterna.

7. **Pulsante di accensione**

   - **Pressione singola**: Attiva l'uscita di alimentazione.
   - **Pressione prolungata (2 secondi)**: Invia una richiesta di spegnimento sicuro via I²C.
   - **Pressione prolungata (5 secondi)**: Forza uno spegnimento immediato (spegnimento forzato).
   - **Personalizzabile**: Le azioni di pressione singola e doppia possono essere riconfigurate via software.

8. **Terminale per pulsante di accensione esterno (ZH1.5 2P)**

   - Consente il collegamento di un pulsante di accensione fisico esterno.

9. **Connettore per pulsante di accensione esterno (2.54mm)**

   - Un'opzione alternativa saldabile per il collegamento di un pulsante di accensione esterno.

10. **LED indicatori batteria**

    - Visualizzano la capacità residua della batteria e lo stato di carica.
    - Nota: Anche quando il sistema è spento, i LED rimangono attivi durante la carica fino al completamento.

11. **Interfaccia I²C (SH1.0 4P)**

    - Compatibile con gli ecosistemi **Qwiic** e **STEMMA QT**.
    - Utilizzata per la comunicazione con il microcontrollore integrato e le periferiche esterne.

12. **Interfaccia I²C (connettore 1x4P 2.54mm)**

    - Breakout I²C alternativo con **uscita alimentazione 3V3**, configurabile come sempre attiva o commutata.

13. **Ponticello selezione alimentazione I²C**

    - **PERM**: L'alimentazione 3V3 è sempre attiva quando l'alimentazione esterna è collegata.
    - **SHUT (predefinito)**: L'alimentazione 3V3 si scollega automaticamente quando il sistema si spegne.

14. **Porta uscita USB Type-A**

    - Fornisce **uscita 5V regolata**, adatta per alimentare periferiche o altri dispositivi.
    - Quando si alimenta un Raspberry Pi, potrebbe apparire un avviso di alimentazione non-PD, che può essere ignorato in sicurezza.

15. **Connettore uscita alimentazione 2x4P 2.54mm**

    - Uscita 5V aggiuntiva per moduli esterni o SBC.

16. **Connettore GPIO Raspberry Pi (connettore femmina)**

    - Interfaccia diretta per Raspberry Pi, che trasmette alimentazione, I²C e altri segnali.
    - Completamente compatibile con la piedinatura Raspberry Pi.

17. **Connettore GPIO Raspberry Pi (breakout pin maschi)**

    - Espone i pin GPIO di Raspberry Pi per l'impilamento di HAT o espansione esterna.
    - **Nota**: Le linee I²C e il Pin 26 sono già occupati dalle funzioni di PiPower5.
    - È anche possibile collegare un cavo di estensione GPIO (dal fondo del pannello laterale) per sperimentare su breadboard.

18. **Connettore batteria (XH2.54 3P)**

    - Interfaccia di connessione della batteria.
    - Ordine dei pin (da sinistra a destra): Negativo, Punto medio (tra due celle), Positivo.
    - Progettato per **batterie Li-ion/LiPo 7.4V (2 celle)**.

19. **LED di avviso batteria invertita**

    - Due LED rossi si accendono se la batteria è collegata con polarità invertita, avvertendo di un'installazione errata.

20. **Morsetti a vite per batteria e alimentazione in ingresso**

    - Metodo di connessione alternativo per batterie esterne e fonti di alimentazione.
    - Supporta **ingresso esterno 5V–15V** (consigliato: >9V).
    - Supporto batteria: **solo 2 x 3.7V Li-ion / LiPo** (NON compatibile con batterie LiFePO₄).


Tabella delle specifiche
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 20 20

   * - Parametro
     - Minimo
     - Tipico
     - Massimo
     - Unità
   * - Corrente di spegnimento batteria
     - \-
     - 60
     - \-
     - µA
   * - Corrente di riposo batteria
     - \-
     - 25
     - \-
     - mA
   * - Tensione uscita DC-DC
     - 5,1957
     - 5,2855
     - 5,3766
     - V
   * - Protezione sovratemperatura DC-DC
     - \-
     - 150
     - \-
     - ℃
   * - Potenza di carica batteria
     - \-
     - \-
     - 20
     - W
   * - Protezione sovratemperatura carica
     - \-
     - 125
     - \-
     - ℃
   * - Resistore di bilanciamento
     - \-
     - 60
     - \-
     - Ω
   * - Tensione attivazione bilanciamento
     - \-
     - 4,2
     - \-
     - V


.. _power_input:

Ingresso alimentazione
-----------------------

.. image:: img/power_input.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

Quando si utilizza Raspberry Pi 5, si consiglia di utilizzare un alimentatore USB PD o un alimentatore CC con un'uscita minima di 32W. In caso contrario, durante i periodi di elevato consumo energetico, la batteria potrebbe non caricarsi correttamente o addirittura scaricarsi a causa di un'alimentazione insufficiente.

È possibile monitorare l'indicatore **LED BAT** per verificare lo stato della batteria. Quando l'alimentazione esterna è sufficiente, il LED BAT dovrebbe rimanere spento, indicando che la batteria è in modalità standby e non si sta scaricando. Se il LED BAT si accende, significa che la batteria sta alimentando il dispositivo, probabilmente a causa di un'alimentazione esterna insufficiente o scollegata. Un'illuminazione prolungata del LED BAT può portare a una scarica eccessiva della batteria, impedendole di funzionare come gruppo di continuità (UPS) durante le interruzioni di corrente. Assicurarsi di utilizzare una fonte di alimentazione che soddisfi le specifiche richieste per evitare tali scenari.




.. image:: img/bat_led.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>


**Percorso di alimentazione**

PiPower 5 integra la gestione del percorso di alimentazione, consentendo la commutazione automatica della fonte di alimentazione per ridurre al minimo l'usura della batteria e garantire un'alimentazione ininterrotta. Le funzionalità chiave includono:

- Quando è collegata una fonte di alimentazione esterna, l'uscita 5V viene fornita tramite un circuito step-down dalla fonte esterna. L'uscita può essere disattivata tramite un interruttore. Se le condizioni lo consentono, la fonte esterna può anche caricare contemporaneamente la batteria (vedere la sezione "Corrente di carica" per i dettagli).
- Alla disconnessione della fonte di alimentazione esterna, il sistema passa immediatamente all'alimentazione a batteria tramite un circuito step-down. Questa transizione senza interruzioni garantisce che il sistema continui a funzionare normalmente durante le interruzioni di corrente.

È possibile controllare l'indicatore LED BAT per verificare se la batteria sta attualmente alimentando il sistema.




**Corrente di carica**

La corrente di carica è soggetta a due tipi di limitazioni:

.. note::

   La corrente di carica è determinata sia dalla "Limitazione di carica da alimentazione a morsetti" che dalla "Limitazione di selezione potenza di carica" ed è vincolata dal valore più piccolo tra i due.

1. Limitazione di carica da alimentazione a morsetti

   Quando si alimenta tramite ingresso a morsetti, la corrente di carica viene regolata automaticamente in base alla tensione di ingresso, come mostrato di seguito:

   .. list-table::
      :header-rows: 1

      * - Tensione ingresso (VBUS)
        - Corrente di carica massima
      * - 4,5 < VBUS ≤ 6,5V
        - 3A
      * - 6,5 < VBUS ≤ 9,5V
        - 2A
      * - 9,5 < VBUS ≤ 13,5V
        - 1,5A
      * - 13,5 < VBUS ≤ 16,5V
        - 2A

2. Limitazione di selezione potenza di carica

   Un DIP switch a 2 posizioni sulla scheda consente la selezione di diversi livelli di potenza di carica. L'allocazione corrispondente di potenza di carica e potenza di uscita per ogni impostazione è la seguente:

   .. image:: img/power_selector.png
     :width: 50%
     :align: center

   .. list-table::
      :header-rows: 1

      * - Carica Sel 1
        - Carica Sel 2
        - Potenza di carica
      * - 0
        - 0
        - 5W
      * - 1
        - 0
        - 10W
      * - 0
        - 1
        - 15W
      * - 1
        - 1
        - 20W


**Come scegliere la potenza di carica**

La formula è:

*Capacità alimentatore = Potenza richiesta Raspberry Pi + Potenza di carica*

Si consiglia di stimare il fabbisogno energetico del Raspberry Pi a **20W - 25W**.

- Se si utilizza un **alimentatore da 30W**, impostare la potenza di carica su **10W** o **5W**.
- Se si utilizza un **alimentatore da 45W**, è possibile impostare in sicurezza la potenza di carica su **20W**.

Se si conoscono bene le esigenze energetiche del proprio Raspberry Pi, è possibile impostare una potenza di carica più elevata purché si mantenga un margine sufficiente per i picchi di potenza occasionali.

⚠️ Attenzione: una potenza insufficiente può causare lo spegnimento imprevisto del Raspberry Pi.




**Processo di carica**

- Quando la tensione della batteria ``VBAT <= 2,5V``, il sistema esegue la carica di mantenimento a bassa corrente, circa 50 mA.
- Quando ``2,5V < VBAT <= VTRKL``, la carica di mantenimento continua e la corrente di carica della batteria aumenta a circa 200 mA.
- Quando ``VTRKL < VBAT < VCV``, il sistema passa alla carica a corrente costante, fornendo una corrente costante preimpostata alla batteria.
- Una volta ``VBAT = VCV`` e la tensione della batteria si avvicina al livello di piena carica, la corrente di carica diminuisce gradualmente, passando alla carica a tensione costante.
- Durante la carica a tensione costante, quando la corrente di carica scende al di sotto di ``ISTOP`` e la tensione della batteria è vicina alla soglia di tensione costante, la carica si interrompe e la batteria entra in uno stato di piena carica.
- Nello stato di piena carica, il sistema monitora continuamente la tensione della batteria. Se la tensione scende al di sotto di ``VRCH``, la carica riprende automaticamente.

**Funzionalità di protezione**

PiPower 5 offre funzionalità di protezione complete, tra cui protezione da sottotensione e sovratensione in ingresso, nonché protezione da surriscaldamento per il chip di carica e il convertitore DC-DC. Queste funzionalità garantiscono un funzionamento stabile e affidabile del sistema.

**Bilanciamento di carica**

Il chip di bilanciamento di carica integrato attiva un resistore da 60Ω per scaricare la batteria a bassa corrente quando rileva che la tensione di una singola cella supera 4,2V. Questa funzionalità aiuta a mantenere l'equilibrio di tensione tra le celle.

**Protezione temperatura**

Il processo di carica viene automaticamente interrotto quando la temperatura interna del chip di carica supera 125°C. Allo stesso modo, il chip DC-DC disabilita l'uscita quando la sua temperatura interna supera 150°C.

.. _power_button:

Pulsante di accensione
------------------------





.. image:: img/power_button.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

Pulsante di accensione integrato per controllare l'alimentazione della scheda:

* **Pressione singola**: Attiva l'uscita.
* **Tenere premuto per 2 secondi fino all'accensione dei due LED centrali della batteria, quindi rilasciare**: Invia una richiesta di spegnimento via I2C.
* **Tenere premuto per più di 5 secondi**: Spegne direttamente l'uscita.


.. _battery_indicators:

Indicatori batteria
--------------------

Quattro LED integrati indicano il livello della batteria e lo stato di carica.

.. note::

   Se il dispositivo è in carica durante lo spegnimento, la spia indicatrice continuerà a visualizzare lo stato di carica fino al completamento.




.. image:: img/battery_indicator.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

* **4 LED accesi**: Batteria > 80%
* **3 LED accesi**: 60% < Batteria < 80%
* **2 LED accesi**: 40% < Batteria < 60%
* **1 LED acceso**: 20% < Batteria < 40%
* **Primo LED lampeggiante**: Batteria < 20%
* **I LED si accendono sequenzialmente in ciclo**: Ricarica in corso
* **Due LED centrali lampeggianti**: In attesa del segnale di spegnimento
* **Tutti i LED spenti**: Dispositivo spento o in modalità sospensione

.. _battery_connector:

Connettore batteria
--------------------
Connettore batteria VH3.96 2P e connettore batteria a morsetti.

.. image:: img/battery_pin.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

.. _cap_btn:

Terminale e connettore per pulsante di accensione esterno
----------------------------------------------------------

.. image:: img/btn_jumper.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

Questo terminale o connettore è progettato per collegare un pulsante di accensione esterno. Collegare un interruttore momentaneo, come un pulsante tattile o un pulsante metallico in stile vintage, ai pin del ponticello. I due fili del pulsante possono essere collegati ai pin del ponticello in qualsiasi direzione, poiché la polarità non è richiesta. Una volta collegato, è possibile utilizzare il pulsante esterno proprio come il pulsante di accensione integrato.

.. _cap_sdsig:

Ponticello SDSIG
------------------





.. image:: img/sdsig_jumper.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

Fornisce il rilevamento dello spegnimento per Raspberry Pi.

* Quando collegato a PI3V3, funziona con Raspberry Pi 4 e Pi 5.
* Quando cortocircuitato al Pin 26, supporta Pi 3 e Pi Zero.

Dopo una corretta configurazione, PiPower5 scollegherà automaticamente l'alimentazione una volta spento il Raspberry Pi.

.. _cap_onoff:

Ponticello Default ON/OFF
---------------------------





.. image:: img/default_jumper.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

Questo ponticello viene utilizzato per selezionare se l'uscita di alimentazione USB è abilitata per impostazione predefinita dopo uno spegnimento. Utilizzare il cappuccio del ponticello per collegare i pin etichettati ON o OFF per effettuare la selezione.

* Se il cappuccio del ponticello è posizionato a sinistra e collegato a OFF, l'inserimento dell'alimentazione USB dopo uno spegnimento non attiverà l'uscita.
* Se il cappuccio del ponticello è posizionato a destra e collegato a ON, l'inserimento dell'alimentazione USB dopo uno spegnimento attiverà l'uscita.

Questa funzionalità è tipicamente utilizzata per dispositivi che devono avviarsi automaticamente, come i server personali. Ad esempio, in caso di interruzione di corrente, PiPower 5 prenderà il controllo dell'alimentazione del Raspberry Pi, garantendo uno spegnimento sicuro. Una volta ripristinata l'alimentazione, PiPower 5 accende automaticamente il Raspberry Pi, eliminando la necessità di intervento manuale.

.. _pin_header:

Connettori pin per RPi
-----------------------

Il connettore pin è progettato per la connessione diretta a un Raspberry Pi, includendo sia la comunicazione I2C che l'alimentazione.




.. image:: img/pin_header.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

Il connettore supporta l'impilamento di HAT aggiuntivi. Tuttavia, notare che i pin I2C e il pin 26 sono già collegati e potrebbero richiedere una gestione attenta per evitare conflitti.

.. list-table::
   :widths: 15 15
   :header-rows: 1

   * - Raspberry Pi
     - MCU integrato
   * - SDA
     - SDA
   * - SCL
     - SCL
   * - GPIO26
     - SHUTDOWN
   * - ID_SD
     - ID_EEPROM SDA
   * - ID_SC
     - ID_EEPROM SCL

Comunicazione I2C
------------------






.. image:: img/i2c.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

Indirizzo I2C: 0x5C

Il microcontrollore integrato raccoglie vari segnali dalla scheda e li memorizza nei registri. Questi segnali sono accessibili via I2C utilizzando le seguenti tabelle dei registri.

.. raw:: html

   <style>
       .custom-register-table {
           border-collapse: collapse;
           width: 100%;
           margin: 20px 0;
           font-size: 14px;
           text-align: left;
       }
       .custom-register-table th, .custom-register-table td {
           border: 1px solid #ddd;
           padding: 8px;
       }
       .custom-register-table th {
           background-color: #f4f4f4;
           font-weight: bold;
       }
       .custom-register-table tr:nth-child(even) {
           background-color: #f9f9f9;
       }
       .custom-register-table tr:hover {
           background-color: #f1f1f1;
       }
       .custom-register-table caption {
           font-size: 16px;
           font-weight: bold;
           margin-bottom: 10px;
           text-align: center;
       }
   </style>

   <table class="custom-register-table">
       <caption>Tabella dei registri</caption>
       <thead>
           <tr>
               <th>Nome</th>
               <th>Indirizzo</th>
               <th>Lunghezza dati</th>
               <th>Tipo dati</th>
               <th>Unità</th>
               <th>Descrizione</th>
           </tr>
       </thead>
       <tbody>
           <tr>
               <td>Tensione ingresso</td>
               <td>0</td>
               <td>2</td>
               <td>u16</td>
               <td>mV</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Corrente ingresso</td>
               <td>2</td>
               <td>2</td>
               <td>u16</td>
               <td>mA</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Tensione uscita</td>
               <td>4</td>
               <td>2</td>
               <td>u16</td>
               <td>mV</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Corrente uscita</td>
               <td>6</td>
               <td>2</td>
               <td>u16</td>
               <td>mA</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Tensione batteria</td>
               <td>8</td>
               <td>2</td>
               <td>u16</td>
               <td>mV</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Corrente batteria</td>
               <td>10</td>
               <td>2</td>
               <td>i16</td>
               <td>mA</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Percentuale batteria</td>
               <td>12</td>
               <td>1</td>
               <td>u8</td>
               <td>%</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Capacità batteria</td>
               <td>13</td>
               <td>2</td>
               <td>u16</td>
               <td>mAh</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Fonte alimentazione</td>
               <td>15</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>0: Batteria non in uso.<br> 1: Batteria in uso.</td>
           </tr>
           <tr>
               <td>Stato connessione USB</td>
               <td>16</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>0: USB scollegato.<br> 1: USB collegato.</td>
           </tr>
           <tr>
               <td>RISERVATO</td>
               <td>17</td>
               <td>1</td>
               <td>-</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Stato carica</td>
               <td>18</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>0: Non in carica.<br> 1: In carica.</td>
           </tr>
           <tr>
               <td>Potenza ventola</td>
               <td>19</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Livello potenza ventola (0–100).</td>
           </tr>
           <tr>
               <td>Richiesta spegnimento</td>
               <td>20</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>1: Attivato da batteria scarica.<br>2: Attivato dalla pressione del pulsante.</td>
           </tr>
           <tr>
               <td>Versione firmware (Maggiore)</td>
               <td>128</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Versione firmware (Minore)</td>
               <td>129</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Versione firmware (Patch)</td>
               <td>130</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Codice reset</td>
               <td>131</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Codice motivo reset MCU.</td>
           </tr>
           <tr>
               <td>RTC Anno</td>
               <td>132</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RTC Mese</td>
               <td>133</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RTC Giorno</td>
               <td>134</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RTC Ora</td>
               <td>135</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RTC Minuto</td>
               <td>136</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RTC Secondo</td>
               <td>137</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RTC Sottosecondo</td>
               <td>138</td>
               <td>1</td>
               <td>u8</td>
               <td>1/128 s</td>
               <td>Sottosecondo RTC (1/128 secondo).</td>
           </tr>
           <tr>
               <td>Funzione Always-On</td>
               <td>139</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>0: Abilitato.<br> 1: Disabilitato.</td>
           </tr>
           <tr>
               <td>ID Scheda</td>
               <td>140</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Identificazione scheda: <br> 0: Pironman U1.<br> 1: Pironman 4.<br> 2: PiPower 3.<br>4: PiPower 5.</td>
           </tr>
           <tr>
               <td>RISERVATO</td>
               <td>141</td>
               <td>1</td>
               <td>-</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RISERVATO</td>
               <td>142</td>
               <td>1</td>
               <td>-</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Percentuale spegnimento</td>
               <td>143</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Soglia percentuale batteria per spegnimento.</td>
           </tr>
           <tr>
               <td>RISERVATO</td>
               <td>144</td>
               <td>1</td>
               <td>-</td>
               <td>-</td>
               <td>-</td>
           </tr>
       </tbody>
   </table>


   <table class="custom-register-table">
       <caption>Tabella impostazioni registri</caption>
       <thead>
           <tr>
               <th>Nome</th>
               <th>Indirizzo</th>
               <th>Lunghezza dati</th>
               <th>Tipo dati</th>
               <th>Unità</th>
               <th>Descrizione</th>
           </tr>
       </thead>
       <tbody>
           <tr>
               <td>Potenza ventola</td>
               <td>0</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Imposta velocità ventola (0–100).</td>
           </tr>
           <tr>
               <td>RTC Anno</td>
               <td>1</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Imposta anno RTC.</td>
           </tr>
           <tr>
               <td>RTC Mese</td>
               <td>2</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Imposta mese RTC.</td>
           </tr>
           <tr>
               <td>RTC Giorno</td>
               <td>3</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Imposta giorno RTC.</td>
           </tr>
           <tr>
               <td>RTC Ora</td>
               <td>4</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Imposta ora RTC.</td>
           </tr>
           <tr>
               <td>RTC Minuto</td>
               <td>5</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Imposta minuto RTC.</td>
           </tr>
           <tr>
               <td>RTC Secondo</td>
               <td>6</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Imposta secondo RTC.</td>
           </tr>
           <tr>
               <td>RTC Sottosecondo</td>
               <td>7</td>
               <td>1</td>
               <td>u8</td>
               <td>1/128 s</td>
               <td>Imposta sottosecondo RTC.</td>
           </tr>
           <tr>
               <td>Impostazione RTC</td>
               <td>8</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Abilita impostazione RTC: <br> 1: Abilitato.</td>
           </tr>
           <tr>
               <td>Percentuale spegnimento</td>
               <td>9</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Imposta soglia percentuale batteria per spegnimento (0–100).</td>
           </tr>
           <tr>
               <td>Percentuale spegnimento forzato</td>
               <td>10</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Imposta soglia percentuale batteria per spegnimento forzato (0–100).</td>
           </tr>
       </tbody>
   </table>

