.. _pipower_software_python:

Python
------------------------------------------------------

Sie können auch mit Python mit PiPower interagieren.

.. code-block:: shell

   source /opt/pipower5/venv/bin/activate

Wir stellen mehrere Python-Beispiele zur Verfügung, die verschiedene Anwendungsfälle demonstrieren. Navigieren Sie zum Beispielverzeichnis, um sie zu erkunden:

.. code-block:: shell

   cd ~/pipower5/examples

Hier sind die verfügbaren Skripte und ihre Funktionen:

- ``read_all.py``: Liest alle PiPower 5-Statusinformationen auf einmal und verarbeitet jedes Element einzeln.
- ``read_individual.py``: Demonstriert, wie bestimmte PiPower 5-Datenelemente einzeln gelesen werden können.
- ``set_shutdown_percentage.py``: Konfiguriert den Abschalt-Prozentsatz. Wenn der Akkustand unter den konfigurierten Schwellenwert fällt, sendet PiPower 5 eine Shutdown-Anforderung an den Host und trennt die Stromversorgung nach Abschluss des Herunterfahrens.
- ``read_power_btn.py``: Liest den aktuellen Zustand der PiPower 5-Power-Taste.
