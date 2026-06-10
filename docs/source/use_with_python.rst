.. _pipower_software_python:

Python
------------------------------------------------------

Vous pouvez également interagir avec le PiPower en utilisant Python.

.. code-block:: shell

   source /opt/pipower5/venv/bin/activate

Nous fournissons plusieurs exemples Python pour démontrer différents cas d'utilisation. Accédez au répertoire d'exemples pour les explorer :

.. code-block:: shell

   cd ~/pipower5/examples

Voici les scripts disponibles et leurs fonctions :

- ``read_all.py`` : Lit toutes les informations d'état du PiPower 5 en une seule fois et traite chaque élément individuellement.
- ``read_individual.py`` : Montre comment lire des données spécifiques du PiPower 5 individuellement.
- ``set_shutdown_percentage.py`` : Configure le pourcentage d'arrêt. Lorsque le niveau de la batterie descend en dessous du seuil configuré, le PiPower 5 envoie une demande d'arrêt à l'hôte et coupe l'alimentation une fois l'arrêt terminé.
- ``read_power_btn.py`` : Lit l'état actuel du bouton d'alimentation du PiPower 5.
