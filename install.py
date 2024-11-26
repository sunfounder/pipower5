#!/usr/bin/env python3

from tools.sf_installer import SF_Installer

installer = SF_Installer(
    name='pipower5',
    friendly_name='PiPower 5',

    # - Setup install command description if needed, default to "Installer for {friendly_name}""
    # description='Installer for PiPower 5',

    # - Setup venv options if needed, default to []
    venv_options=[
        '--system-site-packages',
    ],

    # - Setup Work Dir if needed, default to /opt/{name}
    # work_dir='/opt/pipower5',

    # - Setup log dir if needed, default to /var/log/{name}
    # log_dir='/var/log/pipower5',

    # - Install from apt
    apt_dependencies=[
    ],

    # - Install from pip
    # pip_dependencies=[
    #     'influxdb',
    #     'Pillow',
    #     'adafruit-circuitpython-ssd1306',
    # ]

    # - Install python source code from git
    python_source={
        'pipower5': './',
        'spc': 'git+http://github.com/sunfounder/spc.git',
    },

    # - Setup config txt
    # config_txt = {
    #     'dtparam=spi': 'on',
    #     'dtparam=i2c_arm': 'on',
    #     'dtoverlay=gpio-ir,gpio_pin': '13',
    # },

    # - Autostart settings
    # - Set service filenames
    service_files = ['pipower5.service'],
    # - Set bin files
    bin_files = ['pipower5'],

    # - Copy device tree overlay to /boot/overlays
    # dtoverlay = [],
    dtoverlay = ['sunfounder-pipower5.dtbo'],

)
installer.install()
