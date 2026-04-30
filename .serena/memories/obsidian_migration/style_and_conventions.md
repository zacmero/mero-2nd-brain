# Style and conventions
- Python only in `scripts/`.
- Use `pathlib.Path`, small helper functions, simple procedural scripts.
- Markdown notes preserve author voice; avoid lossy rewriting.
- Kindle note styling uses inline HTML spans for color inside markdown.
- Existing convention: raw highlight blocks use `<!-- hash: ... -->` markers; generated notes group highlights into page-range sections.
- When improving TOC/sections, prefer deterministic anchors and preserve note order.