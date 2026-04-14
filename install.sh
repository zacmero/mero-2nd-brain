#!/usr/bin/env bash
# Obsidian Vault Git Environment Setup Script (Linux & macOS)

set -e

echo "==============================================="
echo " Setting up Obsidian Environment (Linux/macOS)"
echo "==============================================="

# Ask for vault path, default to ~/Documents/mero-vault
read -p "Enter path to your vault [default: $HOME/Documents/mero-vault]: " VAULT_DIR
VAULT_DIR=${VAULT_DIR:-"$HOME/Documents/mero-vault"}

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
CONFIG_SOURCE="$REPO_DIR/obsidian-config"

if [ ! -d "$VAULT_DIR" ]; then
    echo "[+] Creating vault directory at $VAULT_DIR..."
    mkdir -p "$VAULT_DIR"
fi

if [ -L "$VAULT_DIR/.obsidian" ]; then
    echo "[+] Symlink already exists. Re-creating to ensure correct path..."
    rm "$VAULT_DIR/.obsidian"
elif [ -d "$VAULT_DIR/.obsidian" ]; then
    echo "[!] Found physical .obsidian folder. Backing it up to .obsidian.bak..."
    mv "$VAULT_DIR/.obsidian" "$VAULT_DIR/.obsidian.bak"
fi

echo "[+] Linking $CONFIG_SOURCE -> $VAULT_DIR/.obsidian"
ln -s "$CONFIG_SOURCE" "$VAULT_DIR/.obsidian"

echo "==============================================="
echo " Setup Complete! "
echo " Remember to configure Syncthing to sync: $VAULT_DIR"
echo "==============================================="
