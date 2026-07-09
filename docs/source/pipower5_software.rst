.. _pipower5_tool:

Outil PiPower 5
===============================

L'outil PiPower 5 est le logiciel compagnon du PiPower 5.

Il fournit :

- Prise en charge de l'arrêt sécurisé
- Gestion de la batterie et de la charge
- Surveillance de l'alimentation
- Accès au tableau de bord Web
- Notifications d'événements

Le PiPower 5 peut envoyer des demandes d'arrêt au Raspberry Pi dans les situations suivantes :

- Le bouton PiPower est maintenu enfoncé pendant 2 secondes
- Le niveau de la batterie descend en dessous du pourcentage d'arrêt configuré

Une fois l'arrêt du Raspberry Pi terminé, le PiPower 5 peut automatiquement couper l'alimentation pour aider à prévenir la corruption de la carte SD et les problèmes de perte d'alimentation inattendue.

.. start_install_pipower5

.. important::

   PiPower 5 requires a **64-bit** operating system. The ``pipower5`` service
   does not support 32-bit Raspberry Pi OS.

   To check your system architecture, run:

   .. code-block:: shell

      uname -m

   - ``aarch64`` → 64-bit (supported)
   - ``armv7l`` → 32-bit (not supported)

   If you are running a 32-bit OS, please reinstall with the 64-bit version of
   Raspberry Pi OS before proceeding.

Installer l'outil ``pipower5``
----------------------------------------------------

Installez l'outil PiPower 5 :

1. Cloner le dépôt :

   .. code-block:: shell

      git clone https://github.com/sunfounder/pipower5

2. Entrer dans le répertoire :

   .. code-block:: shell

      cd pipower5

3. Exécuter l'installateur :

   .. code-block:: shell

      sudo python3 install.py

4. Redémarrer le Raspberry Pi lorsqu'il vous est demandé.

.. end_install_pipower5

Référence des commandes
---------------------------------------

L'outil ``pipower5`` donne accès aux informations d'état et aux options de configuration du PiPower 5.

Par exemple, la commande suivante affiche l'état actuel du PiPower 5 :

.. code-block:: shell

   pipower5 -a

Exemple de sortie :

.. code-block::

   Input:
      voltage: 0 mV
      current: 0 mA
      power: 0.000 W
      plugged in: False
   Output:
      voltage: 5296 mV
      current: 452 mA
      power: 2.394 W
   Battery:
      voltage: 8028 mV
      current: -315 mA
      power: -2.529 W
      percentage: 91 %
      source: 1 - Battery
      charging: False

   Internal:
      shutdown request: 0 - NONE
      power button: 0 - RELEASED
      max charging current: 0 mA
      default on: on
      shutdown percentage: 10 %

Vous pouvez personnaliser ces paramètres selon vos besoins.

Utilisez ``pipower5`` ou ``pipower5 -h`` pour les instructions.

.. code-block:: text


  usage: pipower5 [-h] [-v] [-c] [-drd [DATABASE_RETENTION_DAYS]]
                  [-dl [{debug,info,warning,error,critical}]] [-rd]
                  [-cp [CONFIG_PATH]] [-sp [SHUTDOWN_PERCENTAGE]] [-iv] [-ic]
                  [-ov] [-oc] [-bv] [-bc] [-bp] [-bs] [-ii] [-ichg] [-do] [-sr]
                  [-pb] [-cc] [-a] [-fv] [-pfs [POWER_FAILURE_SIMULATION]]
                  [-seo [SEND_EMAIL_ON]] [-set [SEND_EMAIL_TO]]
                  [-ss [SMTP_SERVER]] [-smp [SMTP_PORT]] [-se [SMTP_EMAIL]]
                  [-spw [SMTP_PASSWORD]] [-ssc [SMTP_SECURITY]] [-bzo [BUZZ_ON]]
                  [-bzv [BUZZER_VOLUME]] [-bzt [BUZZER_TEST]] [-u [{C,F}]]
                  [{start,stop}]

  PiPower 5

  positional arguments:
    {start,stop}          Command

  options:
    -h, --help            show this help message and exit
    -v, --version         Show version
    -c, --config          Show config
    -drd [DATABASE_RETENTION_DAYS], --database-retention-days [DATABASE_RETENTION_DAYS]
                          Database retention days
    -dl [{debug,info,warning,error,critical}], --debug-level [{debug,info,warning,error,critical}]
                          Debug level
    -rd, --remove-dashboard
                          Remove dashboard
    -cp [CONFIG_PATH], --config-path [CONFIG_PATH]
                          Config path
    -sp [SHUTDOWN_PERCENTAGE], --shutdown-percentage [SHUTDOWN_PERCENTAGE]
                          Set shutdown percentage, leave empty to read
    -iv, --input-voltage  Read input voltage
    -ic, --input-current  Read input current
    -ov, --output-voltage
                          Read output voltage
    -oc, --output-current
                          Read output current
    -bv, --battery-voltage
                          Read battery voltage
    -bc, --battery-current
                          Read battery current
    -bp, --battery-percentage
                          Read battery percentage
    -bs, --battery-source
                          Read battery source
    -ii, --is-input-plugged_in
                          Read is input plugged in
    -ichg, --is-charging  Read is charging
    -do, --default-on     Read default on
    -sr, --shutdown-request
                          Read shutdown request
    -pb, --power-btn      Read power button
    -cc, --charging-current
                          Max charging current
    -a, --all             Show all status
    -fv, --firmware       PiPower5 firmware version
    -pfs [POWER_FAILURE_SIMULATION], --power-failure-simulation [POWER_FAILURE_SIMULATION]
                          Power failure simulation
    -seo [SEND_EMAIL_ON], --send-email-on [SEND_EMAIL_ON]
                          Send email on: ['battery_activated', 'low_battery',
                          'power_disconnected', 'power_restored',
                          'power_insufficient', 'battery_critical_shutdown',
                          'battery_voltage_critical_shutdown']
    -set [SEND_EMAIL_TO], --send-email-to [SEND_EMAIL_TO]
                          Email address to send email to
    -ss [SMTP_SERVER], --smtp-server [SMTP_SERVER]
                          SMTP server
    -smp [SMTP_PORT], --smtp-port [SMTP_PORT]
                          SMTP port
    -se [SMTP_EMAIL], --smtp-email [SMTP_EMAIL]
                          SMTP email
    -spw [SMTP_PASSWORD], --smtp-password [SMTP_PASSWORD]
                          SMTP password
    -ssc [SMTP_SECURITY], --smtp-security [SMTP_SECURITY]
                          SMTP security, 'none', 'ssl' or 'tls'
    -bzo [BUZZ_ON], --buzz-on [BUZZ_ON]
                          Buzz on: ['battery_activated', 'low_battery',
                          'power_disconnected', 'power_restored',
                          'power_insufficient', 'battery_critical_shutdown',
                          'battery_voltage_critical_shutdown']
    -bzv [BUZZER_VOLUME], --buzzer-volume [BUZZER_VOLUME]
                          Buzz volume
    -bzt [BUZZER_TEST], --buzzer-test [BUZZER_TEST]
                          Test buzzer on selected event.
    -u [{C,F}], --temperature-unit [{C,F}]
                          Temperature unit

.. note::

   Chaque fois que vous modifiez l'état de ``pipower5.service``, vous devez utiliser la commande suivante pour que les modifications de configuration prennent effet.

   .. code-block:: shell

      sudo systemctl restart pipower5.service

   Vérifiez l'état du programme pipower5 à l'aide de l'outil systemctl.

   .. code-block:: shell

      sudo systemctl status pipower5.service

   Alternativement, inspectez les fichiers journaux générés par le programme.

   .. code-block:: shell

      cat /opt/pipower5/log

Tableau de bord Web
----------------------------------------------------

L'outil PiPower 5 inclut un tableau de bord Web intégré pour la surveillance et la configuration.

Accédez au tableau de bord depuis votre navigateur :

.. code-block:: text

   http://<adresse-ip-raspberry-pi>:34001

Les fonctionnalités du tableau de bord incluent :

- Surveillance du pourcentage de la batterie
- Surveillance de l'état de charge
- Surveillance de la tension d'entrée et de sortie
- Surveillance du courant
- Configuration du pourcentage d'arrêt
- Gestion des notifications
- Informations sur l'appareil Raspberry Pi

.. image:: img/web_dashboard.png
   :width: 100%
   :align: center

.. image:: img/web_dashboard_2.png
   :width: 100%
   :align: center

Vous pouvez également configurer le pourcentage d'arrêt directement depuis le tableau de bord :

.. image:: img/web_dashboard_3.png
   :width: 100%
   :align: center

Si vous n'avez pas besoin du tableau de bord, supprimez-le avec :

.. code-block:: shell

   pipower5 --remove-dashboard

Arrêt sécurisé
----------------------------------------------------

Le PiPower 5 prend en charge la protection par arrêt sécurisé automatique pour les systèmes Raspberry Pi.

Flux de travail d'arrêt :

.. code-block:: text

   Arrêt déclenché
   -> Le Raspberry Pi effectue un arrêt sécurisé
   -> Le PiPower 5 détecte la fin de l'arrêt
   -> Le PiPower 5 coupe automatiquement l'alimentation

Cela aide à prévenir :

- La corruption de la carte SD
- Les dommages au système de fichiers
- Les problèmes de perte d'alimentation inattendue


Coupure d'alimentation après l'arrêt du Raspberry Pi
++++++++++++++++++++++++++++++++++++++++++++++++++++

.. start_power_off_after_shutdown

Pour permettre au PiPower 5 de couper automatiquement l'alimentation après l'arrêt du Raspberry Pi, une configuration supplémentaire est requise.

1. Si vous utilisez un **Raspberry Pi 4 ou 5** :

   * Assurez-vous que le cavalier ``SDSIG`` du PiPower 5 est connecté à ``PI3V3``.

     .. image:: img/safe_shutdown_3v3.png
        :width: 400

   * Ouvrez la configuration du Raspberry Pi :

     .. code-block:: shell

        sudo raspi-config

   * Accédez à :

     .. code-block:: text

        6 Advanced Options
        -> A11 Shutdown Behaviour
        -> B1 Full power off Switch off Pi ...

   * Redémarrez le Raspberry Pi lorsqu'il vous est demandé.

2. Si vous utilisez un **Raspberry Pi 3** ou antérieur :

   * Réglez le cavalier ``SDSIG`` du PiPower 5 sur ``GPIO26``.

     .. image:: img/safe_shutdown_io26.png
        :width: 400

   * Ouvrez ``/boot/firmware/config.txt`` :

     .. code-block:: shell

        sudo nano /boot/firmware/config.txt

   * Ajoutez les lignes suivantes :

     .. code-block:: shell

        dtoverlay=gpio-poweroff,gpio_pin=26,active_low=1
        gpio=26=op,dh

   * Appuyez sur ``Ctrl+X``, puis ``Y``, et appuyez sur ``Entrée`` pour enregistrer le fichier et quitter.

   * Redémarrez le Raspberry Pi.

     .. code-block:: shell

        sudo reboot

Après la configuration, le PiPower 5 peut détecter automatiquement l'arrêt du Raspberry Pi et couper l'alimentation en toute sécurité.

Les méthodes d'arrêt sécurisé prises en charge incluent :

- Maintenir le bouton PiPower enfoncé pendant 2 secondes
- Arrêter depuis le menu du bureau Raspberry Pi
- Exécuter ``sudo shutdown now``
- Arrêt automatique lorsque le niveau de la batterie descend en dessous du pourcentage d'arrêt configuré

.. end_power_off_after_shutdown

Configurer le pourcentage d'arrêt
++++++++++++++++++++++++++++++++++++++

Vous pouvez configurer le pourcentage de batterie qui déclenche l'arrêt automatique.

Exemple :

.. code-block:: shell

   pipower5 -sp 30

Cela définit le seuil d'arrêt à 30%.

Utilisez ensuite la commande suivante pour que les modifications de configuration prennent effet.

.. code-block:: shell

   sudo systemctl restart pipower5.service

Lorsque le niveau de la batterie descend en dessous de 30%, le PiPower 5 demandera au Raspberry Pi de s'arrêter et coupera automatiquement l'alimentation.


Vous pouvez également lire le pourcentage d'arrêt actuel :

.. code-block:: shell

   pipower5 -sp

.. tip::

   Pour les systèmes Raspberry Pi 5 à forte consommation d'énergie (>3A), il est recommandé de définir le pourcentage d'arrêt à ``100%``.

   Cela garantit que le Raspberry Pi s'arrête immédiatement lorsque l'alimentation externe est déconnectée, aidant à protéger le système et les périphériques de stockage.


Surveillance de l'alimentation
----------------------------------------------------

Le PiPower 5 fournit une surveillance en temps réel pour :

- Pourcentage de la batterie
- État de charge
- Tension d'entrée
- Tension de sortie
- Courant d'entrée
- Courant de sortie
- Tension de la batterie
- Courant de la batterie

Commandes utiles :

Afficher le pourcentage de la batterie :

.. code-block:: shell

   pipower5 -bp

Afficher l'état de charge :

.. code-block:: shell

   pipower5 -ichg

Afficher la tension d'entrée :

.. code-block:: shell

   pipower5 -iv

Afficher toutes les informations d'état :

.. code-block:: shell

   pipower5 -a

Pour la liste complète des commandes :

.. code-block:: shell

   pipower5 --help


Notifications
----------------------------------------------------

Le PiPower5 prend en charge les notifications pilotées par événements via :

- Alertes par buzzer
- Notifications par email

Les événements pris en charge incluent :

- ``battery_activated``
- ``low_battery``
- ``power_disconnected``
- ``power_restored``
- ``power_insufficient``
- ``battery_critical_shutdown``
- ``battery_voltage_critical_shutdown``

.. note::

   Chaque fois que vous modifiez l'état de ``pipower5.service``, vous devez utiliser la commande suivante pour que les modifications de configuration prennent effet.

   .. code-block:: shell

      sudo systemctl restart pipower5.service

Descriptions des événements
+++++++++++++++++++++++++++++++++++++++++++++++++

1. ``battery_activated``

   Déclenché lorsque la batterie commence à fournir de l'énergie. Cela se produit généralement si la source d'alimentation externe est déconnectée ou incapable de fournir une puissance suffisante.

   * **Condition de réinitialisation** : Se réinitialise automatiquement après la déconnexion de l'alimentation externe.

2. ``low_battery``

   Activé lorsque le niveau de charge de la batterie descend en dessous du **seuil d'arrêt configuré**.

   * **Répétition** : Si la batterie reste en dessous de ce seuil, l'événement est déclenché toutes les 10 minutes.
   * **Condition de réinitialisation** : Se réinitialise lorsque la charge de la batterie remonte au-dessus du **seuil d'arrêt + 5%**.

3. ``power_disconnected``

   Déclenché lorsque la source d'alimentation externe est déconnectée.

   * **Condition de réinitialisation** : Se réinitialise lorsque l'alimentation externe est rétablie.

4. ``power_restored``

   Déclenché lorsque la source d'alimentation externe est rétablie.

   * **Condition de réinitialisation** : Se réinitialise si l'alimentation externe est à nouveau déconnectée.

5. ``power_insufficient``

   Se produit lorsque l'alimentation externe est insuffisante, nécessitant que la batterie fournisse une puissance supplémentaire.

   * **Action recommandée** : Vérifiez la puissance nominale de la source d'alimentation ou vérifiez les paramètres de puissance de charge configurés.
   * **Condition de réinitialisation** : Se réinitialise lorsque la source d'alimentation externe est déconnectée.

6. ``battery_critical_shutdown``

   Déclenché juste avant l'arrêt du système en raison d'une **capacité de batterie extrêmement faible**.

7. ``battery_voltage_critical_shutdown``

   Déclenché lorsque la **tension de la batterie** descend en dessous du seuil critique, entraînant l'arrêt.

   * **Remarque** : Cet événement est rarement déclenché en utilisation normale. Généralement, l'événement ``low_battery`` initie une séquence d'arrêt avant que la tension ne descende aussi bas. Cela sert de **mécanisme d'arrêt de sécurité**.

Avec ces événements, le PiPower5 fournit à la fois des avertissements proactifs (par ex., batterie faible, puissance insuffisante) et des sauvegardes critiques (par ex., déclencheurs d'arrêt), assurant un fonctionnement stable et une protection des données.



Alertes par buzzer
+++++++++++++++++++++++++++++++++++++++++++++++++

Le PiPower5 prend en charge les notifications par buzzer pour différents événements système.

Vous pouvez configurer les alertes par buzzer via le **tableau de bord Web** ou l'**outil en ligne de commande**.
Lorsqu'un événement configuré se produit, le PiPower5 joue le son de buzzer correspondant.

Les fonctionnalités incluent :

- Notifications par buzzer basées sur les événements
- Volume du buzzer réglable (1–10)
- Aperçu du son des événements
- Prise en charge des effets sonores personnalisés

Les utilisateurs avancés peuvent également créer des effets sonores de buzzer personnalisés.

1. Ouvrez le fichier de configuration :

   .. code-block:: shell

      /opt/pipower5/venv/lib/python3.11/site-packages/pipower5/config.json

2. Localisez la section ``pipower5_buzz_sequence``.

3. Chaque effet sonore est défini en utilisant le format suivant :

   .. code-block:: text

      [action, duration]

   Où :

   - ``action`` peut être :

     - Une note de musique, telle que ``"A4"``, ``"D3"`` ou ``"C#4"``
     - Une valeur de fréquence (entier)
     - ``"pause"`` pour le silence

   - ``duration`` est le temps de lecture en millisecondes (ms)


Alertes par email
+++++++++++++++++++++++++++++++++++++++++++++++++

Le PiPower5 prend en charge les notifications par email pour les événements système importants, tels que :

- Batterie faible
- Alimentation déconnectée
- Alimentation rétablie
- Événements d'arrêt critiques

Les notifications par email peuvent être configurées via le **tableau de bord Web** ou l'**outil en ligne de commande**.

Pour utiliser les alertes par email, un serveur SMTP est requis. La plupart des fournisseurs de messagerie prennent en charge les services SMTP.

- Pour Gmail, créez simplement un **mot de passe d'application**
- Pour les autres fournisseurs, activez l'accès SMTP et générez un mot de passe SMTP dédié si nécessaire

Avant la configuration, préparez les informations suivantes :

- Adresse du serveur SMTP
  (Exemple : ``smtp.gmail.com``)

- Port SMTP
  (Exemple : ``465`` ou ``25``)

- Type de chiffrement
  (``None`` / ``SSL`` / ``TLS``)

- Compte SMTP
  (Généralement votre adresse email)

- Mot de passe SMTP
  (Mot de passe d'application ou mot de passe SMTP)

Après avoir saisi les informations SMTP, configurez l'adresse email du destinataire.

.. note::

   Le PiPower5 utilise le serveur SMTP pour se connecter à votre compte email et envoyer des notifications.

   Vous pouvez utiliser la même adresse email comme expéditeur et destinataire.

Après la configuration, utilisez la commande de test pour vérifier la connexion SMTP et la livraison des emails.
