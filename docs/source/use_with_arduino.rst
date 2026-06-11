Arduino
===================================

Si está usando el PiPower 5 para alimentar su placa Arduino, puede conectar el Arduino al puerto de salida Tipo A del PiPower 5 o usar dos cables jumper. Conecte la interfaz I2C de la placa usando un jumper.

.. Si no se requiere ninguna operación antes de apagar, conecte directamente el jumper **SDSIG** a GND. Si son necesarias operaciones antes del apagado, retire el jumper y conecte el cable intermedio a un puerto IO en el Arduino para notificar a PiPower 5 que puede apagarse de forma segura.

Proporcionamos una biblioteca que le permite monitorear voltajes de entrada y salida, voltaje y porcentaje de batería, fuente de alimentación, estado de carga y otros datos internos.

#. En el IDE de Arduino, abra el **Gestor de Bibliotecas**, busque ``SunFounderPowerControl``, descárguelo e instálelo.

   .. image:: img/install_arduino_lib.png
      :width: 100%

#. Después de la instalación, puede navegar a **Archivo** -> **Ejemplos** -> **SunFounderPowerControl** -> **PiPower 5**, donde encontrará cuatro ejemplos.

   .. image:: img/arduino_lib_example.png
      :width: 100%

   * ``read_all``: Use este ejemplo si necesita leer todos los datos a la vez y procesarlos individualmente.
   * ``read_individual``: Si solo necesita leer ciertos datos, este ejemplo proporciona instrucciones de lectura de datos individuales.
   * ``set_shutdown_percentage``: Este ejemplo enseña cómo establecer un porcentaje de batería para apagado. Esta función envía una señal de apagado al host cuando la batería no se está cargando y cae por debajo del porcentaje establecido. Después de que el host se apaga, solo se apagará después de recibir una señal de corte de alimentación. Normalmente se usa con SBCs como Raspberry Pi. Para microcontroladores, retire el jumper **SDSIG** y conecte el cable intermedio a un pin. Después de apagarse de forma segura al recibir la señal de apagado, ponga este pin en alto para apagar PiPower 5.
   * ``shutdown_when_request``: Este ejemplo muestra cómo manejar operaciones después de recibir una señal de apagado. Retire el jumper **SDSIG** y conecte el cable intermedio a un pin.

#. Elija uno de los ejemplos y cárguelo en su placa.

   .. note::

      En algunas placas donde I2C se puede modificar, si necesita cambiar los pines I2C, necesita modificar el código ``Wire.begin()``.

Documentación de la API de la Biblioteca Arduino: https://github.com/sunfounder/arduino_spc?tab=readme-ov-file#api

