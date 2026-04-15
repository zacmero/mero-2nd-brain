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

# 2. Install Dependencies (Ubuntu/Debian)
echo "[+] Installing Docker & UFW..."
sudo apt update
sudo apt install -y docker.io docker-compose-v2 ufw iptables-persistent

# Add user to docker group if not already
if ! groups $USER | grep -q '\bdocker\b'; then
    sudo usermod -aG docker $USER
    echo "[!] Added $USER to docker group. You may need to log out and back in later."
fi

# 3. Handle Oracle Cloud Specific Firewall (iptables)
# Oracle Cloud Ubuntu images block 80/443 at the iptables level by default
echo "[+] Opening ports 80 and 443 in local iptables..."
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT || true
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT || true
sudo netfilter-persistent save || true

# 4. Generate Caddyfile
echo "[+] Generating Caddyfile for $DOMAIN_NAME..."
cat << EOF > "$INFRA_DIR/Caddyfile"
$DOMAIN_NAME {
    reverse_proxy couchdb:5984
}
EOF

# 5. Generate .env file for Docker Compose
echo "[+] Generating .env file..."
cat << EOF > "$INFRA_DIR/.env"
DB_USER=admin
DB_PASSWORD=$DB_PASSWORD
EOF

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
