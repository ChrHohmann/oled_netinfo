#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="oled_netinfo"

# Stoppen & deaktivieren
sudo systemctl disable --now ${SERVICE_NAME}.timer 2>/dev/null || true
sudo systemctl disable --now ${SERVICE_NAME}.service 2>/dev/null || true

# Units entfernen
sudo rm -f /etc/systemd/system/${SERVICE_NAME}.timer
sudo rm -f /etc/systemd/system/${SERVICE_NAME}.service

# Reload
sudo systemctl daemon-reload
sudo systemctl reset-failed || true

echo "Entfernt. Prüfe mit: systemctl list-timers | grep ${SERVICE_NAME}  /  systemctl status ${SERVICE_NAME}.service"