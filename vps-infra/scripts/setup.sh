#!/usr/bin/env bash

set -euo pipefail

echo "============================================="
echo " Syncthing VPS Setup "
echo "============================================="

INFRA_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." &> /dev/null && pwd)"
DEFAULT_TZ="$(timedatectl show --property=Timezone --value 2>/dev/null || true)"
DEFAULT_TZ="${DEFAULT_TZ:-UTC}"

read -p "Timezone for the container [default: $DEFAULT_TZ]: " TZ_INPUT
TZ_VALUE="${TZ_INPUT:-$DEFAULT_TZ}"

PUID="$(id -u)"
PGID="$(id -g)"

echo "[+] Installing Docker & UFW..."
sudo apt update
sudo apt install -y docker.io docker-compose-v2 ufw

if ! groups "$USER" | grep -q '\bdocker\b'; then
    sudo usermod -aG docker "$USER"
    echo "[!] Added $USER to docker group. You may need to log out and back in later."
fi

echo "[+] Opening Syncthing sync ports in UFW..."
sudo ufw allow 22000/tcp || true
sudo ufw allow 22000/udp || true
sudo ufw reload || true

echo "[+] Opening Syncthing sync ports in local iptables..."
sudo iptables -C INPUT -p tcp --dport 22000 -j ACCEPT 2>/dev/null || sudo iptables -I INPUT -p tcp --dport 22000 -j ACCEPT
sudo iptables -C INPUT -p udp --dport 22000 -j ACCEPT 2>/dev/null || sudo iptables -I INPUT -p udp --dport 22000 -j ACCEPT

echo "[+] Writing .env..."
{
    printf 'PUID=%s\n' "$PUID"
    printf 'PGID=%s\n' "$PGID"
    printf 'TZ=%s\n' "$TZ_VALUE"
} > "$INFRA_DIR/.env"

mkdir -p "$INFRA_DIR/data/config" "$INFRA_DIR/data/vault"

echo "[+] Starting Syncthing..."
cd "$INFRA_DIR"
sudo docker compose up -d

echo "============================================="
echo " Setup Complete "
echo
echo " Vault path on VPS: $INFRA_DIR/data/vault"
echo " GUI is bound to localhost only: http://127.0.0.1:8384"
echo
echo " Next Steps:"
echo " 1. SSH tunnel to the VPS: ssh -L 8384:127.0.0.1:8384 <user>@<vps>"
echo " 2. Open http://127.0.0.1:8384 locally and set a GUI username/password."
echo " 3. Add the VPS device to desktop and iPhone MobiusSync."
echo " 4. Share the folder backed by $INFRA_DIR/data/vault"
echo "============================================="
