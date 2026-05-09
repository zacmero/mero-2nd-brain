# 🧠 Cognitive Assistant Workflow

This folder contains the local "brain" of the Pi agent as it operates within the Mero Vault. All interactions are logged locally to ensure continuity across machines and sessions.

- **On the desktop ArchMerOS, the vault is located in "/home/zacmero/Documents/mero-vault/"**
- **On the VM, where the syncthing main service is, the vault is on "/home/ubuntu/mero-2nd-brain/vps-infra/data/vault"**
- **On the iPhone it is on the folder "On My iPhone/Obsidian/Mero Vault"**



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
4. **Collapsible Table of Contents & Links**: Generate an Obsidian callout-based TOC at the beginning using `> [!info]- 📑 Table of Contents`. To ensure smooth scrolling without flashing/highlighting the chapter text, use an invisible HTML anchor placed immediately before the colored header: `<a name="sec-1" id="sec-1"></a>\n## <span style="color:#e5c07b">Title</span>`. Link to it via standard markdown `> - [Title](#sec-1)`.
5. **Deduplicate Fragmented Notes**: Automatically collapse fragmented notes (created by typing on Kindle) into the final, longest version before inserting.
6. **Format Notes with Safe Indentation**: Do NOT use `&nbsp;` to indent notes, as it may render as literal text in some themes. Use a clean CSS margin wrap instead: `<div style="margin-left: 2em;"><span style="color:#5db0d7">↑ <b>Note:</b></span> <span style="color:#ffffff">[The user's note text]</span></div>`. Note text should be bright white (`#ffffff`), while the highlight should be slightly dimmer (`#d4d4d4`). Location should be dim grey (`#888888`).
7. **Preserve Appended User Content**: Always check if `## <span style="color:#e5c07b">🔗 Conceptual Links & Connections</span>` exists in the target file before overwriting it, and append that entire block back to the end of the new output so user-generated links are never lost.
8. **Preserve Cover Art**: When re-promoting a note, manually extract and retain the existing cover image (`![cover.jpeg](...)`) below the new main title.

## 🔗 Bidirectional & Rich Block Linking Conventions

When establishing connections between notes (especially books and conceptual project notes), you **must** adhere to the following quality-of-life linking styles:

1. **No Generic One-Way Links**: Never use lazy, general links at the bottom of a page pointing to a whole book. The notes need to explicitly "talk to each other" based on specific concepts.
2. **Use Block Anchors (`^anchor-name`)**: When targeting a specific highlight, paragraph, or concept, append a block anchor (e.g., `^outcomes-vs-process`) to the end of that specific line in the destination file.
3. **Disambiguate File Paths**: Always use the full or explicit folder path in the link (e.g., `[[5_ Knowledge_Library/Information Theory/Decoding the Universe - Charles Seife#^randomness-information|Decoding the Universe - Charles Seife]]`) to prevent Obsidian from accidentally routing the link to the `raw_book_notes/` version.
4. **True Bidirectional Linking**: 
   - **Forward Link**: The source note should have an entry in its `## <span style="color:#e5c07b">🔗 Conceptual Links & Connections</span>` section pointing directly to the target block anchor, including a short explanation of *why* they connect.
   - **Return Link (Backlink)**: In the destination note, place a visual return link immediately next to the targeted block anchor to instantly jump back. 
     *Example:* `...end of highlight text. ^target-anchor [[1_ Projects Stack/Traders/Origin Note#^origin-anchor|🔗 Origin Note]]`
5. **Always Verify Link Integrity**: Before considering a linking task done, double-check that both sides of the bidirectional link are active, correct, and point to the promoted notes (not the raw clippings).

## 🖥 Leveraging the Obsidian CLI

The custom script at `agent/bin/obsidian-cli` (which hooks into the Local REST API) is an incredibly powerful tool for deep vault interactions. Future agents should utilize it when:
1. **Visualizing Context:** You need to open specific notes on the user's screen or trigger UI updates to guide their attention.
2. **Advanced Searching:** Raw `grep`/`rg` is fast for simple strings, but the CLI allows you to leverage Obsidian's native search engine, enabling powerful queries using tags, properties, paths, and DataView logic.
3. **Safe Refactoring:** If you are renaming or moving files, using the CLI (if supported by your commands) ensures Obsidian can automatically update all internal links across the vault, which raw bash `mv` commands cannot do natively.
4. **Canvas Editing & Visual Feedback:** The `screenshot` feature in the CLI is **crucial** when helping the user with Canvas editing or any visual spatial organization, as it allows the agent to "see" the current state of the UI.
