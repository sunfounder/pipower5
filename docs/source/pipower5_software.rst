.. _pipower5_tool:

PiPower 5 工具
===============================

PiPower 5 工具是 PiPower 5 的配套软件。

它提供：

- 安全关机支持
- 电池和充电管理
- 电源监控
- Web 仪表板访问
- 事件通知

PiPower 5 可以在以下情况下向 Raspberry Pi 发送关机请求：

- PiPower 按钮按住 2 秒
- 电池电量低于配置的关机百分比

Raspberry Pi 完成关机后，PiPower 5 可以自动断开电源，以帮助防止 SD 卡损坏和意外断电问题。

.. start_install_pipower5

安装 ``pipower5`` 工具
----------------------------------------------------

安装 PiPower 5 工具：

1. 克隆仓库：

   .. code-block:: shell

      git clone https://github.com/sunfounder/pipower5

2. 进入目录：

   .. code-block:: shell

      cd pipower5

3. 运行安装程序：

   .. code-block:: shell

      sudo python3 install.py

4. 提示时重启 Raspberry Pi。

.. end_install_pipower5

命令参考
---------------------------------------

``pipower5`` 工具提供对 PiPower 5 状态信息和配置选项的访问。

例如，以下命令显示当前 PiPower 5 状态：

.. code-block:: shell

   pipower5 -a

示例输出：

.. code-block::

   Input:
      voltage: 0 mV
      current: 0 mA
      power: 0.000 W
      plugged in: False
   Output:
      voltage: 5296 mV
      current: 452 mA
      power: 2.394 W
   Battery:
      voltage: 8028 mV
      current: -315 mA
      power: -2.529 W
      percentage: 91 %
      source: 1 - Battery
      charging: False

   Internal:
      shutdown request: 0 - NONE
      power button: 0 - RELEASED
      max charging current: 0 mA
      default on: on
      shutdown percentage: 10 %

您可以根据需要自定义这些设置。

使用 ``pipower5`` 或 ``pipower5 -h`` 查看说明。

.. code-block:: text


  usage: pipower5 [-h] [-v] [-c] [-drd [DATABASE_RETENTION_DAYS]]
                  [-dl [{debug,info,warning,error,critical}]] [-rd]
                  [-cp [CONFIG_PATH]] [-sp [SHUTDOWN_PERCENTAGE]] [-iv] [-ic]
                  [-ov] [-oc] [-bv] [-bc] [-bp] [-bs] [-ii] [-ichg] [-do] [-sr]
                  [-pb] [-cc] [-a] [-fv] [-pfs [POWER_FAILURE_SIMULATION]]
                  [-seo [SEND_EMAIL_ON]] [-set [SEND_EMAIL_TO]]
                  [-ss [SMTP_SERVER]] [-smp [SMTP_PORT]] [-se [SMTP_EMAIL]]
                  [-spw [SMTP_PASSWORD]] [-ssc [SMTP_SECURITY]] [-bzo [BUZZ_ON]]
                  [-bzv [BUZZER_VOLUME]] [-bzt [BUZZER_TEST]] [-u [{C,F}]]
                  [{start,stop}]

  PiPower 5

  positional arguments:
    {start,stop}          命令

  options:
    -h, --help            显示此帮助信息并退出
    -v, --version         显示版本
    -c, --config          显示配置
    -drd [DATABASE_RETENTION_DAYS], --database-retention-days [DATABASE_RETENTION_DAYS]
                          数据库保留天数
    -dl [{debug,info,warning,error,critical}], --debug-level [{debug,info,warning,error,critical}]
                          调试级别
    -rd, --remove-dashboard
                          移除仪表板
    -cp [CONFIG_PATH], --config-path [CONFIG_PATH]
                          配置路径
    -sp [SHUTDOWN_PERCENTAGE], --shutdown-percentage [SHUTDOWN_PERCENTAGE]
                          设置关机百分比，留空为读取
    -iv, --input-voltage  读取输入电压
    -ic, --input-current  读取输入电流
    -ov, --output-voltage
                          读取输出电压
    -oc, --output-current
                          读取输出电流
    -bv, --battery-voltage
                          读取电池电压
    -bc, --battery-current
                          读取电池电流
    -bp, --battery-percentage
                          读取电池百分比
    -bs, --battery-source
                          读取电池来源
    -ii, --is-input-plugged_in
                          读取输入是否插入
    -ichg, --is-charging  读取是否正在充电
    -do, --default-on     读取默认开机
    -sr, --shutdown-request
                          读取关机请求
    -pb, --power-btn      读取电源按钮
    -cc, --charging-current
                          最大充电电流
    -a, --all             显示所有状态
    -fv, --firmware       PiPower5 固件版本
    -pfs [POWER_FAILURE_SIMULATION], --power-failure-simulation [POWER_FAILURE_SIMULATION]
                          电源故障模拟
    -seo [SEND_EMAIL_ON], --send-email-on [SEND_EMAIL_ON]
                          发送邮件的触发事件：['battery_activated', 'low_battery',
                          'power_disconnected', 'power_restored',
                          'power_insufficient', 'battery_critical_shutdown',
                          'battery_voltage_critical_shutdown']
    -set [SEND_EMAIL_TO], --send-email-to [SEND_EMAIL_TO]
                          接收邮件的邮箱地址
    -ss [SMTP_SERVER], --smtp-server [SMTP_SERVER]
                          SMTP 服务器
    -smp [SMTP_PORT], --smtp-port [SMTP_PORT]
                          SMTP 端口
    -se [SMTP_EMAIL], --smtp-email [SMTP_EMAIL]
                          SMTP 邮箱
    -spw [SMTP_PASSWORD], --smtp-password [SMTP_PASSWORD]
                          SMTP 密码
    -ssc [SMTP_SECURITY], --smtp-security [SMTP_SECURITY]
                          SMTP 安全类型，'none'、'ssl' 或 'tls'
    -bzo [BUZZ_ON], --buzz-on [BUZZ_ON]
                          蜂鸣器触发事件：['battery_activated', 'low_battery',
                          'power_disconnected', 'power_restored',
                          'power_insufficient', 'battery_critical_shutdown',
                          'battery_voltage_critical_shutdown']
    -bzv [BUZZER_VOLUME], --buzzer-volume [BUZZER_VOLUME]
                          蜂鸣器音量
    -bzt [BUZZER_TEST], --buzzer-test [BUZZER_TEST]
                          测试选定事件的蜂鸣器。
    -u [{C,F}], --temperature-unit [{C,F}]
                          温度单位

.. note::

   每次修改 ``pipower5.service`` 的状态时，您需要使用以下命令使配置更改生效。

   .. code-block:: shell

      sudo systemctl restart pipower5.service

   使用 systemctl 工具验证 pipower5 程序状态。

   .. code-block:: shell

      sudo systemctl status pipower5.service

   或者，检查程序生成的日志文件。

   .. code-block:: shell

      cat /opt/pipower5/log

Web 仪表板
----------------------------------------------------

PiPower 5 工具包含一个内置的 Web 仪表板，用于监控和配置。

从浏览器访问仪表板：

.. code-block:: text

   http://<raspberry-pi-ip>:34001

仪表板功能包括：

- 电池百分比监控
- 充电状态监控
- 输入和输出电压监控
- 电流监控
- 关机百分比配置
- 通知管理
- Raspberry Pi 设备信息

.. image:: img/web_dashboard.png
   :width: 100%
   :align: center

.. image:: img/web_dashboard_2.png
   :width: 100%
   :align: center

您也可以直接从仪表板配置关机百分比：

.. image:: img/web_dashboard_3.png
   :width: 100%
   :align: center

如果不需要仪表板，可以用以下命令移除：

.. code-block:: shell

   pipower5 --remove-dashboard

安全关机
----------------------------------------------------

PiPower 5 支持 Raspberry Pi 系统的自动安全关机保护。

关机工作流程：

.. code-block:: text

   关机触发
   -> Raspberry Pi 执行安全关机
   -> PiPower 5 检测到关机完成
   -> PiPower 5 自动切断电源

这有助于防止：

- SD 卡损坏
- 文件系统损坏
- 意外断电问题


Raspberry Pi 关机后断电
++++++++++++++++++++++++++++++++++++++

.. start_power_off_after_shutdown

要使 PiPower 5 在 Raspberry Pi 关机后自动切断电源，需要进行一些额外配置。

1. 如果您使用的是 **Raspberry Pi 4 或 5**：

   * 确保 PiPower 5 上的 ``SDSIG`` 跳线连接到 ``PI3V3``。

     .. image:: img/safe_shutdown_3v3.png
        :width: 400

   * 打开 Raspberry Pi 配置：

     .. code-block:: shell

        sudo raspi-config

   * 导航至：

     .. code-block:: text

        6 Advanced Options
        -> A11 Shutdown Behaviour
        -> B1 Full power off Switch off Pi ...

   * 提示时重启 Raspberry Pi。

2. 如果您使用的是 **Raspberry Pi 3** 或更早版本：

   * 将 PiPower 5 上的 ``SDSIG`` 跳线设置为 ``GPIO26``。

     .. image:: img/safe_shutdown_io26.png
        :width: 400

   * 打开 ``/boot/firmware/config.txt``：

     .. code-block:: shell

        sudo nano /boot/firmware/config.txt

   * 添加以下行：

     .. code-block:: shell

        dtoverlay=gpio-poweroff,gpio_pin=26,active_low=1
        gpio=26=op,dh

   * 按 ``Ctrl+X``，然后按 ``Y``，再按 ``Enter`` 保存文件并退出。

   * 重启 Raspberry Pi。

     .. code-block:: shell

        sudo reboot

配置完成后，PiPower 5 可以自动检测 Raspberry Pi 关机并安全断开电源。

支持的安全关机方法包括：

- 按住 PiPower 按钮 2 秒
- 从 Raspberry Pi 桌面菜单关机
- 运行 ``sudo shutdown now``
- 电池电量低于配置的关机百分比时自动关机

.. end_power_off_after_shutdown

配置关机百分比
++++++++++++++++++++++++++++++++++++++

您可以配置触发自动关机的电池百分比。

示例：

.. code-block:: shell

   pipower5 -sp 30

这将关机阈值设置为 30%。

然后使用以下命令使配置更改生效。

.. code-block:: shell

   sudo systemctl restart pipower5.service

当电池电量低于 30% 时，PiPower 5 将通知 Raspberry Pi 关机并自动断开电源。


您也可以读取当前的关机百分比：

.. code-block:: shell

   pipower5 -sp

.. tip::

   对于高功耗（>3A）的 Raspberry Pi 5 系统，建议将关机百分比设置为 ``100%``。

   这确保在外部电源断开时 Raspberry Pi 立即关机，有助于保护系统和存储设备。


电源监控
----------------------------------------------------

PiPower 5 提供以下实时监控：

- 电池百分比
- 充电状态
- 输入电压
- 输出电压
- 输入电流
- 输出电流
- 电池电压
- 电池电流

常用命令：

显示电池百分比：

.. code-block:: shell

   pipower5 -bp

显示充电状态：

.. code-block:: shell

   pipower5 -ichg

显示输入电压：

.. code-block:: shell

   pipower5 -iv

显示所有状态信息：

.. code-block:: shell

   pipower5 -a

获取完整命令列表：

.. code-block:: shell

   pipower5 --help


通知
----------------------------------------------------

PiPower5 通过以下方式支持事件驱动的通知：

- 蜂鸣器警报
- 邮件通知

支持的事件包括：

- ``battery_activated``
- ``low_battery``
- ``power_disconnected``
- ``power_restored``
- ``power_insufficient``
- ``battery_critical_shutdown``
- ``battery_voltage_critical_shutdown``

.. note::

   每次修改 ``pipower5.service`` 的状态时，您需要使用以下命令使配置更改生效。

   .. code-block:: shell

      sudo systemctl restart pipower5.service

事件说明
+++++++++++++++++++++++++++++++++++++++++++++++++

1. ``battery_activated``

   电池开始供电时触发。这通常发生在外部电源断开或无法提供足够电力时。

   * **重置条件**：外部电源断开后自动重置。

2. ``low_battery``

   电池电量低于**配置的关机阈值**时激活。

   * **重复**：如果电池保持低于此阈值，该事件每 10 分钟触发一次。
   * **重置条件**：电池电量回升到**关机阈值 + 5%** 以上后重置。

3. ``power_disconnected``

   外部电源断开时触发。

   * **重置条件**：外部电源恢复后重置。

4. ``power_restored``

   外部电源恢复时触发。

   * **重置条件**：外部电源再次断开时重置。

5. ``power_insufficient``

   外部电源不足，需要电池提供补充电力时发生。

   * **建议操作**：检查电源的额定输出，或验证配置的充电功率设置。
   * **重置条件**：外部电源断开时重置。

6. ``battery_critical_shutdown``

   系统因**电池容量严重不足**而即将关机前触发。

7. ``battery_voltage_critical_shutdown``

   **电池电压**\ 低于临界阈值导致关机时触发。

   * **注意**：此事件在正常使用中很少触发。通常，``low_battery`` 事件会在电压降到此低之前启动关机序列。这充当**故障安全关机机制**。

通过这些事件，PiPower5 提供主动警告（如低电量、功率不足）和关键保护（如关机触发器），确保稳定运行和数据保护。



蜂鸣器警报
+++++++++++++++++++++++++++++++++++++++++++++++++

PiPower5 支持不同系统事件的蜂鸣器通知。

您可以通过\ **Web 仪表板**\ 或\ **命令行工具**\ 配置蜂鸣器警报。
当配置的事件发生时，PiPower5 会播放相应的蜂鸣器声音。

功能包括：

- 基于事件的蜂鸣器通知
- 可调蜂鸣器音量（1–10）
- 事件声音预览
- 自定义音效支持

高级用户还可以创建自定义蜂鸣器音效。

1. 打开配置文件：

   .. code-block:: shell

      /opt/pipower5/venv/lib/python3.11/site-packages/pipower5/config.json

2. 找到 ``pipower5_buzz_sequence`` 部分。

3. 每个音效使用以下格式定义：

   .. code-block:: text

      [action, duration]

   其中：

   - ``action`` 可以是：

     - 音符，如 ``"A4"``、``"D3"`` 或 ``"C#4"``
     - 频率值（整数）
     - ``"pause"`` 表示静音

   - ``duration`` 是播放时间，以毫秒（ms）为单位


邮件警报
+++++++++++++++++++++++++++++++++++++++++++++++++

PiPower5 支持重要系统事件的邮件通知，例如：

- 电池电量低
- 电源断开
- 电源恢复
- 严重关机事件

可以通过\ **Web 仪表板**\ 或\ **命令行工具**\ 配置邮件通知。

要使用邮件警报，需要 SMTP 服务器。大多数邮件提供商支持 SMTP 服务。

- 对于 Gmail，只需创建一个**应用密码**
- 对于其他提供商，启用 SMTP 访问并在需要时生成专用 SMTP 密码

配置前，请准备以下信息：

- SMTP 服务器地址
  （示例：``smtp.gmail.com``）

- SMTP 端口
  （示例：``465`` 或 ``25``）

- 加密类型
  （``None`` / ``SSL`` / ``TLS``）

- SMTP 账户
  （通常是您的邮箱地址）

- SMTP 密码
  （应用密码或 SMTP 密码）

输入 SMTP 信息后，配置收件人邮箱地址。

.. note::

   PiPower5 使用 SMTP 服务器登录您的邮箱账户并发送通知。

   您可以使用同一邮箱地址作为发件人和收件人。

设置完成后，使用测试命令验证 SMTP 连接和邮件递送。
