Guía Rápida de Usuario
===============================

Esta guía le ayuda a comenzar rápidamente con PiPower 5 después del montaje del hardware.

Cargar la Batería
----------------------------------------------------

Antes del primer uso, cargue completamente la batería.

Recomendaciones:

- Use un adaptador de corriente USB-C de alta calidad
- Se recomienda una fuente de alimentación de 5V 5A para Raspberry Pi 5
- Se recomiendan adaptadores de mayor potencia al usar SSD u otros periféricos de alto consumo

Durante la Carga:

- Use una fuente de alimentación USB-C de alta calidad para cargar PiPower 5.

  .. image:: img/power_input.png
     :width: 50%
     :align: center

- Durante la carga, los LEDs indicadores de batería se encienden progresivamente en secuencia.

  .. image:: img/battery_indicator.png
     :width: 50%
     :align: center

  El estado de la batería se indica por el número de LEDs encendidos:

  * **4 LEDs encendidos**: Batería >80%
  * **3 LEDs encendidos**: 60%< Batería <80%
  * **2 LEDs encendidos**: 40%< Batería <60%
  * **1 LED encendido**: 20%< Batería <40%
  * **Primer LED parpadeando**: Batería <20%
  * **LEDs se encienden incrementalmente en un ciclo**: Cargando
  * **Dos LEDs centrales parpadeando**: Esperando señal de apagado
  * **Todos los LEDs apagados**: Sin alimentación o en modo reposo
  * Durante la carga, el indicador permanece encendido **incluso en estado apagado** hasta que esté completamente cargado.

Encender
----------------------------------------------------

Para dispositivos Raspberry Pi, no se requiere cableado de alimentación adicional. PiPower 5 suministra alimentación directamente a través del conector GPIO.

Para otros dispositivos, puede alimentarlos usando:

- El puerto de salida USB-A
- Los pines 5V/GND junto al puerto USB-A

.. image:: img/power_output.png
   :width: 50%
   :align: center

Presione el botón de encendido una vez para encender PiPower 5. Cuando está encendido:

- El **LED PWR** se enciende
- El dispositivo conectado comienza a recibir alimentación de PiPower 5

.. image:: img/pwr_led.png
   :width: 50%
   :align: center

.. include:: /pipower5_software.rst
    :start-after: start_install_pipower5
    :end-before: end_install_pipower5

Abrir el Panel de Control Web
----------------------------------------------------

Después de la instalación, abra el panel de control en su navegador:

.. code-block:: text

   http://<dirección-ip-raspberry-pi>:34001

El panel de control le permite:

- Ver el porcentaje de batería
- Monitorear el estado de carga
- Verificar voltaje y corriente
- Configurar el porcentaje de apagado
- Gestionar notificaciones

.. image:: img/web_dashboard.png
   :width: 100%
   :align: center


Apagado Seguro
----------------------------------------------------

.. include:: /pipower5_software.rst
    :start-after: start_power_off_after_shutdown
    :end-before: end_power_off_after_shutdown

.. note::

   Para funciones avanzadas y opciones de configuración detalladas, incluyendo:

   - Comandos de monitoreo de alimentación
   - Configuración de notificaciones
   - Alertas de zumbador
   - Alertas de correo electrónico
   - Configuración avanzada

   Consulte:

   * :ref:`pipower5_tool`
