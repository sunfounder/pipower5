.. note::

    Facebook上のSunFounder Raspberry Pi & Arduino & ESP32エンスージアストコミュニティへようこそ！仲間のエンスージアストと共に、Raspberry Pi、Arduino、ESP32についてより深く学びましょう。

    **参加する理由**

    - **エキスパートサポート**: コミュニティとチームの助けを借りて、販売後の問題や技術的な課題を解決します。
    - **学びと共有**: ヒントやチュートリアルを交換してスキルを向上させましょう。
    - **独占プレビュー**: 新製品の発表や先行紹介にいち早くアクセスできます。
    - **特別割引**: 最新製品の独占割引をお楽しみください。
    - **お祭りプロモーションとプレゼント**: プレゼント企画やホリデープロモーションに参加しましょう。

    👉 私たちと一緒に探求し創造する準備はできましたか？[|link_sf_facebook|]をクリックして今すぐ参加しましょう！

.. _faq:

よくある質問
============

PiPower 5 の再インストール方法
------------------------------

PiPower 5 が正常に動作せず、クリーンな再インストールを実行したい場合は、以下の手順に従ってください:

**1. 現在のインストールをアンインストール:**

.. code-block:: shell

   cd ~/pipower5
   sudo python3 install.py --uninstall

**2. ソースから再インストール:**

.. code-block:: shell

   git clone https://github.com/sunfounder/pipower5
   cd pipower5
   sudo python3 install.py

**3. プロンプトが表示されたら Raspberry Pi を再起動します。**

再起動後、インストールを確認します:

.. code-block:: shell

   pipower5 -a
   sudo systemctl status pipower5.service

.. tip::

   元のインストールから ``~/pipower5`` ディレクトリがもう存在しない場合は、アンインストール手順をスキップして、再インストール手順に直接進んでください。


ダッシュボードに「Database Required」またはデータが表示されない
------------------------------------------------------------------

**表示される症状**: Web ダッシュボードはブラウザで正常に開くが、すべてのデータパネルが空であるか、「database required」と表示される。

**これが通常意味すること**: これはめったにハードウェアの問題ではありません。ほとんどの場合、InfluxDB バックエンドに設定の問題があります — 破損したデータベース、不足しているバケット、または期限切れのトークンです。

**以下の順序で確認してください:**

1. **PiPower 5 サービスが実行中か確認:**

   .. code-block:: shell

      sudo systemctl status pipower5

   サービスがアクティブでない場合、起動します:

   .. code-block:: shell

      sudo systemctl start pipower5

2. **InfluxDB バケットが存在するか確認:**

   .. code-block:: shell

      sudo influx bucket list

   出力で ``pipower5`` という名前のバケットを探します。不足している場合、データベースを再作成する必要があります。

3. **サービルログでエラーを確認:**

   .. code-block:: shell

      journalctl -u pipower5 -n 50

   InfluxDB に関連するエラーメッセージを探します。例:

   - ``unauthorized`` または ``token`` — 認証トークンの問題を示します。
   - ``bucket not found`` — データベースバケットが不足しています。
   - ``connection refused`` — InfluxDB が実行されていません。

4. **InfluxDB 自体がダウンしている場合**、再起動します:

   .. code-block:: shell

      sudo systemctl restart influxdb
      sudo systemctl restart pipower5

.. note::

   InfluxDB が手動でインストールされたか、古いバージョンから移行された場合、設定パスや認証トークンが変更されている可能性があります。その場合、PiPower 5 のクリーンな再インストール (上記参照) により、InfluxDB セットアップも再初期化されます。
