# Repositorio de Documentación PiPower 5

> **Sincronizado desde la fuente canónica.** Este CLAUDE.md está sincronizado desde el repositorio fuente en inglés (rama `docs`). La versión autoritativa reside en el espacio de trabajo principal. Esta rama: `docs-es` — Traducción al español.

## Identidad del Proyecto

| Campo | Valor |
|---|---|
| **Producto** | SunFounder PiPower 5 — UPS HAT para Raspberry Pi |
| **Repositorio** | `https://github.com/sunfounder/pipower5` |
| **Documentación** | Sphinx + ReadTheDocs (`sphinx_rtd_theme`) |
| **Publicado en** | `https://docs.sunfounder.com/projects/pipower5/<lang>/latest/` |
| **Empresa** | SunFounder (service@sunfounder.com) |
| **Licencia** | GPL v2 |

Este repositorio en la rama `docs` contiene **solo documentación** para el PiPower 5 UPS HAT. El código de la biblioteca Python (`pipower5`), el controlador del kernel y el instalador residen en la rama `main`. La rama `docs` construye un sitio de documentación Sphinx a través de ReadTheDocs.

---

## Estrategia de Ramas

| Rama | Rol |
|---|---|
| `main` | Código fuente Python, controlador del kernel, instalador, ejemplos |
| `docs` | **Fuente de documentación** — archivos RST de Sphinx, imágenes, configuración RTD |

### Regla Fundamental

> **`docs` es la rama de documentación.** Todos los cambios de documentación (contenido, estructura, imágenes, configuración) ocurren en `docs`. La rama `main` es para la biblioteca Python y el código del controlador. Estas dos ramas tienen propósitos diferentes y no deben confundirse.

---

## Estructura del Repositorio (rama docs)

```
pipower5/
├── .readthedocs.yaml          # Configuración de compilación RTD (Sphinx 7.3.7, Python 3.11, Ubuntu 22.04)
├── .gitignore                 # Ignora: .vscode, build/, archivos secretos
├── LICENSE                    # GPL v2
├── README.md                  # Descripción general del producto + enlaces rápidos
├── show                       # Script de visualización de licencia/garantía
├── CLAUDE.md                  # Este archivo — guía para asistentes AI
└── docs/
    ├── requirements.txt       # sphinx==7.3.7, sphinx_rtd_theme==3.0.2, sphinx_copybutton
    ├── Makefile / make.bat    # Compilación Sphinx (SOURCEDIR=source, BUILDDIR=build)
    └── source/
        ├── conf.py            # Configuración Sphinx: extensiones, tema, JS/CSS, enlaces rst_epilog
        ├── index.rst          # Índice raíz — Inicio + Hardware + Software + Apéndice
        ├── assembly.rst       # Instrucciones de montaje
        ├── quick_guide.rst    # Guía rápida de usuario
        ├── pipower_hat.rst    # Descripción general del hardware HAT (interfaz, especificaciones, alimentación, registros I2C)
        ├── battery.rst        # Guía de batería
        ├── pipower5_software.rst  # Herramienta de software (instalación, referencia CLI, panel, apagado, notificaciones)
        ├── update_firmware.rst    # Guía de actualización de firmware
        ├── use_with_python.rst    # Uso con Python (ejemplos, API)
        ├── use_with_arduino.rst   # Uso con biblioteca Arduino
        ├── use_with_micropython.rst  # Uso con biblioteca MicroPython
        ├── compatible_sbc.rst     # Lista de SBCs compatibles
        ├── faq.rst               # Preguntas frecuentes
        ├── troubleshooting.rst   # Guía de solución de problemas
        ├── _static/
        │   └── lang.js           # Script de redirección multi-idioma
        ├── _templates/
        │   └── layout.html       # Plantilla HTML Sphinx (barra de navegación SunFounder)
        └── img/                  # Todas las imágenes de documentación
```

---

## Convenciones de Documentación

### Etiquetas de Referencia RST

Cada archivo `.rst` puede definir una etiqueta de referencia para enlaces cruzados entre documentos:

| Etiqueta | Archivo | Contenido |
|---|---|---|
| `pipower5_assembly` | `assembly.rst` | Instrucciones de montaje |
| `pipower5_tool` | `pipower5_software.rst` | Referencia de la herramienta de software |
| `power_input` | `pipower_hat.rst` | Sección de entrada de alimentación |
| `power_button` | `pipower_hat.rst` | Sección del botón de encendido |
| `battery_indicators` | `pipower_hat.rst` | Sección de indicadores de batería |
| `battery_connector` | `pipower_hat.rst` | Sección del conector de batería |
| `cap_btn` | `pipower_hat.rst` | Sección del botón de encendido externo |
| `cap_sdsig` | `pipower_hat.rst` | Sección del jumper SDSIG |
| `cap_onoff` | `pipower_hat.rst` | Sección del jumper ON/OFF predeterminado |
| `pin_header` | `pipower_hat.rst` | Sección de pines para RPi |
| `pipower_software_python` | `use_with_python.rst` | Sección de uso con Python |

Estas etiquetas **deben permanecer consistentes** — son el mecanismo de enlace entre documentos.

### Directivas Include

Algunas páginas reutilizan contenido mediante directivas Sphinx `include` con marcadores `start-after` / `end-before`:

```rst
.. include:: /pipower5_software.rst
    :start-after: start_install_pipower5
    :end-before: end_install_pipower5
```

Los marcadores en el archivo fuente usan el formato:
```rst
.. start_install_pipower5

# ... contenido a incluir ...

.. end_install_pipower5
```

Al modificar contenido entre marcadores, asegúrese de que tanto el archivo fuente como todos los archivos que lo incluyen permanezcan consistentes.

### Sustituciones de Enlaces (`rst_epilog` en `conf.py`)

Todos los enlaces externos residen como sustituciones RST en `conf.py` bajo `rst_epilog`:

| Sustitución | Propósito |
|---|---|
| `\|link_sf_facebook\|` | Comunidad de Facebook de SunFounder |
| `\|link_german_tutorials\|` | Tutoriales en alemán (PiPower 3 — heredado) |
| `\|link_jp_tutorials\|` | Tutoriales en japonés (PiPower 3 — heredado) |
| `\|link_en_tutorials\|` | Tutoriales en inglés (PiPower 3 — heredado) |
| `\|link_PiPower_5_buy\|` | Enlace de compra |
| `\|link_PiPower_5\|` | Enlace del producto PiPower 5 |
| `\|link_spc_lib\|` | Biblioteca SPC I2C en GitHub |
| `\|link_pipower_tool\|` | Repositorio GitHub de la herramienta PiPower 5 |

Al agregar un nuevo enlace externo, añada la definición `|link_xxx|` a `conf.py` `rst_epilog`.

### Rutas de Imágenes

Todas las imágenes residen en `docs/source/img/` y se referencian en relación con el directorio fuente o con rutas absolutas:
```rst
.. image:: img/pipower5_ov.png
   :width: 100%

.. image:: img/power_input.png
   :width: 50%
   :align: center
```

### Nombrado de Archivos

- Hardware: `pipower_hat.rst`, `battery.rst` (snake_case)
- Software: `pipower5_software.rst` (snake_case)
- Guías: `quick_guide.rst`, `update_firmware.rst` (snake_case)
- Integración: `use_with_python.rst`, `use_with_arduino.rst`, `use_with_micropython.rst`

### Plantilla de Archivos RST

Cada archivo de lección/guía comienza con una nota de la comunidad de Facebook, seguida de la etiqueta de referencia (si la hay), luego el título:

```rst
.. note::

    Hello, welcome to the SunFounder Raspberry Pi & Arduino & ESP32 ...
    👉 Ready to explore and create with us? Click [|link_sf_facebook|] and join today!

.. _pipower5_tool:

PiPower 5 Tool
===============================
```

---

## Compilación y Vista Previa

### Compilación Local (Sphinx)

```bash
cd docs
pip install -r requirements.txt
make html          # Salida: docs/build/html/index.html
```

En Windows:
```batch
cd docs
make.bat html
```

### ReadTheDocs

Se compila automáticamente al hacer push a la rama `docs`. Configuración en `.readthedocs.yaml`:
- SO: Ubuntu 22.04, Python 3.11
- Configuración Sphinx: `docs/source/conf.py`
- Compila todos los formatos (HTML, PDF, ePub)

### URLs Publicadas

```
https://docs.sunfounder.com/projects/pipower5/en/latest/
```

---

## Configuración de Sphinx (conf.py)

### Extensiones

| Extensión | Propósito |
|---|---|
| `sphinx.ext.autosectionlabel` | **DESHABILITADO** — mantener comentado en `conf.py`. Causa advertencias de etiquetas duplicadas con títulos de sección CJK |
| `sphinx_copybutton` | Agrega botón de copia a los bloques de código |
| `sphinx_rtd_theme` | Tema ReadTheDocs |

### Tema

- **Tema**: `sphinx_rtd_theme`
- **Opciones**: flyout adjunto, selectores de versión/idioma deshabilitados
- **Integración GitHub**: Habilitada, apuntando a `sunfounder/pipower5` en la rama `docs`

### Recursos Personalizados

- **JS**: `https://ezblock.cc/readDocFile/custom.js`, `./lang.js`
- **CSS**: `https://ezblock.cc/readDocFile/custom.css`
- **Plantilla**: `_templates/layout.html` (barra de navegación SunFounder con logo)

### Multi-Idioma

El script `lang.js` en `_static/` maneja la detección automática de idioma y redirección. Soporta `en`, `de`, `ja` y presenta una barra de notificación cuando el idioma del navegador difiere del idioma de la página actual.

La variable de idioma en `conf.py` está configurada a `'en'` por defecto. Al compilar para otros idiomas:
- Configurar `language = '<locale>'` en `conf.py`
- Agregar archivos `.po` de traducción en `docs/source/locale/`

---

## Tareas Comunes de Mantenimiento

### Agregar una Nueva Página de Documentación

1. Crear el archivo `.rst` en `docs/source/`
2. Definir una `.. _ref_label:` al principio si la página tendrá referencias cruzadas
3. Agregar el archivo a la directiva `.. toctree::` apropiada en `index.rst`
4. Si se necesitan nuevos enlaces externos, agregar definiciones `|link_xxx|` a `conf.py` `rst_epilog`
5. Compilar localmente para verificar: `cd docs && make html`
6. Hacer commit en `docs`

### Actualizar la Estructura del toctree

El toctree raíz está en `index.rst`. Tiene cuatro grupos de capítulos:

1. **Primeros Pasos**: Acerca de PiPower 5, montaje, guía rápida
2. **Descripción General del Hardware**: PiPower 5 HAT, batería
3. **Configuración de Software**: Herramienta PiPower 5, actualización de firmware, uso con Python
4. **Apéndice**: SBCs compatibles

Actualmente faltan en el toctree: `use_with_arduino.rst` y `use_with_micropython.rst` — estos archivos existen pero no están incluidos en ningún toctree.

### Agregar Contenido con Marcadores Include

Cuando el contenido necesita ser compartido entre páginas:

1. Agregar `.. start_<marcador>` antes y `.. end_<marcador>` después del bloque reutilizable
2. En el archivo de destino, usar:
   ```rst
   .. include:: /archivo_fuente.rst
       :start-after: start_<marcador>
       :end-before: end_<marcador>
   ```

### Modificar la Tabla de Registros

La tabla de registros I2C en `pipower_hat.rst` utiliza tablas HTML sin procesar con CSS personalizado. Al editar:
- Mantener la estructura HTML intacta
- Asegurar que los nombres de clase CSS personalizados (`custom-register-table`) se conserven
- Las direcciones de registro, tipos de datos y descripciones deben coincidir con el firmware real

---

## Notas para Asistentes AI

Al trabajar en este repositorio:

1. **La rama `docs` es solo de documentación.** El código fuente reside en `main`. No agregue archivos Python, controladores o scripts de instalación a `docs`.
2. **La nota de la comunidad de Facebook** al principio de cada archivo `.rst` es parte del estándar de documentación de SunFounder. Aparece en `index.rst`, `pipower5_software.rst` y otras páginas orientadas al usuario.
3. **Las sustituciones de enlaces de `conf.py`** son la única fuente de URLs externas. Nunca codifique enlaces externos en archivos `.rst` — use sustituciones `|link_xxx|`.
4. **Las etiquetas de referencia** (`.. _label:`) son identificadores de código, no texto legible por humanos. Nunca las traduzca.
5. **Los subrayados de sección RST (y sobrelineados) deben coincidir con el ancho de visualización del título.** 
   
   - Para encabezados de subrayado simple (título seguido de `=` o `-`), el subrayado debe ser al menos tan largo como el texto del título.
   - Para encabezados con sobrelineado+subrayado (ej., `----` arriba y abajo del título), **ambos** el sobrelineado y el subrayado deben usar el mismo carácter, tener la **misma longitud exacta** y ser al menos tan largos como el título. Al traducir títulos, actualice siempre ambas líneas juntas.
   - **Ancho de visualización CJK**: docutils cuenta los caracteres CJK como **2 columnas de visualización** cada uno (ASCII = 1 columna). El sobrelineado/subrayado debe coincidir con el ancho total de visualización, no con el número de caracteres. Por ejemplo, `LED & ブザークイックリファレンス` = 6 columnas ASCII + 13 CJK × 2 = 32 columnas → necesita ≥ 32 guiones.
   
   Los títulos traducidos suelen ser más largos que los originales en inglés — extienda los sobrelineados y subrayados en consecuencia. Cuando el título contiene caracteres CJK, el subrayado/sobrelineado será significativamente más largo de lo que sugiere el número de caracteres.
6. **El marcado fuerte en línea (`**...**`) se rompe cuando está adyacente a caracteres CJK.** El reconocimiento de marcado en línea de docutils requiere que los delimitadores `**` estén adyacentes a espacios en blanco o puntuación ASCII (`- : / . , ; ! ? ' " ( ) [ ] { } < >`). Los caracteres CJK (chino, japonés, coreano) **no** son delimitadores válidos.

   Cuando `**texto**` está inmediatamente precedido o seguido por un carácter CJK, docutils emite `WARNING: Inline strong start-string without end-string.` porque no puede encontrar el `**` de cierre.

   **Solución**: Insertar `\ ` (espacio con barra invertida) entre el delimitador `**` y el carácter CJK adyacente:

   .. code-block:: rst

      # INCORRECTO — ** de cierre seguido de CJK に, se emite advertencia:
      **PI3V3**にブリッジすると

      # CORRECTO — \  actúa como delimitador válido:
      **PI3V3**\ にブリッジすると

      # INCORRECTO — ** de apertura precedido de CJK は, se emite advertencia:
      または**コマンドラインツール**

      # CORRECTO:
      または\ **コマンドラインツール**

   Esto se aplica igualmente a otros marcados en línea (`*énfasis*`, ```literal```) cuando están adyacentes a texto CJK. Siempre verifique las advertencias de compilación para "Inline ... start-string without end-string" después de traducir contenido con marcado en línea.
7. **Las listas anidadas requieren líneas en blanco e indentación correcta en RST.** Cuando un elemento de lista numerada o viñeta contiene sub-viñetas, una línea en blanco debe preceder la lista anidada, y los elementos anidados deben estar indentados para alinearse con el texto del elemento padre (típicamente 3+ espacios). Sin la línea en blanco, RST renderiza las viñetas como una sola línea continua.

   **Incorrecto** (sub-viñetas sin línea en blanco):
   ```rst
   3. **Elemento padre**:
      - Primer sub-elemento
      - Segundo sub-elemento
   ```

   **Correcto**:
   ```rst
   3. **Elemento padre**:

        - Primer sub-elemento
        - Segundo sub-elemento
   ```

8. **Los bloques de código** (Python, bash, shell) nunca se traducen. Las cadenas de comandos y rutas de archivos permanecen como están.
9. **Los directorios `_static` y `_templates`** contienen recursos personalizados. Los cambios aquí afectan la apariencia global y el comportamiento del sitio publicado.
10. **La salida de compilación** va a `docs/build/` y está en gitignore — nunca haga commit de artefactos de compilación.
11. **Las imágenes** están todas en `docs/source/img/`. Al agregar nuevas imágenes, colóquelas allí y referéncielas con rutas relativas.
12. **Las tablas de registros** en `pipower_hat.rst` usan HTML sin procesar. Al actualizar valores de registro, edite tanto las secciones "Register Table" (lectura) como "Register Settings Table" (escritura).
13. **El script `show`** en la raíz del repositorio es una utilidad de visualización de licencia GPL — tiene sintaxis Python 2 y debe considerarse heredado.
