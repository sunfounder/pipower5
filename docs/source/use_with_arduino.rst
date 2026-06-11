Arduino
===================================

如果您使用 PiPower 5 为 Arduino 板供电，可以将 Arduino 连接到 PiPower 5 的 Type A 输出端口或使用两根跳线。使用跳线连接板的 I2C 接口。

.. 如果在关机前不需要任何操作，直接将 **SDSIG** 跳线帽连接到 GND。如果关机前需要操作，取下跳线帽，将中间线连接到 Arduino 上的一个 IO 端口，通知 PiPower 5 可以安全关机。

我们提供了一个库，允许您监控输入和输出电压、电池电压和百分比、电源、充电状态以及其他内部数据。

#. 在 Arduino IDE 中，打开**库管理器**，搜索 ``SunFounderPowerControl``，下载并安装。

   .. image:: img/install_arduino_lib.png
      :width: 100%

#. 安装后，您可以导航到**文件** -> **示例** -> **SunFounderPowerControl** -> **PiPower 5**，在那里您会找到四个示例。

   .. image:: img/arduino_lib_example.png
      :width: 100%

   * ``read_all``：如果您需要一次性读取所有数据并分别处理，请使用此示例。
   * ``read_individual``：如果您只需要读取特定数据，此示例提供单独的数据读取说明。
   * ``set_shutdown_percentage``：此示例教您如何设置关机电池百分比。当电池未充电且电量低于设定百分比时，此功能会向主机发送关机信号。主机关机后，只有在收到断电信号后才会断电。通常用于 Raspberry Pi 等 SBC。对于微控制器，取下 **SDSIG** 跳线帽，将中间线连接到一个引脚。收到关机信号后安全关机后，将此引脚拉高以关闭 PiPower 5。
   * ``shutdown_when_request``：此示例展示如何在收到关机信号后处理操作。取下 **SDSIG** 跳线帽，将中间线连接到一个引脚。

#. 选择其中一个示例并将其上传到您的板卡。

   .. note::

      在某些可以修改 I2C 的板卡上，如果需要更改 I2C 引脚，需要修改 ``Wire.begin()`` 代码。

Arduino 库 API 文档：https://github.com/sunfounder/arduino_spc?tab=readme-ov-file#api

