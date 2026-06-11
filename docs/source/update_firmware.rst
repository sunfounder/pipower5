使用 Raspberry Pi 更新 PiPower5 固件
===================================================================

本指南说明如何在 Raspberry Pi 上更新 **PiPower5** 的固件。

**1. 下载** ``pipower5_update_tools`` **并安装依赖**

.. code-block:: shell

   git clone https://github.com/sunfounder/pipower5_update_tools.git --depth 1

   sudo pip3 install blessed --break
   sudo pip3 install smbus2 --break

**2. 检查更新**

.. code-block:: shell

   cd pipower5_update_tools
   git pull

**3. 运行更新工具**

.. code-block:: shell

   python3 run.py

**4. 如果提示则停止服务**

运行 ``pipower5_update_tools`` 时，可能会提示您停止 ``pipower5.service``。按 ``Y`` 停止服务。

.. image:: img/upd_frw_1.png

**5. 选择** ``Update Firmware``

选择 **Update Firmware**。Raspberry Pi 将发送命令，将 PiPower5 切换到 **BOOT 模式**。

.. image:: img/upd_frw_2.png

**6. 验证 BOOT 模式**

成功进入 BOOT 模式后，PiPower5 上的**中间两个 LED** 将交替闪烁，表示 BOOT 模式已激活。

.. image:: img/upd_frw_3.png

**7. 选择固件文件**

选择 ``.bin`` 格式的固件文件，按 ``Enter`` 开始写入。

.. image:: img/upd_frw_4.png

**8. 完成更新**

刷写完成后，选择 **Restart**。
PiPower5 将重新启动并运行新固件。

.. image:: img/upd_frw_5.png

----------------------------------------------------------------

**恢复出厂固件**

如果需要回滚到出厂固件，请使用 ``pipower5_update_tools`` 中的 **Restore Factory Firmware** 选项。
这将重新加载存储在出厂分区中的固件并恢复到原始版本。

.. image:: img/upd_frw_6.png


----------------------------------------------------------------

**强制 BOOT 模式**

如果无法正常进入 BOOT 模式，可以强制进入：

1. 关闭 PiPower5 电源。
2. 短接 **Boot 1 引脚**。
3. 给设备通电。

PiPower5 将直接以 BOOT 模式启动。

.. image:: img/upd_frw_7.png

要退出 BOOT 模式，按住电源按钮两秒钟。
PiPower5 将重新启动进入正常模式。

.. image:: img/upd_frw_8.png

----------------------------------------------------------------

**故障排除**


以下是更新过程中可能遇到的一些常见问题及其解决方案：

- **设备未检测到**

  - 尝试重启 Raspberry Pi 和 PiPower5，然后重新运行更新工具。

- **无法进入 BOOT 模式**

  - 确保在更新前已停止 ``pipower5.service``。
  - 如果自动 BOOT 模式失败，使用**强制 BOOT 模式**方法（短接 Boot 1 引脚）。

- **更新过程卡住或刷写失败**

  - 仔细检查固件文件是否为 ``.bin`` 格式。
  - 重新运行更新工具并重试。
  - 使用稳定的电源以防止刷写过程中断。

- **固件更新完成，但设备工作不正常**

  - 使用内置工具恢复出厂固件。
  - 如果问题仍然存在，请验证固件文件是否与您的 PiPower5 版本匹配。
