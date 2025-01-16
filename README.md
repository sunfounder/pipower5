# pipower5
Python Library for PiPower5


### Debug

Clone the dependency you want to debug or edit

```bash
git clone https://github.com/sunfounder/pipower5.git
git clone https://github.com/sunfounder/pm_dashboard.git
git clone https://github.com/sunfounder/sf_rpi_status.git
```

Make adjustments, and manually install the package

```bash
cd ~/pipower5 && sudo /opt/pipower5/venv/bin/pip3 uninstall pipower5 -y && sudo /opt/pipower5/venv/bin/pip3 install .
cd ~/pm_dashboard && sudo /opt/pipower5/venv/bin/pip3 uninstall pm_dashboard -y && sudo /opt/pipower5/venv/bin/pip3 install .
cd ~/sf_rpi_status && sudo /opt/pipower5/venv/bin/pip3 uninstall sf_rpi_status -y && sudo /opt/pipower5/venv/bin/pip3 install .
```

Start/stop the service for debug

```
sudo systemctl stop pipower5.service
sudo systemctl start pipower5.service
sudo systemctl restart pipower5.service
sudo pipower5 start

sudo /opt/pipower5/venv/bin/python3
```
