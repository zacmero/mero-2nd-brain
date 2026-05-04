# Scripts

This directory holds the vault-maintenance scripts used by the second-brain workflow.

## `promote_kindle.py`

Promotes Kindle raw notes from:

`/home/zacmero/Documents/mero-vault/5_ Knowledge_Library/raw_book_notes/`

into a structured book note without deleting or overwriting the raw source file.

### What it does

- Parses Kindle-exported raw blocks split by `<!-- hash: ... -->`
- Collapses consecutive Kindle typing fragments at the same page/location/type
- Keeps the final completed fragment for each run
- Appends only new promoted highlights into the target note
- Preserves the raw note file unchanged
- Stores a hidden per-entry hash marker so reruns can skip already promoted entries

### Usage

```bash
python3 scripts/promote_kindle.py <raw_path> <target_path> [title] [author] [tags]
```

### Arguments

- `raw_path`
  - Full path to the raw Kindle export note
- `target_path`
  - Full path to the promoted destination note
- `title` *(optional)*
  - Book title used when creating a new promoted note
- `author` *(optional)*
  - Book author used when creating a new promoted note
- `tags` *(optional)*
  - Genre/tag field written into frontmatter when creating a new promoted note
  - Default: `#Sci-Fi`

### Example

```bash
python3 scripts/promote_kindle.py \
  "/home/zacmero/Documents/mero-vault/5_ Knowledge_Library/raw_book_notes/A Deepness in the Sky - Vernor Vinge.md" \
  "/home/zacmero/Documents/mero-vault/5_ Knowledge_Library/Sci-Fi/A Deepness in the Sky.md" \
  "A Deepness in the Sky" \
  "Vernor Vinge" \
  "#Sci-Fi"
```

### Notes

- The script is append-only.
- Existing promoted content is preserved.
- Raw Kindle notes are never cleared by the script.
- The hidden hash marker is stored in the promoted note so later runs can dedupe entries without exposing the marker in rendered view.
