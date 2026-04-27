# Task Plan - Obsidian Thinking Partner Skills

## Goal
Implement a suite of 12 specialized slash commands (Skills) for the Pi agent that leverage the Obsidian vault and `vault_index.json` to act as a cognitive partner.

## Phases
- [x] **Phase 1: Architecture Design**
    - [x] Research the exact format for Pi Skills/Slash commands. (Using Prompt Templates)
    - [x] Map out how each command will interact with `vault_index.json` and `ripgrep`.
- [x] **Phase 2: Core Context Skills**
    - [x] `/context` - Life/Work state summary.
    - [x] `/today` - Daily planning.
    - [x] `/closeday` - EOD logging.
- [x] **Phase 3: Semantic & Evolution Skills**
    - [x] `/trace` - Idea evolution.
    - [x] `/connect` - Bridge domains.
    - [x] `/drift` - Loosely connected themes.
    - [x] `/emerge` - Pattern clustering.
- [x] **Phase 4: Synthesis & Writing Skills**
    - [x] `/ghost` - Emulate user's voice.
    - [x] `/challenge` - Belief pressure-testing.
    - [x] `/ideas` - Emerging pattern report.
- [x] **Phase 5: Knowledge Management Skills**
    - [x] `/graduate` - Promote daily notes to notes.
    - [x] `/schedule` - Priority mapping to time blocks.
- [x] **Phase 6: Integration Expansion**
    - [x] Install `obsidian-cli` in the local venv.
    - [x] Configure Local REST API in Obsidian.
    - [x] Link `obsidian-cli` to the API key.
- [ ] **Phase 7: Advanced Vault Workflows**
    - [x] `/inbox` - Process max 5 items from Check Later.
    - [x] `/quiz` - Spaced repetition and active recall.
    - [ ] Explore other advanced workflows (Conflict Finder, etc.).

## Current Status
All 12 commands implemented as Prompt Templates in `.pi/prompts/`.

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| N/A | | |
