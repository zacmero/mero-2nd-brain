# Obsidian Configuration & Raw-File Sync

This repository stores the Obsidian configuration for `mero-vault` and the VPS infrastructure used to keep the vault available as **raw files**.

The intent is:
- the vault contents sync through Syncthing
- the `.obsidian` config stays versioned here and is symlinked into the real vault on desktop systems
- the VPS holds an always-on raw copy of the vault for automation and later web access

## Installation / Bootstrap
To set up this configuration on a new desktop machine:
1. Clone this repository.
2. Run the appropriate script:
   - Linux / macOS: `./install.sh`
   - Windows: `.\install.ps1`
3. Point Syncthing at the vault directory printed by the installer.

## Sync model
- `obsidian-config/`: versioned Obsidian desktop config
- `.obsidian-mobile/` inside the vault: iPhone override config when needed
- actual vault files: synced directly as files by Syncthing
- `vps-infra/`: Docker-based Syncthing node for the VPS

## Mobile config workflow
- iPhone can use `.obsidian-mobile` as its override config folder.
- The local Git `pre-commit` hook copies `~/Documents/mero-vault/.obsidian-mobile/` into `obsidian-config-mobile/` inside this repo before each commit.
- That means iPhone-side config changes can still be captured in Git without syncing the desktop `.obsidian` symlink onto mobile.

## Existing LiveSync installs
This repo no longer treats LiveSync/CouchDB as the source of truth.

Before removing LiveSync from existing devices:
1. Back up the raw vault from iPhone and desktop.
2. Merge any unsynced changes, especially files flagged as "corrupted" by LiveSync even though they open normally.
3. Seed Syncthing with the confirmed-good raw vault.
4. After all devices converge on the same files, disable or uninstall LiveSync locally.
