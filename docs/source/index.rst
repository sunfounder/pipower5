.. note::

    ¡Hola, bienvenido a la Comunidad de Entusiastas de Raspberry Pi & Arduino & ESP32 de SunFounder en Facebook! Profundice en Raspberry Pi, Arduino y ESP32 con otros entusiastas.

    **¿Por qué unirse?**

    - **Soporte Experto**: Resuelva problemas posventa y desafíos técnicos con la ayuda de nuestra comunidad y equipo.
    - **Aprenda y Comparta**: Intercambie consejos y tutoriales para mejorar sus habilidades.
    - **Avances Exclusivos**: Obtenga acceso anticipado a anuncios de nuevos productos y adelantos.
    - **Descuentos Especiales**: Disfrute de descuentos exclusivos en nuestros productos más nuevos.
    - **Promociones Festivas y Sorteos**: Participe en sorteos y promociones navideñas.

    👉 ¿Listo para explorar y crear con nosotros? ¡Haga clic [|link_sf_facebook|] y únase hoy!

SunFounder PiPower5 - Proteja Su Dispositivo y Sus Datos
================================================================================

.. * |link_PiPower_5_buy|

.. Gracias por elegir nuestro |link_PiPower_5|.

Gracias por elegir nuestro PiPower5.


.. .. note::
..     Este documento está disponible en los siguientes idiomas.

..         * |link_german_tutorials|
..         * |link_jp_tutorials|
..         * |link_en_tutorials|

..     Haga clic en los enlaces respectivos para acceder al documento en su idioma preferido.

.. todo: new pic

.. image:: img/PP.0.A.JPG
    :width: 400
    :align: center

PiPower 5 es una solución UPS versátil diseñada para una integración perfecta con dispositivos Raspberry Pi. Cuenta con una robusta gestión de rutas de alimentación, capacidades de carga y descarga de baterías de litio duales, y protecciones esenciales contra polaridad inversa, sobrecarga y sobredescarga.

Con una salida de hasta 5V/5A, PiPower 5 garantiza un rendimiento estable para una amplia gama de dispositivos. Su configuración HAT+ garantiza compatibilidad con Raspberry Pi 5, mientras que las salidas adicionales, incluyendo un puerto USB-A y un conector 4x2P, proporcionan soporte para varios ordenadores de placa única (SBCs) y plataformas de microcontroladores, como Arduino, Pico y ESP32.

Un microcontrolador integrado gestiona eficientemente las operaciones de alimentación y permite el monitoreo en tiempo real de parámetros clave a través de comunicación I2C. Estos parámetros incluyen voltaje de entrada, voltaje de salida, voltaje de batería, capacidad de batería, estado de conexión de alimentación externa, estado de carga y la fuente de alimentación actual (batería o USB).

Combinando una gestión avanzada de batería con amplia compatibilidad, PiPower 5 es una herramienta esencial para entusiastas de la tecnología y profesionales que buscan optimizar sus configuraciones de hardware.

**Características**

* **Entrada**: 5-15V, 45W, USB Type-C PD, DC5.5-2.1
* **Salida**: 5V/5A a través de GPIO de Raspberry Pi, USB Type-A y pines de 2x4P 2.54mm
* **Potencia de Carga**: Hasta 20W
* **Especificaciones de Batería**: 7.4V 2 Celdas 18650 Ion de litio, conector XH2.54 3P
* **Ajustes Configurables mediante Jumpers**:

  * Jumper de Encendido Predeterminado: Configure si el dispositivo se enciende automáticamente al conectar la alimentación.
  * Jumper de Señal de Apagado: Habilite la detección del estado de apagado del dispositivo.
  * Conector de Botón de Encendido Externo: Conecte un botón de encendido externo para control manual de alimentación.

* **Indicadores y Botones Integrados**:

  * Indicador de estado de batería
  * Indicador de fuente de entrada
  * Botón de encendido
  * Indicador de conexión inversa de batería
  * Indicador de alimentación de salida

* **Microcontrolador Integrado**: ARM Cortex-M23 de 32 bits, compatible con comunicación I2C

* **Interfaces de comunicación I2C**:

  * GPIO de Raspberry Pi
  * SH1.0 4P (compatible con Qwiic y STEMMA QT)
  * Conector de pines 1x4P 2.54mm


.. **Tabla de Contenidos**

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Primeros Pasos

   Acerca de PiPower 5 <self>
   assembly
   quick_guide

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Descripción General del Hardware

   pipower_hat
   battery

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Configuración de Software

   pipower5_software
   update_firmware
   use_with_python


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Apéndice

   compatible_sbc
   troubleshooting
   faq


**Aviso de Derechos de Autor**

Todos los contenidos, incluidos pero no limitados a textos, imágenes y código en este manual, son propiedad de SunFounder Company. Solo debe usarlos para estudio personal, investigación, disfrute u otros fines no comerciales o sin ánimo de lucro, bajo las regulaciones y leyes de derechos de autor correspondientes, sin infringir los derechos legales del autor y los titulares de derechos pertinentes. Para cualquier individuo u organización que utilice estos contenidos con fines comerciales sin permiso, la Compañía se reserva el derecho de emprender acciones legales.

