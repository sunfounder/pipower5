PiPower 5 HAT
======================

.. interface:

Descripción General de la Interfaz
-----------------------------------

.. image:: img/pipower5_ov.png
  :width: 100%



1. **Entrada de Alimentación USB Type-C**

   - Entrada de alimentación externa para suministrar energía al Raspberry Pi y cargar la batería simultáneamente.
   - Soporta **protocolo USB Power Delivery (PD)**, rango de entrada **5V–15V**.

2. **Selector de Entrada de Alimentación (DIP Switch)**

   - Permite la selección de diferentes perfiles de alimentación de entrada para una configuración flexible.

3. **Jumper de Encendido Predeterminado (Default ON)**

   - Define si el sistema debe encenderse automáticamente cuando se conecta la alimentación externa mientras el dispositivo está apagado.
   - ON = Autoencendido habilitado, OFF = Arranque manual requerido.

4. **SDSIG (Señal de Apagado)**

   - Proporciona detección de apagado para Raspberry Pi.
   - Cuando se puentea a **PI3V3**, funciona con Raspberry Pi 4 y Pi 5.
   - Cuando se cortocircuita al **Pin 26**, soporta Pi 3 y Pi Zero.
   - Después de la configuración adecuada, PiPower5 cortará la alimentación automáticamente una vez que el Raspberry Pi se apague.

5. **LED PWR (Indicador de Estado de Salida)**

   - Se enciende cuando la salida del sistema está activa.

6. **LED BAT (Indicador de Estado de Batería)**

   - Se enciende cuando el sistema está alimentado por la batería.
   - Un recordatorio para monitorear el consumo de batería cuando se funciona sin alimentación externa.

7. **Botón de Encendido**

   - **Pulsación simple**: Activar la alimentación de salida.
   - **Pulsación larga (2 segundos)**: Envía una solicitud de apagado seguro a través de I²C.
   - **Pulsación larga (5 segundos)**: Fuerza un apagado inmediato (apagado forzado).
   - **Personalizable**: Las acciones de pulsación simple y doble se pueden reconfigurar por software.

8. **Terminal de Botón de Encendido Externo (ZH1.5 2P)**

   - Permite la conexión de un botón de encendido físico externo.

9. **Conector de Botón de Encendido Externo (2.54mm)**

   - Una opción de conector soldable alternativa para la conexión de botón de encendido externo.

10. **LEDs Indicadores de Batería**

    - Muestran la capacidad restante de la batería y el estado de carga.
    - Nota: Incluso cuando el sistema está apagado, los LEDs permanecen activos durante la carga hasta que la batería esté completamente cargada.

11. **Interfaz I²C (SH1.0 4P)**

    - Compatible con los ecosistemas **Qwiic** y **STEMMA QT**.
    - Utilizada para comunicación con el microcontrolador integrado y periféricos externos.

12. **Interfaz I²C (Conector 1x4P 2.54mm)**

    - Breakout I²C alternativo con **salida de alimentación 3V3**, configurable como siempre encendido o conmutado.

13. **Jumper de Selección de Alimentación I²C**

    - **PERM**: La alimentación de 3V3 está siempre encendida cuando hay alimentación externa conectada.
    - **SHUT (predeterminado)**: La alimentación de 3V3 se corta automáticamente cuando el sistema se apaga.

14. **Puerto de Salida USB Type-A**

    - Proporciona **salida regulada de 5V**, adecuada para alimentar periféricos u otros dispositivos.
    - Al alimentar un Raspberry Pi, puede encontrar una advertencia de fuente de alimentación no PD, que se puede ignorar de forma segura.

15. **Conector de Salida de Alimentación 2x4P 2.54mm**

    - Salida adicional de 5V para módulos externos o SBCs.

16. **Conector GPIO de Raspberry Pi (Conector Hembra)**

    - Interfaz directa para Raspberry Pi, transmitiendo alimentación, I²C y otras señales.
    - Totalmente compatible con el pinout de Raspberry Pi.

17. **Conector GPIO de Raspberry Pi (Breakout de Pines Macho)**

    - Expone los pines GPIO de Raspberry Pi para apilar HATs o expansión externa.
    - **Nota**: Las líneas I²C y el Pin 26 ya están ocupados por las funciones de PiPower5.
    - También puede conectar un cable de extensión GPIO (desde la parte inferior del panel lateral) para experimentar en una protoboard.

18. **Conector de Batería (XH2.54 3P)**

    - Interfaz de conexión de batería.
    - Orden de pines (de izquierda a derecha): Negativo, Punto medio (entre dos celdas), Positivo.
    - Diseñado para **baterías de 7.4V (2 celdas) de Ion de Litio/LiPo**.

19. **LEDs de Advertencia de Batería Inversa**

    - Dos LEDs rojos se encienden si la batería está conectada con polaridad inversa, advirtiendo de una instalación incorrecta.

20. **Terminales de Tornillo para Batería y Alimentación de Entrada**

    - Método de conexión alternativo para baterías externas y fuentes de alimentación.
    - Soporta **entrada externa de 5V–15V** (recomendado: >9V).
    - Soporte de batería: **Solo 2 celdas de Ion de Litio/LiPo de 3.7V** (NO compatible con baterías LiFePO₄).


Tabla de Especificaciones
-----------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 20 20

   * - Parámetro
     - Mínimo
     - Típico
     - Máximo
     - Unidad
   * - Corriente de Apagado de Batería
     - \-
     - 60
     - \-
     - µA
   * - Corriente de Reposo de Batería
     - \-
     - 25
     - \-
     - mA
   * - Voltaje de Salida DC-DC
     - 5.1957
     - 5.2855
     - 5.3766
     - V
   * - Protección de Sobretemperatura DC-DC
     - \-
     - 150
     - \-
     - ℃
   * - Potencia de Carga de Batería
     - \-
     - \-
     - 20
     - W
   * - Protección de Sobretemperatura de Carga
     - \-
     - 125
     - \-
     - ℃
   * - Resistencia de Balanceo
     - \-
     - 60
     - \-
     - Ω
   * - Voltaje de Activación de Balanceo
     - \-
     - 4.2
     - \-
     - V


.. _power_input:

Entrada de Alimentación
-----------------------

.. image:: img/power_input.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

Al usar Raspberry Pi 5, se recomienda usar una fuente de alimentación USB PD o una fuente de alimentación DC con una salida mínima de 32W. De lo contrario, durante períodos de alto consumo de energía, la batería puede no cargarse correctamente o incluso agotar su carga debido a una alimentación insuficiente.

Puede monitorear el indicador **LED BAT** para verificar el estado de la batería. Cuando la alimentación externa es suficiente, el LED BAT debe permanecer apagado, indicando que la batería está en modo de espera y no se está descargando. Si el LED BAT se enciende, significa que la batería está suministrando energía al dispositivo, posiblemente debido a una alimentación externa insuficiente o desconectada. La iluminación prolongada del LED BAT puede llevar a una descarga excesiva de la batería, impidiendo que funcione como una fuente de alimentación ininterrumpida (UPS) durante cortes de energía. Asegúrese de usar una fuente de alimentación que cumpla con las especificaciones requeridas para evitar tales escenarios.




.. image:: img/bat_led.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>


**Ruta de Alimentación**

El PiPower 5 integra gestión de rutas de alimentación, permitiendo la conmutación automática de fuente de alimentación para minimizar el desgaste de la batería y asegurar un suministro de energía ininterrumpido. Las funcionalidades clave incluyen:

- Cuando se conecta una fuente de alimentación externa, la salida de 5V se suministra a través de un circuito reductor desde la fuente externa. La salida se puede apagar usando un interruptor. Si las condiciones lo permiten, la fuente de alimentación externa también puede cargar la batería simultáneamente (consulte la sección "Corriente de Carga" para más detalles).
- Al desconectar la fuente de alimentación externa, el sistema cambia inmediatamente a la alimentación por batería a través de un circuito reductor. Esta transición perfecta asegura que el sistema continúe funcionando normalmente durante las interrupciones de alimentación.

Puede verificar el indicador LED BAT para confirmar si la batería está actualmente alimentando el sistema.




**Corriente de Carga**

La corriente de carga está sujeta a dos tipos de limitaciones:

.. note::

   La corriente de carga está determinada tanto por la "Limitación de Carga por Alimentación de Terminal de Tornillo" como por la "Limitación de Selección de Potencia de Carga" y está limitada por el valor más pequeño entre las dos.

1. Limitación de Carga por Alimentación de Terminal de Tornillo

   Al suministrar alimentación a través de la entrada de terminal de tornillo, la corriente de carga se ajusta automáticamente según el voltaje de entrada, como se muestra a continuación:

   .. list-table::
      :header-rows: 1

      * - Voltaje de Entrada (VBUS)
        - Corriente de Carga Máxima
      * - 4.5 < VBUS ≤ 6.5V
        - 3A
      * - 6.5 < VBUS ≤ 9.5V
        - 2A
      * - 9.5 < VBUS ≤ 13.5V
        - 1.5A
      * - 13.5 < VBUS ≤ 16.5V
        - 2A

2. Limitación de Selección de Potencia de Carga

   Un DIP switch de 2 posiciones en la placa permite la selección de diferentes niveles de potencia de carga. La asignación correspondiente de potencia de carga y potencia de salida para cada configuración es la siguiente:

   .. image:: img/power_selector.png
     :width: 50%
     :align: center

   .. list-table::
      :header-rows: 1

      * - Carga Sel 1
        - Carga Sel 2
        - Potencia de Carga
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


**Cómo elegir la potencia de carga**

La fórmula es:

*Capacidad de la fuente de alimentación = Potencia requerida por Raspberry Pi + Potencia de carga*

Recomendamos estimar el requisito de potencia del Raspberry Pi en **20W a 25W**.

- Si usa una **fuente de alimentación de 30W**, configure la potencia de carga a **10W** o **5W**.
- Si usa una **fuente de alimentación de 45W**, puede configurar con seguridad la potencia de carga a **20W**.

Si está familiarizado con las necesidades de potencia de su Raspberry Pi, puede establecer una potencia de carga más alta siempre que reserve suficiente margen para picos de potencia ocasionales.

⚠️ Tenga cuidado: una potencia insuficiente puede causar que el Raspberry Pi se apague inesperadamente.




**Proceso de Carga**

- Cuando el voltaje de la batería ``VBAT <= 2.5V``, el sistema realiza carga por goteo a baja corriente, aproximadamente 50 mA.
- Cuando ``2.5V < VBAT <= VTRKL``, la carga por goteo continúa, y la corriente de carga de la batería aumenta a aproximadamente 200 mA.
- Cuando ``VTRKL < VBAT < VCV``, el sistema cambia a carga de corriente constante, suministrando una corriente constante preestablecida a la batería.
- Una vez que ``VBAT = VCV``, y el voltaje de la batería se acerca al nivel de completamente cargada, la corriente de carga disminuye gradualmente, transitando a carga de voltaje constante.
- Durante la carga de voltaje constante, cuando la corriente de carga cae por debajo de ``ISTOP`` y el voltaje de la batería está cerca del umbral de voltaje constante, la carga se detiene, y la batería entra en un estado de completamente cargada.
- En el estado de completamente cargada, el sistema monitorea continuamente el voltaje de la batería. Si el voltaje cae por debajo de ``VRCH``, la carga se reanuda automáticamente.

**Características de Protección**

El PiPower 5 ofrece características de protección integrales, incluyendo protección contra subvoltaje y sobrevoltaje de entrada, así como protección contra sobrecalentamiento tanto para el chip de carga como para el convertidor DC-DC. Estas características aseguran un funcionamiento estable y confiable del sistema.

**Balanceo de Carga**

El chip de balanceo de carga integrado activa una resistencia de 60Ω para descargar la batería a baja corriente cuando detecta que el voltaje de una sola celda excede 4.2V. Esta característica ayuda a mantener el equilibrio de voltaje entre celdas.

**Protección de Temperatura**

El proceso de carga se detiene automáticamente cuando la temperatura interna del chip de carga excede 125°C. De manera similar, el chip DC-DC deshabilita la salida cuando su temperatura interna supera los 150°C.

.. _power_button:

Botón de Encendido
------------------





.. image:: img/power_button.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

Botón de encendido integrado para controlar la alimentación de la placa:

* **Pulsación simple**: Activa la salida.
* **Mantener presionado durante 2 segundos hasta que los dos LEDs centrales de batería se enciendan, luego soltar**: Envía una solicitud de apagado a través de I2C.
* **Mantener presionado por más de 5 segundos**: Apaga directamente la salida.


.. _battery_indicators:

Indicadores de Batería
--------------------------------

Cuatro LEDs integrados indican el nivel de batería y el estado de carga.

.. note::

   Si el dispositivo se está cargando durante el apagado, la luz indicadora continuará mostrando el estado de carga hasta que la carga esté completa.





.. image:: img/battery_indicator.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

* **4 LEDs encendidos**: Batería >80%
* **3 LEDs encendidos**: 60%< Batería <80%
* **2 LEDs encendidos**: 40%< Batería <60%
* **1 LED encendido**: 20%< Batería <40%
* **Primer LED parpadeando**: Batería <20%
* **Los LEDs se encienden secuencialmente en un ciclo**: Carga en progreso
* **Dos LEDs centrales parpadeando**: Esperando señal de apagado
* **Todos los LEDs apagados**: Sin alimentación o en modo reposo

.. _battery_connector:

Conector de Batería
------------------------
Conector de batería VH3.96 2P y conector de batería de terminal de tornillo.

.. image:: img/battery_pin.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

.. _cap_btn:

Terminal y Conector de Botón de Encendido Externo
---------------------------------------------------

.. image:: img/btn_jumper.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

Este terminal o conector está diseñado para conectar un botón de encendido externo. Conecte un interruptor momentáneo, como un pulsador táctil o un botón metálico de estilo vintage, a los pines del jumper. Los dos cables del botón se pueden conectar a los pines del jumper en cualquier dirección, ya que no se requiere polaridad. Una vez conectado, puede usar el botón externo igual que el botón de encendido integrado.

.. _cap_sdsig:

Jumper SDSIG
------------





.. image:: img/sdsig_jumper.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

Proporciona detección de apagado para Raspberry Pi.

* Cuando se puentea a PI3V3, funciona con Raspberry Pi 4 y Pi 5.
* Cuando se cortocircuita al Pin 26, soporta Pi 3 y Pi Zero.

Después de la configuración adecuada, PiPower5 cortará la alimentación automáticamente una vez que el Raspberry Pi se apague.

.. _cap_onoff:

Jumper ON/OFF Predeterminado
-----------------------------





.. image:: img/default_jumper.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

Este jumper se usa para seleccionar si la salida de alimentación USB está habilitada por defecto después de un apagado. Use la tapa del jumper para conectar los pines etiquetados como ON u OFF para hacer la selección.

* Si la tapa del jumper está posicionada a la izquierda y conectada a OFF, insertar alimentación USB después de un apagado no activará la salida.
* Si la tapa del jumper está posicionada a la derecha y conectada a ON, insertar alimentación USB después de un apagado activará la salida.

Esta característica se usa típicamente para dispositivos que necesitan iniciarse automáticamente, como servidores personales. Por ejemplo, si hay un corte de energía, PiPower 5 tomará el control del suministro de energía del Raspberry Pi, asegurando un apagado seguro. Una vez que se restablece la energía, PiPower 5 enciende automáticamente el Raspberry Pi, eliminando la necesidad de intervención manual.

.. _pin_header:

Conectores de Pines para RPi
-----------------------------

El conector de pines está diseñado para conexión directa a un Raspberry Pi, incluyendo tanto comunicación I2C como suministro de energía.





.. image:: img/pin_header.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

El conector soporta el apilamiento de HATs adicionales. Sin embargo, tenga en cuenta que los pines I2C y el pin 26 ya están conectados y pueden necesitar ser gestionados cuidadosamente para evitar conflictos.

.. list-table::
   :widths: 15 15
   :header-rows: 1

   * - Raspberry Pi
     - MCU Integrado
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

Comunicación I2C
-------------------------------






.. image:: img/i2c.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

Dirección I2C: 0x5C

El microcontrolador integrado recopila varias señales de la placa y las almacena en registros. Estas señales se pueden acceder a través de I2C usando las siguientes tablas de registros.

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
       <caption>Tabla de Registros</caption>
       <thead>
           <tr>
               <th>Nombre</th>
               <th>Dirección</th>
               <th>Longitud de Datos</th>
               <th>Tipo de Dato</th>
               <th>Unidad</th>
               <th>Descripción</th>
           </tr>
       </thead>
       <tbody>
           <tr>
               <td>Voltaje de Entrada</td>
               <td>0</td>
               <td>2</td>
               <td>u16</td>
               <td>mV</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Corriente de Entrada</td>
               <td>2</td>
               <td>2</td>
               <td>u16</td>
               <td>mA</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Voltaje de Salida</td>
               <td>4</td>
               <td>2</td>
               <td>u16</td>
               <td>mV</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Corriente de Salida</td>
               <td>6</td>
               <td>2</td>
               <td>u16</td>
               <td>mA</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Voltaje de Batería</td>
               <td>8</td>
               <td>2</td>
               <td>u16</td>
               <td>mV</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Corriente de Batería</td>
               <td>10</td>
               <td>2</td>
               <td>i16</td>
               <td>mA</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Porcentaje de Batería</td>
               <td>12</td>
               <td>1</td>
               <td>u8</td>
               <td>%</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Capacidad de Batería</td>
               <td>13</td>
               <td>2</td>
               <td>u16</td>
               <td>mAh</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Fuente de Alimentación</td>
               <td>15</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>0: Batería no suministrando energía.<br> 1: Batería suministrando energía.</td>
           </tr>
           <tr>
               <td>Estado de Conexión USB</td>
               <td>16</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>0: USB desconectado.<br> 1: USB conectado.</td>
           </tr>
           <tr>
               <td>RESERVADO</td>
               <td>17</td>
               <td>1</td>
               <td>-</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Estado de Carga</td>
               <td>18</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>0: No cargando.<br> 1: Cargando.</td>
           </tr>
           <tr>
               <td>Potencia del Ventilador</td>
               <td>19</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Nivel de potencia del ventilador (0–100).</td>
           </tr>
           <tr>
               <td>Solicitud de Apagado</td>
               <td>20</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>1: Activado por batería baja.<br>2: Activado al presionar el botón de encendido.</td>
           </tr>
           <tr>
               <td>Versión de Firmware (Mayor)</td>
               <td>128</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Versión de Firmware (Menor)</td>
               <td>129</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Versión de Firmware (Parche)</td>
               <td>130</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Código de Reinicio</td>
               <td>131</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Código de razón de reinicio del MCU.</td>
           </tr>
           <tr>
               <td>RTC Año</td>
               <td>132</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RTC Mes</td>
               <td>133</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RTC Día</td>
               <td>134</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RTC Hora</td>
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
               <td>RTC Segundo</td>
               <td>137</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RTC Sub-Segundo</td>
               <td>138</td>
               <td>1</td>
               <td>u8</td>
               <td>1/128 s</td>
               <td>Sub-segundo RTC (1/128 segundo).</td>
           </tr>
           <tr>
               <td>Función Siempre Encendido</td>
               <td>139</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>0: Habilitado.<br> 1: Deshabilitado.</td>
           </tr>
           <tr>
               <td>ID de Placa</td>
               <td>140</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Identificación de placa: <br> 0: Pironman U1.<br> 1: Pironman 4.<br> 2: PiPower 3.<br>4: PiPower 5.</td>
           </tr>
           <tr>
               <td>RESERVADO</td>
               <td>141</td>
               <td>1</td>
               <td>-</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RESERVADO</td>
               <td>142</td>
               <td>1</td>
               <td>-</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Porcentaje de Apagado</td>
               <td>143</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Umbral actual de porcentaje de apagado por batería baja.</td>
           </tr>
           <tr>
               <td>RESERVADO</td>
               <td>144</td>
               <td>1</td>
               <td>-</td>
               <td>-</td>
               <td>-</td>
           </tr>
       </tbody>
   </table>


   <table class="custom-register-table">
       <caption>Tabla de Configuración de Registros</caption>
       <thead>
           <tr>
               <th>Nombre</th>
               <th>Dirección</th>
               <th>Longitud de Datos</th>
               <th>Tipo de Dato</th>
               <th>Unidad</th>
               <th>Descripción</th>
           </tr>
       </thead>
       <tbody>
           <tr>
               <td>Potencia del Ventilador</td>
               <td>0</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Establecer velocidad del ventilador (0–100).</td>
           </tr>
           <tr>
               <td>RTC Año</td>
               <td>1</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Establecer año RTC.</td>
           </tr>
           <tr>
               <td>RTC Mes</td>
               <td>2</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Establecer mes RTC.</td>
           </tr>
           <tr>
               <td>RTC Día</td>
               <td>3</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Establecer día RTC.</td>
           </tr>
           <tr>
               <td>RTC Hora</td>
               <td>4</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Establecer hora RTC.</td>
           </tr>
           <tr>
               <td>RTC Minuto</td>
               <td>5</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Establecer minuto RTC.</td>
           </tr>
           <tr>
               <td>RTC Segundo</td>
               <td>6</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Establecer segundo RTC.</td>
           </tr>
           <tr>
               <td>RTC Sub-Segundo</td>
               <td>7</td>
               <td>1</td>
               <td>u8</td>
               <td>1/128 s</td>
               <td>Establecer sub-segundo RTC.</td>
           </tr>
           <tr>
               <td>Configuración RTC</td>
               <td>8</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Habilitar configuración RTC: <br> 1: Habilitado.</td>
           </tr>
           <tr>
               <td>Porcentaje de Apagado</td>
               <td>9</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Establecer umbral de porcentaje de apagado por batería baja (0–100).</td>
           </tr>
           <tr>
               <td>Porcentaje de Corte de Alimentación</td>
               <td>10</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Establecer umbral de porcentaje de corte de alimentación por batería baja (0–100).</td>
           </tr>
       </tbody>
   </table>

