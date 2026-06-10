Arduino
===================================

PiPower 5 を使用して Arduino ボードに給電する場合、Arduino を PiPower 5 の Type A 出力ポートに接続するか、2 本のジャンパーワイヤーを使用できます。ボードの I2C インターフェースをジャンパーで接続してください。

.. If no operation is required before powering off, directly connect the **SDSIG** jumper cap to the GND. If operations are necessary before shutdown, remove the jumper cap and connect the intermediate wire to an IO port on the Arduino to notify PiPower 5 that it can safely power off.

入力電圧、出力電圧、バッテリー電圧と残量、電源ソース、充電状態、その他の内部データを監視できるライブラリを提供しています。

#. Arduino IDE で**ライブラリマネージャー**を開き、``SunFounderPowerControl`` を検索してダウンロード・インストールします。

   .. image:: img/install_arduino_lib.png
      :width: 100%

#. インストール後、**ファイル** → **スケッチ例** → **SunFounderPowerControl** → **PiPower 5** に移動すると、4 つのサンプルが見つかります。

   .. image:: img/arduino_lib_example.png
      :width: 100%

   * ``read_all``: すべてのデータを一度に読み取り、個別に処理する必要がある場合に使用します。
   * ``read_individual``: 特定のデータのみを読み取る必要がある場合、このサンプルは個別のデータ取得手順を提供します。
   * ``set_shutdown_percentage``: シャットダウンバッテリー残量の設定方法を示します。この機能は、バッテリーが充電中でなく、設定された残量を下回った場合にホストにシャットダウン信号を送信します。ホストのシャットダウン後、電源オフ信号を受信した後にのみ電源が切れます。通常は Raspberry Pi などの SBC で使用します。マイクロコントローラーの場合は、**SDSIG** ジャンパーキャップを取り外し、中間ワイヤーをピンに接続します。シャットダウン信号を受信して安全にシャットダウンした後、このピンを High にすることで PiPower 5 の電源を切ります。
   * ``shutdown_when_request``: シャットダウン信号受信後の操作処理方法を示します。**SDSIG** ジャンパーキャップを取り外し、中間ワイヤーをピンに接続します。

#. サンプルのいずれかを選択してボードにアップロードします。

   .. note::

      I2C が変更可能な一部のボードでは、I2C ピンを変更する必要がある場合、コード ``Wire.begin()`` を変更する必要があります。

Arduino ライブラリ API ドキュメント: https://github.com/sunfounder/arduino_spc?tab=readme-ov-file#api
