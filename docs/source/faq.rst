.. note::

    ¡Hola, bienvenido a la Comunidad de Entusiastas de Raspberry Pi & Arduino & ESP32 de SunFounder en Facebook! Profundice en Raspberry Pi, Arduino y ESP32 con otros entusiastas.

    **¿Por qué unirse?**

    - **Soporte Experto**: Resuelva problemas posventa y desafíos técnicos con la ayuda de nuestra comunidad y equipo.
    - **Aprenda y Comparta**: Intercambie consejos y tutoriales para mejorar sus habilidades.
    - **Avances Exclusivos**: Obtenga acceso anticipado a anuncios de nuevos productos y adelantos.
    - **Descuentos Especiales**: Disfrute de descuentos exclusivos en nuestros productos más nuevos.
    - **Promociones Festivas y Sorteos**: Participe en sorteos y promociones navideñas.

    👉 ¿Listo para explorar y crear con nosotros? ¡Haga clic [|link_sf_facebook|] y únase hoy!

.. _faq:

Preguntas Frecuentes
===

Cómo Reinstalar PiPower 5
--------------------------

Si PiPower 5 no funciona correctamente y desea realizar una reinstalación limpia, siga estos pasos:

**1. Desinstalar la instalación actual:**

.. code-block:: shell

   cd ~/pipower5
   sudo python3 install.py --uninstall

**2. Reinstalar desde la fuente:**

.. code-block:: shell

   git clone https://github.com/sunfounder/pipower5
   cd pipower5
   sudo python3 install.py

**3. Reinicie la Raspberry Pi cuando se le solicite.**

Después de reiniciar, verifique la instalación:

.. code-block:: shell

   pipower5 -a
   sudo systemctl status pipower5.service

.. tip::

   Si el directorio ``~/pipower5`` ya no existe de la instalación original, omita el paso de desinstalación y vaya directamente al paso de reinstalación.


El Panel Muestra "Base de Datos Requerida" o No Hay Datos
---------------------------------------------------------

**Lo que ve**: El Panel de Control Web se abre normalmente en su navegador, pero todos los paneles de datos están vacíos o muestran "base de datos requerida".

**Lo que esto significa generalmente**: Rara vez es un problema de hardware. En la mayoría de los casos, el backend InfluxDB tiene un problema de configuración — una base de datos corrupta, un bucket faltante o un token expirado.

**Compruebe esto, en orden:**

1. **Compruebe que el servicio PiPower 5 esté en ejecución:**

   .. code-block:: shell

      sudo systemctl status pipower5

   Si el servicio no está activo, inícielo:

   .. code-block:: shell

      sudo systemctl start pipower5

2. **Compruebe si el bucket de InfluxDB existe:**

   .. code-block:: shell

      sudo influx bucket list

   Busque un bucket llamado ``pipower5`` en la salida. Si falta, la base de datos necesita ser recreada.

3. **Compruebe los registros del servicio en busca de errores:**

   .. code-block:: shell

      journalctl -u pipower5 -n 50

   Busque mensajes de error relacionados con InfluxDB, como:

   - ``unauthorized`` o ``token`` — indica un problema de token de autenticación.
   - ``bucket not found`` — el bucket de la base de datos no existe.
   - ``connection refused`` — InfluxDB no está en ejecución.

4. **Si InfluxDB mismo está caído**, reinícielo:

   .. code-block:: shell

      sudo systemctl restart influxdb
      sudo systemctl restart pipower5

.. note::

   Si InfluxDB se instaló manualmente o se migró desde una versión anterior, las rutas de configuración o los tokens de autenticación pueden haber cambiado. En ese caso, una reinstalación limpia de PiPower 5 (ver arriba) también reinicializará la configuración de InfluxDB.
