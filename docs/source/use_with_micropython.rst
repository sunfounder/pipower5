MicroPython
==========================================================

Proporcionamos una biblioteca que le permite monitorear voltajes de entrada y salida, voltaje y porcentaje de batería, fuente de alimentación, estado de carga y otros datos internos.

Si está usando el PiPower 5 para alimentar su placa Raspberry Pi Pico o ESP32, puede conectar la placa al PiPower 5 a través del puerto de salida Tipo-A o dos cables jumper.

Para conectar la interfaz I2C del PiPower 5, use un jumper.

.. Si no se necesitan operaciones antes de apagar, conecte el jumper SDSIG directamente al pin GND. Si se requieren operaciones antes del apagado, retire el jumper y conecte el cable intermedio a un pin I/O en la placa Raspberry Pi Pico o ESP32. Esta configuración notifica al PiPower 5 que el proceso de apagado está completo y puede apagarse de forma segura.

#. Descargue la biblioteca desde GitHub. Puede descargarla rápidamente usando el enlace de abajo o visite: https://github.com/sunfounder/micropython_spc.

   * :download:`micropython_spc <https://github.com/sunfounder/micropython_spc/archive/refs/heads/main.zip>`

#. Después de descargar y descomprimir, suba la carpeta ``spc`` a su placa Raspberry Pi Pico o ESP32. Se recomienda Thonny para este propósito.

   .. image:: img/micropython_upload.png
       :width: 100%
       :align: center

   .. raw:: html

      <br/>

#. Una vez que la biblioteca esté cargada, puede probarla usando los ejemplos proporcionados en la carpeta ``micropython_spc-main/examples/pipower5``:

   * ``pipower_5_read_all.py``: Use este ejemplo si necesita leer todos los datos. Demuestra cómo leer todos los datos disponibles a la vez y procesarlos individualmente.

   * ``pipower_5_read_individual.py``: Este ejemplo proporciona instrucciones para leer datos específicos individualmente. Úselo si solo necesita acceder a ciertos datos.

   * ``pipower_5_set_shutdown_percentage.py``: Este ejemplo explica cómo establecer el porcentaje de batería para apagado. Cuando la batería no se está cargando y su nivel cae por debajo del porcentaje especificado, el PiPower 5 envía una señal de apagado al host. Se apaga solo después de que el host haya completado el apagado y enviado una señal de corte de alimentación.

     * Para SBCs (ej., Raspberry Pi): No se requiere configuración adicional.
     * Para microcontroladores: Retire el jumper **SDSIG** y conecte el cable intermedio a un pin. Después de recibir la señal de apagado y apagarse de forma segura, ponga este pin en alto para notificar al PiPower 5 que se apague.

   * ``pipower_5_shutdown_when_request.py``: Este ejemplo demuestra cómo manejar operaciones después de recibir una señal de apagado. Necesita retirar el jumper **SDSIG** y conectar el cable intermedio a un pin.

Documentación de la API de la Biblioteca Micropython: https://github.com/sunfounder/micropython_spc?tab=readme-ov-file#api
