# Obsidian VPS Infrastructure

This directory now provisions a **Syncthing node** for the raw vault files.

## Scope
- This repo-managed stack is only for vault sync.
- It does **not** manage or remove unrelated VM services.
- The legacy CouchDB/Caddy stack can be removed with `scripts/remove-legacy-stack.sh`, which only touches containers and files owned by this repo directory.

## Why this replaces LiveSync
- Raw `.md`, `.txt`, `.pdf`, and attachment files live directly on disk on the VPS.
- Syncthing moves files, not chunked database documents.
- The VPS can serve as the always-on peer for desktop, iPhone/MobiusSync, and later any web tooling you want to point at the vault path.

## What gets created
- `data/config`: Syncthing config and device state
- `data/vault`: the actual synced vault contents
- `.env`: local runtime values for UID/GID/timezone

## Initial setup on the VPS
1. Copy this repository to the VPS.
2. Change into this directory: `cd mero-2nd-brain/vps-infra`
3. Run `./scripts/setup.sh`
4. Create an SSH tunnel from your local machine:
   `ssh -L 8384:127.0.0.1:8384 <user>@<vps>`
5. Open `http://127.0.0.1:8384`
6. Set a Syncthing GUI username/password immediately.
7. Add the desktop and iPhone MobiusSync as peers.
8. Share the folder backed by `data/vault`

## Seed The Vault From Arch
After the VPS Syncthing node is up, copy your real vault from Arch into `vps-infra/data/vault`.

From your Arch machine:

```bash
rsync -a --delete /home/zacmero/Documents/mero-vault/ <user>@<vps>:/path/to/mero-2nd-brain/vps-infra/data/vault/
```

Important:
- keep `.stignore` included in the vault copy
- `.obsidian` stays excluded if your `.stignore` contains `.obsidian`
- `.obsidian-mobile` can sync normally when it exists

## Safe cutover from LiveSync
1. Freeze writes while you migrate.
2. Make a raw backup of the vault from the iPhone and from the desktop.
3. Manually confirm the newest iPhone edits and the 3 falsely-"corrupted" text files exist as normal files in the backup.
4. Choose one merged raw vault copy as the Syncthing seed, and place it in `data/vault`.
5. Bring Syncthing online and let the desktop sync first.
6. Verify the desktop vault matches the seed copy.
7. Connect iPhone/MobiusSync and let it reconcile against the same raw files.
8. Only after that, disable/remove LiveSync on the devices and remove the legacy VPS stack.

## Legacy stack removal
Run this from `vps-infra` on the VPS:

```bash
./scripts/remove-legacy-stack.sh
```

What it removes:
- the old `couchdb` container if it is owned by this repo path
- the old `caddy` container if it is owned by this repo path
- `vps-infra/.env`
- `vps-infra/Caddyfile`
- `vps-infra/dbdata`

What it does **not** remove:
- other Docker containers
- other Caddy instances not owned by this repo path
- anything outside this repo's `vps-infra` directory

## Notes
- Only ports `22000/tcp` and `22000/udp` are opened for sync traffic.
- The Syncthing GUI stays bound to localhost on the VPS; administer it through SSH tunneling instead of exposing it publicly.
- At the cloud provider layer, allow only `22000/tcp` and `22000/udp`. Do not expose `8384` publicly.
- After migration, rotate any secrets that were previously stored for LiveSync/CouchDB.
