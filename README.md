# OLED Netinfo (Raspberry Pi)

Kleines Tool zur Anzeige von Host-/Netzwerk-Infos auf einem Waveshare 0.91" OLED (128x32).

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py

## Systemd-Installation

```bash
# Code an Zielort bringen (z. B. /opt) und venv anlegen
sudo mkdir -p /opt/oled_netinfo
sudo rsync -a ./ /opt/oled_netinfo/
sudo chown -R pi:pi /opt/oled_netinfo

cd /opt/oled_netinfo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Units installieren
./scripts/install-systemd.sh