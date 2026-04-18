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

## Auto pull on always-on machines
If a machine should stay close to the latest repo state, install the user timer:

```bash
./scripts/install-autopull-systemd.sh
```

Optional:

```bash
./scripts/install-autopull-systemd.sh --interval 5 --linger
```

What it does:
- installs a `systemd --user` timer and service for this repo
- runs a conservative pull loop every few minutes
- only fast-forwards from `origin/<current-branch>`
- skips pulls when the working tree has local changes or untracked files
- never merges or resets your local work

Operational commands:
- check status: `systemctl --user status mero-2nd-brain-autopull.timer`
- view logs: `journalctl --user -u mero-2nd-brain-autopull.service -f`
- run once manually: `~/.local/share/mero-2nd-brain-autopull/pull.sh`
- disable: `systemctl --user disable --now mero-2nd-brain-autopull.timer`

If you want the timer to run on a headless VM without an active login session, pass `--linger` once during install. That enables user lingering for the current account and is the lightweight way to keep a user service alive across reboots.

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
