PiPower 5 HAT
======================

.. interface:

インターフェース概要
--------------------

.. image:: img/pipower5_ov.png
  :width: 100%



1. **USB Type-C 電源入力**

   - Raspberry Piへの給電とバッテリー充電を同時に行う外部電源入力です。
   - **USB Power Delivery (PD) プロトコル**に対応、入力範囲 **5V～15V**。

2. **電源入力セレクター (DIPスイッチ)**

   - 柔軟な設定のために異なる入力電力プロファイルを選択できます。

3. **デフォルトONジャンパー**

   - デバイスがシャットダウン状態のときに外部電源が接続された場合、システムを自動起動するかどうかを定義します。
   - ON = 自動電源投入有効、OFF = 手動起動が必要。

4. **SDSIG (シャットダウン信号)**

   - Raspberry Piのシャットダウン検出を提供します。
   - **PI3V3**\ にブリッジすると、Raspberry Pi 4およびPi 5で動作します。
   - **ピン26**\ に短絡すると、Pi 3およびPi Zeroをサポートします。
   - 適切に設定すると、Raspberry Piのシャットダウン完了後にPiPower5が自動的に電源を切断します。

5. **PWR LED (出力状態インジケーター)**

   - システム出力がアクティブなときに点灯します。

6. **BAT LED (バッテリー状態インジケーター)**

   - システムがバッテリーで駆動しているときに点灯します。
   - 外部電源なしで動作している場合のバッテリー消費の監視を促します。

7. **電源ボタン**

   - **シングルプレス**: 出力電源を有効にします。
   - **長押し (2秒)**: I²C経由で安全なシャットダウン要求を送信します。
   - **長押し (5秒)**: 即時電源オフを強制します (ハードシャットダウン)。
   - **カスタマイズ可能**: シングルおよびダブルプレスの動作はソフトウェアで再設定できます。

8. **外部電源ボタン端子 (ZH1.5 2P)**

   - 外部の物理電源ボタンの接続を可能にします。

9. **外部電源ボタンヘッダー (2.54mm)**

   - 外部電源ボタン接続用の代替はんだ付けヘッダーオプションです。

10. **バッテリーインジケーターLED**

    - 残りのバッテリー容量と充電状態を表示します。
    - 注意: システムがオフの状態でも、バッテリーが満充電になるまで充電中はLEDがアクティブのままです。

11. **I²Cインターフェース (SH1.0 4P)**

    - **Qwiic**\ および\ **STEMMA QT**\ エコシステムと互換性があります。
    - 内蔵マイクロコントローラーおよび外部周辺機器との通信に使用されます。

12. **I²Cインターフェース (1x4P 2.54mm ヘッダー)**

    - 常時オンまたはスイッチドとして設定可能な**3V3電源出力**付きの代替I²Cブレイクアウトです。

13. **I²C電源選択ジャンパー**

    - **PERM**: 外部電源接続時に3V3電源が常時オンになります。
    - **SHUT (デフォルト)**: システムシャットダウン時に3V3電源が自動的に切断されます。

14. **USB Type-A 出力ポート**

    - **安定化5V出力**\ を提供し、周辺機器や他のデバイスへの給電に適しています。
    - Raspberry Piに給電する場合、非PD電源警告が表示されることがありますが、安全に無視できます。

15. **2x4P 2.54mm 電源出力ヘッダー**

    - 外部モジュールやSBC用の追加5V出力です。

16. **Raspberry Pi GPIOヘッダー (メスコネクタ)**

    - Raspberry Piとの直接インターフェースで、電源、I²C、その他の信号を通過させます。
    - Raspberry Piのピン配置と完全に互換性があります。

17. **Raspberry Pi GPIOヘッダー (オスピンブレイクアウト)**

    - Raspberry PiのGPIOピンをHATのスタックや外部拡張用に引き出します。
    - **注意**: I²Cラインとピン26は既にPiPower5の機能で使用されています。
    - サイドパネルの下部からGPIO延長ケーブルを接続してブレッドボードで実験することもできます。

18. **バッテリーコネクタ (XH2.54 3P)**

    - バッテリー接続インターフェースです。
    - ピン配置 (左から右): マイナス、中間点 (2セル間)、プラス。
    - **7.4V (2セル) Li-ion/LiPoバッテリー**\ 用に設計されています。

19. **逆接続警告LED**

    - バッテリーが逆極性で接続された場合、2つの赤色LEDが点灯し、誤った取り付けを警告します。

20. **バッテリー・入力電源用スクリュー端子**

    - 外部バッテリーおよび電源用の代替接続方法です。
    - **5V～15Vの外部入力**\ に対応 (推奨: >9V)。
    - バッテリー対応: **2 x 3.7V Li-ion / LiPoセルのみ**\  (LiFePO₄バッテリーには非対応)。


仕様表
------

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 20 20

   * - パラメーター
     - 最小
     - 標準
     - 最大
     - 単位
   * - バッテリーシャットダウン電流
     - \-
     - 60
     - \-
     - µA
   * - バッテリー静止電流
     - \-
     - 25
     - \-
     - mA
   * - DC-DC出力電圧
     - 5.1957
     - 5.2855
     - 5.3766
     - V
   * - DC-DC過熱保護
     - \-
     - 150
     - \-
     - ℃
   * - バッテリー充電電力
     - \-
     - \-
     - 20
     - W
   * - 充電過熱保護
     - \-
     - 125
     - \-
     - ℃
   * - バランス抵抗
     - \-
     - 60
     - \-
     - Ω
   * - バランス開始電圧
     - \-
     - 4.2
     - \-
     - V


.. _power_input:

電源入力
--------

.. image:: img/power_input.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

Raspberry Pi 5を使用する場合、最小出力32WのUSB PD電源またはDC電源の使用を推奨します。そうしないと、高電力消費時にバッテリーが適切に充電されなかったり、電力不足で放電してしまう可能性があります。

**BAT LED**\ インジケーターでバッテリー状態を監視できます。外部電源が十分な場合、BAT LEDは消灯したままで、バッテリーがスタンバイモードで放電していないことを示します。BAT LEDが点灯した場合、バッテリーがデバイスに電力を供給していることを意味し、外部電源の不足または切断が考えられます。BAT LEDの長時間の点灯はバッテリーの過放電を招き、停電時の無停電電源装置 (UPS) としての機能を果たせなくなる可能性があります。このような状況を避けるために、必要な仕様を満たす電源を使用してください。




.. image:: img/bat_led.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>


**電源パス**

PiPower 5は電源パス管理を統合し、バッテリーの消耗を最小限に抑え、無停電電源供給を確保するための自動電源切り替えを可能にします。主な機能は次のとおりです:

- 外部電源接続時、5V出力は外部電源からの降圧回路を通じて供給されます。出力はスイッチでオフにできます。条件が許せば、外部電源はバッテリーを同時に充電することもできます (詳細は「充電電流」セクションを参照)。
- 外部電源の切断時、システムは直ちに降圧回路を通じてバッテリー電源に切り替わります。このシームレスな移行により、電源遮断時もシステムが正常に動作し続けます。

BAT LEDインジケーターでバッテリーが現在システムに電力を供給しているかどうかを確認できます。




**充電電流**

充電電流には2種類の制限があります:

.. note::

   充電電流は「スクリュー端子電源充電制限」と「充電電力選択制限」の両方によって決定され、2つのうち小さい方の値に制約されます。

1. スクリュー端子電源充電制限

   スクリュー端子電源入力から給電する場合、充電電流は入力電圧に基づいて自動的に調整されます:

   .. list-table::
      :header-rows: 1

      * - 入力電圧 (VBUS)
        - 最大充電電流
      * - 4.5 < VBUS ≤ 6.5V
        - 3A
      * - 6.5 < VBUS ≤ 9.5V
        - 2A
      * - 9.5 < VBUS ≤ 13.5V
        - 1.5A
      * - 13.5 < VBUS ≤ 16.5V
        - 2A

2. 充電電力選択制限

   基板上の2ポジションDIPスイッチで異なる充電電力レベルを選択できます。各設定の充電電力と出力電力の割り当ては以下の通りです:

   .. image:: img/power_selector.png
     :width: 50%
     :align: center

   .. list-table::
      :header-rows: 1

      * - 充電選択 1
        - 充電選択 2
        - 充電電力
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


**充電電力の選び方**

計算式:

*電源容量 = Raspberry Pi必要電力 + 充電電力*

Raspberry Piの電力要件を**20W～25W**と見積もることを推奨します。

- **30W電源**\ を使用する場合、充電電力を\ **10W**\ または\ **5W**\ に設定してください。
- **45W電源**\ を使用する場合、充電電力を安全に\ **20W**\ に設定できます。

Raspberry Piの電力ニーズに詳しい場合、時折の電力スパイクに十分な余裕を残す限り、より高い充電電力を設定できます。

⚠️ 注意: 電力不足はRaspberry Piの予期しないシャットダウンを引き起こす可能性があります。




**充電プロセス**

- バッテリー電圧が ``VBAT <= 2.5V`` の場合、システムは約50 mAの低電流でトリクル充電を行います。
- ``2.5V < VBAT <= VTRKL`` の場合、トリクル充電が継続され、バッテリー充電電流は約200 mAに増加します。
- ``VTRKL < VBAT < VCV`` の場合、システムは定電流充電に切り替わり、プリセットされた定電流をバッテリーに供給します。
- ``VBAT = VCV`` に達し、バッテリー電圧が満充電レベルに近づくと、充電電流は徐々に減少し、定電圧充電に移行します。
- 定電圧充電中、充電電流が ``ISTOP`` を下回り、バッテリー電圧が定電圧閾値付近になると充電が停止し、バッテリーは満充電状態になります。
- 満充電状態では、システムはバッテリー電圧を継続的に監視します。電圧が ``VRCH`` を下回ると、充電が自動的に再開されます。

**保護機能**

PiPower 5は、入力不足電圧および過電圧保護、充電チップとDC-DCコンバーターの過熱保護など、包括的な保護機能を提供します。これらの機能により、安定した信頼性の高いシステム動作が保証されます。

**充電バランシング**

内蔵充電バランシングチップは、単一セルの電圧が4.2Vを超えたことを検出すると、60Ωの抵抗器を作動させてバッテリーを低電流で放電します。この機能はセル間の電圧バランスを維持するのに役立ちます。

**温度保護**

充電チップの内部温度が125°Cを超えると、充電プロセスが自動的に停止されます。同様に、DC-DCチップは内部温度が150°Cを超えると出力を無効にします。

.. _power_button:

電源ボタン
----------

.. image:: img/power_button.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

基板の電源を制御するための内蔵電源ボタン:

* **シングルプレス**: 出力を有効にします。
* **中央のバッテリーLED 2つが点灯するまで2秒間長押ししてから放す**: I2C経由でシャットダウン要求を送信します。
* **5秒以上の長押し**: 出力を直接オフにします。


.. _battery_indicators:

バッテリーインジケーター
------------------------

4つの内蔵LEDがバッテリーレベルと充電状態を表示します。

.. note::

   シャットダウン中に充電中の場合、充電が完了するまでインジケーターライトが充電状態を表示し続けます。




.. image:: img/battery_indicator.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

* **4 LED点灯**: バッテリー >80%
* **3 LED点灯**: 60%< バッテリー <80%
* **2 LED点灯**: 40%< バッテリー <60%
* **1 LED点灯**: 20%< バッテリー <40%
* **最初のLEDが点滅**: バッテリー <20%
* **LEDが順番にサイクル点灯**: 充電中
* **中央の2つのLEDが点滅**: シャットダウン信号待ち
* **全LED消灯**: 電源未供給またはスリープモード

.. _battery_connector:

バッテリーコネクタ
------------------
VH3.96 2Pバッテリーコネクタとスクリュー端子バッテリーコネクタ。

.. image:: img/battery_pin.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

.. _cap_btn:

外部電源ボタン端子 & ヘッダー
-----------------------------

.. image:: img/btn_jumper.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

この端子またはヘッダーは、外部電源ボタンを接続するために設計されています。タクタイルスイッチやビンテージスタイルのメタルボタンなどのモーメンタリスイッチをジャンパーピンに接続してください。極性は不要なため、ボタンの2本のリード線はどちらの方向でもジャンパーピンに接続できます。接続後、内蔵電源ボタンと同様に外部ボタンを使用できます。

.. _cap_sdsig:

SDSIGジャンパー
---------------

.. image:: img/sdsig_jumper.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

Raspberry Piのシャットダウン検出を提供します。

* PI3V3にブリッジすると、Raspberry Pi 4およびPi 5で動作します。
* ピン26に短絡すると、Pi 3およびPi Zeroをサポートします。

適切に設定すると、Raspberry Piのシャットダウン完了後にPiPower5が自動的に電源を切断します。

.. _cap_onoff:

デフォルトON/OFFジャンパー
--------------------------

.. image:: img/default_jumper.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

このジャンパーは、シャットダウン後にUSB電源出力をデフォルトで有効にするかどうかを選択するために使用します。ジャンパーキャップを使用して、ONまたはOFFと表示されたピンを接続して選択してください。

* ジャンパーキャップが左側のOFFに接続されている場合、シャットダウン後にUSB電源を挿入しても出力は有効になりません。
* ジャンパーキャップが右側のONに接続されている場合、シャットダウン後にUSB電源を挿入すると出力が有効になります。

この機能は通常、パーソナルサーバーなど自動起動が必要なデバイスに使用されます。たとえば停電が発生した場合、PiPower 5がRaspberry Piの電源を引き継ぎ、安全なシャットダウンを保証します。電源が復旧すると、PiPower 5が自動的にRaspberry Piを起動するため、手動介入が不要になります。

.. _pin_header:

Raspberry Pi用ピンヘッダー
--------------------------

ピンヘッダーは、I2C通信と電源供給を含むRaspberry Piへの直接接続用に設計されています。




.. image:: img/pin_header.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

このヘッダーは追加HATのスタックをサポートします。ただし、I2Cピンとピン26は既に接続されているため、競合を避けるために注意深く管理する必要がある場合があります。

.. list-table::
   :widths: 15 15
   :header-rows: 1

   * - Raspberry Pi
     - 基板上MCU
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

I2C通信
-------

.. image:: img/i2c.png
  :width: 50%
  :align: center

.. raw:: html

   <br/>

I2Cアドレス: 0x5C

内蔵マイクロコントローラーは基板からさまざまな信号を収集し、レジスターに保存します。これらの信号は以下のレジスターテーブルを使用してI2C経由でアクセスできます。

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
       <caption>レジスターテーブル</caption>
       <thead>
           <tr>
               <th>名前</th>
               <th>アドレス</th>
               <th>データ長</th>
               <th>データ型</th>
               <th>単位</th>
               <th>説明</th>
           </tr>
       </thead>
       <tbody>
           <tr>
               <td>入力電圧</td>
               <td>0</td>
               <td>2</td>
               <td>u16</td>
               <td>mV</td>
               <td>-</td>
           </tr>
           <tr>
               <td>入力電流</td>
               <td>2</td>
               <td>2</td>
               <td>u16</td>
               <td>mA</td>
               <td>-</td>
           </tr>
           <tr>
               <td>出力電圧</td>
               <td>4</td>
               <td>2</td>
               <td>u16</td>
               <td>mV</td>
               <td>-</td>
           </tr>
           <tr>
               <td>出力電流</td>
               <td>6</td>
               <td>2</td>
               <td>u16</td>
               <td>mA</td>
               <td>-</td>
           </tr>
           <tr>
               <td>バッテリー電圧</td>
               <td>8</td>
               <td>2</td>
               <td>u16</td>
               <td>mV</td>
               <td>-</td>
           </tr>
           <tr>
               <td>バッテリー電流</td>
               <td>10</td>
               <td>2</td>
               <td>i16</td>
               <td>mA</td>
               <td>-</td>
           </tr>
           <tr>
               <td>バッテリー残量</td>
               <td>12</td>
               <td>1</td>
               <td>u8</td>
               <td>%</td>
               <td>-</td>
           </tr>
           <tr>
               <td>バッテリー容量</td>
               <td>13</td>
               <td>2</td>
               <td>u16</td>
               <td>mAh</td>
               <td>-</td>
           </tr>
           <tr>
               <td>電源ソース</td>
               <td>15</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>0: バッテリー給電なし。<br> 1: バッテリー給電中。</td>
           </tr>
           <tr>
               <td>USB接続状態</td>
               <td>16</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>0: USB未接続。<br> 1: USB接続中。</td>
           </tr>
           <tr>
               <td>予約済み</td>
               <td>17</td>
               <td>1</td>
               <td>-</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>充電状態</td>
               <td>18</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>0: 充電していません。<br> 1: 充電中。</td>
           </tr>
           <tr>
               <td>ファン電力</td>
               <td>19</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>ファン電力レベル (0～100)。</td>
           </tr>
           <tr>
               <td>シャットダウン要求</td>
               <td>20</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>1: バッテリー低下によりトリガー。<br>2: 電源ボタン押下によりトリガー。</td>
           </tr>
           <tr>
               <td>ファームウェアバージョン (メジャー)</td>
               <td>128</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>ファームウェアバージョン (マイナー)</td>
               <td>129</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>ファームウェアバージョン (パッチ)</td>
               <td>130</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>リセットコード</td>
               <td>131</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>MCUリセット原因コード。</td>
           </tr>
           <tr>
               <td>RTC 年</td>
               <td>132</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RTC 月</td>
               <td>133</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RTC 日</td>
               <td>134</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RTC 時</td>
               <td>135</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RTC 分</td>
               <td>136</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RTC 秒</td>
               <td>137</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>RTC サブ秒</td>
               <td>138</td>
               <td>1</td>
               <td>u8</td>
               <td>1/128 s</td>
               <td>RTCサブ秒 (1/128秒)。</td>
           </tr>
           <tr>
               <td>常時オン機能</td>
               <td>139</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>0: 有効。<br> 1: 無効。</td>
           </tr>
           <tr>
               <td>ボードID</td>
               <td>140</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>ボード識別: <br> 0: Pironman U1.<br> 1: Pironman 4.<br> 2: PiPower 3.<br>4: PiPower 5.</td>
           </tr>
           <tr>
               <td>予約済み</td>
               <td>141</td>
               <td>1</td>
               <td>-</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>予約済み</td>
               <td>142</td>
               <td>1</td>
               <td>-</td>
               <td>-</td>
               <td>-</td>
           </tr>
           <tr>
               <td>シャットダウン残量</td>
               <td>143</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>現在の低バッテリーシャットダウン残量閾値。</td>
           </tr>
           <tr>
               <td>予約済み</td>
               <td>144</td>
               <td>1</td>
               <td>-</td>
               <td>-</td>
               <td>-</td>
           </tr>
       </tbody>
   </table>


   <table class="custom-register-table">
       <caption>レジスター設定テーブル</caption>
       <thead>
           <tr>
               <th>名前</th>
               <th>アドレス</th>
               <th>データ長</th>
               <th>データ型</th>
               <th>単位</th>
               <th>説明</th>
           </tr>
       </thead>
       <tbody>
           <tr>
               <td>ファン電力</td>
               <td>0</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>ファン速度を設定 (0～100)。</td>
           </tr>
           <tr>
               <td>RTC 年</td>
               <td>1</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>RTC年を設定。</td>
           </tr>
           <tr>
               <td>RTC 月</td>
               <td>2</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>RTC月を設定。</td>
           </tr>
           <tr>
               <td>RTC 日</td>
               <td>3</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>RTC日を設定。</td>
           </tr>
           <tr>
               <td>RTC 時</td>
               <td>4</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>RTC時を設定。</td>
           </tr>
           <tr>
               <td>RTC 分</td>
               <td>5</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>RTC分を設定。</td>
           </tr>
           <tr>
               <td>RTC 秒</td>
               <td>6</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>RTC秒を設定。</td>
           </tr>
           <tr>
               <td>RTC サブ秒</td>
               <td>7</td>
               <td>1</td>
               <td>u8</td>
               <td>1/128 s</td>
               <td>RTCサブ秒を設定。</td>
           </tr>
           <tr>
               <td>RTC設定</td>
               <td>8</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>RTC設定を有効化: <br> 1: 有効。</td>
           </tr>
           <tr>
               <td>シャットダウン残量</td>
               <td>9</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>低バッテリーシャットダウン残量閾値を設定 (0～100)。</td>
           </tr>
           <tr>
               <td>電源オフ残量</td>
               <td>10</td>
               <td>1</td>
               <td>u8</td>
               <td>-</td>
               <td>低バッテリー電源オフ残量閾値を設定 (0～100)。</td>
           </tr>
       </tbody>
   </table>
