MicroPython
==========================================================

入力電圧、出力電圧、バッテリー電圧と残量、電源ソース、充電状態、その他の内部データを監視できるライブラリを提供しています。

PiPower 5 を使用して Raspberry Pi Pico または ESP32 ボードに給電する場合、Type-A 出力ポートまたは 2 本のジャンパーワイヤーを介してボードを PiPower 5 に接続できます。

PiPower 5 の I2C インターフェースに接続するには、ジャンパーを使用してください。

.. If no operations are needed before shutting down, connect the SDSIG jumper cap directly to the GND pin. If operations are required before shutdown, remove the jumper cap and connect the intermediate wire to an I/O pin on the Raspberry Pi Pico or ESP32 board. This setup notifies the PiPower 5 that the shutdown process is complete and it can safely power off.

#. GitHub からライブラリをダウンロードします。以下のリンクからすぐにダウンロードするか、https://github.com/sunfounder/micropython_spc にアクセスしてください。

   * :download:`micropython_spc <https://github.com/sunfounder/micropython_spc/archive/refs/heads/main.zip>`

#. ダウンロードして解凍した後、``spc`` フォルダーを Raspberry Pi Pico または ESP32 ボードにアップロードします。この目的には Thonny の使用を推奨します。

   .. image:: img/micropython_upload.png
       :width: 100%
       :align: center

   .. raw:: html

      <br/>

#. ライブラリをアップロードしたら、``micropython_spc-main/examples/pipower5`` フォルダーにあるサンプルを使用してテストできます:

   * ``pipower_5_read_all.py``: すべてのデータを読み取る必要がある場合にこのサンプルを使用します。利用可能なすべてのデータを一度に読み取り、個別に処理する方法を示します。

   * ``pipower_5_read_individual.py``: このサンプルは特定のデータを個別に読み取る手順を提供します。特定のデータにのみアクセスする必要がある場合に使用します。

   * ``pipower_5_set_shutdown_percentage.py``: このサンプルはシャットダウンバッテリー残量の設定方法を説明します。バッテリーが充電中でなく、そのレベルが指定された残量を下回ると、PiPower 5 はホストにシャットダウン信号を送信します。ホストがシャットダウンを完了し、電源オフ信号を送り返した後にのみ電源が切れます。

     * SBC (例: Raspberry Pi) の場合: 追加設定は不要です。
     * マイクロコントローラーの場合: **SDSIG** ジャンパーキャップを取り外し、中間ワイヤーをピンに接続します。シャットダウン信号を受信して安全にシャットダウンした後、このピンを High にして PiPower 5 に電源オフを通知します。

   * ``pipower_5_shutdown_when_request.py``: このサンプルはシャットダウン信号受信後の操作処理方法を示します。**SDSIG** ジャンパーキャップを取り外し、中間ワイヤーをピンに接続する必要があります。

MicroPython ライブラリ API ドキュメント: https://github.com/sunfounder/micropython_spc?tab=readme-ov-file#api
