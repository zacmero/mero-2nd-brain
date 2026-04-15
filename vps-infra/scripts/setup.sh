#!/usr/bin/env bash

set -e

echo "============================================="
echo " Obsidian VPS Infrastructure Setup "
echo "============================================="

# 1. Variables
read -p "Enter your Domain Name (e.g., sync.mydomain.com): " DOMAIN_NAME
read -sp "Enter a strong Database Password: " DB_PASSWORD
echo ""

INFRA_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." &> /dev/null && pwd)"

# Normalize common copy/paste input like https://example.com/
DOMAIN_NAME="${DOMAIN_NAME#http://}"
DOMAIN_NAME="${DOMAIN_NAME#https://}"
DOMAIN_NAME="${DOMAIN_NAME%%/*}"

if [[ -z "$DOMAIN_NAME" ]]; then
    echo "[!] Domain name cannot be empty."
    exit 1
fi

if [[ -z "$DB_PASSWORD" ]]; then
    echo "[!] Database password cannot be empty."
    exit 1
fi

# 2. Install Dependencies (Ubuntu/Debian)
echo "[+] Installing Docker & UFW..."
sudo apt update
sudo apt install -y docker.io docker-compose-v2 ufw

# Add user to docker group if not already
if ! groups $USER | grep -q '\bdocker\b'; then
    sudo usermod -aG docker $USER
    echo "[!] Added $USER to docker group. You may need to log out and back in later."
fi

# 3. Open required ports locally
echo "[+] Opening ports 80 and 443 in UFW..."
sudo ufw allow 80/tcp || true
sudo ufw allow 443/tcp || true
sudo ufw reload || true

# Some cloud images also inject iptables rules outside UFW. Add non-persistent
# accepts so the stack can come up now; provider-level firewall rules must also allow 80/443.
echo "[+] Opening ports 80 and 443 in local iptables..."
sudo iptables -C INPUT -p tcp --dport 80 -j ACCEPT 2>/dev/null || sudo iptables -I INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -C INPUT -p tcp --dport 443 -j ACCEPT 2>/dev/null || sudo iptables -I INPUT -p tcp --dport 443 -j ACCEPT

# 4. Generate Caddyfile
echo "[+] Generating Caddyfile for $DOMAIN_NAME..."
cat << EOF > "$INFRA_DIR/Caddyfile"
$DOMAIN_NAME {
    reverse_proxy couchdb:5984
}
EOF

# 5. Generate .env file for Docker Compose
echo "[+] Generating .env file..."
{
    printf 'DB_USER=admin\n'
    printf 'DB_PASSWORD=%s\n' "$DB_PASSWORD"
} > "$INFRA_DIR/.env"

# 6. Create Database Data Directory
mkdir -p "$INFRA_DIR/dbdata"

# 7. Start the Stack
echo "[+] Starting up CouchDB and Caddy..."
cd "$INFRA_DIR"
sudo docker compose up -d

echo "============================================="
echo " Setup Complete! "
echo " "
echo " Database Address: https://$DOMAIN_NAME"
echo " Username: admin"
echo " "
echo " Next Steps:"
echo " 1. Ensure your domain's DNS A Record points to this server's public IP."
echo " 2. Ensure your Cloud Provider's Web Firewall (e.g., Oracle VCN) allows Ingress on ports 80 and 443."
echo "============================================="
