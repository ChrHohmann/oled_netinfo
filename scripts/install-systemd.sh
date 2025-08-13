#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="oled_netinfo"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 1) Units nach /etc/systemd/system/ kopieren
sudo cp "${SRC_DIR}/systemd/${SERVICE_NAME}.service" /etc/systemd/system/
sudo cp "${SRC_DIR}/systemd/${SERVICE_NAME}.timer"   /etc/systemd/system/ || true  # falls kein Timer gewünscht, Zeile auskommentieren

# 2) Rechte & Eigentümer sinnvoll setzen (Units gehören root)
sudo chown root:root /etc/systemd/system/${SERVICE_NAME}.service
[ -f /etc/systemd/system/${SERVICE_NAME}.timer ] && sudo chown root:root /etc/systemd/system/${SERVICE_NAME}.timer

# 3) systemd neu laden
sudo systemctl daemon-reload

# 4) Aktivieren/Starten
# Wenn du den Timer nutzt:
if [ -f /etc/systemd/system/${SERVICE_NAME}.timer ]; then
  sudo systemctl enable --now ${SERVICE_NAME}.timer
  echo ">> ${SERVICE_NAME}.timer aktiviert. Status:"
  systemctl status ${SERVICE_NAME}.timer --no-pager || true
else
  # Alternativ: Service dauerhaft
  sudo systemctl enable --now ${SERVICE_NAME}.service
  echo ">> ${SERVICE_NAME}.service aktiviert. Status:"
  systemctl status ${SERVICE_NAME}.service --no-pager || true
fi

echo "Hinweis: Logs mit 'journalctl -u ${SERVICE_NAME}.service -f'"
