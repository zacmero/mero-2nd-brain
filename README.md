# Obsidian Configuration & Sync Setup

This repository contains the configuration, styling, and hacking of the Obsidian vault (`mero-vault`).
To keep the main vault files synced securely and efficiently while allowing deep system changes, the `.obsidian` configuration is stored here and symlinked to the actual vault directory.

## Installation / Bootstrap
To set up this configuration on a new machine:
1. Clone this repository.
2. Run the appropriate script:
   - **Linux / macOS:** `./install.sh`
   - **Windows:** `.\install.ps1` (Requires running as Administrator or Developer Mode to create symlinks)

## Mobile Configuration & Git Automation

iOS does not handle symlinks well, meaning we cannot use the same symlinked `.obsidian` folder. Instead, the iPhone uses `.obsidian-mobile` as an override configuration folder.

To keep the mobile config version-controlled:
1. An automated **Git Hook** (`pre-commit`) has been added to this repository.
2. Every time you commit, it checks your local vault for `.obsidian-mobile/`.
3. If found, it uses `rsync` to pull those files into the `/obsidian-config-mobile/` directory inside this repo and automatically adds them to the commit.

You do **not** need to manually run scripts to update the mobile config. Just run `git commit` as usual.
