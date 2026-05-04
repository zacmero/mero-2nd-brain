#!/usr/bin/env python3
import sys
import re
from pathlib import Path

HASH_MARKER_RE = re.compile(r'<!--\s*hash:\s*([a-f0-9]+)\s*-->|data-kindle-hash="([a-f0-9]+)"')

def parse_raw_entries(content):
    blocks = content.split('<!-- hash:')
    parsed = []

    for block in blocks[1:]:
        lines = [l.strip() for l in block.split('\n') if l.strip()]
        if len(lines) < 2:
            continue

        hash_val = lines[0].replace('-->', '').strip()
        quote = ""
        meta = ""
        for line in lines[1:]:
            if line.startswith('>-') or line.startswith('> *-'):
                meta = line.replace('>-', '').replace('> *-', '').replace('*', '').strip()
            elif line.startswith('>'):
                quote += line.replace('>', '').strip() + " "
        quote = quote.strip()

        loc_match = re.search(r'Location ([\d-]+)', meta)
        loc = loc_match.group(1) if loc_match else "Unknown Location"
        page_match = re.search(r'page (\d+)', meta)
        page = int(page_match.group(1)) if page_match else 0

        entry_type = 'note' if "Your Note" in meta else 'highlight'
        parsed.append({
            'type': entry_type,
            'text': quote,
            'loc': loc,
            'page': page,
            'hash': hash_val,
        })

    return parsed

def collapse_fragments(entries):
    collapsed = []
    for item in entries:
        if collapsed:
            prev = collapsed[-1]
            same_scope = (
                prev['type'] == item['type']
                and prev['loc'] == item['loc']
                and prev['page'] == item['page']
            )
            if same_scope:
                # Kindle typing artifacts often arrive as a sequence of
                # same-location fragments. Keep the final fragment, which is
                # usually the full completed note/highlight.
                prev['text'] = item['text']
                prev['hash'] = item['hash']
                continue

        collapsed.append(item)

    return collapsed

def promote_book(raw_path_str, target_path_str, title=None, author=None, tags="#Sci-Fi"):
    raw_path = Path(raw_path_str)
    target_path = Path(target_path_str)
    
    if not raw_path.exists():
        print(f"Error: {raw_path} does not exist.")
        sys.exit(1)

    target_path.parent.mkdir(parents=True, exist_ok=True)

    # 1. Parse raw Kindle export and collapse typing fragments first.
    content = raw_path.read_text(encoding='utf-8')
    new_entries = collapse_fragments(parse_raw_entries(content))

    # 2. Load existing content
    if target_path.exists():
        target_content = target_path.read_text(encoding='utf-8')
        links_marker = "## 🔗 Conceptual Links & Connections"
        if links_marker in target_content:
            split_content = target_content.split(links_marker)
            main_body = split_content[0]
            conceptual_links = "\n\n" + links_marker + split_content[1]
        else:
            main_body = target_content
            conceptual_links = ""
    else:
        # Create new file with basic metadata
        target_content = "" # Initialize to avoid UnboundLocalError
        main_body = f"---\ncssclasses: kindle-book\ntags: {tags}\nauthor: {author}\n---\n# {title}\n\n**{author}**\n\n* * *\n\n"
        conceptual_links = ""

    # 3. Format and append new highlights
    existing_hashes = set()
    for match in HASH_MARKER_RE.finditer(target_content):
        existing_hashes.add(match.group(1) or match.group(2))

    formatted_entries = ""
    skipped_existing = 0
    appended_entries = 0
    for i, entry in enumerate(new_entries):
        if entry['type'] == 'note': continue
        if entry['hash'] in existing_hashes:
            skipped_existing += 1
            continue
        
        note_text = ""
        if i + 1 < len(new_entries) and new_entries[i+1]['type'] == 'note':
            note_text = new_entries[i+1]['text']
        
        loc_str = f"Location {entry['loc']}"
        if entry['page'] > 0:
            loc_str = f"Page {entry['page']} | " + loc_str
            
        formatted_entries += f"<span hidden data-kindle-hash=\"{entry['hash']}\"></span>\n"
        formatted_entries += f"<span style=\"color:#888888\">{loc_str}</span>\n"
        # Highlights made even brighter (#dcdcdc) but still dimmer than personal notes (#ffffff)
        formatted_entries += f"> <span style=\"color:#dcdcdc\">{entry['text']}</span>\n"
        if note_text:
            formatted_entries += f"<div style=\"margin-left: 2em;\"><span style=\"color:#5db0d7\">↑ <b>Note:</b></span> <span style=\"color:#fff9c4\">{note_text}</span></div>\n"
        formatted_entries += "\n"
        appended_entries += 1

    # 4. Write back
    if formatted_entries:
        main_body = main_body.rstrip() + "\n\n"
    target_path.write_text(main_body + formatted_entries + conceptual_links, encoding='utf-8')
    
    # 5. Preserve raw file (Don't clear it)
    # open(raw_path, 'w').close()
    print(f"Appended {appended_entries} highlights to {target_path}")
    print(f"Skipped {skipped_existing} existing highlights already promoted")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: promote_kindle.py <raw_path> <target_path> [title] [author] [tags]")
        sys.exit(1)
    
    title = sys.argv[3] if len(sys.argv) > 3 else "Unknown Title"
    author = sys.argv[4] if len(sys.argv) > 4 else "Unknown Author"
    tags = sys.argv[5] if len(sys.argv) > 5 else "#Sci-Fi"
    
    promote_book(sys.argv[1], sys.argv[2], title, author, tags)
