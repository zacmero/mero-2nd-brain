# Obsidian VPS Infrastructure

This directory contains the necessary infrastructure as code to run a self-hosted CouchDB instance for the Obsidian Self-hosted LiveSync plugin.

## How it relates to your Vault
- **Syncthing / Git:** Handles your `.obsidian` configurations and plugin settings.
- **CouchDB (This VPS):** Handles the high-speed, always-on synchronization of your actual Markdown text, PDFs, and images.

## Prerequisites
1. A Linux VPS (Tested on Ubuntu 24.04 ARM64 / Oracle Cloud Free Tier).
2. A Domain Name pointing to the public IP of the VPS (e.g., `sync.mydomain.com`).
3. Port 80 and 443 opened on your Cloud Provider's Web Dashboard (e.g., Oracle VCN Security Rules).

## Installation

1. Copy this entire repository to your VPS (e.g., `git clone` or `rsync`).
2. Navigate to this directory:
   ```bash
   cd mero-2nd-brain/vps-infra
   ```
3. Run the setup script:
   ```bash
   ./scripts/setup.sh
   ```
4. Follow the prompts to enter your domain name and set a secure database password.
   Use only the hostname, for example `mero-vault.duckdns.org`, not `https://mero-vault.duckdns.org`.

The script will automatically install Docker, open local OS firewalls, configure the required CORS settings for Obsidian, and spin up Caddy (for auto-SSL) and CouchDB.

## DNS Setup
Before running the installer, make sure your domain resolves to the VPS public IP.

For DuckDNS:
1. Find the VPS public IP:
   ```bash
   curl -4 ifconfig.me
   ```
2. Log in to DuckDNS and open your subdomain settings.
3. Point the subdomain (for example `mero-vault.duckdns.org`) to that public IP.
4. Verify DNS from the VPS:
   ```bash
   dig +short mero-vault.duckdns.org
   ```
   If `dig` is not installed:
   ```bash
   getent hosts mero-vault.duckdns.org
   ```
5. Confirm the returned IP matches the VPS public IP before starting the stack.

## Generated Local Files
The installer creates runtime files that should not be committed:
- `vps-infra/.env`
- `vps-infra/Caddyfile`
- `vps-infra/dbdata/`

## Connecting Obsidian
1. Install the **Self-hosted LiveSync** plugin in Obsidian.
2. Enter your setup Server URI: `https://your-domain.com`
3. Enter your Username: `admin`
4. Enter the Password you created during setup.
5. **IMPORTANT:** In the LiveSync settings, configure the "Hidden File Sync" to **EXCLUDE** the `.obsidian` and `.obsidian-mobile` directories to prevent conflicts with your Git setup.
