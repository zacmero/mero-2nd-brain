# Findings

- Append-only (`>>`) is insufficient for a robust sync because it fails to capture edits or deletions.
- The `vps-infra/data/vault` volume mount is the correct place to write files; do not touch the git repository root directly.
- The Python parser must re-hash *every* highlight in the book, not just new ones, and rebuild the file content to match the state in `My Clippings.txt`.
