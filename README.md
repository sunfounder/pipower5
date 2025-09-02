# PiPower 5

## Installation

Install the required packages:

```bash
sudo apt-get update
sudo apt-get install git python3-pip python3-dev python3-setuptools
```

Install PiPower 5
```bash
sudo python install.py
```

> Note: This will also install a dashboard to monitor the PiPower 5 and your Raspberry Pi. If you don't need it, you can add a flag `--disable-dashboard` to the installation command.
> ```bash
> sudo python install.py --disable-dashboard
> ```
> Or you can uninstall the dashboard later by cli
> ```bash
> sudo pipower5 --remove-dashboard
> ```

## Debug

Clone the dependency you want to debug or edit

```bash
git clone https://github.com/sunfounder/pipower5.git
git clone https://github.com/sunfounder/pm_dashboard.git
git clone https://github.com/sunfounder/sf_rpi_status.git
```

Make adjustments, and manually install the package

```bash
cd ~/pipower5 && sudo rm -rf build pipower5.egg-info && sudo /opt/pipower5/venv/bin/pip3 uninstall pipower5 -y && sudo /opt/pipower5/venv/bin/pip3 install . --no-build-isolation
cd ~/pm_dashboard && sudo rm -rf build pm_dashboard.egg-info && sudo /opt/pipower5/venv/bin/pip3 uninstall pm_dashboard -y && sudo /opt/pipower5/venv/bin/pip3 install . --no-build-isolation
cd ~/pm_auto && sudo rm -rf build pm_auto.egg-info && sudo /opt/pipower5/venv/bin/pip3 uninstall pm_auto -y && sudo /opt/pipower5/venv/bin/pip3 install . --no-build-isolation
cd ~/sf_rpi_status && sudo rm -rf build sf_rpi_status.egg-info && sudo /opt/pipower5/venv/bin/pip3 uninstall sf_rpi_status -y && sudo /opt/pipower5/venv/bin/pip3 install . --no-build-isolation
sudo /opt/pipower5/venv/bin/pip3 uninstall spc -y && sudo /opt/pipower5/venv/bin/pip3 install git+https://github.com/sunfounder/spc.git --no-build-isolation

```

Start/stop the service for debug

```
sudo systemctl stop pipower5.service
sudo systemctl start pipower5.service
sudo systemctl restart pipower5.service
sudo pipower5 start

sudo /opt/pipower5/venv/bin/python3
```

## Setting power-off singal for Pi 3B+ / Pi Zero
edit `/boot/firmware/config.txt` and add the following line:
```
dtoverlay=gpio-poweroff,gpio_pin=26,active_low=1
gpio=26=op,dh
```

