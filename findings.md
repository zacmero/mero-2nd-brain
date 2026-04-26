# Findings

- The vault is located at `/home/zacmero/Documents/mero-vault`.
- The configuration repo is at `/home/zacmero/projects/mero-2nd-brain`.
- Syncthing is actively syncing the vault files.
- The user had an issue where aggressive termination of `electron`/`obsidian` processes corrupted `~/.config/obsidian/obsidian.json`, causing the vault to "disappear". This has been fixed, but it serves as a strict boundary: DO NOT kill the Obsidian process directly.
- Templater is configured to trigger on file creation, matching the root path `/` and `""`.
- The index script is located at `Templates/Default.md`.