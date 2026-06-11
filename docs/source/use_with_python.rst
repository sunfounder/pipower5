.. _pipower_software_python:

Python
------------------------------------------------------

您也可以使用 Python 与 PiPower 交互。

.. code-block:: shell

   source /opt/pipower5/venv/bin/activate

我们提供了几个 Python 示例来演示不同的用例。进入示例目录探索它们：

.. code-block:: shell

   cd ~/pipower5/examples

以下是可用的脚本及其功能：

- ``read_all.py``：一次性读取所有 PiPower 5 状态信息并逐个处理。
- ``read_individual.py``：演示如何单独读取特定的 PiPower 5 数据项。
- ``set_shutdown_percentage.py``：配置关机百分比。当电池电量低于配置的阈值时，PiPower 5 会向主机发送关机请求，并在关机完成后切断电源。
- ``read_power_btn.py``：读取 PiPower 5 电源按钮的当前状态。
