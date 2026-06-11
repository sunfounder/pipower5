.. _pipower_software_python:

Python
------------------------------------------------------

También puede interactuar con PiPower usando Python.

.. code-block:: shell

   source /opt/pipower5/venv/bin/activate

Proporcionamos varios ejemplos de Python para demostrar diferentes casos de uso. Navegue al directorio de ejemplos para explorarlos:

.. code-block:: shell

   cd ~/pipower5/examples

Aquí están los scripts disponibles y sus funciones:

- ``read_all.py``: Lee toda la información de estado de PiPower 5 de una vez y procesa cada elemento individualmente.
- ``read_individual.py``: Demuestra cómo leer elementos de datos específicos de PiPower 5 individualmente.
- ``set_shutdown_percentage.py``: Configura el porcentaje de apagado. Cuando el nivel de batería cae por debajo del umbral configurado, PiPower 5 envía una solicitud de apagado al host y corta la alimentación después de completar el apagado.
- ``read_power_btn.py``: Lee el estado actual del botón de encendido de PiPower 5.
