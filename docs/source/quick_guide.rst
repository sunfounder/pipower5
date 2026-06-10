クイックユーザーガイド
===============================

このガイドは、ハードウェア組み立て後の PiPower 5 のクイックスタートを支援します。

バッテリーの充電
----------------------------------------------------

初めて使用する前に、バッテリーを完全に充電してください。

推奨事項:

- 高品質の USB-C 電源アダプターを使用してください
- Raspberry Pi 5 には 5V 5A 電源を推奨します
- SSD やその他の高電力周辺機器を使用する場合は、より高出力のアダプターを推奨します

充電中:

- 高品質の USB-C 電源を使用して PiPower 5 を充電してください。

  .. image:: img/power_input.png
     :width: 50%
     :align: center

- 充電中、バッテリーインジケーター LED が順次点灯します。

  .. image:: img/battery_indicator.png
     :width: 50%
     :align: center

  点灯しているLEDの数でバッテリー状態がわかります:

  * **4 LED 点灯**: バッテリー >80%
  * **3 LED 点灯**: 60%< バッテリー <80%
  * **2 LED 点灯**: 40%< バッテリー <60%
  * **1 LED 点灯**: 20%< バッテリー <40%
  * **最初のLEDが点滅**: バッテリー <20%
  * **LEDがサイクルで順次点灯**: 充電中
  * **中央の2つのLEDが点滅**: シャットダウン信号待ち
  * **全LED消灯**: 電源未供給またはスリープモード
  * 充電中は、満充電になるまで**オフの状態でも**インジケーターが点灯したままです。

電源オン
----------------------------------------------------

Raspberry Pi デバイスの場合、追加の電源配線は不要です。PiPower 5 は GPIO ヘッダーを通じて直接電力を供給します。

その他のデバイスには、以下を使用して給電できます:

- USB-A 出力ポート
- USB-A ポート横の 5V/GND ピン

.. image:: img/power_output.png
   :width: 50%
   :align: center

電源ボタンを1回押して PiPower 5 をオンにします。電源が入ると:

- **PWR LED** が点灯します
- 接続されたデバイスが PiPower 5 から電力を受け取り始めます

.. image:: img/pwr_led.png
   :width: 50%
   :align: center

.. include:: /pipower5_software.rst
    :start-after: start_install_pipower5
    :end-before: end_install_pipower5

Web ダッシュボードを開く
----------------------------------------------------

インストール後、ブラウザでダッシュボードを開きます:

.. code-block:: text

   http://<raspberry-pi-ip>:34001

ダッシュボードで以下が可能です:

- バッテリー残量の表示
- 充電状態の監視
- 電圧と電流の確認
- シャットダウン残量の設定
- 通知の管理

.. image:: img/web_dashboard.png
   :width: 100%
   :align: center


安全なシャットダウン
----------------------------------------------------

.. include:: /pipower5_software.rst
    :start-after: start_power_off_after_shutdown
    :end-before: end_power_off_after_shutdown

.. note::

   以下のような高度な機能と詳細な設定オプションについては:

   - 電力監視コマンド
   - 通知設定
   - ブザーアラート
   - メールアラート
   - 高度な設定

   以下を参照してください:

   * :ref:`pipower5_tool`
