.. note::

    Bonjour, bienvenue dans la communauté SunFounder des passionnés de Raspberry Pi, Arduino et ESP32 sur Facebook ! Explorez plus en profondeur Raspberry Pi, Arduino et ESP32 avec d'autres passionnés.

    **Pourquoi nous rejoindre ?**

    - **Assistance d'experts** : Résolvez les problèmes post-achat et les défis techniques avec l'aide de notre communauté et de notre équipe.
    - **Apprendre et partager** : Échangez des astuces et des tutoriels pour améliorer vos compétences.
    - **Aperçus exclusifs** : Accédez en avant-première aux annonces de nouveaux produits et aux aperçus.
    - **Réductions spéciales** : Profitez de remises exclusives sur nos produits les plus récents.
    - **Promotions festives et cadeaux** : Participez à des concours et à des promotions saisonnières.

    👉 Prêt à explorer et à créer avec nous ? Cliquez [|link_sf_facebook|] et rejoignez-nous dès aujourd'hui !

.. _faq:

FAQ
===

Comment réinstaller PiPower 5
-----------------------------

Si le PiPower 5 ne fonctionne pas correctement et que vous souhaitez effectuer une réinstallation propre, suivez ces étapes :

**1. Désinstaller l'installation actuelle :**

.. code-block:: shell

   cd ~/pipower5
   sudo python3 install.py --uninstall

**2. Réinstaller à partir des sources :**

.. code-block:: shell

   git clone https://github.com/sunfounder/pipower5
   cd pipower5
   sudo python3 install.py

**3. Redémarrer le Raspberry Pi lorsqu'il vous est demandé.**

Après le redémarrage, vérifiez l'installation :

.. code-block:: shell

   pipower5 -a
   sudo systemctl status pipower5.service

.. tip::

   Si le répertoire ``~/pipower5`` n'existe plus de l'installation d'origine, ignorez l'étape de désinstallation et passez directement à l'étape de réinstallation.


Le tableau de bord affiche « Database Required » ou aucune donnée
------------------------------------------------------------------

**Ce que vous voyez** : Le tableau de bord Web s'ouvre normalement dans votre navigateur, mais tous les panneaux de données sont vides ou affichent « database required ».

**Ce que cela signifie généralement** : C'est rarement un problème matériel. Dans la plupart des cas, le backend InfluxDB a un problème de configuration — une base de données corrompue, un bucket manquant ou un jeton expiré.

**Vérifiez ces points, dans l'ordre :**

1. **Vérifier que le service PiPower 5 est en cours d'exécution :**

   .. code-block:: shell

      sudo systemctl status pipower5

   Si le service n'est pas actif, démarrez-le :

   .. code-block:: shell

      sudo systemctl start pipower5

2. **Vérifier si le bucket InfluxDB existe :**

   .. code-block:: shell

      sudo influx bucket list

   Recherchez un bucket nommé ``pipower5`` dans la sortie. S'il est manquant, la base de données doit être recréée.

3. **Vérifier les journaux de service pour les erreurs :**

   .. code-block:: shell

      journalctl -u pipower5 -n 50

   Recherchez les messages d'erreur liés à InfluxDB, tels que :

   - ``unauthorized`` ou ``token`` — indique un problème de jeton d'authentification.
   - ``bucket not found`` — le bucket de base de données est manquant.
   - ``connection refused`` — InfluxDB n'est pas en cours d'exécution.

4. **Si InfluxDB lui-même est arrêté**, redémarrez-le :

   .. code-block:: shell

      sudo systemctl restart influxdb
      sudo systemctl restart pipower5

.. note::

   Si InfluxDB a été installé manuellement ou migré depuis une version antérieure, les chemins de configuration ou les jetons d'authentification peuvent avoir changé. Dans ce cas, une réinstallation propre de PiPower 5 (voir ci-dessus) réinitialisera également la configuration InfluxDB.
