# 🧠 Cognitive Assistant Workflow

This folder contains the local "brain" of the Pi agent as it operates within the Mero Vault. All interactions are logged locally to ensure continuity across machines and sessions.

## 🛠 Setup & Infrastructure

- **Conversation Logs**: Saved in `conversations/` as `.jsonl` files.
- **MCP Server**: Integrated with **Serena** for advanced code analysis and project manipulation.
- **Dynamic Index**: Utilizes `vault_index.json` (root) for fast, token-efficient knowledge retrieval.
- **Obsidian CLI**: Custom script at `agent/bin/obsidian-cli` using Local REST API for UI sync.
- **Kindle Sync**: Use the `notesync` alias in KTerm on the Kindle to push highlights to the VPS.
- **Kindle Parser**: `scripts/parse_clippings.py` (VPS) processes the pushed clippings into individual book notes.

## 🚀 Thinking Partner Commands

The following slash commands are available within this project.

| Command | Purpose | Usage |
|:---|:---|:---|
| `/context` | Loads your current life/work state, projects, and priorities. | `/context` |
| `/today` | Generates a prioritized plan based on daily notes and tasks. | `/today` |
| `/trace` | Tracks the evolution of a specific idea over time. | `/trace <topic>` |
| `/connect` | Finds unexpected bridges between two different domains. | `/connect <A> <B>` |
| `/ghost` | Answers questions using your specific voice and beliefs. | `/ghost <question>` |
| `/challenge` | Stress-tests your thinking and finds internal contradictions. | `/challenge <topic>` |
| `/ideas` | Scans for emerging patterns and suggests tools/writing topics. | `/ideas` |
| `/graduate` | Promotes "seeds" from daily notes into standalone files. | `/graduate` |
| `/closeday` | Captures progress and lessons learned at the end of the day. | `/closeday` |
| `/drift` | Surfaces subconscious themes recurring across unrelated notes. | `/drift` |
| `/emerge` | Identifies clusters of ideas ready to become formal projects. | `/emerge` |
| `/schedule` | Maps priorities to actual time blocks and flags mismatches. | `/schedule` |
| `/inbox` | Processes a small batch (max 5) of inbox notes with suggestions. | `/inbox` |
| `/quiz` | Tests your understanding of a random complex concept. | `/quiz` |
| `/kindle` | Synthesizes new raw highlights into structured book notes. | `/kindle` |

## ⚙️ Core Principles (from AGENTS.md)

1. **Principle 0: Dynamic Indexing**: Rebuild `vault_index.json` before complex retrieval.
2. **Human Authorship is Primary**: Suggestions only, never override intent.
3. **Preserve Nuance**: Avoid destructive simplification.

## 📖 Promoting Kindle Notes

When promoting a raw book note into the Knowledge Library, follow these strict formatting rules:
1. **Never erase or modify the original raw file**: The promoted file must be created separately, preserving the raw notes for embeds.
2. **Intelligent Colored Headers**: Organize the highlights using logical `##` and `###` headers representing themes or chapters. To differentiate them from location numbers, wrap the header text in a light yellow span: `## <span style="color:#e5c07b">Chapter Name</span>`.
3. **Format Locations, Highlights, and Notes**:
   - Location should be greyed out as it is secondary: `<span style="color:#888888">Location [loc]</span>`
   - Highlights should be slightly white/light grey: `> <span style="color:#e8e8e8">highlight text</span>`
   - Notes must be placed immediately on the next line (no blank lines), with the arrow/Note in blue and bold (using HTML `<b>`), and the text in bright white:
     `<span style="color:#5db0d7">↑ <b>Note:</b></span> <span style="color:#ffffff">[The user's note text]</span>`
4. **Deduplicate Fragmented Notes**: Automatically collapse fragmented notes (created by typing on Kindle) into the final, longest version before inserting.
