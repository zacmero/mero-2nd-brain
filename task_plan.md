# Task Plan - Kindle Robust Sync Architecture

## Goal
Implement an idempotent, robust sync pipeline for Kindle clippings that mirrors the source state, prevents data loss, and maintains Obsidian integrity.

## Phases
- [ ] **Phase 1: Architecture Cleanup** - Remove brittle aliases/scripts and adopt a clean VPS-based execution.
- [ ] **Phase 2: Idempotent Parser Implementation** - Rewrite `scripts/parse_clippings.py` to mirror the full state of highlights for each book rather than just appending new ones.
- [ ] **Phase 3: Vault Integrity** - Ensure `5_ Knowledge_Library/raw_book_notes/` notes are consistently updated without breaking existing Obsidian embeds.
- [ ] **Phase 4: Validation** - Verify update/delete/edit scenarios.

## Current Status
- **PROJECT IN "SAFE/NON-DESTRUCTIVE MODE"**: All automated promotion scripts (`promote_kindle.py`) have been disabled. 
- All future knowledge integration must be manual or explicitly pre-approved by the owner.
- The pipeline is now "Append-Only" for highlights, but headers and structure must remain untouched.

