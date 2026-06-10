PiPower 5 HAT
======================

.. interface:

Aperçu de l'interface
----------------------

.. image:: img/pipower5_ov.png
  :width: 100%



1. **Entrée d'alimentation USB Type-C**

   - Entrée d'alimentation externe pour alimenter le Raspberry Pi et charger la batterie simultanément.
   - Prend en charge le protocole **USB Power Delivery (PD)**, plage d'entrée **5V–15V**.

2. **Sélecteur d'entrée d'alimentation (DIP Switch)**

   - Permet la sélection de différents profils de puissance d'entrée pour une configuration flexible.

3. **Cavalier Default ON**

   - Définit si le système doit s'allumer automatiquement lorsque l'alimentation externe est connectée alors que l'appareil est éteint.
   - ON = Mise sous tension automatique activée, OFF = Démarrage manuel requis.

4. **SDSIG (Signal d'arrêt)**

   - Fournit la détection d'arrêt pour le Raspberry Pi.
   - Lorsqu'il est relié à **PI3V3**, il fonctionne avec les Raspberry Pi 4 et Pi 5.
   - Lorsqu'il est court-circuité à la **broche 26**, il prend en charge les Pi 3 et Pi Zero.
   - Après une configuration appropriée, le PiPower5 coupera automatiquement l'alimentation une fois le Raspberry Pi arrêté.

5. **LED PWR (Indicateur d'état de sortie)**

   - S'allume lorsque la sortie du système est active.

6. **LED BAT (Indicateur d'état de la batterie)**

   - S'allume lorsque le système est alimenté par la batterie.
   - Un rappel pour surveiller la consommation de la batterie lors du fonctionnement sans alimentation externe.

7. **Bouton d'alimentation**

   - **Appui simple** : Activer la sortie d'alimentation.
   - **Appui long (2 secondes)** : Envoie une demande d'arrêt sécurisé via I²C.
   - **Appui long (5 secondes)** : Force une mise hors tension immédiate (arrêt brutal).
   - **Personnalisable** : Les actions d'appui simple et double peuvent être reconfigurées par logiciel.

8. **Borne pour bouton d'alimentation externe (ZH1.5 2P)**

   - Permet la connexion d'un bouton d'alimentation physique externe.

9. **Connecteur pour bouton d'alimentation externe (2.54mm)**

   - Une option de connecteur soudable alternative pour la connexion d'un bouton d'alimentation externe.

10. **LED indicatrices de batterie**

    - Affichent la capacité restante de la batterie et l'état de charge.
    - Remarque : Même lorsque le système est éteint, les LED restent actives pendant la charge jusqu'à ce que la batterie soit complètement chargée.

11. **Interface I²C (SH1.0 4P)**

    - Compatible avec les écosystèmes **Qwiic** et **STEMMA QT**.
    - Utilisée pour la communication avec le microcontrôleur intégré et les périphériques externes.

12. **Interface I²C (connecteur 1x4P 2.54mm)**

    - Sortie I²C alternative avec **sortie d'alimentation 3V3**, configurable comme toujours active ou commutée.

13. **Cavalier de sélection d'alimentation I²C**

    - **PERM** : L'alimentation 3V3 est toujours active lorsque l'alimentation externe est connectée.
    - **SHUT (par défaut)** : L'alimentation 3V3 se coupe automatiquement lorsque le système s'arrête.

14. **Port de sortie USB Type-A**

    - Fournit une **sortie 5V régulée**, adaptée pour alimenter des périphériques ou d'autres appareils.
    - Lors de l'alimentation d'un Raspberry Pi, vous pouvez rencontrer un avertissement d'alimentation non-PD, qui peut être ignoré en toute sécurité.

15. **Connecteur de sortie d'alimentation 2x4P 2.54mm**

    - Sortie 5V supplémentaire pour les modules externes ou les SBC.

16. **Connecteur GPIO Raspberry Pi (connecteur femelle)**

    - Interface directe pour le Raspberry Pi, transmettant l'alimentation, l'I²C et d'autres signaux.
    - Entièrement compatible avec le brochage du Raspberry Pi.

17. **Connecteur GPIO Raspberry Pi (sortie sur broches mâles)**

    - Expose les broches GPIO du Raspberry Pi pour l'empilage de HAT ou l'extension externe.
    - **Remarque** : Les lignes I²C et la broche 26 sont déjà occupées par les fonctions du PiPower5.
    - Vous pouvez également connecter un câble d'extension GPIO (depuis le bas du panneau latéral) pour expérimenter sur une platine d'essai.

18. **Connecteur de batterie (XH2.54 3P)**

    - Interface de connexion de la batterie.
    - Ordre des broches (de gauche à droite) : Négatif, Point milieu (entre deux cellules), Positif.
    - Conçu pour les **batteries Li-ion/LiPo 7.4V (2 cellules)**.

19. **LED d'avertissement de batterie inversée**

    - Deux LED rouges s'allument si la batterie est connectée en polarité inversée, avertissant d'une installation incorrecte.

20. **Bornes à vis pour batterie et alimentation d'entrée**

    - Méthode de connexion alternative pour les batteries externes et les sources d'alimentation.
    - Prend en charge une **entrée externe 5V–15V** (recommandé : >9V).
    - Prise en charge batterie : **2 x 3.7V Li-ion / LiPo uniquement** (NON compatible avec les batteries LiFePO₄).


Tableau des spécifications
-----------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 20 20

   * - Paramètre
     - Minimum
     - Typique
     - Maximum
     - Unité
   * - Courant d'arrêt de la batterie
     - \-
     - 60
     - \-
     - µA
   * - Courant de repos de la batterie
     - \-
     - 25
     - \-
     - mA
   * - Tension de sortie DC-DC
     - 5,1957
     - 5,2855
     - 5,3766
     - V
   * - Protection contre la surchauffe DC-DC
     - \-
     - 150
     - \-
     - ℃
   * - Puissance de charge de la batterie
     - \-
     - \-
     - 20
     - W
   * - Protection contre la surchauffe de charge
     - \-
     - 125
     - \-
     - ℃
   * - Résistance d'équilibrage
     - \-
     - 60
     - \-
     - Ω
   * - Tension d'activation d'équilibrage
     - \-
     - 4,2
     - \-
     - V


.. _power_input:

Entrée d'alimentation
----------------------

.. image:: img/power_input.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

Lors de l'utilisation du Raspberry Pi 5, il est recommandé d'utiliser une alimentation USB PD ou une alimentation CC avec une sortie minimale de 32W. Sinon, pendant les périodes de forte consommation d'énergie, la batterie peut ne pas se charger correctement ou même épuiser sa charge en raison d'une alimentation insuffisante.

Vous pouvez surveiller l'indicateur **LED BAT** pour vérifier l'état de la batterie. Lorsque l'alimentation externe est suffisante, la LED BAT doit rester éteinte, indiquant que la batterie est en mode veille et ne se décharge pas. Si la LED BAT s'allume, cela signifie que la batterie alimente l'appareil, probablement en raison d'une alimentation externe insuffisante ou déconnectée. Une illumination prolongée de la LED BAT peut entraîner une décharge excessive de la batterie, l'empêchant de fonctionner comme une alimentation sans interruption (UPS) pendant les coupures de courant. Assurez-vous d'utiliser une source d'alimentation qui répond aux spécifications requises pour éviter de tels scénarios.




.. image:: img/bat_led.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>


**Chemin d'alimentation**

Le PiPower 5 intègre la gestion du chemin d'alimentation, permettant la commutation automatique de la source d'alimentation pour minimiser l'usure de la batterie et assurer une alimentation ininterrompue. Les fonctionnalités clés incluent :

- Lorsqu'une source d'alimentation externe est connectée, la sortie 5V est fournie via un circuit abaisseur à partir de la source externe. La sortie peut être désactivée à l'aide d'un interrupteur. Si les conditions le permettent, la source d'alimentation externe peut également charger la batterie simultanément (voir la section « Courant de charge » pour plus de détails).
- Lors de la déconnexion de la source d'alimentation externe, le système passe immédiatement à l'alimentation par batterie via un circuit abaisseur. Cette transition transparente garantit que le système continue de fonctionner normalement pendant les interruptions d'alimentation.

Vous pouvez vérifier l'indicateur LED BAT pour confirmer si la batterie alimente actuellement le système.




**Courant de charge**

Le courant de charge est soumis à deux types de limitations :

.. note::

   Le courant de charge est déterminé à la fois par la « Limitation de charge par alimentation via bornes à vis » et la « Limitation de sélection de puissance de charge » et est contraint par la plus petite valeur des deux.

1. Limitation de charge par alimentation via bornes à vis

   Lors de l'alimentation via l'entrée d'alimentation par bornes à vis, le courant de charge est automatiquement ajusté en fonction de la tension d'entrée, comme indiqué ci-dessous :

   .. list-table::
      :header-rows: 1

      * - Tension d'entrée (VBUS)
        - Courant de charge maximal
      * - 4,5 < VBUS ≤ 6,5V
        - 3A
      * - 6,5 < VBUS ≤ 9,5V
        - 2A
      * - 9,5 < VBUS ≤ 13,5V
        - 1,5A
      * - 13,5 < VBUS ≤ 16,5V
        - 2A

2. Limitation de sélection de puissance de charge

   Un commutateur DIP à 2 positions sur la carte permet la sélection de différents niveaux de puissance de charge. L'allocation correspondante de la puissance de charge et de la puissance de sortie pour chaque réglage est la suivante :

   .. image:: img/power_selector.png
     :width: 50%
     :align: center

   .. list-table::
      :header-rows: 1

      * - Charge Sel 1
        - Charge Sel 2
        - Puissance de charge
      * - 0
        - 0
        - 5W
      * - 1
        - 0
        - 10W
      * - 0
        - 1
        - 15W
      * - 1
        - 1
        - 20W


**Comment choisir la puissance de charge**

La formule est :

*Capacité d'alimentation = Puissance requise du Raspberry Pi + Puissance de charge*

Nous recommandons d'estimer la puissance requise du Raspberry Pi à **20W à 25W**.

- Si vous utilisez une **alimentation 30W**, réglez la puissance de charge sur **10W** ou **5W**.
- Si vous utilisez une **alimentation 45W**, vous pouvez régler en toute sécurité la puissance de charge sur **20W**.

Si vous connaissez bien les besoins en puissance de votre Raspberry Pi, vous pouvez définir une puissance de charge plus élevée tant que vous réservez une marge suffisante pour les pics de puissance occasionnels.

⚠️ Attention : une puissance insuffisante peut entraîner l'arrêt inattendu du Raspberry Pi.




**Processus de charge**

- Lorsque la tension de la batterie ``VBAT <= 2,5V``, le système effectue une charge d'entretien à faible courant, environ 50 mA.
- Lorsque ``2,5V < VBAT <= VTRKL``, la charge d'entretien se poursuit et le courant de charge de la batterie augmente à environ 200 mA.
- Lorsque ``VTRKL < VBAT < VCV``, le système passe en charge à courant constant, fournissant un courant constant prédéfini à la batterie.
- Une fois ``VBAT = VCV`` et que la tension de la batterie approche du niveau de charge complète, le courant de charge diminue progressivement, passant en charge à tension constante.
- Pendant la charge à tension constante, lorsque le courant de charge descend en dessous de ``ISTOP`` et que la tension de la batterie est proche du seuil de tension constante, la charge s'arrête et la batterie entre dans un état complètement chargé.
- Dans l'état complètement chargé, le système surveille en continu la tension de la batterie. Si la tension descend en dessous de ``VRCH``, la charge reprend automatiquement.

**Fonctionnalités de protection**

Le PiPower 5 offre des fonctionnalités de protection complètes, y compris la protection contre les sous-tensions et surtensions d'entrée, ainsi que la protection contre la surchauffe pour la puce de charge et le convertisseur DC-DC. Ces fonctionnalités assurent un fonctionnement stable et fiable du système.

**Équilibrage de charge**

La puce d'équilibrage de charge intégrée active une résistance de 60Ω pour décharger la batterie à faible courant lorsqu'elle détecte que la tension d'une cellule unique dépasse 4,2V. Cette fonctionnalité aide à maintenir l'équilibre de tension entre les cellules.

**Protection de température**

Le processus de charge est automatiquement interrompu lorsque la température interne de la puce de charge dépasse 125°C. De même, la puce DC-DC désactive la sortie lorsque sa température interne dépasse 150°C.

.. _power_button:

Bouton d'alimentation
-----------------------





.. image:: img/power_button.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

Bouton d'alimentation intégré pour contrôler l'alimentation de la carte :

* **Appui simple** : Active la sortie.
* **Maintenir pendant 2 secondes jusqu'à ce que les deux LED centrales de batterie s'allument, puis relâcher** : Envoie une demande d'arrêt via I2C.
* **Maintenir plus de 5 secondes** : Coupe directement la sortie.


.. _battery_indicators:

Indicateurs de batterie
--------------------------------

Quatre LED intégrées indiquent le niveau de la batterie et l'état de charge.

.. note::

   Si l'appareil est en charge pendant l'arrêt, le voyant indicateur continuera d'afficher l'état de charge jusqu'à ce que la charge soit terminée.




.. image:: img/battery_indicator.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

* **4 LED allumées** : Batterie > 80%
* **3 LED allumées** : 60% < Batterie < 80%
* **2 LED allumées** : 40% < Batterie < 60%
* **1 LED allumée** : 20% < Batterie < 40%
* **Première LED clignotante** : Batterie < 20%
* **Les LED s'allument séquentiellement en cycle** : Charge en cours
* **Deux LED centrales clignotantes** : En attente du signal d'arrêt
* **Toutes les LED éteintes** : Hors tension ou en mode veille

.. _battery_connector:

Connecteur de batterie
------------------------
Connecteur de batterie VH3.96 2P et connecteur de batterie à bornes à vis.

.. image:: img/battery_pin.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

.. _cap_btn:

Borne et connecteur pour bouton d'alimentation externe
-------------------------------------------------------

.. image:: img/btn_jumper.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

Cette borne ou ce connecteur est conçu pour connecter un bouton d'alimentation externe. Connectez un interrupteur momentané, tel qu'un bouton tactile ou un bouton métallique de style vintage, aux broches du cavalier. Les deux fils du bouton peuvent être connectés aux broches du cavalier dans n'importe quel sens, car la polarité n'est pas requise. Une fois connecté, vous pouvez utiliser le bouton externe comme le bouton d'alimentation intégré.

.. _cap_sdsig:

Cavalier SDSIG
----------------





.. image:: img/sdsig_jumper.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

Fournit la détection d'arrêt pour le Raspberry Pi.

* Lorsqu'il est relié à PI3V3, il fonctionne avec les Raspberry Pi 4 et Pi 5.
* Lorsqu'il est court-circuité à la broche 26, il prend en charge les Pi 3 et Pi Zero.

Après une configuration appropriée, le PiPower5 coupera automatiquement l'alimentation une fois le Raspberry Pi arrêté.

.. _cap_onoff:

Cavalier Default ON/OFF
-------------------------





.. image:: img/default_jumper.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

Ce cavalier est utilisé pour sélectionner si la sortie d'alimentation USB est activée par défaut après un arrêt. Utilisez le capuchon de cavalier pour connecter les broches étiquetées ON ou OFF pour faire la sélection.

* Si le capuchon de cavalier est positionné à gauche et connecté à OFF, l'insertion de l'alimentation USB après un arrêt n'activera pas la sortie.
* Si le capuchon de cavalier est positionné à droite et connecté à ON, l'insertion de l'alimentation USB après un arrêt activera la sortie.

Cette fonctionnalité est généralement utilisée pour les appareils qui doivent démarrer automatiquement, tels que les serveurs personnels. Par exemple, en cas de panne de courant, le PiPower 5 prendra le relais de l'alimentation du Raspberry Pi, assurant un arrêt sécurisé. Une fois l'alimentation rétablie, le PiPower 5 allume automatiquement le Raspberry Pi, éliminant le besoin d'intervention manuelle.

.. _pin_header:

Connecteurs à broches pour RPi
-------------------------------

Le connecteur à broches est conçu pour une connexion directe à un Raspberry Pi, incluant à la fois la communication I2C et l'alimentation électrique.




.. image:: img/pin_header.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

Le connecteur prend en charge l'empilage de HAT supplémentaires. Cependant, notez que les broches I2C et la broche 26 sont déjà connectées et peuvent nécessiter une gestion attentive pour éviter les conflits.

.. list-table::
   :widths: 15 15
   :header-rows: 1

   * - Raspberry Pi
     - MCU intégré
   * - SDA
     - SDA
   * - SCL
     - SCL
   * - GPIO26
     - SHUTDOWN
   * - ID_SD
     - ID_EEPROM SDA
   * - ID_SC
     - ID_EEPROM SCL

Communication I2C
-------------------------------






.. image:: img/i2c.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

Adresse I2C : 0x5C

Le microcontrôleur intégré collecte divers signaux de la carte et les stocke dans des registres. Ces signaux sont accessibles via I2C en utilisant les tables de registres suivantes.

.. raw:: html

   <style>
       .custom-register-table {
           border-collapse: collapse;
           width: 100%;
           margin: 20px 0;
           font-size: 14px;
           text-align: left;
       }
       .custom-register-table th, .custom-register-table td {
           border: 1px solid #ddd;
           padding: 8px;
       }
       .custom-register-table th {
           background-color: #f4f4f4;
           font-weight: bold;
       }
       .custom-register-table tr:nth-child(even) {
           background-color: #f9f9f9;
       }
       .custom-register-table tr:hover {
           background-color: #f1f1f1;
       }
       .custom-register-table caption {
           font-size: 16px;
           font-weight: bold;
           margin-bottom: 10px;
           text-align: center;
       }
   </style>

   <table class="custom-register-table">
       <caption>Table des registres</caption>
       <thead>
           <tr>
               <th>Nom</th>
               <th>Adresse</th>
               <th>Longueur des données</th>
               <th>Type de données</th>
               <th>Unité</th>
               <th>Description</th>
           </tr>
       </thead>
       <tbody>
           <tr>
               <td>Tension d'entrée</td>
               <td>0</td>
               <td>2</td>
               <td>u16</td>
               <td>mV</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Courant d'entrée</td>
               <td>2</td>
               <td>2</td>
               <td>u16</td>
               <td>mA</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Tension de sortie</td>
               <td>4</td>
               <td>2</td>
               <td>u16</td>
               <td>mV</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Courant de sortie</td>
               <td>6</td>
               <td>2</td>
               <td>u16</td>
               <td>mA</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Tension de la batterie</td>
               <td>8</td>
               <td>2</td>
               <td>u16</td>
               <td>mV</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Courant de la batterie</td>
               <td>10</td>
               <td>2</td>
               <td>i16</td>
               <td>mA</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Pourcentage de la batterie</td>
               <td>12</td>
               <td>1</td>
               <td>u8</td>
               <td>%</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Capacité de la batterie</td>
               <td>13</td>
               <td>2</td>
               <td>u16</td>
               <td>mAh</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Source d'alimentation</td>
               <td>15</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>0 : La batterie ne fournit pas d'alimentation.<br> 1 : La batterie fournit l'alimentation.</td>
           </tr>
           <tr>
               <td>État de connexion USB</td>
               <td>16</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>0 : USB débranché.<br> 1 : USB branché.</td>
           </tr>
           <tr>
               <td>RÉSERVÉ</td>
               <td>17</td>
               <td>1</td>
               <td>-</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>État de charge</td>
               <td>18</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>0 : Pas en charge.<br> 1 : En charge.</td>
           </tr>
           <tr>
               <td>Puissance du ventilateur</td>
               <td>19</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Niveau de puissance du ventilateur (0–100).</td>
           </tr>
           <tr>
               <td>Demande d'arrêt</td>
               <td>20</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>1 : Déclenché par batterie faible.<br>2 : Déclenché par l'appui sur le bouton d'alimentation.</td>
           </tr>
           <tr>
               <td>Version du firmware (Majeure)</td>
               <td>128</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Version du firmware (Mineure)</td>
               <td>129</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Version du firmware (Correctif)</td>
               <td>130</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Code de réinitialisation</td>
               <td>131</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Code de raison de réinitialisation du MCU.</td>
           </tr>
           <tr>
               <td>RTC Année</td>
               <td>132</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RTC Mois</td>
               <td>133</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RTC Jour</td>
               <td>134</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RTC Heure</td>
               <td>135</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RTC Minute</td>
               <td>136</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RTC Seconde</td>
               <td>137</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RTC Sous-seconde</td>
               <td>138</td>
               <td>1</td>
               <td>u8</td>
               <td>1/128 s</td>
               <td>Sous-seconde RTC (1/128 seconde).</td>
           </tr>
           <tr>
               <td>Fonction Always-On</td>
               <td>139</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>0 : Activé.<br> 1 : Désactivé.</td>
           </tr>
           <tr>
               <td>ID de la carte</td>
               <td>140</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Identification de la carte : <br> 0 : Pironman U1.<br> 1 : Pironman 4.<br> 2 : PiPower 3.<br>4 : PiPower 5.</td>
           </tr>
           <tr>
               <td>RÉSERVÉ</td>
               <td>141</td>
               <td>1</td>
               <td>-</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RÉSERVÉ</td>
               <td>142</td>
               <td>1</td>
               <td>-</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>Pourcentage d'arrêt</td>
               <td>143</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Seuil actuel de pourcentage de batterie pour l'arrêt.</td>
           </tr>
           <tr>
               <td>RÉSERVÉ</td>
               <td>144</td>
               <td>1</td>
               <td>-</td>
               <td>-</td>
               <td>-</td>
           </tr>
       </tbody>
   </table>


   <table class="custom-register-table">
       <caption>Table des paramètres des registres</caption>
       <thead>
           <tr>
               <th>Nom</th>
               <th>Adresse</th>
               <th>Longueur des données</th>
               <th>Type de données</th>
               <th>Unité</th>
               <th>Description</th>
           </tr>
       </thead>
       <tbody>
           <tr>
               <td>Puissance du ventilateur</td>
               <td>0</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Définir la vitesse du ventilateur (0–100).</td>
           </tr>
           <tr>
               <td>RTC Année</td>
               <td>1</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Définir l'année RTC.</td>
           </tr>
           <tr>
               <td>RTC Mois</td>
               <td>2</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Définir le mois RTC.</td>
           </tr>
           <tr>
               <td>RTC Jour</td>
               <td>3</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Définir le jour RTC.</td>
           </tr>
           <tr>
               <td>RTC Heure</td>
               <td>4</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Définir l'heure RTC.</td>
           </tr>
           <tr>
               <td>RTC Minute</td>
               <td>5</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Définir la minute RTC.</td>
           </tr>
           <tr>
               <td>RTC Seconde</td>
               <td>6</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Définir la seconde RTC.</td>
           </tr>
           <tr>
               <td>RTC Sous-seconde</td>
               <td>7</td>
               <td>1</td>
               <td>u8</td>
               <td>1/128 s</td>
               <td>Définir la sous-seconde RTC.</td>
           </tr>
           <tr>
               <td>Paramètre RTC</td>
               <td>8</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Activer le paramètre RTC : <br> 1 : Activé.</td>
           </tr>
           <tr>
               <td>Pourcentage d'arrêt</td>
               <td>9</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Définir le seuil de pourcentage de batterie pour l'arrêt (0–100).</td>
           </tr>
           <tr>
               <td>Pourcentage de mise hors tension</td>
               <td>10</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>Définir le seuil de pourcentage de batterie pour la mise hors tension (0–100).</td>
           </tr>
       </tbody>
   </table>

