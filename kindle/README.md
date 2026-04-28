# Kindle-to-Vault Automation

This directory contains the infrastructure for syncing Kindle highlights (`My Clippings.txt`) to your Obsidian vault.

## Architecture Overview
The system relies on a lightweight **transport-and-process** pipeline. The Kindle does *not* do complex processing. It only initiates a secure transfer and triggers the processing on your VPS.

1.  **Transport (Kindle)**: A local `notesync` alias on the Kindle handles the `scp` transfer of the raw clippings file and triggers the remote script.
2.  **Processing (VPS)**: A Python script (`scripts/parse_clippings.py`) on the VPS receives, moves, parses, and hashes new highlights.
3.  **Storage (Vault)**: Processed highlights are appended to book-specific notes in the vault, maintaining integrity with `<!-- hash: ... -->` markers to prevent duplicates.
4.  **Synchronization (Syncthing)**: The vault is managed by Docker (volume: `./data/vault:/data/vault`). Syncthing inside the container sees the new book notes created by the parser script and propagates them to your local machines.

## 1. Kindle Setup (`/mnt/us/.profile`)
The Kindle runs the `ash` shell. Configuration is in `/mnt/us/.profile`. 

### The `notesync` Alias
This alias is designed for the `ash` shell. It:
1.  Prepares the SSH identity.
2.  Uses `scp` to send the clippings file to the VPS.
3.  Uses `ssh` to trigger the Python parser on the VPS.

```bash
alias notesync='cp /mnt/us/usbnet/id_ed25519 /tmp/id_ed25519 && chmod 600 /tmp/id_ed25519 && /mnt/us/usbnet/bin/scp -S /mnt/us/usbnet/bin/ssh -i /tmp/id_ed25519 -o StrictHostKeyChecking=accept-new "/mnt/us/documents/My Clippings.txt" ubuntu@204.216.172.41:"/home/ubuntu/mero-2nd-brain/vps-infra/data/vault/5_ Knowledge_Library/raw_book_notes/My Clippings.txt" && /mnt/us/usbnet/bin/ssh -i /tmp/id_ed25519 ubuntu@204.216.172.41 "/usr/bin/python3 /home/ubuntu/mero-2nd-brain/scripts/parse_clippings.py"'
```

## 2. VPS Processing (`scripts/parse_clippings.py`)
This script resides on the VPS host.
- **Paths**: It uses absolute paths to map the host directory to the Docker volume path.
- **Idempotency**: It uses MD5 hashes of `(title + meta + text)` to ensure each specific highlight is only added once.
- **Atomicity**: It moves the incoming file into the vault, processes it, and cleans up the raw file.

## 3. Why "Embeds" instead of "Vector Embeddings"?
You asked about embeddings. While standard RAG systems use vector embeddings (turning text into numbers for "fuzzy" search), this system uses **Structural Embeds** (`![[...]]`) for several reasons:

1.  **Deterministic Integrity**: Vector embeddings can lose the original context. Structural embeds retain the raw file's full fidelity.
2.  **Performance/Cost**: Vector search is computationally expensive. Obsidian block/file embeds are instantaneous and zero-cost for your VPS/Cloud infrastructure.
3.  **Human/Agent Handoff**: You (and the agent) can read the structured note and immediately click through to the raw, verifiable source data. It is a "glass-box" system, not a "black-box" vector system.
4.  **Scalability**: As your vault grows, standard RAG systems drift. Your current structural approach is immune to that drift because it is built on the vault's native, interlinked graph.

## Troubleshooting
- **If `notesync` fails**: Check the SSH connection on the Kindle via KTerm (`ssh ubuntu@204.216.172.41`).
- **If highlights aren't appearing**: Check the logs on the VPS host by running the python script manually:
  `/usr/bin/python3 /home/ubuntu/mero-2nd-brain/scripts/parse_clippings.py`
