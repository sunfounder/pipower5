#!/usr/bin/env python3


import os
from os import path
import sys

here = path.abspath(path.dirname(__file__))
os.chdir(here)
sys.path.append('./pipower5')
sys.path.append('./tools')

from sf_installer import SF_Installer
from version import __version__

DASHBOARD_VERSION = '1.3.x'
SF_RPI_STATUS_VERSION = '1.1.7'

GITHUB_URL = 'https://github.com/sunfounder/'
GITEE_URL = 'https://gitee.com/sunfounder/'

# Test if github url reachable
import requests
try:
    requests.get(GITHUB_URL)
    GIT_URL = GITHUB_URL
except requests.exceptions.RequestException:
    print(f"Warning: {GITHUB_URL} is not reachable")
    try:
        requests.get(GITEE_URL)
        GIT_URL = GITEE_URL
    except requests.exceptions.RequestException:
        print(f"Error: {GITEE_URL} is not reachable")
        exit(1)


settings = {
    # - Setup venv options if needed, default to []
    'venv_options': [
        '--system-site-packages',
    ],

    # - Build required apt dependencies, default to []
    # 'build_dependencies': [
    #     'curl', # for influxdb key download
    # ],

    # - Before install script, default to {}
    'run_commands_before_install': {
        'Create pipower5 directory': 'mkdir -p /opt/pipower5',
        'Copy email template': 'cp -r email_templates /opt/pipower5/email_templates',
        'Install battery device': 'cd driver && bash install.sh && cd ..',
    },

    # - Install from apt
    'apt_dependencies': [
        'kmod',
        'i2c-tools',
    ],

    # - Install from pip
    # 'pip_dependencies': [
    #     'gpiozero',
    # ],

    # - Install python source code from git
    'python_source': {
        'pipower5': './',
        'sf_rpi_status': f'git+{GIT_URL}sf_rpi_status.git@{SF_RPI_STATUS_VERSION}',
    },

    # create symbolic links from venv/bin/ to /usr/local/bin/
    'symlinks':
    [
        'pipower5',
    ],

    # - Setup config txt
    # 'config_txt':  {
    #     'dtparam=spi': 'on',
    #     'dtparam=i2c_arm': 'on',
    #     'dtoverlay=gpio-ir,gpio_pin': '13',
    # },

    # add modules
    # sudo nano /etc/modules
    'modules': [
        "i2c-dev",
    ],
    # - Autostart settings
    # - Set service filenames
    'service_files': ['pipower5.service'],
    # - Set bin files
    'bin_files': [],
    # - Copy device tree overlay to /boot/overlays
    'dtoverlays': ['sunfounder-pipower5.dtbo'],
}

dashboard_settings = {
    'build_dependencies': [
        'curl', # for influxdb key download
    ],
    'run_commands_before_install': {
        'Setup InfluxDB': 'bash scripts/setup_influxdb.sh',
        # 'Update APT': 'apt-get update',
    },
    'apt_dependencies': [
        'influxdb', # for pm_dashboard
        'lsof', # for pm_dashboard
    ],
    'python_source': {
        'pm_dashboard': f'git+{GIT_URL}pm_dashboard.git@{DASHBOARD_VERSION}',
    },
}

installer = SF_Installer(
    name= 'pipower5',
    friendly_name= 'PiPower 5',
    # - Setup install command description if needed, default to "Installer for {friendly_name}""
    # 'description': 'Installer for PiPower 5',
    # - Setup Work Dir if needed, default to /opt/{name}
    # 'work_dir': '/opt/pipower5',
    # - Setup log dir if needed, default to /var/log/{name}
    # 'log_dir': '/var/log/pipower5',
)

installer.parser.add_argument("--disable-dashboard", action='store_true', help="Disable dashboard")
installer.update_settings(settings)
args = installer.parser.parse_args()
if not args.disable_dashboard:
    installer.update_settings(dashboard_settings)
installer.main()
