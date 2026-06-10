# PiPower 5 Documentation Repository

> **Canonical AI guidance.** This is the authoritative CLAUDE.md for the PiPower 5 documentation project. All language-variant repositories (`pipower5-rtd-*-sync`) should sync their CLAUDE.md from this file. When adding rules or fixes, update this file first, then propagate to other language repos.

## Project Identity

| Field | Value |
|---|---|
| **Product** | SunFounder PiPower 5 — Raspberry Pi UPS HAT |
| **Repository** | `https://github.com/sunfounder/pipower5` |
| **Documentation** | Sphinx + ReadTheDocs (`sphinx_rtd_theme`) |
| **Published at** | `https://docs.sunfounder.com/projects/pipower5/<lang>/latest/` |
| **Company** | SunFounder (service@sunfounder.com) |
| **License** | GPL v2 |

This repository's `docs` branch contains **only documentation** for the PiPower 5 UPS HAT. The Python library code (`pipower5`), kernel driver, and installer live on the `main` branch. The `docs` branch builds a Sphinx documentation site via ReadTheDocs.

---

## Branch Strategy

| Branch | Role |
|---|---|
| `main` | Python source code, kernel driver, installer, examples |
| `docs` | **Documentation source** — Sphinx RST files, images, RTD config |

### Cardinal Rule

> **`docs` is the documentation branch.** All documentation changes (content, structure, images, configuration) happen on `docs`. The `main` branch is for the Python library and driver code. These two branches serve different purposes and should not be confused.

---

## Repository Layout (docs branch)

```
pipower5/
├── .readthedocs.yaml          # RTD build config (Sphinx 7.3.7, Python 3.11, Ubuntu 22.04)
├── .gitignore                 # Ignores: .vscode, build/, secret files
├── LICENSE                    # GPL v2
├── README.md                  # Product overview + quick links
├── show                       # License/warranty display script
├── CLAUDE.md                  # This file — AI assistant guidance
└── docs/
    ├── requirements.txt       # sphinx==7.3.7, sphinx_rtd_theme==3.0.2, sphinx_copybutton
    ├── Makefile / make.bat    # Sphinx build (SOURCEDIR=source, BUILDDIR=build)
    └── source/
        ├── conf.py            # Sphinx config: extensions, theme, JS/CSS, rst_epilog links
        ├── index.rst          # Root toctree — Getting Started + Hardware + Software + Appendix
        ├── assembly.rst       # Assembly instructions
        ├── quick_guide.rst    # Quick user guide
        ├── pipower_hat.rst    # HAT hardware overview (interface, specs, power, I2C registers)
        ├── battery.rst        # Battery guide
        ├── pipower5_software.rst  # Software tool (install, CLI ref, dashboard, shutdown, notifications)
        ├── update_firmware.rst    # Firmware update guide
        ├── use_with_python.rst    # Python usage (examples, API)
        ├── use_with_arduino.rst   # Arduino library usage
        ├── use_with_micropython.rst  # MicroPython library usage
        ├── compatible_sbc.rst     # Compatible SBC list
        ├── faq.rst               # Frequently asked questions
        ├── troubleshooting.rst   # Troubleshooting guide
        ├── _static/
        │   └── lang.js           # Multi-language redirect script
        ├── _templates/
        │   └── layout.html       # Sphinx HTML template (SunFounder nav bar)
        └── img/                  # All documentation images
```

---

## Documentation Conventions

### RST Reference Labels

Each `.rst` file may define a reference label for cross-document linking:

| Label | File | Content |
|---|---|---|
| `pipower5_assembly` | `assembly.rst` | Assembly instructions |
| `pipower5_tool` | `pipower5_software.rst` | Software tool reference |
| `power_input` | `pipower_hat.rst` | Power input section |
| `power_button` | `pipower_hat.rst` | Power button section |
| `battery_indicators` | `pipower_hat.rst` | Battery indicators section |
| `battery_connector` | `pipower_hat.rst` | Battery connector section |
| `cap_btn` | `pipower_hat.rst` | External power button section |
| `cap_sdsig` | `pipower_hat.rst` | SDSIG jumper section |
| `cap_onoff` | `pipower_hat.rst` | Default ON/OFF jumper section |
| `pin_header` | `pipower_hat.rst` | Pin headers for RPi section |
| `pipower_software_python` | `use_with_python.rst` | Python usage section |

These labels **must remain consistent** — they are the cross-document linking mechanism.

### Include Directives

Some pages reuse content via Sphinx `include` directives with `start-after` / `end-before` markers:

```rst
.. include:: /pipower5_software.rst
    :start-after: start_install_pipower5
    :end-before: end_install_pipower5
```

Markers in the source file use the format:
```rst
.. start_install_pipower5

# ... content to include ...

.. end_install_pipower5
```

When modifying content between markers, ensure both the source file and all files that include it remain consistent.

### Link Substitutions (`rst_epilog` in `conf.py`)

All external links live as RST substitutions in `conf.py` under `rst_epilog`:

| Substitution | Purpose |
|---|---|
| `\|link_sf_facebook\|` | SunFounder Facebook community |
| `\|link_german_tutorials\|` | German tutorials (PiPower 3 — legacy) |
| `\|link_jp_tutorials\|` | Japanese tutorials (PiPower 3 — legacy) |
| `\|link_en_tutorials\|` | English tutorials (PiPower 3 — legacy) |
| `\|link_PiPower_5_buy\|` | Purchase link |
| `\|link_PiPower_5\|` | PiPower 5 product link |
| `\|link_spc_lib\|` | SPC I2C library on GitHub |
| `\|link_pipower_tool\|` | PiPower 5 tool GitHub repo |

When adding a new external link, add the `|link_xxx|` definition to `conf.py` `rst_epilog`.

### Image Paths

All images live under `docs/source/img/` and are referenced relative to the source directory or with absolute paths:
```rst
.. image:: img/pipower5_ov.png
   :width: 100%

.. image:: img/power_input.png
   :width: 50%
   :align: center
```

### File Naming

- Hardware: `pipower_hat.rst`, `battery.rst` (snake_case)
- Software: `pipower5_software.rst` (snake_case)
- Guides: `quick_guide.rst`, `update_firmware.rst` (snake_case)
- Integration: `use_with_python.rst`, `use_with_arduino.rst`, `use_with_micropython.rst`

### RST File Boilerplate

Every lesson/guide file starts with a Facebook community note, followed by the reference label (if any), then the title:

```rst
.. note::

    Hello, welcome to the SunFounder Raspberry Pi & Arduino & ESP32 ...
    👉 Ready to explore and create with us? Click [|link_sf_facebook|] and join today!

.. _pipower5_tool:

PiPower 5 Tool
===============================
```

---

## Build & Preview

### Local Build (Sphinx)

```bash
cd docs
pip install -r requirements.txt
make html          # Output: docs/build/html/index.html
```

On Windows:
```batch
cd docs
make.bat html
```

### ReadTheDocs

Builds automatically on push to the `docs` branch. Configuration in `.readthedocs.yaml`:
- OS: Ubuntu 22.04, Python 3.11
- Sphinx config: `docs/source/conf.py`
- Builds all formats (HTML, PDF, ePub)

### Published URLs

```
https://docs.sunfounder.com/projects/pipower5/en/latest/
```

---

## Sphinx Configuration (conf.py)

### Extensions

| Extension | Purpose |
|---|---|
| `sphinx.ext.autosectionlabel` | **DISABLED** — keep commented out in `conf.py`. Causes duplicate label warnings with CJK section titles |
| `sphinx_copybutton` | Adds copy button to code blocks |
| `sphinx_rtd_theme` | ReadTheDocs theme |

### Theme

- **Theme**: `sphinx_rtd_theme`
- **Options**: flyout attached, version/language selectors disabled
- **GitHub integration**: Enabled, pointing to `sunfounder/pipower5` on the `docs` branch

### Custom Assets

- **JS**: `https://ezblock.cc/readDocFile/custom.js`, `./lang.js`
- **CSS**: `https://ezblock.cc/readDocFile/custom.css`
- **Template**: `_templates/layout.html` (SunFounder nav bar with logo)

### Multi-Language

The `lang.js` script in `_static/` handles automatic language detection and redirect. It supports `en`, `de`, `ja` and presents a notification bar when the browser language differs from the current page language.

The language variable in `conf.py` is set to `'en'` by default. When building for other languages:
- Set `language = '<locale>'` in `conf.py`
- Add `.po` translation files under `docs/source/locale/`

---

## Common Maintenance Tasks

### Adding a New Documentation Page

1. Create the `.rst` file in `docs/source/`
2. Define a `.. _ref_label:` at the top if the page will be cross-referenced
3. Add the file to the appropriate `.. toctree::` directive in `index.rst`
4. If new external links are needed, add `|link_xxx|` definitions to `conf.py` `rst_epilog`
5. Build locally to verify: `cd docs && make html`
6. Commit on `docs`

### Updating the toctree Structure

The root toctree is in `index.rst`. It has four chapter groups:

1. **Getting Started**: About PiPower 5, assembly, quick guide
2. **Hardware Overview**: PiPower 5 HAT, battery
3. **Software Configuration**: PiPower 5 tool, firmware update, Python usage
4. **Appendix**: Compatible SBCs

Currently missing from the toctree: `use_with_arduino.rst` and `use_with_micropython.rst` — these files exist but are not included in any toctree.

### Adding Content with Include Markers

When content needs to be shared between pages:

1. Add `.. start_<marker>` before and `.. end_<marker>` after the reusable block
2. In the destination file, use:
   ```rst
   .. include:: /source_file.rst
       :start-after: start_<marker>
       :end-before: end_<marker>
   ```

### Modifying the Register Table

The I2C register table in `pipower_hat.rst` uses raw HTML tables with custom CSS. When editing:
- Keep the HTML structure intact
- Ensure the custom CSS class names (`custom-register-table`) are preserved
- The register addresses, data types, and descriptions must match the actual firmware

---

## Notes for AI Assistants

When working on this repository:

1. **The `docs` branch is documentation-only.** Source code lives on `main`. Do not add Python files, drivers, or installer scripts to `docs`.
2. **The Facebook community note** at the top of each `.rst` file is part of SunFounder's documentation standard. It appears in `index.rst`, `pipower5_software.rst`, and other user-facing pages.
3. **`conf.py` link substitutions** are the single source of external URLs. Never hardcode external links in `.rst` files — use `|link_xxx|` substitutions.
4. **Reference labels** (`.. _label:`) are code identifiers, not human-readable text. Never translate them.
5. **RST section underlines (and overlines) must match title display width.** 
   
   - For single-underline headings (title followed by `=` or `-`), the underline must be at least as long as the title text.
   - For overline+underline headings (e.g., `----` above and below the title), **both** the overline and underline must use the same character, be the **exact same length**, and be at least as long as the title. When translating titles, always update both lines together.
   - **CJK display width**: docutils counts CJK characters as **2 display columns** each (ASCII = 1 column). The overline/underline must match the total display width, not the character count. For example, `LED & ブザークイックリファレンス` = 6 ASCII columns + 13 CJK × 2 = 32 columns → needs ≥ 32 dashes.
   
   Translated titles are often longer than the English originals — extend overlines and underlines accordingly. When the title contains CJK characters, the underline/overline will be significantly longer than the character count suggests.
6. **Inline strong markup (`**...**`) breaks when adjacent to CJK characters.** docutils inline markup recognition requires the `**` delimiters to be adjacent to whitespace or ASCII punctuation (`- : / . , ; ! ? ' " ( ) [ ] { } < >`). CJK characters (Chinese, Japanese, Korean) are **not** valid delimiters.

   When `**text**` is immediately preceded or followed by a CJK character, docutils emits `WARNING: Inline strong start-string without end-string.` because it cannot find the closing `**`.

   **Fix**: Insert `\ ` (backslash-escaped space) between the `**` delimiter and the adjacent CJK character:

   .. code-block:: rst

      # WRONG — closing ** followed by CJK に, warning emitted:
      **PI3V3**にブリッジすると

      # RIGHT — \  acts as a valid delimiter:
      **PI3V3**\ にブリッジすると

      # WRONG — opening ** preceded by CJK は, warning emitted:
      または**コマンドラインツール**

      # RIGHT:
      または\ **コマンドラインツール**

   This applies equally to other inline markup (`*emphasis*`, ```literal```) when adjacent to CJK text. Always check the build warnings for "Inline ... start-string without end-string" after translating content with inline markup.
7. **Nested lists require blank lines and correct indentation in RST.** When a numbered list item or bullet item contains sub-bullets, a blank line must precede the nested list, and the nested items must be indented to align with the text of the parent item (typically 3+ spaces). Without the blank line, RST renders the bullets as a single run-on line.

   **Wrong** (sub-bullets without blank line):
   ```rst
   3. **Parent item**:
      - First sub-item
      - Second sub-item
   ```

   **Correct**:
   ```rst
   3. **Parent item**:

        - First sub-item
        - Second sub-item
   ```

8. **Code blocks** (Python, bash, shell) are never translated. Command strings and file paths stay as-is.
9. **The `_static` and `_templates` directories** contain custom assets. Changes here affect the global look and behavior of the published site.
10. **Build output** goes to `docs/build/` and is gitignored — never commit build artifacts.
11. **Images** are all under `docs/source/img/`. When adding new images, place them there and reference with relative paths.
12. **Register tables** in `pipower_hat.rst` use raw HTML. When updating register values, edit both the "Register Table" (read) and "Register Settings Table" (write) sections.
13. **The `show` script** at the repo root is a GPL license display utility — it is Python 2 syntax and should be considered legacy.
