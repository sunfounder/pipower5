.. _faq:

常见问题
===

如何重新安装 PiPower 5
--------------------------

如果 PiPower 5 工作不正常，您想要进行全新安装，请按照以下步骤操作：

**1. 卸载当前安装：**

.. code-block:: shell

   cd ~/pipower5
   sudo python3 install.py --uninstall

**2. 从源码重新安装：**

.. code-block:: shell

   git clone https://github.com/sunfounder/pipower5
   cd pipower5
   sudo python3 install.py

**3. 提示时重启 Raspberry Pi。**

重启后，验证安装：

.. code-block:: shell

   pipower5 -a
   sudo systemctl status pipower5.service

.. tip::

   如果原始安装的 ``~/pipower5`` 目录已不存在，跳过卸载步骤，直接进入重新安装步骤。


仪表板显示"需要数据库"或无数据
----------------------------------------------

**您看到的情况**：Web 仪表板在浏览器中正常打开，但所有数据面板为空或显示"需要数据库"。

**这通常意味着什么**：这很少是硬件问题。大多数情况下，InfluxDB 后端存在配置问题 — 数据库损坏、bucket 缺失或令牌过期。

**请按顺序检查以下内容：**

1. **检查 PiPower 5 服务是否正在运行：**

   .. code-block:: shell

      sudo systemctl status pipower5

   如果服务未激活，启动它：

   .. code-block:: shell

      sudo systemctl start pipower5

2. **检查 InfluxDB bucket 是否存在：**

   .. code-block:: shell

      sudo influx bucket list

   在输出中查找名为 ``pipower5`` 的 bucket。如果缺失，需要重新创建数据库。

3. **检查服务日志中的错误：**

   .. code-block:: shell

      journalctl -u pipower5 -n 50

   查找与 InfluxDB 相关的错误消息，例如：

   - ``unauthorized`` 或 ``token`` — 表示身份验证令牌问题。
   - ``bucket not found`` — 数据库 bucket 缺失。
   - ``connection refused`` — InfluxDB 未运行。

4. **如果 InfluxDB 本身已关闭**，重新启动它：

   .. code-block:: shell

      sudo systemctl restart influxdb
      sudo systemctl restart pipower5

.. note::

   如果 InfluxDB 是手动安装或从旧版本迁移的，配置路径或身份验证令牌可能已更改。在这种情况下，PiPower 5 的全新安装（见上文）也将重新初始化 InfluxDB 设置。
