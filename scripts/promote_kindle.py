#!/usr/bin/env python3
import sys
import re
from pathlib import Path

def promote_book(raw_path_str, target_path_str, title=None, author=None, tags="#Sci-Fi"):
    raw_path = Path(raw_path_str)
    target_path = Path(target_path_str)
    
    if not raw_path.exists():
        print(f"Error: {raw_path} does not exist.")
        sys.exit(1)

    # 1. Parse ONLY NEW highlights
    content = raw_path.read_text(encoding='utf-8')
    blocks = content.split('<!-- hash:')
    new_entries = []

    for block in blocks[1:]:
        lines = [l.strip() for l in block.split('\n') if l.strip()]
        if len(lines) < 2: continue
        
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
        
        if "Your Note" in meta:
            new_entries.append({'type': 'note', 'text': quote, 'loc': loc, 'page': page, 'hash': hash_val})
        else:
            new_entries.append({'type': 'highlight', 'text': quote, 'loc': loc, 'page': page, 'hash': hash_val})

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
    formatted_entries = ""
    for i, entry in enumerate(new_entries):
        if entry['type'] == 'note': continue
        if entry['hash'] in target_content: continue
        
        note_text = ""
        if i + 1 < len(new_entries) and new_entries[i+1]['type'] == 'note':
            note_text = new_entries[i+1]['text']
        
        loc_str = f"Location {entry['loc']}"
        if entry['page'] > 0:
            loc_str = f"Page {entry['page']} | " + loc_str
            
        formatted_entries += f"<span style=\"color:#888888\">{loc_str}</span>\n"
        # Highlights made even brighter (#dcdcdc) but still dimmer than personal notes (#ffffff)
        formatted_entries += f"> <span style=\"color:#dcdcdc\">{entry['text']}</span>\n"
        if note_text:
            formatted_entries += f"<div style=\"margin-left: 2em;\"><span style=\"color:#5db0d7\">↑ <b>Note:</b></span> <span style=\"color:#ffffff\">{note_text}</span></div>\n"
        formatted_entries += "\n"

    # 4. Write back
    target_path.write_text(main_body + formatted_entries + conceptual_links, encoding='utf-8')
    
    # 5. Preserve raw file (Don't clear it)
    # open(raw_path, 'w').close()
    print(f"Appended highlights to {target_path}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: promote_kindle.py <raw_path> <target_path> [title] [author] [tags]")
        sys.exit(1)
    
    title = sys.argv[3] if len(sys.argv) > 3 else "Unknown Title"
    author = sys.argv[4] if len(sys.argv) > 4 else "Unknown Author"
    tags = sys.argv[5] if len(sys.argv) > 5 else "#Sci-Fi"
    
    promote_book(sys.argv[1], sys.argv[2], title, author, tags)
