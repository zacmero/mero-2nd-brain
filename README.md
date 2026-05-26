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

### Required sync apps
This repo does not install the file-sync apps for you.

- Desktop machines need **Syncthing** installed and running.
- iPhone/iPad devices need **Möbius Sync** installed and configured.

The repo assumes the raw vault files are synchronized by Syncthing/Möbius, while this repo only keeps the Obsidian config and VPS infra in sync.

### How to verify the sync service on this machine
If you are on Arch/Linux and this machine is meant to sync automatically, check:

```bash
systemctl --user status syncthing
```

Useful follow-ups:

```bash
journalctl --user -u syncthing -f
systemctl --user is-enabled syncthing
```

If `syncthing.service` is `active (running)` and `enabled`, this machine has a permanent user service watching the vault folder.

## Sync model
- `obsidian-config/`: versioned Obsidian desktop config
- `.obsidian-mobile/` inside the vault: iPhone override config when needed
- actual vault files: synced directly as files by Syncthing
- `vps-infra/`: Docker-based Syncthing node for the VPS

### Device roles
- Desktop: install Syncthing and keep it running as a user service.
- iPhone: install Möbius Sync and point it at the vault folder you want Obsidian to open.
- VPS: run the repo-managed Syncthing container under `vps-infra/`.
- Obsidian itself only reads/writes files; it does not perform the sync transport.

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

For the VPS, use the stack-aware installer instead:

```bash
./scripts/install-vps-autopull-systemd.sh
```

That variant does the same fast-forward pull, then refreshes `vps-infra/docker-compose.yml` with `docker compose up -d --remove-orphans` after a successful update.

## Mobile config workflow
- iPhone can use `.obsidian-mobile` as its override config folder.
- The local Git `pre-commit` hook copies `~/Documents/mero-vault/.obsidian-mobile/` into `obsidian-config-mobile/` inside this repo before each commit.
- That means iPhone-side config changes can still be captured in Git without syncing the desktop `.obsidian` symlink onto mobile.

## Templater workflow
The active desktop template lives in `~/Documents/mero-vault/Templates/Default.md` and is loaded automatically by Templater for new files.

### Active template behavior
- Keeps the note body clean at the top.
- Appends a metadata callout at the bottom.
- Uses Templater for static creation fields like `Created` and `UUID`.
- Uses Dataview inline metadata for the live `Modified` field:
  - `**Modified:** \`= dateformat(this.file.mtime, "yyyy-MM-dd HH:mm")\``
- The `Modified` line only evaluates if Dataview is enabled on the device.

### Backup template
- `~/Documents/mero-vault/Templates/Default_bak.md` is the backup copy.
- Leave it untouched unless you are intentionally migrating template behavior.

### Daily note template
- `~/Documents/mero-vault/Templates/daily_notes.md` is the fast daily-diary template.
- It is designed for low-friction journaling when you want a quick daily entry instead of a structured project note.
- It can be assigned in Templater or used manually as a starting point.

### Attachment folder rule
- Both desktop and mobile should use `Attachments` as the Obsidian attachment folder.
- Keep the folder name plain ASCII. Avoid emoji or alternate variants like `Attachments 📎`, because they create duplicate attachment trees and break path consistency.
- If you rename the attachment folder, do it inside Obsidian so `alwaysUpdateLinks` can update the references. External renames can leave old links behind.
- New attachments from iPhone should land in `Attachments/` once `.obsidian-mobile/app.json` has the same `attachmentFolderPath` setting as desktop.

## Sync health checklist
When a device is not syncing, check the app/service first:

- Desktop/Linux:
  - `systemctl --user status syncthing`
  - `journalctl --user -u syncthing -f`
- iPhone:
  - open Möbius Sync and confirm the folder/device shows connected
  - if iOS suspended the app, bring Möbius to the foreground to force a sync pass
- VPS:
  - `docker ps`
  - `docker logs mero-syncthing`

If Syncthing reports NAT-PMP/UPnP port mapping failures, that usually means the router refused automatic port forwarding or the port is already occupied. It is not always fatal, but direct connectivity is better if port `22000` is reachable.

## Existing LiveSync installs
This repo no longer treats LiveSync/CouchDB as the source of truth.

Before removing LiveSync from existing devices:
1. Back up the raw vault from iPhone and desktop.
2. Merge any unsynced changes, especially files flagged as "corrupted" by LiveSync even though they open normally.
3. Seed Syncthing with the confirmed-good raw vault.
4. After all devices converge on the same files, disable or uninstall LiveSync locally.
