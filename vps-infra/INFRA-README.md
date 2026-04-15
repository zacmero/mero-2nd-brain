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
2. Navigate to this directory: `cd mero-2nd-brain/vps-infra`
3. Run the setup script: `./scripts/setup.sh`
4. Follow the prompts to enter your domain name and set a secure database password.

The script will automatically install Docker, open local OS firewalls, configure the required CORS settings for Obsidian, and spin up Caddy (for auto-SSL) and CouchDB.

---

## ⚠️ Obsidian LiveSync Setup & Known UI Traps
*Read this before configuring the plugin on a new device.*

### 1. Connecting the Desktop (The Master Upload)
1. Install **Self-hosted LiveSync**.
2. **DO NOT** use the "Setup URI" wizard box for your standard web URL (it expects an encrypted string, not `https://...`). Instead, go to the **Remote Configuration** tab and enter your URI, username (`admin`), and database password.
3. **CRITICAL:** Under the **Sync Settings** tab, ensure **Hidden File Sync** and **Customisation Sync** are disabled. Exclude `^\.obsidian/`, `^\.obsidian-mobile/`, and `^\.git/`.
4. Click **Replicate Now -> Push local to remote**. This will declare the desktop vault as the master and begin chunking your files to the server.

### 2. The "Broken Files Detected" Bug
When you first enable the plugin, you might get a terrifying pop-up stating: **"Due to a recent bug... some files may not have been saved correctly in the sync database."**
- **Don't Panic.** This is a known plugin quirk where its internal scanner trips over attachments. 
- **Fix:** Just click the **Fix** button at the bottom of the prompt and let it heal itself.

### 3. The "Fetch Remote Configuration Failed" Error
Right after connecting to the database for the first time, you may see this error. 
- **Why:** The plugin is looking for server configurations, but because you just spun up the VPS, the database is completely empty.
- **Fix:** Click **Skip and proceed**. The configurations will be created upon your first push.

### 4. Connecting Mobile Devices (iPhone/iPad)
1. On the desktop, go to LiveSync Settings -> **Wizard Icon (🧙‍♂️)** -> **Show QR code** (Under "To setup other devices"). *Type your database password if it asks for a passphrase.*
2. On the mobile device, ensure Settings > About > Advanced > **Override config folder** is set to `.obsidian-mobile`.
3. Install LiveSync, open its settings, and scan the QR code.
4. When prompted with 3 options, select **Option 2: "My remote server is already set up. I want to join this device."**
5. Select **Fetch from remote** to download the vault.

### 5. Mobile Sync "Read Errors"
During a massive initial download (1GB+) to an iPhone, you will see a stream of notifications saying **"Something went wrong on reading..."**
- **Why:** iOS severely restricts memory/network threads. The plugin trips over itself trying to read chunks that haven't fully downloaded.
- **Fix:** Ignore it. Do not close the app. LiveSync is eventually consistent. It will do a second/third pass automatically to grab missing chunks until the vault is complete.