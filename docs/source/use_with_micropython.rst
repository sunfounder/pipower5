MicroPython
==========================================================

我们提供了一个库，允许您监控输入和输出电压、电池电压和百分比、电源、充电状态以及其他内部数据。

如果您使用 PiPower 5 为 Raspberry Pi Pico 或 ESP32 板供电，可以通过 Type-A 输出端口或两根跳线将板连接到 PiPower 5。

要连接 PiPower 5 的 I2C 接口，请使用跳线。

.. 如果关机前不需要操作，直接将 SDSIG 跳线帽连接到 GND 引脚。如果关机前需要操作，取下跳线帽，将中间线连接到 Raspberry Pi Pico 或 ESP32 板上的 I/O 引脚。此设置通知 PiPower 5 关机过程已完成，可以安全断电。

#. 从 GitHub 下载库。您可以使用以下链接快速下载，或访问：https://github.com/sunfounder/micropython_spc。

   * :download:`micropython_spc <https://github.com/sunfounder/micropython_spc/archive/refs/heads/main.zip>`

#. 下载并解压后，将 ``spc`` 文件夹上传到您的 Raspberry Pi Pico 或 ESP32 板。推荐使用 Thonny 进行此操作。

   .. image:: img/micropython_upload.png
       :width: 100%
       :align: center

   .. raw:: html

      <br/>

#. 库上传后，您可以使用 ``micropython_spc-main/examples/pipower5`` 文件夹中提供的示例进行测试：

   * ``pipower_5_read_all.py``：如果您需要读取所有数据，请使用此示例。它演示了如何一次性读取所有可用数据并分别处理。

   * ``pipower_5_read_individual.py``：此示例提供单独读取特定数据的说明。如果您只需要访问某些数据，请使用它。

   * ``pipower_5_set_shutdown_percentage.py``：此示例说明如何设置关机电池百分比。当电池未充电且电量低于指定百分比时，PiPower 5 会向主机发送关机信号。它只有在主机完成关机并发送断电信号后才会断电。

     * 对于 SBC（如 Raspberry Pi）：无需额外配置。
     * 对于微控制器：取下 **SDSIG** 跳线帽，将中间线连接到一个引脚。收到关机信号并安全关机后，将此引脚拉高以通知 PiPower 5 断电。

   * ``pipower_5_shutdown_when_request.py``：此示例演示如何在收到关机信号后处理操作。您需要取下 **SDSIG** 跳线帽，将中间线连接到一个引脚。

Micropython 库 API 文档：https://github.com/sunfounder/micropython_spc?tab=readme-ov-file#api
