# Project overview
- Repo: `/home/zacmero/projects/mero-2nd-brain`
- Purpose: Obsidian config + raw-file sync repo for `mero-vault`; includes Kindle-to-vault automation and VPS Syncthing infra.
- Actual vault path used during work: `/home/zacmero/Documents/mero-vault`
- Key areas:
  - `scripts/`: Kindle automation / promotion / autopull scripts
  - `kindle/`: Kindle sync docs and setup
  - `obsidian-config/` and `obsidian-config-mobile/`: Obsidian config snapshots
  - `vps-infra/`: Docker/Syncthing VPS stack
- No dedicated test suite found; validation is usually run scripts + inspect generated markdown.