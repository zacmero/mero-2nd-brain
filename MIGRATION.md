# LiveSync to Syncthing Migration Runbook

This runbook is intentionally conservative. The goal is to preserve the newest vault data, including files that LiveSync incorrectly reports as corrupted.

## Rules
- Do not delete the old VPS stack until the newest iPhone edits exist in the raw Syncthing seed.
- Do not trust LiveSync "corrupted" labels as proof of file damage if the files open normally outside LiveSync.
- Treat the raw files as the source of truth during migration.

## Phase 1: Freeze and back up
1. Stop editing the vault on every device.
2. On the iPhone, copy/export the full vault as raw files to a safe backup location.
3. On the desktop, make a second raw backup of the current vault folder.
4. Keep both backups untouched.

## Phase 2: Recover the newest data
1. Inspect the specific note you edited on the iPhone and make sure that exact newer content exists in the iPhone raw backup.
2. Inspect the 3 files flagged by LiveSync as corrupted.
3. If those files open normally, keep them as-is in the backup; do not rewrite them just to satisfy LiveSync.
4. Build one merged raw vault copy that contains the newest correct version of every file.

## Phase 3: Prepare the VPS
1. Copy this repo to the VPS.
2. Run [`vps-infra/scripts/setup.sh`](/home/zacmero/projects/mero-2nd-brain/vps-infra/scripts/setup.sh).
3. Put the merged raw vault into `vps-infra/data/vault` on the VPS.
4. Open the Syncthing GUI through SSH tunneling and set GUI authentication.

## Phase 4: Converge devices
1. Connect the desktop to the VPS Syncthing node.
2. Let the desktop fully sync and verify its vault matches the merged seed copy.
3. Install/configure MobiusSync on the iPhone against the VPS Syncthing node.
4. Let the iPhone reconcile against the same raw vault.
5. Confirm the previously problematic files open normally on both sides.

## Phase 5: Remove old sync infrastructure
1. Disable LiveSync in Obsidian on desktop.
2. Disable/remove LiveSync on iPhone after the Syncthing copy is confirmed.
3. On the VPS, run [`vps-infra/scripts/remove-legacy-stack.sh`](/home/zacmero/projects/mero-2nd-brain/vps-infra/scripts/remove-legacy-stack.sh).
4. Rotate any old CouchDB/LiveSync secrets.

## Validation checklist
- The newest iPhone-only edit exists in the raw vault on desktop and VPS.
- The 3 falsely-corrupted files open normally from the Syncthing-backed vault.
- Syncthing reports the folder in sync.
- No device still depends on CouchDB to fetch vault content.
