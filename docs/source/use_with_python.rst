.. _pipower_software_python:

Python
------------------------------------------------------

You can also interact with PiPower using Python.

.. code-block:: shell

   source /opt/pipower5/venv/bin/activate

We provide several Python examples to demonstrate different use cases. Navigate to the examples directory to explore them:

.. code-block:: shell

   cd ~/pipower5/examples

Here are the available scripts and their functions:

- ``read_all.py``: Reads all PiPower 5 status information at once and processes each item individually.
- ``read_individual.py``: Demonstrates how to read specific PiPower 5 data items individually.
- ``set_shutdown_percentage.py``: Configures the shutdown percentage. When the battery level falls below the configured threshold, PiPower 5 sends a shutdown request to the host and cuts power after shutdown completes.
- ``read_power_btn.py``: Reads the current state of the PiPower 5 power button.