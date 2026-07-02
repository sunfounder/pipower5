SunFounder PiPower5 — 保护您的设备与数据
================================================================================

.. * |link_PiPower_5_buy|

.. 感谢您选择我们的 |link_PiPower_5|。

感谢您选择我们的 PiPower5。


.. .. note::
..     本文档提供以下语言版本。

..         * |link_german_tutorials|
..         * |link_jp_tutorials|
..         * |link_en_tutorials|

..     请点击相应链接以您偏好的语言访问文档。

.. todo: new pic

.. image:: img/PP.0.A.JPG
    :width: 400
    :align: center

PiPower 5 是一款多功能 UPS 解决方案，专为与 Raspberry Pi 设备无缝集成而设计。它具有强大的电源路径管理、双锂电池充放电能力，以及防反接、过充和过放等基本保护功能。

PiPower 5 输出高达 5V/5A，确保各种设备稳定运行。其 HAT+ 配置保证与 Raspberry Pi 5 兼容，而额外的输出（包括 USB-A 端口和 4x2P 排针）为各种单板计算机（SBC）和微控制器平台（如 Arduino、Pico 和 ESP32）提供支持。

板载微控制器高效管理电源操作，并通过 I2C 通信实现关键参数的实时监控。这些参数包括输入电压、输出电压、电池电压、电池容量、外部电源连接状态、充电状态以及当前电源（电池或 USB）。

PiPower 5 结合先进的电池管理和广泛的兼容性，是技术爱好者和专业人士优化硬件配置的必备工具。

**特点**

* **输入**：5-15V，45W，USB Type-C PD，DC5.5-2.1
* **输出**：通过 Raspberry Pi GPIO 5V/5A、USB Type-A 和 2x4P 2.54mm 排针输出
* **充电功率**：高达 20W
* **电池规格**：7.4V 2 节 锂离子电池，XH2.54 3P 连接器
* **通过跳线可配置的设置**：

  * 默认开机跳线：配置设备在接通电源时是否自动开机。
  * 关机信号跳线：启用设备关机状态检测。
  * 外部电源按钮排针：连接外部电源按钮以手动控制电源。

* **板载指示灯和按钮**：

  * 电池状态指示灯
  * 输入源指示灯
  * 电源按钮
  * 电池反接指示灯
  * 输出电源指示灯

* **板载微控制器**：32 位 ARM Cortex-M23，支持 I2C 通信

* **I2C 通信接口**：

  * Raspberry Pi GPIO
  * SH1.0 4P（兼容 Qwiic 和 STEMMA QT）
  * 1x4P 2.54mm 排针


.. **目录**

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: 入门

   关于 PiPower 5 <self>
   assembly
   quick_guide

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: 硬件概述

   pipower_hat


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: 软件配置

   pipower5_software
   update_firmware
   use_with_python


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: 附录

   compatible_sbc
   troubleshooting
   faq


**版权声明**

本手册中的所有内容，包括但不限于文本、图片和代码，均归 SunFounder 公司所有。您只能在相关法规和版权法的规定下，将其用于个人学习、研究、欣赏或其他非商业或非营利目的，不得侵犯作者和相关权利人的合法权利。对于任何未经许可将这些内容用于商业盈利目的的个人或组织，本公司保留采取法律行动的权利。

