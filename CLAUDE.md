# PiPower 5 文档仓库

> **从规范源同步。** 此 CLAUDE.md 从英文源仓库（`docs` 分支）同步。权威版本位于主工作区。当前分支：`docs-zh` — 中文翻译。

## 项目标识

| 字段 | 值 |
|---|---|
| **产品** | SunFounder PiPower 5 — Raspberry Pi UPS HAT |
| **仓库** | `https://github.com/sunfounder/pipower5` |
| **文档** | Sphinx + ReadTheDocs（`sphinx_rtd_theme`） |
| **发布地址** | `https://docs.sunfounder.com/projects/pipower5/<lang>/latest/` |
| **公司** | SunFounder（service@sunfounder.com） |
| **许可证** | GPL v2 |

本仓库的 `docs` 分支**仅包含** PiPower 5 UPS HAT 的文档。Python 库代码（`pipower5`）、内核驱动程序和安装程序位于 `main` 分支。`docs` 分支通过 ReadTheDocs 构建 Sphinx 文档站点。

---

## 分支策略

| 分支 | 角色 |
|---|---|
| `main` | Python 源代码、内核驱动、安装程序、示例 |
| `docs` | **文档源** — Sphinx RST 文件、图片、RTD 配置 |

### 基本规则

> **`docs` 是文档分支。** 所有文档更改（内容、结构、图片、配置）都在 `docs` 上进行。`main` 分支用于 Python 库和驱动程序代码。这两个分支服务于不同的目的，不应混淆。

---

## 仓库结构（docs 分支）

```
pipower5/
├── .readthedocs.yaml          # RTD 构建配置（Sphinx 7.3.7，Python 3.11，Ubuntu 22.04）
├── .gitignore                 # 忽略：.vscode，build/，秘密文件
├── LICENSE                    # GPL v2
├── README.md                  # 产品概述 + 快速链接
├── show                       # 许可证/保修显示脚本
├── CLAUDE.md                  # 本文件 — AI 助手指南
└── docs/
    ├── requirements.txt       # sphinx==7.3.7，sphinx_rtd_theme==3.0.2，sphinx_copybutton
    ├── Makefile / make.bat    # Sphinx 构建（SOURCEDIR=source，BUILDDIR=build）
    └── source/
        ├── conf.py            # Sphinx 配置：扩展、主题、JS/CSS、rst_epilog 链接
        ├── index.rst          # 根目录树 — 入门 + 硬件 + 软件 + 附录
        ├── assembly.rst       # 组装说明
        ├── quick_guide.rst    # 快速用户指南
        ├── pipower_hat.rst    # HAT 硬件概述（接口、规格、电源、I2C 寄存器）
        ├── battery.rst        # 电池指南
        ├── pipower5_software.rst  # 软件工具（安装、CLI 参考、仪表板、关机、通知）
        ├── update_firmware.rst    # 固件更新指南
        ├── use_with_python.rst    # Python 使用（示例、API）
        ├── use_with_arduino.rst   # Arduino 库使用
        ├── use_with_micropython.rst  # MicroPython 库使用
        ├── compatible_sbc.rst     # 兼容 SBC 列表
        ├── faq.rst               # 常见问题
        ├── troubleshooting.rst   # 故障排除指南
        ├── _static/
        │   └── lang.js           # 多语言重定向脚本
        ├── _templates/
        │   └── layout.html       # Sphinx HTML 模板（SunFounder 导航栏）
        └── img/                  # 所有文档图片
```

---

## 文档规范

### RST 参考标签

每个 `.rst` 文件可以定义一个参考标签用于跨文档链接：

| 标签 | 文件 | 内容 |
|---|---|---|
| `pipower5_assembly` | `assembly.rst` | 组装说明 |
| `pipower5_tool` | `pipower5_software.rst` | 软件工具参考 |
| `power_input` | `pipower_hat.rst` | 电源输入部分 |
| `power_button` | `pipower_hat.rst` | 电源按钮部分 |
| `battery_indicators` | `pipower_hat.rst` | 电池指示灯部分 |
| `battery_connector` | `pipower_hat.rst` | 电池连接器部分 |
| `cap_btn` | `pipower_hat.rst` | 外部电源按钮部分 |
| `cap_sdsig` | `pipower_hat.rst` | SDSIG 跳线部分 |
| `cap_onoff` | `pipower_hat.rst` | 默认 ON/OFF 跳线部分 |
| `pin_header` | `pipower_hat.rst` | RPi 排针部分 |
| `pipower_software_python` | `use_with_python.rst` | Python 使用部分 |

这些标签**必须保持一致** — 它们是跨文档链接机制。

### Include 指令

某些页面通过 Sphinx `include` 指令重用内容，使用 `start-after` / `end-before` 标记：

```rst
.. include:: /pipower5_software.rst
    :start-after: start_install_pipower5
    :end-before: end_install_pipower5
```

源文件中的标记使用以下格式：
```rst
.. start_install_pipower5

# ... 要包含的内容 ...

.. end_install_pipower5
```

修改标记之间的内容时，确保源文件和所有包含它的文件保持一致。

### 链接替换（`conf.py` 中的 `rst_epilog`）

所有外部链接作为 RST 替换放在 `conf.py` 的 `rst_epilog` 下：

| 替换 | 用途 |
|---|---|
| `\|link_sf_facebook\|` | SunFounder Facebook 社区 |
| `\|link_german_tutorials\|` | 德语教程（PiPower 3 — 旧版） |
| `\|link_jp_tutorials\|` | 日语教程（PiPower 3 — 旧版） |
| `\|link_en_tutorials\|` | 英语教程（PiPower 3 — 旧版） |
| `\|link_PiPower_5_buy\|` | 购买链接 |
| `\|link_PiPower_5\|` | PiPower 5 产品链接 |
| `\|link_spc_lib\|` | GitHub 上的 SPC I2C 库 |
| `\|link_pipower_tool\|` | PiPower 5 工具 GitHub 仓库 |

添加新的外部链接时，将 `|link_xxx|` 定义添加到 `conf.py` 的 `rst_epilog`。

### 图片路径

所有图片位于 `docs/source/img/`，相对于源目录或使用绝对路径引用：
```rst
.. image:: img/pipower5_ov.png
   :width: 100%

.. image:: img/power_input.png
   :width: 50%
   :align: center
```

### 文件命名

- 硬件：`pipower_hat.rst`、`battery.rst`（snake_case）
- 软件：`pipower5_software.rst`（snake_case）
- 指南：`quick_guide.rst`、`update_firmware.rst`（snake_case）
- 集成：`use_with_python.rst`、`use_with_arduino.rst`、`use_with_micropython.rst`

### RST 文件模板

每个课程/指南文件以 Facebook 社区说明开头，后跟参考标签（如有），然后是标题：

```rst
.. note::

    Hello, welcome to the SunFounder Raspberry Pi & Arduino & ESP32 ...
    👉 Ready to explore and create with us? Click [|link_sf_facebook|] and join today!

.. _pipower5_tool:

PiPower 5 Tool
===============================
```

---

## 构建与预览

### 本地构建（Sphinx）

```bash
cd docs
pip install -r requirements.txt
make html          # 输出：docs/build/html/index.html
```

在 Windows 上：
```batch
cd docs
make.bat html
```

### ReadTheDocs

推送到 `docs` 分支时自动构建。配置在 `.readthedocs.yaml` 中：
- 操作系统：Ubuntu 22.04，Python 3.11
- Sphinx 配置：`docs/source/conf.py`
- 构建所有格式（HTML、PDF、ePub）

### 发布 URL

```
https://docs.sunfounder.com/projects/pipower5/en/latest/
```

---

## Sphinx 配置（conf.py）

### 扩展

| 扩展 | 用途 |
|---|---|
| `sphinx.ext.autosectionlabel` | **已禁用** — 在 `conf.py` 中保持注释。会导致 CJK 章节标题出现重复标签警告 |
| `sphinx_copybutton` | 为代码块添加复制按钮 |
| `sphinx_rtd_theme` | ReadTheDocs 主题 |

### 主题

- **主题**：`sphinx_rtd_theme`
- **选项**：附加弹出窗口，禁用版本/语言选择器
- **GitHub 集成**：已启用，指向 `sunfounder/pipower5` 的 `docs` 分支

### 自定义资源

- **JS**：`https://ezblock.cc/readDocFile/custom.js`、`./lang.js`
- **CSS**：`https://ezblock.cc/readDocFile/custom.css`
- **模板**：`_templates/layout.html`（带 logo 的 SunFounder 导航栏）

### 多语言

`_static/` 中的 `lang.js` 脚本处理自动语言检测和重定向。支持 `en`、`de`、`ja`，当浏览器语言与当前页面语言不同时显示通知栏。

`conf.py` 中的语言变量默认设置为 `'en'`。为其他语言构建时：
- 在 `conf.py` 中设置 `language = '<locale>'`
- 在 `docs/source/locale/` 下添加 `.po` 翻译文件

---

## 常见维护任务

### 添加新的文档页面

1. 在 `docs/source/` 中创建 `.rst` 文件
2. 如果页面将被交叉引用，在顶部定义 `.. _ref_label:`
3. 将文件添加到 `index.rst` 中相应的 `.. toctree::` 指令
4. 如果需要新的外部链接，将 `|link_xxx|` 定义添加到 `conf.py` 的 `rst_epilog`
5. 本地构建验证：`cd docs && make html`
6. 在 `docs` 上提交

### 更新 toctree 结构

根 toctree 在 `index.rst` 中。它有四个章节组：

1. **入门**：关于 PiPower 5、组装、快速指南
2. **硬件概述**：PiPower 5 HAT、电池
3. **软件配置**：PiPower 5 工具、固件更新、Python 使用
4. **附录**：兼容 SBC

目前 toctree 中缺少：`use_with_arduino.rst` 和 `use_with_micropython.rst` — 这些文件存在但未包含在任何 toctree 中。

### 使用 Include 标记添加内容

当内容需要在页面之间共享时：

1. 在可重用块之前添加 `.. start_<marker>`，之后添加 `.. end_<marker>`
2. 在目标文件中，使用：
   ```rst
   .. include:: /source_file.rst
       :start-after: start_<marker>
       :end-before: end_<marker>
   ```

### 修改寄存器表

`pipower_hat.rst` 中的 I2C 寄存器表使用带有自定义 CSS 的原始 HTML 表格。编辑时：
- 保持 HTML 结构完整
- 确保自定义 CSS 类名（`custom-register-table`）被保留
- 寄存器地址、数据类型和描述必须与实际固件匹配

---

## 给 AI 助手的注意事项

在本仓库工作时：

1. **`docs` 分支仅用于文档。** 源代码位于 `main`。不要向 `docs` 添加 Python 文件、驱动程序或安装脚本。
2. **每个 `.rst` 文件顶部的 Facebook 社区说明**是 SunFounder 文档标准的一部分。它出现在 `index.rst`、`pipower5_software.rst` 和其他面向用户的页面中。
3. **`conf.py` 链接替换**是外部 URL 的唯一来源。永远不要在 `.rst` 文件中硬编码外部链接 — 使用 `|link_xxx|` 替换。
4. **参考标签**（`.. _label:`）是代码标识符，不是人类可读文本。永远不要翻译它们。
5. **RST 章节下划线（和上划线）必须与标题显示宽度匹配。**
   
   - 对于单下划线标题（标题后跟 `=` 或 `-`），下划线必须至少与标题文本一样长。
   - 对于上划线+下划线标题（如标题上方和下方的 `----`），**两者**必须使用相同的字符，**长度完全相同**，并且至少与标题一样长。翻译标题时，始终同时更新这两行。
   - **CJK 显示宽度**：docutils 将 CJK 字符计为每个 **2 个显示列**（ASCII = 1 列）。上划线/下划线必须匹配总显示宽度，而不是字符数。例如，`LED & ブザークイックリファレンス` = 6 个 ASCII 列 + 13 个 CJK × 2 = 32 列 → 需要 ≥ 32 个破折号。
   
   翻译后的标题通常比英文原文更长 — 相应地扩展上划线和下划线。当标题包含 CJK 字符时，下划线/上划线将明显长于字符数所暗示的长度。
6. **行内强调标记（`**...**`）在与 CJK 字符相邻时会出错。** docutils 行内标记识别要求 `**` 分隔符与空白或 ASCII 标点符号（`- : / . , ; ! ? ' " ( ) [ ] { } < >`）相邻。CJK 字符（中文、日文、韩文）**不是**有效的分隔符。

   当 `**text**` 紧邻 CJK 字符之前或之后时，docutils 会发出 `WARNING: Inline strong start-string without end-string.`，因为它找不到闭合的 `**`。

   **解决方法**：在 `**` 分隔符和相邻的 CJK 字符之间插入 `\ `（反斜杠转义空格）：

   .. code-block:: rst

      # 错误 — 闭合 ** 后跟 CJK に，会发出警告：
      **PI3V3**にブリッジすると

      # 正确 — \  充当有效的分隔符：
      **PI3V3**\ にブリッジすると

      # 错误 — 开头 ** 前有 CJK は，会发出警告：
      または**コマンドラインツール**

      # 正确：
      または\ **コマンドラインツール**

   这同样适用于与 CJK 文本相邻的其他行内标记（`*强调*`、```文字```）。翻译包含行内标记的内容后，始终检查构建警告中的 "Inline ... start-string without end-string"。
7. **RST 中嵌套列表需要空行和正确的缩进。** 当编号列表项或项目符号包含子项目符号时，嵌套列表前必须有空行，嵌套项必须缩进以与父项文本对齐（通常 3+ 个空格）。没有空行，RST 会将项目符号渲染为单一连续行。

   **错误**（子项目符号没有空行）：
   ```rst
   3. **父项**：
      - 第一个子项
      - 第二个子项
   ```

   **正确**：
   ```rst
   3. **父项**：

        - 第一个子项
        - 第二个子项
   ```

8. **代码块**（Python、bash、shell）永远不翻译。命令字符串和文件路径保持原样。
9. **`_static` 和 `_templates` 目录**包含自定义资源。此处的更改会影响发布站点的全局外观和行为。
10. **构建输出**转到 `docs/build/` 并被 gitignore — 永远不要提交构建产物。
11. **图片**全部位于 `docs/source/img/`。添加新图片时，将它们放在那里并使用相对路径引用。
12. **`pipower_hat.rst` 中的寄存器表格**使用原始 HTML。更新寄存器值时，同时编辑"Register Table"（读取）和"Register Settings Table"（写入）部分。
13. **仓库根目录的 `show` 脚本**是 GPL 许可证显示工具 — 它是 Python 2 语法，应视为旧版。
