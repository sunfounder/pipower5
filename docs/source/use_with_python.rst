.. _pipower_software_python:

Python
------------------------------------------------------

You can also interact with PiPower using Python.

PiPower5 utilizes the |link_spc_lib| (SunFounder Power Control Core) library to fetch data and configure parameters. The SPC library is pre-installed in the virtual environment when you set up PiPower5. To activate the virtual environment, use the following command:

.. code-block:: shell

   source /opt/pipower5/venv/bin/activate

We provide several Python examples to demonstrate different use cases. Navigate to the examples directory to explore them:

.. code-block:: shell

   cd ~/pipower5/examples

Here are the available scripts and their functions:

- ``read_all.py``: Reads all data at once and processes each item individually.
- ``read_individual.py``: Reads specific data items, showcasing examples of fetching individual data points.
- ``set_shutdown_percentage.py``: Configures the shutdown percentage. When the battery level falls below the set threshold, PiPower 5 sends a shutdown signal to the host. Once the shutdown process is complete, it cuts power.
- ``shutdown_when_request.py``: Demonstrates how to handle shutdown signals. For microcontroller use, remove the SDSIG jumper cap and connect the middle pin to a GPIO pin. After receiving a shutdown signal and completing a safe shutdown, pull the GPIO pin high to allow PiPower 5 to cut power.

Python Library API Documentation: https://github.com/sunfounder/spc?tab=readme-ov-file#api

