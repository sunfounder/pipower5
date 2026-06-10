.. _pipower_software_python:

Python
------------------------------------------------------

È anche possibile interagire con PiPower utilizzando Python.

.. code-block:: shell

   source /opt/pipower5/venv/bin/activate

Forniamo diversi esempi Python per dimostrare diversi casi d'uso. Accedere alla directory degli esempi per esplorarli:

.. code-block:: shell

   cd ~/pipower5/examples

Ecco gli script disponibili e le loro funzioni:

- ``read_all.py`` : Legge tutte le informazioni di stato del PiPower 5 in una sola volta ed elabora ogni elemento individualmente.
- ``read_individual.py`` : Mostra come leggere singolarmente dati specifici del PiPower 5.
- ``set_shutdown_percentage.py`` : Configura la percentuale di spegnimento. Quando il livello della batteria scende al di sotto della soglia configurata, PiPower 5 invia una richiesta di spegnimento all'host e interrompe l'alimentazione dopo il completamento dello spegnimento.
- ``read_power_btn.py`` : Legge lo stato corrente del pulsante di accensione del PiPower 5.
