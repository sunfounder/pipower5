.. note::

    Facebook上のSunFounder Raspberry Pi & Arduino & ESP32エンスージアストコミュニティへようこそ！仲間のエンスージアストと共に、Raspberry Pi、Arduino、ESP32についてより深く学びましょう。

    **参加する理由**

    - **エキスパートサポート**: コミュニティとチームの助けを借りて、販売後の問題や技術的な課題を解決します。
    - **学びと共有**: ヒントやチュートリアルを交換してスキルを向上させましょう。
    - **独占プレビュー**: 新製品の発表や先行紹介にいち早くアクセスできます。
    - **特別割引**: 最新製品の独占割引をお楽しみください。
    - **お祭りプロモーションとプレゼント**: プレゼント企画やホリデープロモーションに参加しましょう。

    👉 私たちと一緒に探求し創造する準備はできましたか？[|link_sf_facebook|]をクリックして今すぐ参加しましょう！

SunFounder PiPower5 - デバイスとデータを保護
================================================================================

.. * |link_PiPower_5_buy|

.. Thank you for choosing our |link_PiPower_5|.

PiPower5 をお選びいただきありがとうございます。


.. .. note::
..     This document is available in the following languages.

..         * |link_german_tutorials|
..         * |link_jp_tutorials|
..         * |link_en_tutorials|

..     Please click on the respective links to access the document in your preferred language.

.. todo: new pic

.. image:: img/PP.0.A.JPG
    :width: 400
    :align: center

PiPower 5 は、Raspberry Pi デバイスとのシームレスな統合のために設計された多用途 UPS ソリューションです。堅牢な電源パス管理、デュアルリチウムバッテリーの充放電機能、逆極性・過充電・過放電に対する必須保護機能を備えています。

最大 5V/5A の出力により、PiPower 5 は幅広いデバイスで安定したパフォーマンスを保証します。HAT+ 構成は Raspberry Pi 5 との互換性を保証し、USB-A ポートと 4x2P ヘッダーを含む追加出力は、Arduino、Pico、ESP32 などのさまざまなシングルボードコンピューター (SBC) およびマイクロコントローラープラットフォームをサポートします。

内蔵マイクロコントローラーが電源操作を効率的に管理し、I2C 通信を介して主要パラメーターのリアルタイム監視を可能にします。これらのパラメーターには、入力電圧、出力電圧、バッテリー電圧、バッテリー容量、外部電源接続状態、充電状態、現在の電源ソース (バッテリーまたはUSB) が含まれます。

高度なバッテリー管理と幅広い互換性を組み合わせた PiPower 5 は、ハードウェアセットアップの最適化を目指す技術愛好家や専門家にとって不可欠なツールです。

**機能**

* **入力**: 5-15V、45W、USB Type-C PD、DC5.5-2.1
* **出力**: Raspberry Pi GPIO 経由で 5V/5A、USB Type-A、2x4P 2.54mm ピンヘッダー
* **充電電力**: 最大 20W
* **バッテリー仕様**: 7.4V 2セル Li-ion、XH2.54 3P コネクタ
* **ジャンパーによる設定可能な設定**:

  * デフォルトONジャンパー: 電源接続時にデバイスを自動起動するかどうかを設定。
  * シャットダウン信号ジャンパー: デバイスのシャットダウン状態の検出を有効化。
  * 外部電源ボタンピンヘッダー: 手動電源制御用の外部電源ボタンを接続。

* **内蔵インジケーターとボタン**:

  * バッテリー状態インジケーター
  * 入力ソースインジケーター
  * 電源ボタン
  * バッテリー逆接続インジケーター
  * 出力電源インジケーター

* **内蔵マイクロコントローラー**: 32-bit ARM Cortex-M23、I2C通信対応

* **I2C通信インターフェース**:

  * Raspberry Pi GPIO
  * SH1.0 4P (Qwiic および STEMMA QT 互換)
  * 1x4P 2.54mm ピンヘッダー


.. **Table of Contents**

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: はじめに

   About PiPower 5 <self>
   assembly
   quick_guide

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: ハードウェア概要

   pipower_hat


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: ソフトウェア設定

   pipower5_software
   update_firmware
   use_with_python


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: 付録

   compatible_sbc
   troubleshooting
   faq


**著作権表示**

本書のテキスト、画像、コードを含むがこれらに限定されないすべての内容は、SunFounder Company が所有しています。著作者および関連する権利所有者の法的権利を侵害することなく、関連法規および著作権法の下で、個人的な学習、調査、娯楽、またはその他の非商業的・非営利目的にのみ使用することができます。許可なくこれらを商業的利益のために使用する個人または組織に対して、当社は法的措置を取る権利を留保します。
