MicroPython
==========================================================

Nous fournissons une bibliothèque qui vous permet de surveiller les tensions d'entrée et de sortie, la tension et le pourcentage de la batterie, la source d'alimentation, l'état de charge et d'autres données internes.

Si vous utilisez le PiPower 5 pour alimenter votre carte Raspberry Pi Pico ou ESP32, vous pouvez connecter la carte au PiPower 5 via le port de sortie Type-A ou deux câbles de liaison.

Pour connecter l'interface I2C du PiPower 5, utilisez un cavalier.

.. If no operations are needed before shutting down, connect the SDSIG jumper cap directly to the GND pin. If operations are required before shutdown, remove the jumper cap and connect the intermediate wire to an I/O pin on the Raspberry Pi Pico or ESP32 board. This setup notifies the PiPower 5 that the shutdown process is complete and it can safely power off.

#. Téléchargez la bibliothèque depuis GitHub. Vous pouvez la télécharger rapidement en utilisant le lien ci-dessous ou visitez : https://github.com/sunfounder/micropython_spc.

   * :download:`micropython_spc <https://github.com/sunfounder/micropython_spc/archive/refs/heads/main.zip>`

#. Après avoir téléchargé et décompressé, téléversez le dossier ``spc`` sur votre carte Raspberry Pi Pico ou ESP32. Thonny est recommandé pour cette opération.

   .. image:: img/micropython_upload.png
       :width: 100%
       :align: center

   .. raw:: html

      <br/>

#. Une fois la bibliothèque téléversée, vous pouvez la tester en utilisant les exemples fournis dans le dossier ``micropython_spc-main/examples/pipower5`` :

   * ``pipower_5_read_all.py`` : Utilisez cet exemple si vous avez besoin de lire toutes les données. Il montre comment lire toutes les données disponibles en une fois et les traiter individuellement.

   * ``pipower_5_read_individual.py`` : Cet exemple fournit des instructions pour lire des données spécifiques individuellement. Utilisez-le si vous n'avez besoin d'accéder qu'à certaines données.

   * ``pipower_5_set_shutdown_percentage.py`` : Cet exemple explique comment définir le pourcentage de batterie d'arrêt. Lorsque la batterie n'est pas en charge et que son niveau descend en dessous du pourcentage spécifié, le PiPower 5 envoie un signal d'arrêt à l'hôte. Il ne se met hors tension qu'après que l'hôte a terminé son arrêt et renvoyé un signal de mise hors tension.

     * Pour les SBC (ex. Raspberry Pi) : Aucune configuration supplémentaire n'est requise.
     * Pour les microcontrôleurs : Retirez le cavalier **SDSIG** et connectez le fil intermédiaire à une broche. Après avoir reçu le signal d'arrêt et effectué un arrêt sécurisé, mettez cette broche à l'état haut pour indiquer au PiPower 5 de se mettre hors tension.

   * ``pipower_5_shutdown_when_request.py`` : Cet exemple montre comment gérer les opérations après avoir reçu un signal d'arrêt. Vous devez retirer le cavalier **SDSIG** et connecter le fil intermédiaire à une broche.

Documentation de l'API de la bibliothèque MicroPython : https://github.com/sunfounder/micropython_spc?tab=readme-ov-file#api
