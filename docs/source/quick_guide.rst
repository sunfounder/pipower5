Guide de démarrage rapide
===============================

Ce guide vous aide à démarrer rapidement avec le PiPower 5 après l'assemblage matériel.

Charger la batterie
----------------------------------------------------

Avant la première utilisation, chargez complètement la batterie.

Recommandations :

- Utilisez un adaptateur secteur USB-C de haute qualité
- Une alimentation 5V 5A est recommandée pour le Raspberry Pi 5
- Des adaptateurs de puissance supérieure sont recommandés lors de l'utilisation de SSD ou d'autres périphériques haute puissance

Pendant la charge :

- Utilisez une alimentation USB-C de haute qualité pour charger le PiPower 5.

  .. image:: img/power_input.png
     :width: 50%
     :align: center

- Pendant la charge, les LED indicatrices de batterie s'allument progressivement en séquence.

  .. image:: img/battery_indicator.png
     :width: 50%
     :align: center

  L'état de la batterie est indiqué par le nombre de LED allumées :

  * **4 LED allumées** : Batterie > 80%
  * **3 LED allumées** : 60% < Batterie < 80%
  * **2 LED allumées** : 40% < Batterie < 60%
  * **1 LED allumée** : 20% < Batterie < 40%
  * **Première LED clignotante** : Batterie < 20%
  * **Les LED s'allument progressivement en cycle** : Charge en cours
  * **Deux LED centrales clignotantes** : En attente du signal d'arrêt
  * **Toutes les LED éteintes** : Hors tension ou en mode veille
  * Pendant la charge, l'indicateur reste allumé **même à l'état éteint** jusqu'à ce que la charge soit complète.

Mise sous tension
----------------------------------------------------

Pour les appareils Raspberry Pi, aucun câblage d'alimentation supplémentaire n'est requis. Le PiPower 5 fournit l'alimentation directement via le connecteur GPIO.

Pour les autres appareils, vous pouvez les alimenter en utilisant :

- Le port de sortie USB-A
- Les broches 5V/GND à côté du port USB-A

.. image:: img/power_output.png
   :width: 50%
   :align: center

Appuyez une fois sur le bouton d'alimentation pour allumer le PiPower 5. Lorsqu'il est sous tension :

- La **LED PWR** s'allume
- L'appareil connecté commence à recevoir l'alimentation du PiPower 5

.. image:: img/pwr_led.png
   :width: 50%
   :align: center

.. include:: /pipower5_software.rst
    :start-after: start_install_pipower5
    :end-before: end_install_pipower5

Ouvrir le tableau de bord Web
----------------------------------------------------

Après l'installation, ouvrez le tableau de bord dans votre navigateur :

.. code-block:: text

   http://<adresse-ip-raspberry-pi>:34001

Le tableau de bord vous permet de :

- Voir le pourcentage de la batterie
- Surveiller l'état de charge
- Vérifier la tension et le courant
- Configurer le pourcentage d'arrêt
- Gérer les notifications

.. image:: img/web_dashboard.png
   :width: 100%
   :align: center


Arrêt sécurisé
----------------------------------------------------

.. include:: /pipower5_software.rst
    :start-after: start_power_off_after_shutdown
    :end-before: end_power_off_after_shutdown

.. note::

   Pour les fonctionnalités avancées et les options de configuration détaillées, y compris :

   - Commandes de surveillance de l'alimentation
   - Paramètres de notification
   - Alertes par buzzer
   - Alertes par email
   - Configuration avancée

   Veuillez vous référer à :

   * :ref:`pipower5_tool`
