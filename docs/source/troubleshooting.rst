.. note::

    ¡Hola, bienvenido a la Comunidad de Entusiastas de Raspberry Pi & Arduino & ESP32 de SunFounder en Facebook! Profundice en Raspberry Pi, Arduino y ESP32 con otros entusiastas.

    **¿Por qué unirse?**

    - **Soporte Experto**: Resuelva problemas posventa y desafíos técnicos con la ayuda de nuestra comunidad y equipo.
    - **Aprenda y Comparta**: Intercambie consejos y tutoriales para mejorar sus habilidades.
    - **Avances Exclusivos**: Obtenga acceso anticipado a anuncios de nuevos productos y adelantos.
    - **Descuentos Especiales**: Disfrute de descuentos exclusivos en nuestros productos más nuevos.
    - **Promociones Festivas y Sorteos**: Participe en sorteos y promociones navideñas.

    👉 ¿Listo para explorar y crear con nosotros? ¡Haga clic [|link_sf_facebook|] y únase hoy!

.. _troubleshooting:

Solución de Problemas
=====================

Esta página le ayuda a diagnosticar problemas de PiPower 5 usando los LEDs integrados, el zumbador y las herramientas de software. Comience con las tablas de referencia rápida a continuación, luego siga las guías basadas en síntomas para pasos detallados.

.. contents:: Tabla de Contenidos
   :local:
   :depth: 2


----------------------------------------
Referencia Rápida de LEDs y Zumbador
----------------------------------------

Antes de profundizar en síntomas específicos, use estas tablas para interpretar lo que la placa le está diciendo.

LEDs de Alimentación y Estado
+++++++++++++++++++++++++++++

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - LED
     - Estado
     - Lo Que Significa
   * - **LED PWR** (verde)
     - ENCENDIDO
     - La alimentación de salida está activa — la placa está suministrando 5V a su dispositivo.
   * -
     - APAGADO
     - La salida está apagada. Presione el botón de encendido una vez para encenderla.
   * - **LED BAT** (amarillo)
     - ENCENDIDO
     - La batería está suministrando energía actualmente. Si la alimentación externa está conectada, esto indica potencia de entrada insuficiente.
   * -
     - APAGADO
     - La batería está en espera — la alimentación externa es suficiente.
   * - **LEDs de Batería Inversa** (2× rojo)
     - ENCENDIDOS (ambos)
     - ¡La polaridad de la batería está invertida! Desconecte inmediatamente y corrija el cableado.

LEDs de Nivel de Batería
++++++++++++++++++++++++

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Patrón de LEDs
     - Significado
   * - 4 LEDs encendidos
     - Batería > 80%
   * - 3 LEDs encendidos
     - Batería 60% – 80%
   * - 2 LEDs encendidos
     - Batería 40% – 60%
   * - 1 LED encendido
     - Batería 20% – 40%
   * - Primer LED parpadeando
     - Batería < 20% — cargar pronto
   * - LEDs ciclando secuencialmente
     - Carga en progreso
   * - Dos LEDs centrales parpadeando
     - Esperando señal de apagado del Raspberry Pi
   * - Todos los LEDs apagados
     - Placa sin alimentación o en modo reposo

.. note::

   Los LEDs de batería permanecen activos durante la carga incluso cuando la placa está en estado apagado. Se apagan solo cuando la carga está completa.

Señales del Zumbador
++++++++++++++++++++

Si el zumbador está habilitado, estos sonidos indican eventos específicos:

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Evento
     - Sonido Típico
     - Lo Que Significa
   * - ``battery_activated``
     - Dos tonos ascendentes
     - La batería ha tomado el suministro de energía (alimentación externa perdida o insuficiente).
   * - ``low_battery``
     - Dos tonos repetidos del mismo tono
     - El nivel de batería ha caído por debajo del porcentaje de apagado configurado. Cargue inmediatamente.
   * - ``power_disconnected``
     - Tono alto → tono bajo
     - La alimentación externa fue desconectada. El sistema ahora funciona con batería.
   * - ``power_restored``
     - Tono bajo → tono alto
     - La alimentación externa fue restaurada. La batería ya no se está descargando.
   * - ``power_insufficient``
     - Tres tonos rápidos del mismo tono
     - La alimentación externa está conectada pero es demasiado débil. La batería está suplementando. Verifique su adaptador de corriente.
   * - ``battery_critical_shutdown``
     - Tres tonos descendentes rápidos
     - Capacidad de batería críticamente baja. El sistema se apagará.
   * - ``battery_voltage_critical_shutdown``
     - Cuatro tonos descendentes rápidos
     - Voltaje de batería críticamente bajo (seguridad). El sistema se apagará inmediatamente.

.. tip::

   Si nunca escucha sonidos del zumbador, el zumbador puede estar deshabilitado o su volumen configurado a 0. Ejecute ``pipower5 -bzv`` para verificar el volumen actual, o pruebe con ``pipower5 -bzt low_battery``.


-------------------------------
Diagnóstico Basado en Síntomas
-------------------------------

"Sin Alimentación" — Todos los LEDs Apagados, Sin Salida
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

**Lo que ve**: LED PWR apagado, LEDs de batería apagados, el dispositivo conectado no muestra alimentación.

**Compruebe esto, en orden:**

1. **¿Está la batería instalada?**
   PiPower 5 no puede funcionar sin una batería. Asegúrese de que el conector de batería (XH2.54 3P) esté firmemente asentado. Consulte :ref:`battery_connector`.

2. **¿Está la batería completamente agotada?**
   Una batería profundamente descargada (< 2.5V por celda) entra en modo de carga por goteo y puede no alimentar la placa durante varios minutos.

   - Conecte alimentación externa y espere 10–15 minutos.
   - Si los LEDs de batería permanecen apagados después de 15 minutos, la batería puede estar defectuosa.

3. **¿Está la alimentación externa conectada correctamente?**
   - Use una fuente de alimentación USB-C PD (5V–15V) o alimentación DC a través de los terminales de tornillo.
   - Asegúrese de que el cable USB-C soporte power delivery — algunos cables solo de datos no funcionarán.
   - Pruebe con un adaptador de corriente y cable diferentes.

4. **Presione el botón de encendido una vez.**
   PiPower 5 requiere una pulsación del botón para activar la salida, a menos que el jumper de Encendido Predeterminado esté configurado.

5. **Verifique el jumper de Encendido Predeterminado.** Consulte :ref:`cap_onoff`.
   - Jumper en **ON**: La salida se activa automáticamente cuando se conecta la alimentación externa.
   - Jumper en **OFF**: Debe presionar el botón de encendido cada vez.

6. **Verifique la instalación inversa de la batería.**
   Si ambos LEDs rojos cerca del conector de batería están encendidos, la polaridad de la batería está invertida. Apague inmediatamente, desconecte la batería y vuelva a conectar con la polaridad correcta. Consulte :ref:`battery_connector`.


"LED BAT Siempre Encendido" — La Alimentación Externa Parece Insuficiente
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

**Lo que ve**: La alimentación externa está conectada, pero el LED BAT permanece encendido. La batería se está descargando a pesar de que hay alimentación externa presente.

**Lo que esto significa**: La fuente de alimentación externa no puede satisfacer la demanda total de energía. La batería está suplementando el déficit.

**Compruebe esto, en orden:**

1. **¿Es su adaptador de corriente suficientemente potente?**
   La fórmula es: *Potencia del adaptador ≥ Potencia del Raspberry Pi (~20–25W) + Potencia de carga (configurada mediante DIP switch)*.

   - Raspberry Pi 5 bajo carga puede consumir > 25W.
   - Si la potencia de carga está configurada a 20W (ambos DIP switches en ON), necesita un adaptador de **45W+**.
   - Para un adaptador de 30W, reduzca la potencia de carga a 10W o 5W.

2. **Verifique el DIP switch (selector de potencia de carga).**
   Consulte la tabla de potencia de carga en :ref:`power_input`. Reduzca la potencia de carga si su adaptador es de baja potencia.

3. **Pruebe con un cable USB-C diferente.**
   No todos los cables soportan USB PD a potencias más altas. Use el cable que vino con su adaptador de corriente.

4. **Verifique el perfil PD del adaptador.**
   Algunos adaptadores anuncian alta potencia pero solo en combinaciones específicas de voltaje/corriente. PiPower 5 requiere una fuente compatible con PD. Los adaptadores no PD (ej., solo 5V fijo) pueden no proporcionar suficiente corriente.

5. **Para entrada por terminal de tornillo**, asegúrese de que el voltaje de entrada sea ≥ 9V para un rendimiento óptimo. Consulte :ref:`power_input` para los límites de voltaje a corriente.


"LED PWR Apagado" — El Dispositivo No Recibe Alimentación
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

**Lo que ve**: Los LEDs de batería están encendidos (la placa tiene alimentación), pero el LED PWR está apagado y el dispositivo conectado no arranca.

**Compruebe esto:**

1. **Presione el botón de encendido una vez.**
   La placa tiene alimentación pero la salida no está habilitada.

2. **¿Está el conector GPIO correctamente asentado?**
   Si está usando un Raspberry Pi, retire y vuelva a colocar el HAT PiPower 5. Verifique si hay pines doblados o residuos en el conector.

3. **Pruebe una salida alternativa.**
   Conecte un dispositivo al puerto USB-A o al conector 2x4P. Si estos funcionan, el problema está en el paso a través de GPIO.


"El Dispositivo Se Sigue Apagando Inesperadamente"
+++++++++++++++++++++++++++++++++++++++++++++++++++

**Lo que ve**: El Raspberry Pi o dispositivo conectado se apaga sin advertencia.

**Compruebe esto:**

1. **Verifique el porcentaje de apagado.**
   Ejecute ``pipower5 -sp``. Si está configurado alto (ej., 50% o más), la placa activará un apagado temprano. Establezca un valor más bajo si es necesario:

   .. code-block:: shell

      pipower5 -sp 10
      sudo systemctl restart pipower5.service

2. **Verifique si la batería se está descargando realmente.**
   Ejecute ``pipower5 -a`` y observe:
   - ``source``: Debe ser "0 - External" cuando la alimentación externa está conectada.
   - ``battery current``: Negativo = cargando, positivo = descargando.

3. **Para Raspberry Pi 5 con periféricos de alta potencia (SSD, HATs)**:
   Considere configurar ``pipower5 -sp 100`` para activar un apagado seguro inmediato cuando se pierde la alimentación externa. Consulte :ref:`pipower5_tool`.

4. **Verifique el adaptador de corriente.**
   Si se activan eventos ``power_insufficient`` (zumbador o registro), el adaptador es demasiado débil. Actualice a una fuente de mayor potencia o reduzca el DIP switch de potencia de carga.


"La Batería No Carga"
++++++++++++++++++++++

**Lo que ve**: Alimentación externa conectada, pero los LEDs de batería no muestran la animación de carga (ciclo secuencial).

**Compruebe esto:**

1. **¿Está la batería ya llena?**
   4 LEDs fijos = batería > 80%. El circuito de carga puede haberse detenido porque la batería está llena o en la fase de voltaje constante.

2. **Verifique el estado de carga mediante software.**
   Ejecute ``pipower5 -ichg``. Si devuelve ``False``, la placa informa que no está cargando. Verifique ``pipower5 -bp`` para el porcentaje de batería actual.

3. **Protección de sobretemperatura activa.**
   Si la placa ha estado bajo carga pesada en un ambiente cálido, el chip de carga puede haber excedido 125°C y detenido la carga. Deje que la placa se enfríe e intente de nuevo.

4. **Voltaje de entrada demasiado bajo por terminales de tornillo.**
   Si usa terminales de tornillo con voltaje ≤ 6.5V, la corriente de carga está limitada. Use ≥ 9V para una carga confiable.

5. **Verifique la salud de la batería.**
   Una batería que nunca alcanza la carga completa o carga muy lentamente puede tener celdas degradadas. Pruebe con una batería compatible diferente (7.4V 2 celdas Ion de Litio, XH2.54 3P).


"Fallo de Comunicación I2C" — El Comando `pipower5` Devuelve Errores
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

**Lo que ve**: Ejecutar ``pipower5 -a`` produce un error o no hay datos.

**Compruebe esto:**

1. **¿Está I2C habilitado en el Raspberry Pi?**
   Ejecute ``sudo raspi-config`` → Interface Options → I2C → Enable.

2. **¿Se detecta el dispositivo I2C?**

   .. code-block:: shell

      sudo i2cdetect -y 1

   PiPower 5 debería aparecer en la dirección ``0x5a``. Si no aparece ningún dispositivo:

   - Reasiente el HAT en el conector GPIO.
   - Verifique que ``i2c-dev`` esté cargado: ``lsmod | grep i2c``.
   - Verifique que ``dtparam=i2c_arm=on`` esté en ``/boot/firmware/config.txt``.

3. **¿Está el servicio `pipower5` en ejecución?**

   .. code-block:: shell

      sudo systemctl status pipower5.service

   Si está inactivo, inícielo: ``sudo systemctl start pipower5.service``.

4. **¿Conflicto de múltiples dispositivos I2C?**
   PiPower 5 usa la dirección I2C ``0x5a``. Verifique que ningún otro HAT o dispositivo esté usando esta dirección. Consulte :ref:`pin_header`.

5. **Reinicie.**
   A veces un reinicio en frío tanto del Raspberry Pi como de PiPower 5 resuelve problemas del bus I2C. Apague completamente, espere 10 segundos, luego encienda.


"Zumbador Silencioso" — Sin Sonido en Eventos
++++++++++++++++++++++++++++++++++++++++++++++

**Lo que ve**: Ocurren eventos (desconexión de alimentación, batería baja, etc.) pero no hay sonido del zumbador.

**Compruebe esto:**

1. **Verifique el volumen del zumbador.**

   .. code-block:: shell

      pipower5 -bzv

   Si devuelve 0, el zumbador está silenciado. Configure un volumen (1–10):

   .. code-block:: shell

      pipower5 -bzv 5
      sudo systemctl restart pipower5.service

2. **Verifique qué eventos tienen el zumbador habilitado.**

   .. code-block:: shell

      pipower5 -bzo

   Asegúrese de que el evento que espera esté en la lista. Para agregar un evento:

   .. code-block:: shell

      pipower5 -bzo low_battery,power_disconnected

3. **Pruebe el zumbador directamente.**

   .. code-block:: shell

      pipower5 -bzt low_battery

   Si escucha sonido, el hardware del zumbador está funcionando — el problema está en la configuración de eventos.


"pipower5 Service Fails to Start" — 32-bit System
+++++++++++++++++++++++++++++++++++++++++++++++++++

**What you see**: After installation, ``sudo systemctl status pipower5.service``
shows the service failed to start, or ``pipower5`` commands return errors.

**Check your system architecture:**

.. code-block:: shell

   uname -m

If the output is ``armv7l``, you are running a **32-bit** version of Raspberry Pi OS.
PiPower 5 only supports **64-bit** systems (``aarch64``).

**Solution**: Reinstall your Raspberry Pi with the 64-bit version of Raspberry Pi OS,
then reinstall PiPower 5.


"El Raspberry Pi Muestra Advertencia de Bajo Voltaje"
+++++++++++++++++++++++++++++++++++++++++++++++++++++

**Lo que ve**: El escritorio del Raspberry Pi o ``dmesg`` muestra advertencias de bajo voltaje.

**Este es un comportamiento esperado en algunos casos:**

- Al alimentar un Raspberry Pi desde el puerto USB-A del PiPower 5 (en lugar del conector GPIO), el Pi puede informar una advertencia de fuente de alimentación no PD. Esto se puede ignorar de forma segura.
- Si está usando el conector GPIO y aún ve advertencias, la salida de PiPower 5 puede estar bajo carga pesada. Verifique el consumo total de corriente de su configuración.

**Compruebe esto:**

1. Ejecute ``pipower5 -a`` y verifique ``Output: voltage``. Debe ser estable alrededor de 5.2–5.3V. Si cae por debajo de 5.0V bajo carga, el consumo total de corriente puede exceder el límite de 5A.

2. Desconecte periféricos USB no esenciales y vuelva a probar.

3. Si el problema persiste, el convertidor DC-DC puede estar defectuoso. Contacte con soporte.


--------------------------------------
Comandos de Diagnóstico por Software
--------------------------------------

La herramienta CLI ``pipower5`` es su interfaz de diagnóstico principal. Aquí están los comandos más útiles:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Comando
     - Lo Que Le Dice
   * - ``pipower5 -a``
     - Instantánea completa del estado: voltaje de entrada/salida, estado de batería, estado de carga, solicitud de apagado, estado del botón.
   * - ``pipower5 -bp``
     - Porcentaje de batería.
   * - ``pipower5 -ichg``
     - Si la batería se está cargando actualmente (``True`` / ``False``).
   * - ``pipower5 -ii``
     - Si la alimentación externa está conectada.
   * - ``pipower5 -sp``
     - Umbral actual del porcentaje de apagado.
   * - ``pipower5 -sr``
     - Estado actual de solicitud de apagado (0 = Ninguna, 1 = Batería Baja, 2 = Botón).
   * - ``pipower5 -pb``
     - Estado actual del botón de encendido.
   * - ``pipower5 -bzv``
     - Volumen actual del zumbador.
   * - ``pipower5 -fv``
     - Versión de firmware (verifique que tiene la última).
   * - ``pipower5 -c``
     - Volcado completo de configuración.
   * - ``pipower5 -pfs 60``
     - Ejecutar una simulación de fallo de alimentación de 60 segundos para probar la autonomía de la batería.
   * - ``sudo systemctl status pipower5.service``
     - Verificar si el servicio en segundo plano de PiPower 5 está en ejecución.
   * - ``cat /opt/pipower5/log``
     - Ver registros del servicio para mensajes de error.

.. tip::

   Para una verificación rápida de salud, ejecute ``pipower5 -a`` y verifique:

   - ``shutdown request`` es ``0 - NONE`` (sin apagado pendiente).
   - ``battery percentage`` está por encima de su ``shutdown percentage``.
   - ``Output: voltage`` está entre 5.1V y 5.4V.


--------------------------
¿Sigue Teniendo Problemas?
--------------------------

Si nada de lo anterior resuelve su problema, recopile la siguiente información antes de contactar con soporte:

1. **Información del sistema**:

   .. code-block:: shell

      pipower5 -a
      pipower5 -fv
      pipower5 -c

2. **Registros del servicio**:

   .. code-block:: shell

      cat /opt/pipower5/log
      sudo journalctl -u pipower5.service --no-pager -n 100

3. **Detalles del hardware**:
   - Modelo de Raspberry Pi
   - Modelo de adaptador de corriente y potencia nominal
   - Tipo y antigüedad de la batería
   - Configuración del DIP switch de PiPower 5
   - Posiciones de los jumpers SDSIG y Default ON

