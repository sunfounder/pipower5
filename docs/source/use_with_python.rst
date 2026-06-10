.. _pipower_software_python:

Python
------------------------------------------------------

Python を使用して PiPower と対話することもできます。

.. code-block:: shell

   source /opt/pipower5/venv/bin/activate

さまざまなユースケースを示す Python のサンプルをいくつか提供しています。サンプルディレクトリに移動して探索してください:

.. code-block:: shell

   cd ~/pipower5/examples

利用可能なスクリプトとその機能は以下の通りです:

- ``read_all.py``: PiPower 5 のすべてのステータス情報を一度に読み取り、各項目を個別に処理します。
- ``read_individual.py``: 特定の PiPower 5 データ項目を個別に読み取る方法を示します。
- ``set_shutdown_percentage.py``: シャットダウン残量を設定します。バッテリーレベルが設定された閾値を下回ると、PiPower 5 はホストにシャットダウン要求を送信し、シャットダウン完了後に電源を切断します。
- ``read_power_btn.py``: PiPower 5 の電源ボタンの現在の状態を読み取ります。
