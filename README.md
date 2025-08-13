# OLED Netinfo (Raspberry Pi)

Kleines Tool zur Anzeige von Host-/Netzwerk-Infos auf einem Waveshare 0.91" OLED (128x32).
Repo zu Installation der Software zur Ansteuerung des OLED am MECH_LAB-RPi


## 1) Voraussetzungen
(Bei Bedarf prüfen - nicht immer zwingend erforderlich)
```bash
# System aktualisieren
sudo apt-get update
sudo apt-get -y upgrade

# Tools & Python-Grundlagen
sudo apt-get install -y git python3-venv python3-pip i2c-tools

# I²C aktivieren (interaktiv)
sudo raspi-config
# -> Interface Options -> I2C -> Enable
# danach rebooten:
sudo reboot
```

## 2) Überprüfen, ob Display erkannt wird (nach Reboot)
```bash
# Prüfen, ob das OLED (meist 0x3C) auf I²C sichtbar ist:
i2cdetect -y 1

# User pi sicherheitshalber in i2c-Gruppe aufnehmen (falls nicht schon geschehen)
sudo usermod -aG i2c pi
# (wirksam nach Reboot; oft nicht sofort nötig, wenn Service als root läuft – wir nehmen pi)
```

## 3) Code nach /opt bringen
```bash
cd /opt
sudo git clone https://github.com/<DEIN_GH_USERNAME>/oled_netinfo.git
sudo chown -R pi:pi /opt/oled_netinfo
cd /opt/oled_netinfo
```

## 4) Virtuelle Umgebung & Abhängigkeiten
```bash
# venv anlegen & aktivieren
python3 -m venv venv
source venv/bin/activate

# Abhängigkeiten installieren
pip install --upgrade pip
pip install -r requirements.txt

# Optional: Testlauf (manuell)
python main.py
deactivate
```

## 5) systemd-Units deployen
```bash
cd /opt/oled_netinfo
chmod +x scripts/install-systemd.sh
./scripts/install-systemd.sh
```
Das Script kopiert .service/.timer nach /etc/systemd/system/, lädt systemd neu und aktiviert Timer oder Service.


## 6) Vorgehen beim Update
```bash
d /opt/oled_netinfo
sudo -u pi git pull

# Abhängigkeiten ggf. aktualisieren
source venv/bin/activate
pip install -r requirements.txt
deactivate

# systemd neu laden (falls sich Unit-Dateien geändert haben)
sudo systemctl daemon-reload

# Neustart (abhängig vom Betriebsmodus)
sudo systemctl restart oled_netinfo.service           # bei Dauerbetrieb
# oder: beim Timer-Modus startet es beim nächsten Tick automatisch
#   (manuell anstoßen:)
sudo systemctl start oled_netinfo.service
```