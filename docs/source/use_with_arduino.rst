Arduino
===================================

Si vous utilisez le PiPower 5 pour alimenter votre carte Arduino, vous pouvez connecter l'Arduino au port de sortie Type A du PiPower 5 ou utiliser deux câbles de liaison. Connectez l'interface I2C de la carte à l'aide d'un cavalier.

.. If no operation is required before powering off, directly connect the **SDSIG** jumper cap to the GND. If operations are necessary before shutdown, remove the jumper cap and connect the intermediate wire to an IO port on the Arduino to notify PiPower 5 that it can safely power off.

Nous fournissons une bibliothèque qui vous permet de surveiller les tensions d'entrée et de sortie, la tension et le pourcentage de la batterie, la source d'alimentation, l'état de charge et d'autres données internes.

#. Dans l'IDE Arduino, ouvrez le **Gestionnaire de bibliothèques**, recherchez ``SunFounderPowerControl``, puis téléchargez et installez-la.

   .. image:: img/install_arduino_lib.png
      :width: 100%

#. Après l'installation, vous pouvez accéder à **Fichier** -> **Exemples** -> **SunFounderPowerControl** -> **PiPower 5**, où vous trouverez quatre exemples.

   .. image:: img/arduino_lib_example.png
      :width: 100%

   * ``read_all`` : Utilisez cet exemple si vous avez besoin de lire toutes les données en une fois et de les traiter individuellement.
   * ``read_individual`` : Si vous n'avez besoin de lire que certaines données, cet exemple fournit des instructions de récupération de données individuelles.
   * ``set_shutdown_percentage`` : Cet exemple explique comment définir un pourcentage de batterie d'arrêt. Cette fonction envoie un signal d'arrêt à l'hôte lorsque la batterie n'est pas en charge et descend en dessous du pourcentage défini. Après l'arrêt de l'hôte, il ne se mettra hors tension qu'après avoir reçu un signal de mise hors tension. Généralement utilisé avec des SBC comme le Raspberry Pi. Pour les microcontrôleurs, retirez le cavalier **SDSIG** et connectez le fil intermédiaire à une broche. Après un arrêt sécurisé suite à la réception du signal d'arrêt, mettez cette broche à l'état haut pour éteindre le PiPower 5.
   * ``shutdown_when_request`` : Cet exemple montre comment gérer les opérations après avoir reçu un signal d'arrêt. Retirez le cavalier **SDSIG** et connectez le fil intermédiaire à une broche.

#. Choisissez l'un des exemples et téléversez-le sur votre carte.

   .. note::

      Sur certaines cartes où l'I2C peut être modifié, si vous devez changer les broches I2C, vous devez modifier le code ``Wire.begin()``.

Documentation de l'API de la bibliothèque Arduino : https://github.com/sunfounder/arduino_spc?tab=readme-ov-file#api

