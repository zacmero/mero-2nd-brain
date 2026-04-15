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
4. Verify the container is running:
   `sudo docker ps`
5. Verify the vault path exists on the VPS:
   `ls -la /home/ubuntu/mero-2nd-brain/vps-infra/data/vault`

## Remove the old LiveSync stack
If this VPS previously ran the CouchDB/Caddy setup from this repo, remove it first:

```bash
cd /home/ubuntu/mero-2nd-brain/vps-infra
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

## Seed The Vault From Arch
After the VPS Syncthing node is up, copy your real vault from Arch into `vps-infra/data/vault`.

From your Arch machine:

```bash
rsync -a --delete /home/zacmero/Documents/mero-vault/ <user>@<vps>:/path/to/mero-2nd-brain/vps-infra/data/vault/
```

If you want visible progress:

```bash
rsync -avh --delete --info=progress2 /home/zacmero/Documents/mero-vault/ <user>@<vps>:/path/to/mero-2nd-brain/vps-infra/data/vault/
```

Important:
- keep `.stignore` included in the vault copy
- `.obsidian` stays excluded if your `.stignore` contains `.obsidian`
- `.obsidian-mobile` can sync normally when it exists
- if your source vault contains a local `.obsidian` symlink, remove that broken symlink from the VPS copy after seeding

## Open the VPS Syncthing UI
If your local machine already runs Syncthing on `127.0.0.1:8384`, do **not** tunnel the VPS to the same local port or you will just open your local Syncthing UI.

Use a different local port:

```bash
ssh -L 8385:127.0.0.1:8384 <user>@<vps>
```

Then open:

```text
http://127.0.0.1:8385
```

Set a GUI username/password immediately on the VPS UI.

## Add the VPS as a Syncthing device
The VPS has its own Syncthing device ID. Add that VPS device to your existing Arch Syncthing and your iPhone/MobiusSync.

Current VPS device ID:

```text
SLAMRST-76KO7YB-5Z3OTD6-FT27BFK-TIE2BKE-YCUZVID-W3NT5AJ-6XCZPQ2
```

### Arch side
1. Open your existing Arch Syncthing UI.
2. Click `Add Remote Device`.
3. Paste the VPS device ID.
4. Name it something like `mero-vps`.
5. Save.

### iPhone / MobiusSync side
1. Open MobiusSync.
2. Add a new remote device.
3. Paste the same VPS device ID.
4. Save.

### VPS side
1. In the VPS Syncthing UI, add your Arch device if it was not auto-added already.
2. In the VPS Syncthing UI, add your iPhone device ID.
3. Approve both remote devices on the VPS.

## Share the same vault folder across all three devices
Use a single folder ID across Arch, iPhone, and VPS. Do **not** create multiple vault folders for the same data.

Recommended folder ID:

```text
mero-vault
```

From Arch:
1. Open the existing vault folder in Syncthing.
2. Share it with both the iPhone and the VPS device.

From iPhone / MobiusSync:
1. Open the existing vault folder.
2. Make sure it is shared with both Arch and the VPS device.

From the VPS UI:
1. Accept the shared folder request.
2. Use the same folder ID already used by your existing peers.
3. Set the folder path to:
   ```text
   /data/vault
   ```

Important:
- on the VPS Syncthing UI, the correct folder path is `/data/vault`
- do **not** use the host path `/home/ubuntu/mero-2nd-brain/vps-infra/data/vault` in the Syncthing UI
- the host path is mounted into the container as `/data/vault`

## Expected final topology
At the end, all three devices should know each other directly:
- Arch knows iPhone and VPS
- iPhone knows Arch and VPS
- VPS knows Arch and iPhone

## Safe cutover from LiveSync
1. Freeze writes while you migrate.
2. Make a raw backup of the vault from the iPhone and from the desktop.
3. Manually confirm the newest iPhone edits and the previously problematic text files exist as normal files in the backup.
4. Choose one merged raw vault copy as the Syncthing seed, and place it in `data/vault`.
5. Bring Syncthing online and let the desktop sync first.
6. Verify the desktop vault matches the seed copy.
7. Connect iPhone/MobiusSync and let it reconcile against the same raw files.
8. Verify all three devices can connect directly.
9. Only after that, disable/remove LiveSync on the devices and remove the legacy VPS stack.

## Notes
- Only ports `22000/tcp` and `22000/udp` are opened for sync traffic.
- The Syncthing GUI stays bound to localhost on the VPS; administer it through SSH tunneling instead of exposing it publicly.
- At the cloud provider layer, allow only `22000/tcp` and `22000/udp`. Do not expose `8384` publicly.
- After migration, rotate any secrets that were previously stored for LiveSync/CouchDB.
