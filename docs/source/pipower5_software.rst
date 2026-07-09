.. _pipower5_tool:

Herramienta PiPower 5
===============================

La Herramienta PiPower 5 es el software complementario para PiPower 5.

Proporciona:

- Soporte de apagado seguro
- Gestión de batería y carga
- Monitoreo de alimentación
- Acceso al Panel de Control Web
- Notificaciones de eventos

PiPower 5 puede enviar solicitudes de apagado al Raspberry Pi en las siguientes situaciones:

- El botón PiPower se mantiene presionado durante 2 segundos
- El nivel de batería cae por debajo del porcentaje de apagado configurado

Después de que el Raspberry Pi complete el apagado, PiPower 5 puede desconectar automáticamente la alimentación para ayudar a prevenir la corrupción de la tarjeta SD y problemas de pérdida inesperada de alimentación.

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

Instalar la Herramienta ``pipower5``
----------------------------------------------------

Instale la Herramienta PiPower 5:

1. Clonar el repositorio:

   .. code-block:: shell

      git clone https://github.com/sunfounder/pipower5

2. Entrar en el directorio:

   .. code-block:: shell

      cd pipower5

3. Ejecutar el instalador:

   .. code-block:: shell

      sudo python3 install.py

4. Reinicie el Raspberry Pi cuando se le solicite.

.. end_install_pipower5

Referencia de Comandos
---------------------------------------

La herramienta ``pipower5`` proporciona acceso a la información de estado y opciones de configuración de PiPower 5.

Por ejemplo, el siguiente comando muestra el estado actual de PiPower 5:

.. code-block:: shell

   pipower5 -a

Ejemplo de salida:

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

Puede personalizar estas configuraciones según sus necesidades.

Use ``pipower5`` o ``pipower5 -h`` para instrucciones.

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
    {start,stop}          Comando

  options:
    -h, --help            mostrar este mensaje de ayuda y salir
    -v, --version         Mostrar versión
    -c, --config          Mostrar configuración
    -drd [DATABASE_RETENTION_DAYS], --database-retention-days [DATABASE_RETENTION_DAYS]
                          Días de retención de la base de datos
    -dl [{debug,info,warning,error,critical}], --debug-level [{debug,info,warning,error,critical}]
                          Nivel de depuración
    -rd, --remove-dashboard
                          Eliminar panel de control
    -cp [CONFIG_PATH], --config-path [CONFIG_PATH]
                          Ruta de configuración
    -sp [SHUTDOWN_PERCENTAGE], --shutdown-percentage [SHUTDOWN_PERCENTAGE]
                          Establecer porcentaje de apagado, dejar vacío para leer
    -iv, --input-voltage  Leer voltaje de entrada
    -ic, --input-current  Leer corriente de entrada
    -ov, --output-voltage
                          Leer voltaje de salida
    -oc, --output-current
                          Leer corriente de salida
    -bv, --battery-voltage
                          Leer voltaje de batería
    -bc, --battery-current
                          Leer corriente de batería
    -bp, --battery-percentage
                          Leer porcentaje de batería
    -bs, --battery-source
                          Leer fuente de batería
    -ii, --is-input-plugged_in
                          Leer si la entrada está conectada
    -ichg, --is-charging  Leer si está cargando
    -do, --default-on     Leer encendido predeterminado
    -sr, --shutdown-request
                          Leer solicitud de apagado
    -pb, --power-btn      Leer botón de encendido
    -cc, --charging-current
                          Corriente máxima de carga
    -a, --all             Mostrar todo el estado
    -fv, --firmware       Versión de firmware de PiPower5
    -pfs [POWER_FAILURE_SIMULATION], --power-failure-simulation [POWER_FAILURE_SIMULATION]
                          Simulación de fallo de alimentación
    -seo [SEND_EMAIL_ON], --send-email-on [SEND_EMAIL_ON]
                          Enviar correo en: ['battery_activated', 'low_battery',
                          'power_disconnected', 'power_restored',
                          'power_insufficient', 'battery_critical_shutdown',
                          'battery_voltage_critical_shutdown']
    -set [SEND_EMAIL_TO], --send-email-to [SEND_EMAIL_TO]
                          Dirección de correo para enviar
    -ss [SMTP_SERVER], --smtp-server [SMTP_SERVER]
                          Servidor SMTP
    -smp [SMTP_PORT], --smtp-port [SMTP_PORT]
                          Puerto SMTP
    -se [SMTP_EMAIL], --smtp-email [SMTP_EMAIL]
                          Correo SMTP
    -spw [SMTP_PASSWORD], --smtp-password [SMTP_PASSWORD]
                          Contraseña SMTP
    -ssc [SMTP_SECURITY], --smtp-security [SMTP_SECURITY]
                          Seguridad SMTP, 'none', 'ssl' o 'tls'
    -bzo [BUZZ_ON], --buzz-on [BUZZ_ON]
                          Zumbador en: ['battery_activated', 'low_battery',
                          'power_disconnected', 'power_restored',
                          'power_insufficient', 'battery_critical_shutdown',
                          'battery_voltage_critical_shutdown']
    -bzv [BUZZER_VOLUME], --buzzer-volume [BUZZER_VOLUME]
                          Volumen del zumbador
    -bzt [BUZZER_TEST], --buzzer-test [BUZZER_TEST]
                          Probar zumbador en evento seleccionado.
    -u [{C,F}], --temperature-unit [{C,F}]
                          Unidad de temperatura

.. note::

   Cada vez que modifique el estado de ``pipower5.service``, necesita usar el siguiente comando para que los cambios de configuración surtan efecto.

   .. code-block:: shell

      sudo systemctl restart pipower5.service

   Verifique el estado del programa pipower5 usando la herramienta systemctl.

   .. code-block:: shell

      sudo systemctl status pipower5.service

   Alternativamente, inspeccione los archivos de registro generados por el programa.

   .. code-block:: shell

      cat /opt/pipower5/log

Panel de Control Web
----------------------------------------------------

La Herramienta PiPower 5 incluye un Panel de Control Web integrado para monitoreo y configuración.

Acceda al panel de control desde su navegador:

.. code-block:: text

   http://<dirección-ip-raspberry-pi>:34001

Las funciones del panel incluyen:

- Monitoreo del porcentaje de batería
- Monitoreo del estado de carga
- Monitoreo de voltaje de entrada y salida
- Monitoreo de corriente
- Configuración del porcentaje de apagado
- Gestión de notificaciones
- Información del dispositivo Raspberry Pi

.. image:: img/web_dashboard.png
   :width: 100%
   :align: center

.. image:: img/web_dashboard_2.png
   :width: 100%
   :align: center

También puede configurar el porcentaje de apagado directamente desde el panel de control:

.. image:: img/web_dashboard_3.png
   :width: 100%
   :align: center

Si no necesita el panel de control, elimínelo con:

.. code-block:: shell

   pipower5 --remove-dashboard

Apagado Seguro
----------------------------------------------------

PiPower 5 soporta protección de apagado seguro automático para sistemas Raspberry Pi.

Flujo de trabajo de apagado:

.. code-block:: text

   Apagado activado
   -> El Raspberry Pi realiza un apagado seguro
   -> PiPower 5 detecta la finalización del apagado
   -> PiPower 5 corta automáticamente la alimentación

Esto ayuda a prevenir:

- Corrupción de la tarjeta SD
- Daños en el sistema de archivos
- Problemas de pérdida inesperada de alimentación


Corte de Alimentación Después del Apagado del Raspberry Pi
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. start_power_off_after_shutdown

Para permitir que PiPower 5 corte automáticamente la alimentación después de que el Raspberry Pi se apague, se requiere cierta configuración adicional.

1. Si está usando un **Raspberry Pi 4 o 5**:

   * Asegúrese de que el jumper ``SDSIG`` en PiPower 5 esté conectado a ``PI3V3``.

     .. image:: img/safe_shutdown_3v3.png
        :width: 400

   * Abra la Configuración de Raspberry Pi:

     .. code-block:: shell

        sudo raspi-config

   * Navegue a:

     .. code-block:: text

        6 Advanced Options
        -> A11 Shutdown Behaviour
        -> B1 Full power off Switch off Pi ...

   * Reinicie el Raspberry Pi cuando se le solicite.

2. Si está usando un **Raspberry Pi 3** o anterior:

   * Configure el jumper ``SDSIG`` en PiPower 5 a ``GPIO26``.

     .. image:: img/safe_shutdown_io26.png
        :width: 400

   * Abra ``/boot/firmware/config.txt``:

     .. code-block:: shell

        sudo nano /boot/firmware/config.txt

   * Agregue las siguientes líneas:

     .. code-block:: shell

        dtoverlay=gpio-poweroff,gpio_pin=26,active_low=1
        gpio=26=op,dh

   * Presione ``Ctrl+X``, luego ``Y``, y presione ``Enter`` para guardar el archivo y salir.

   * Reinicie el Raspberry Pi.

     .. code-block:: shell

        sudo reboot

Después de la configuración, PiPower 5 puede detectar automáticamente el apagado del Raspberry Pi y desconectar la alimentación de forma segura.

Los métodos de apagado seguro soportados incluyen:

- Mantener presionado el botón PiPower durante 2 segundos
- Apagar desde el menú de escritorio del Raspberry Pi
- Ejecutar ``sudo shutdown now``
- Apagado automático cuando el nivel de batería cae por debajo del porcentaje de apagado configurado

.. end_power_off_after_shutdown

Configurar el Porcentaje de Apagado
++++++++++++++++++++++++++++++++++++++

Puede configurar el porcentaje de batería que activa el apagado automático.

Ejemplo:

.. code-block:: shell

   pipower5 -sp 30

Esto establece el umbral de apagado al 30%.

Luego use el siguiente comando para que los cambios de configuración surtan efecto.

.. code-block:: shell

   sudo systemctl restart pipower5.service

Cuando el nivel de batería cae por debajo del 30%, PiPower 5 notificará al Raspberry Pi para que se apague y desconectará la alimentación automáticamente.


También puede leer el porcentaje de apagado actual:

.. code-block:: shell

   pipower5 -sp

.. tip::

   Para sistemas Raspberry Pi 5 con alto consumo de energía (>3A), se recomienda establecer el porcentaje de apagado al ``100%``.

   Esto asegura que el Raspberry Pi se apague inmediatamente cuando se desconecta la alimentación externa, ayudando a proteger el sistema y los dispositivos de almacenamiento.


Monitoreo de Alimentación
----------------------------------------------------

PiPower 5 proporciona monitoreo en tiempo real de:

- Porcentaje de batería
- Estado de carga
- Voltaje de entrada
- Voltaje de salida
- Corriente de entrada
- Corriente de salida
- Voltaje de batería
- Corriente de batería

Comandos útiles:

Mostrar porcentaje de batería:

.. code-block:: shell

   pipower5 -bp

Mostrar estado de carga:

.. code-block:: shell

   pipower5 -ichg

Mostrar voltaje de entrada:

.. code-block:: shell

   pipower5 -iv

Mostrar toda la información de estado:

.. code-block:: shell

   pipower5 -a

Para la lista completa de comandos:

.. code-block:: shell

   pipower5 --help


Notificaciones
----------------------------------------------------

PiPower5 soporta notificaciones basadas en eventos a través de:

- Alertas de zumbador
- Notificaciones por correo electrónico

Los eventos soportados incluyen:

- ``battery_activated``
- ``low_battery``
- ``power_disconnected``
- ``power_restored``
- ``power_insufficient``
- ``battery_critical_shutdown``
- ``battery_voltage_critical_shutdown``

.. note::

   Cada vez que modifique el estado de ``pipower5.service``, necesita usar el siguiente comando para que los cambios de configuración surtan efecto.

   .. code-block:: shell

      sudo systemctl restart pipower5.service

Descripciones de Eventos
+++++++++++++++++++++++++++++++++++++++++++++++++

1. ``battery_activated``

   Se activa cuando la batería comienza a suministrar alimentación. Esto ocurre típicamente si la fuente de alimentación externa está desconectada o no puede proporcionar suficiente potencia.

   * **Condición de Restablecimiento**: Se restablece automáticamente después de que la alimentación externa se desconecta.

2. ``low_battery``

   Se activa cuando el nivel de carga de la batería cae por debajo del **umbral de apagado configurado**.

   * **Repetición**: Si la batería permanece por debajo de este umbral, el evento se activa cada 10 minutos.
   * **Condición de Restablecimiento**: Se restablece una vez que la carga de la batería sube por encima del **umbral de apagado + 5%**.

3. ``power_disconnected``

   Se activa cuando la fuente de alimentación externa se desconecta.

   * **Condición de Restablecimiento**: Se restablece una vez que la alimentación externa se restaura.

4. ``power_restored``

   Se activa cuando la fuente de alimentación externa se restaura.

   * **Condición de Restablecimiento**: Se restablece si la alimentación externa se desconecta de nuevo.

5. ``power_insufficient``

   Ocurre cuando la alimentación externa es insuficiente, requiriendo que la batería proporcione energía suplementaria.

   * **Acción Recomendada**: Verifique la potencia nominal de la fuente de alimentación, o compruebe la configuración de potencia de carga.
   * **Condición de Restablecimiento**: Se restablece cuando la fuente de alimentación externa se desconecta.

6. ``battery_critical_shutdown``

   Se activa justo antes de que el sistema se apague debido a una **capacidad de batería críticamente baja**.

7. ``battery_voltage_critical_shutdown``

   Se activa cuando el **voltaje de la batería** cae por debajo del umbral crítico, llevando al apagado.

   * **Nota**: Este evento rara vez se activa en uso normal. Típicamente, el evento ``low_battery`` iniciará una secuencia de apagado antes de que el voltaje caiga tanto. Esto sirve como un **mecanismo de apagado de seguridad**.

Con estos eventos, PiPower5 proporciona tanto advertencias proactivas (ej., batería baja, potencia insuficiente) como salvaguardas críticas (ej., activadores de apagado), asegurando un funcionamiento estable y protección de datos.



Alertas de Zumbador
+++++++++++++++++++++++++++++++++++++++++++++++++

PiPower5 soporta notificaciones de zumbador para diferentes eventos del sistema.

Puede configurar las alertas de zumbador a través del **Panel de Control Web** o la **herramienta de línea de comandos**.
Cuando ocurre un evento configurado, PiPower5 reproducirá el sonido de zumbador correspondiente.

Las características incluyen:

- Notificaciones de zumbador basadas en eventos
- Volumen de zumbador ajustable (1–10)
- Vista previa de sonido de eventos
- Soporte para efectos de sonido personalizados

Los usuarios avanzados también pueden crear efectos de sonido de zumbador personalizados.

1. Abra el archivo de configuración:

   .. code-block:: shell

      /opt/pipower5/venv/lib/python3.11/site-packages/pipower5/config.json

2. Localice la sección ``pipower5_buzz_sequence``.

3. Cada efecto de sonido se define usando el siguiente formato:

   .. code-block:: text

      [action, duration]

   Donde:

   - ``action`` puede ser:

     - Una nota musical, como ``"A4"``, ``"D3"`` o ``"C#4"``
     - Un valor de frecuencia (entero)
     - ``"pause"`` para silencio

   - ``duration`` es el tiempo de reproducción en milisegundos (ms)


Alertas de Correo Electrónico
+++++++++++++++++++++++++++++++++++++++++++++++++

PiPower5 soporta notificaciones por correo electrónico para eventos importantes del sistema, como:

- Batería baja
- Alimentación desconectada
- Alimentación restaurada
- Eventos de apagado crítico

Las notificaciones por correo electrónico se pueden configurar a través del **Panel de Control Web** o la **herramienta de línea de comandos**.

Para usar alertas de correo electrónico, se requiere un servidor SMTP. La mayoría de los proveedores de correo electrónico soportan servicios SMTP.

- Para Gmail, simplemente cree una **Contraseña de Aplicación**
- Para otros proveedores, habilite el acceso SMTP y genere una contraseña SMTP dedicada si es necesario

Antes de la configuración, prepare la siguiente información:

- Dirección del servidor SMTP
  (Ejemplo: ``smtp.gmail.com``)

- Puerto SMTP
  (Ejemplo: ``465`` o ``25``)

- Tipo de cifrado
  (``None`` / ``SSL`` / ``TLS``)

- Cuenta SMTP
  (Generalmente su dirección de correo electrónico)

- Contraseña SMTP
  (Contraseña de Aplicación o contraseña SMTP)

Después de ingresar la información SMTP, configure la dirección de correo electrónico del destinatario.

.. note::

   PiPower5 usa el servidor SMTP para iniciar sesión en su cuenta de correo electrónico y enviar notificaciones.

   Puede usar la misma dirección de correo electrónico como remitente y destinatario.

Después de la configuración, use el comando de prueba para verificar la conexión SMTP y la entrega de correo electrónico.
