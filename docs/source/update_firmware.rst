Mise à jour du firmware du PiPower5 avec le Raspberry Pi
===================================================================

Ce guide explique comment mettre à jour le firmware du **PiPower5** sur un Raspberry Pi.

**1. Télécharger** ``pipower5_update_tools`` **et installer les dépendances**

.. code-block:: shell

   git clone https://github.com/sunfounder/pipower5_update_tools.git --depth 1

   sudo pip3 install blessed --break
   sudo pip3 install smbus2 --break

**2. Vérifier les mises à jour**

.. code-block:: shell

   cd pipower5_update_tools
   git pull

**3. Exécuter l'outil de mise à jour**

.. code-block:: shell

   python3 run.py

**4. Arrêter le service si demandé**

Lors de l'exécution de ``pipower5_update_tools``, il peut vous être demandé d'arrêter ``pipower5.service``. Appuyez sur ``Y`` pour arrêter le service.

.. image:: img/upd_frw_1.png

**5. Sélectionner** ``Update Firmware``

Choisissez **Update Firmware**. Le Raspberry Pi enverra une commande qui fait passer le PiPower5 en **mode BOOT**.

.. image:: img/upd_frw_2.png

**6. Vérifier le mode BOOT**

Une fois en mode BOOT avec succès, les **deux LED centrales** du PiPower5 clignoteront alternativement, indiquant que le mode BOOT est actif.

.. image:: img/upd_frw_3.png

**7. Choisir le fichier firmware**

Sélectionnez un fichier firmware au format ``.bin`` et appuyez sur ``Entrée`` pour commencer l'écriture.

.. image:: img/upd_frw_4.png

**8. Terminer la mise à jour**

Une fois le flashage terminé, sélectionnez **Restart**.
Le PiPower5 redémarrera et exécutera le nouveau firmware.

.. image:: img/upd_frw_5.png

----------------------------------------------------------------

**Restaurer le firmware d'usine**

Si vous devez revenir au firmware d'usine, utilisez l'option **Restore Factory Firmware** dans ``pipower5_update_tools``.
Cela rechargera le firmware stocké dans la partition d'usine et rétablira la version d'origine.

.. image:: img/upd_frw_6.png


----------------------------------------------------------------

**Forcer le mode BOOT**

Si vous ne pouvez pas entrer en mode BOOT normalement, vous pouvez le forcer :

1. Éteignez le PiPower5.
2. Court-circuitez la **broche Boot 1**.
3. Mettez l'appareil sous tension.

Le PiPower5 démarrera directement en mode BOOT.

.. image:: img/upd_frw_7.png

Pour quitter le mode BOOT, maintenez le bouton d'alimentation enfoncé pendant deux secondes.
Le PiPower5 redémarrera alors en mode normal.

.. image:: img/upd_frw_8.png

----------------------------------------------------------------

**Dépannage**


Voici quelques problèmes courants que vous pouvez rencontrer pendant le processus de mise à jour et leurs solutions :

- **Appareil non détecté**

  - Essayez de redémarrer à la fois le Raspberry Pi et le PiPower5, puis réexécutez l'outil de mise à jour.

- **Échec de l'entrée en mode BOOT**

  - Assurez-vous que ``pipower5.service`` est arrêté avant la mise à jour.
  - Si le mode BOOT automatique échoue, utilisez la méthode **Forcer le mode BOOT** (court-circuit de la broche Boot 1).

- **Processus de mise à jour bloqué ou flashage échoué**

  - Vérifiez que le fichier firmware est au format ``.bin``.
  - Réexécutez l'outil de mise à jour et réessayez.
  - Utilisez une alimentation stable pour éviter les interruptions pendant le flashage.

- **Mise à jour du firmware terminée, mais l'appareil ne fonctionne pas correctement**

  - Restaurez le firmware d'usine à l'aide de l'outil intégré.
  - Si le problème persiste, vérifiez que le fichier firmware correspond à votre version du PiPower5.
