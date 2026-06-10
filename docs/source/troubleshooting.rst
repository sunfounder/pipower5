.. note::

    Bonjour, bienvenue dans la communauté SunFounder des passionnés de Raspberry Pi, Arduino et ESP32 sur Facebook ! Explorez plus en profondeur Raspberry Pi, Arduino et ESP32 avec d'autres passionnés.

    **Pourquoi nous rejoindre ?**

    - **Assistance d'experts** : Résolvez les problèmes post-achat et les défis techniques avec l'aide de notre communauté et de notre équipe.
    - **Apprendre et partager** : Échangez des astuces et des tutoriels pour améliorer vos compétences.
    - **Aperçus exclusifs** : Accédez en avant-première aux annonces de nouveaux produits et aux aperçus.
    - **Réductions spéciales** : Profitez de remises exclusives sur nos produits les plus récents.
    - **Promotions festives et cadeaux** : Participez à des concours et à des promotions saisonnières.

    👉 Prêt à explorer et à créer avec nous ? Cliquez [|link_sf_facebook|] et rejoignez-nous dès aujourd'hui !

.. _troubleshooting:

Dépannage
===============

Cette page vous aide à diagnostiquer les problèmes du PiPower 5 en utilisant les LED intégrées, le buzzer et les outils logiciels. Commencez par les tableaux de référence rapide ci-dessous, puis suivez les guides basés sur les symptômes pour des étapes détaillées.

.. contents:: Table des matières
   :local:
   :depth: 2


-----------------------------------
Référence rapide LED et buzzer
-----------------------------------

Avant de plonger dans les symptômes spécifiques, utilisez ces tableaux pour interpréter ce que la carte vous indique.

LED d'alimentation et d'état
++++++++++++++++++++++++++++++

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - LED
     - État
     - Signification
   * - **LED PWR** (verte)
     - ON
     - La puissance de sortie est active — la carte fournit 5V à votre appareil.
   * -
     - OFF
     - La sortie est désactivée. Appuyez une fois sur le bouton d'alimentation pour l'activer.
   * - **LED BAT** (jaune)
     - ON
     - La batterie fournit actuellement l'alimentation. Si l'alimentation externe est connectée, cela indique une puissance d'entrée insuffisante.
   * -
     - OFF
     - La batterie est en veille — l'alimentation externe est suffisante.
   * - **LED de batterie inversée** (2× rouge)
     - ON (les deux)
     - La polarité de la batterie est inversée ! Déconnectez immédiatement et corrigez le câblage.

LED de niveau de batterie
+++++++++++++++++++++++++++

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Schéma des LED
     - Signification
   * - 4 LED allumées
     - Batterie > 80%
   * - 3 LED allumées
     - Batterie 60% – 80%
   * - 2 LED allumées
     - Batterie 40% – 60%
   * - 1 LED allumée
     - Batterie 20% – 40%
   * - Première LED clignotante
     - Batterie < 20% — charger bientôt
   * - LED défilant séquentiellement
     - Charge en cours
   * - Deux LED centrales clignotantes
     - En attente du signal d'arrêt du Raspberry Pi
   * - Toutes les LED éteintes
     - Carte hors tension ou en mode veille

.. note::

   Les LED de batterie restent actives pendant la charge même lorsque la carte est à l'état éteint. Elles s'éteignent uniquement lorsque la charge est terminée.

Signaux du buzzer
+++++++++++++++++++

Si le buzzer est activé, ces sons indiquent des événements spécifiques :

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Événement
     - Son typique
     - Signification
   * - ``battery_activated``
     - Deux tonalités ascendantes
     - La batterie a pris le relais de l'alimentation (alimentation externe perdue ou insuffisante).
   * - ``low_battery``
     - Deux tonalités répétées de même hauteur
     - Le niveau de la batterie est descendu en dessous du pourcentage d'arrêt configuré. Chargez immédiatement.
   * - ``power_disconnected``
     - Tonalité haute → tonalité basse
     - L'alimentation externe a été déconnectée. Le système fonctionne maintenant sur batterie.
   * - ``power_restored``
     - Tonalité basse → tonalité haute
     - L'alimentation externe a été rétablie. La batterie ne se décharge plus.
   * - ``power_insufficient``
     - Trois tonalités rapides de même hauteur
     - L'alimentation externe est connectée mais trop faible. La batterie fournit un complément. Vérifiez votre adaptateur secteur.
   * - ``battery_critical_shutdown``
     - Trois tonalités descendantes rapides
     - La capacité de la batterie est extrêmement faible. Le système va s'arrêter.
   * - ``battery_voltage_critical_shutdown``
     - Quatre tonalités descendantes rapides
     - La tension de la batterie est extrêmement faible (sécurité). Le système va s'arrêter immédiatement.

.. tip::

   Si vous n'entendez jamais les sons du buzzer, le buzzer est peut-être désactivé ou son volume réglé sur 0. Exécutez ``pipower5 -bzv`` pour vérifier le volume actuel, ou testez avec ``pipower5 -bzt low_battery``.


---------------------------------
Diagnostic basé sur les symptômes
---------------------------------

« Pas d'alimentation » — Toutes les LED éteintes, pas de sortie
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

**Ce que vous voyez** : LED PWR éteinte, LED de batterie éteintes, l'appareil connecté n'affiche aucune alimentation.

**Vérifiez ces points, dans l'ordre :**

1. **La batterie est-elle installée ?**
   Le PiPower 5 ne peut pas fonctionner sans batterie. Assurez-vous que le connecteur de batterie (XH2.54 3P) est fermement inséré. Voir :ref:`battery_connector`.

2. **La batterie est-elle complètement déchargée ?**
   Une batterie profondément déchargée (< 2,5V par cellule) entre en mode de charge d'entretien et peut ne pas alimenter la carte pendant plusieurs minutes.

   - Connectez l'alimentation externe et attendez 10–15 minutes.
   - Si les LED de batterie restent éteintes après 15 minutes, la batterie est peut-être défectueuse.

3. **L'alimentation externe est-elle correctement connectée ?**

     - Utilisez une alimentation USB-C PD (5V–15V) ou une alimentation CC via les bornes à vis.
     - Assurez-vous que le câble USB-C prend en charge la fourniture d'énergie — certains câbles de données uniquement ne fonctionneront pas.
     - Essayez un autre adaptateur secteur et câble.

4. **Appuyez une fois sur le bouton d'alimentation.**
   Le PiPower 5 nécessite un appui sur le bouton pour activer la sortie, sauf si le cavalier Default ON est réglé.

5. **Vérifiez le cavalier Default ON.** Voir :ref:`cap_onoff`.
   - Cavalier sur **ON** : La sortie s'active automatiquement lorsque l'alimentation externe est connectée.
   - Cavalier sur **OFF** : Vous devez appuyer sur le bouton d'alimentation à chaque fois.

6. **Vérifiez l'installation inversée de la batterie.**
   Si les deux LED rouges près du connecteur de batterie sont allumées, la polarité de la batterie est inversée. Mettez hors tension immédiatement, déconnectez la batterie et reconnectez avec la polarité correcte. Voir :ref:`battery_connector`.


« LED BAT toujours allumée » — L'alimentation externe semble insuffisante
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

**Ce que vous voyez** : L'alimentation externe est connectée, mais la LED BAT reste allumée. La batterie se décharge malgré la présence d'une alimentation externe.

**Ce que cela signifie** : L'alimentation externe ne peut pas répondre à la demande totale de puissance. La batterie comble le déficit.

**Vérifiez ces points, dans l'ordre :**

1. **Votre adaptateur secteur est-il assez puissant ?**
   La formule est : *Puissance de l'adaptateur ≥ Puissance du Raspberry Pi (~20–25W) + Puissance de charge (définie via le DIP switch)*.

   - Le Raspberry Pi 5 sous charge peut consommer > 25W.
   - Si la puissance de charge est réglée sur 20W (les deux DIP switches sur ON), vous avez besoin d'un adaptateur **45W+**.
   - Pour un adaptateur 30W, réduisez la puissance de charge à 10W ou 5W.

2. **Vérifiez le DIP switch (sélecteur de puissance de charge).**
   Consultez le tableau de puissance de charge dans :ref:`power_input`. Réduisez la puissance de charge si votre adaptateur est sous-dimensionné.

3. **Essayez un autre câble USB-C.**
   Tous les câbles ne prennent pas en charge l'USB PD à des puissances élevées. Utilisez le câble fourni avec votre adaptateur secteur.

4. **Vérifiez le profil PD de l'adaptateur.**
   Certains adaptateurs annoncent une puissance élevée mais uniquement sur des combinaisons tension/courant spécifiques. Le PiPower 5 nécessite une alimentation conforme PD. Les adaptateurs non-PD (par ex., 5V fixe uniquement) peuvent ne pas fournir assez de courant.

5. **Pour l'entrée par bornes à vis**, assurez-vous que la tension d'entrée est ≥ 9V pour des performances optimales. Voir :ref:`power_input` pour les limites tension-courant.


« LED PWR éteinte » — L'appareil ne reçoit pas d'alimentation
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

**Ce que vous voyez** : Les LED de batterie sont allumées (la carte est alimentée), mais la LED PWR est éteinte et l'appareil connecté ne démarre pas.

**Vérifiez ces points :**

1. **Appuyez une fois sur le bouton d'alimentation.**
   La carte est alimentée mais la sortie n'est pas activée.

2. **Le connecteur GPIO est-il correctement inséré ?**
   Si vous utilisez un Raspberry Pi, retirez et réinsérez le HAT PiPower 5. Vérifiez l'absence de broches tordues ou de débris dans le connecteur.

3. **Essayez une sortie alternative.**
   Connectez un appareil au port USB-A ou au connecteur 2x4P. Si ceux-ci fonctionnent, le problème vient du passthrough GPIO.


« L'appareil s'arrête de façon inattendue »
+++++++++++++++++++++++++++++++++++++++++++++

**Ce que vous voyez** : Le Raspberry Pi ou l'appareil connecté s'arrête sans avertissement.

**Vérifiez ces points :**

1. **Vérifiez le pourcentage d'arrêt.**
   Exécutez ``pipower5 -sp``. S'il est réglé haut (par ex., 50% ou plus), la carte déclenchera un arrêt précoce. Définissez une valeur plus basse si nécessaire :

   .. code-block:: shell

      pipower5 -sp 10
      sudo systemctl restart pipower5.service

2. **Vérifiez si la batterie se décharge réellement.**

     Exécutez ``pipower5 -a`` et regardez :

     - ``source`` : Doit être "0 - External" lorsque l'alimentation externe est connectée.
     - ``battery current`` : Négatif = charge, Positif = décharge.

3. **Pour Raspberry Pi 5 avec périphériques haute puissance (SSD, HAT)** :
   Envisagez de définir ``pipower5 -sp 100`` pour déclencher un arrêt sécurisé immédiat lorsque l'alimentation externe est perdue. Voir :ref:`pipower5_tool`.

4. **Vérifiez l'adaptateur secteur.**
   Si des événements ``power_insufficient`` sont déclenchés (buzzer ou journal), l'adaptateur est trop faible. Passez à une alimentation de puissance supérieure ou réduisez le DIP switch de puissance de charge.


« La batterie ne charge pas »
+++++++++++++++++++++++++++++++

**Ce que vous voyez** : Alimentation externe connectée, mais les LED de batterie n'affichent pas l'animation de charge (défilement séquentiel).

**Vérifiez ces points :**

1. **La batterie est-elle déjà pleine ?**
   4 LED fixes = batterie > 80%. Le circuit de charge peut s'être arrêté parce que la batterie est pleine ou en phase de tension constante.

2. **Vérifiez l'état de charge via le logiciel.**
   Exécutez ``pipower5 -ichg``. S'il renvoie ``False``, la carte signale qu'elle n'est pas en charge. Vérifiez ``pipower5 -bp`` pour le pourcentage actuel de la batterie.

3. **Protection contre la surchauffe active.**
   Si la carte a été soumise à une charge élevée dans un environnement chaud, la puce de charge peut avoir dépassé 125°C et arrêté la charge. Laissez la carte refroidir et réessayez.

4. **Tension d'entrée trop basse via les bornes à vis.**
   Si vous utilisez les bornes à vis avec une tension ≤ 6,5V, le courant de charge est limité. Utilisez ≥ 9V pour une charge fiable.

5. **Vérifiez l'état de la batterie.**
   Une batterie qui n'atteint jamais la charge complète ou qui charge très lentement peut avoir des cellules dégradées. Essayez une autre batterie compatible (Li-ion 7.4V 2 cellules, XH2.54 3P).


« Échec de la communication I2C » — La commande `pipower5` renvoie des erreurs
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

**Ce que vous voyez** : L'exécution de ``pipower5 -a`` produit une erreur ou aucune donnée.

**Vérifiez ces points :**

1. **L'I2C est-il activé sur le Raspberry Pi ?**
   Exécutez ``sudo raspi-config`` → Interface Options → I2C → Enable.

2. **Le périphérique I2C est-il détecté ?**

   .. code-block:: shell

      sudo i2cdetect -y 1

   Le PiPower 5 devrait apparaître à l'adresse ``0x5a``. Si aucun périphérique n'apparaît :

   - Réinsérez le HAT sur le connecteur GPIO.
   - Vérifiez que ``i2c-dev`` est chargé : ``lsmod | grep i2c``.
   - Vérifiez que ``dtparam=i2c_arm=on`` est dans ``/boot/firmware/config.txt``.

3. **Le service `pipower5` est-il en cours d'exécution ?**

   .. code-block:: shell

      sudo systemctl status pipower5.service

   S'il est inactif, démarrez-le : ``sudo systemctl start pipower5.service``.

4. **Conflit entre plusieurs périphériques I2C ?**
   Le PiPower 5 utilise l'adresse I2C ``0x5a``. Vérifiez qu'aucun autre HAT ou périphérique n'utilise cette adresse. Voir :ref:`pin_header`.

5. **Redémarrez.**
   Parfois, un redémarrage à froid du Raspberry Pi et du PiPower 5 résout les problèmes de bus I2C. Mettez hors tension complètement, attendez 10 secondes, puis remettez sous tension.


« Buzzer silencieux » — Aucun son lors des événements
++++++++++++++++++++++++++++++++++++++++++++++++++++++

**Ce que vous voyez** : Des événements se produisent (déconnexion d'alimentation, batterie faible, etc.) mais aucun son du buzzer.

**Vérifiez ces points :**

1. **Vérifiez le volume du buzzer.**

   .. code-block:: shell

      pipower5 -bzv

   S'il renvoie 0, le buzzer est en sourdine. Définissez un volume (1–10) :

   .. code-block:: shell

      pipower5 -bzv 5
      sudo systemctl restart pipower5.service

2. **Vérifiez quels événements ont le buzzer activé.**

   .. code-block:: shell

      pipower5 -bzo

   Assurez-vous que l'événement attendu est dans la liste. Pour ajouter un événement :

   .. code-block:: shell

      pipower5 -bzo low_battery,power_disconnected

3. **Testez le buzzer directement.**

   .. code-block:: shell

      pipower5 -bzt low_battery

   Si vous entendez un son, le matériel du buzzer fonctionne — le problème vient de la configuration des événements.


« Le Raspberry Pi affiche un avertissement de basse tension »
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

**Ce que vous voyez** : Le bureau du Raspberry Pi ou ``dmesg`` affiche des avertissements de sous-tension.

**C'est un comportement normal dans certains cas :**

- Lors de l'alimentation d'un Raspberry Pi depuis le port USB-A du PiPower 5 (au lieu du connecteur GPIO), le Pi peut signaler un avertissement d'alimentation non-PD. Cela peut être ignoré en toute sécurité.
- Si vous utilisez le connecteur GPIO et voyez toujours des avertissements, la sortie du PiPower 5 est peut-être soumise à une charge élevée. Vérifiez la consommation totale de courant de votre configuration.

**Vérifiez ces points :**

1. Exécutez ``pipower5 -a`` et vérifiez ``Output: voltage``. Il devrait être stable autour de 5,2–5,3V. S'il descend en dessous de 5,0V en charge, la consommation totale de courant peut dépasser la limite de 5A.

2. Déconnectez les périphériques USB non essentiels et retestez.

3. Si le problème persiste, le convertisseur DC-DC est peut-être défectueux. Contactez le support.


--------------------------------------
Commandes de diagnostic logiciel
--------------------------------------

L'outil CLI ``pipower5`` est votre interface de diagnostic principale. Voici les commandes les plus utiles :

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Commande
     - Ce qu'elle vous indique
   * - ``pipower5 -a``
     - Aperçu complet de l'état : tension d'entrée/sortie, état de la batterie, état de charge, demande d'arrêt, état du bouton.
   * - ``pipower5 -bp``
     - Pourcentage de la batterie.
   * - ``pipower5 -ichg``
     - Si la batterie est actuellement en charge (``True`` / ``False``).
   * - ``pipower5 -ii``
     - Si l'alimentation externe est connectée.
   * - ``pipower5 -sp``
     - Seuil actuel du pourcentage d'arrêt.
   * - ``pipower5 -sr``
     - État actuel de la demande d'arrêt (0 = Aucune, 1 = Batterie faible, 2 = Bouton).
   * - ``pipower5 -pb``
     - État actuel du bouton d'alimentation.
   * - ``pipower5 -bzv``
     - Volume actuel du buzzer.
   * - ``pipower5 -fv``
     - Version du firmware (vérifiez que vous avez la dernière version).
   * - ``pipower5 -c``
     - Vidage complet de la configuration.
   * - ``pipower5 -pfs 60``
     - Exécute une simulation de panne de courant de 60 secondes pour tester l'autonomie de la batterie.
   * - ``sudo systemctl status pipower5.service``
     - Vérifie si le service en arrière-plan PiPower 5 est en cours d'exécution.
   * - ``cat /opt/pipower5/log``
     - Affiche les journaux de service pour les messages d'erreur.

.. tip::

   Pour une vérification rapide de l'état, exécutez ``pipower5 -a`` et vérifiez :

   - ``shutdown request`` est ``0 - NONE`` (aucun arrêt en attente).
   - ``battery percentage`` est au-dessus de votre ``shutdown percentage``.
   - ``Output: voltage`` est entre 5,1V et 5,4V.


--------------------------------
Vous avez encore des problèmes ?
--------------------------------

Si aucune des solutions ci-dessus ne résout votre problème, collectez les informations suivantes avant de contacter le support :

1. **Informations système** :

   .. code-block:: shell

      pipower5 -a
      pipower5 -fv
      pipower5 -c

2. **Journaux de service** :

   .. code-block:: shell

      cat /opt/pipower5/log
      sudo journalctl -u pipower5.service --no-pager -n 100

3. **Détails matériels** :

     - Modèle de Raspberry Pi
     - Modèle d'adaptateur secteur et puissance nominale
     - Type et âge de la batterie
     - Paramètres du DIP switch du PiPower 5
     - Positions des cavaliers SDSIG et Default ON

