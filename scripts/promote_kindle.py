#!/usr/bin/env python3
import sys
import re
from pathlib import Path

def promote_book(raw_path_str, target_path_str):
    raw_path = Path(raw_path_str)
    target_path = Path(target_path_str)
    
    if not raw_path.exists():
        print(f"Error: {raw_path} does not exist.")
        sys.exit(1)
        
    target_path.parent.mkdir(parents=True, exist_ok=True)

    content = raw_path.read_text(encoding='utf-8')
    blocks = content.split('<!-- hash:')
    parsed = []

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
        
        if "Your Note" in meta:
            parsed.append({'type': 'note', 'text': quote, 'loc': loc})
        else:
            parsed.append({'type': 'highlight', 'text': quote, 'loc': loc})

    collapsed = []
    for item in parsed:
        if item['type'] == 'note':
            if collapsed and collapsed[-1]['type'] == 'note':
                if len(item['text']) > len(collapsed[-1]['text']):
                    collapsed[-1]['text'] = item['text']
                else:
                    collapsed[-1]['text'] = item['text']
            else:
                collapsed.append(item)
        else:
            collapsed.append(item)

    metaverse_quotes = []
    language_quotes = []
    society_quotes = []
    programming_quotes = []

    for i, item in enumerate(collapsed):
        if item['type'] == 'note': continue
        
        text_lower = item['text'].lower()
        note_text = ""
        if i + 1 < len(collapsed) and collapsed[i+1]['type'] == 'note':
            note_text = collapsed[i+1]['text']
        
        entry = {"loc": item['loc'], "text": item['text'], "note": note_text}
        
        if any(k in text_lower for k in ['metaverse', 'daemon', 'avatar', 'goggle', 'optic']):
            metaverse_quotes.append(entry)
        elif any(k in text_lower for k in ['babel', 'asherah', 'enki', 'language', 'sumer', 'virus']):
            language_quotes.append(entry)
        elif any(k in text_lower for k in ['hacker', 'machine language', 'program']):
            programming_quotes.append(entry)
        else:
            society_quotes.append(entry)

    markdown = """# Snow Crash

---
Tag(s): #Neal-Stephenson #Sci-Fi #Cyberpunk

---

**Neal Stephenson**

* * *

"""

    def write_section(title, entries):
        if not entries: return ""
        # The light yellow color makes the section visually distinct
        sec = f"## <span style=\"color:#e5c07b\">{title}</span>\n\n"
        for e in entries:
            # Location is secondary (grey), highlight is primary (light grey/white), note is brightest (white)
            sec += f"<span style=\"color:#888888\">Location {e['loc']}</span>\n"
            sec += f"> <span style=\"color:#e8e8e8\">{e['text']}</span>\n"
            if e['note']:
                # Note sits exactly below the highlight block with NO blank lines between them
                # Using HTML <b> tag because markdown ** inside HTML spans can be ignored by Obsidian
                sec += f"<span style=\"color:#5db0d7\">↑ <b>Note:</b></span> <span style=\"color:#ffffff\">{e['note']}</span>\n"
            sec += "\n"
        return sec

    markdown += write_section("1. The Metaverse and Technology", metaverse_quotes)
    markdown += write_section("2. Language, Sumerian Myth, and Metaviruses", language_quotes)
    markdown += write_section("3. Programming and Hackers", programming_quotes)
    markdown += write_section("4. World and Society", society_quotes)

    target_path.write_text(markdown, encoding='utf-8')
    print(f"File promoted successfully to {target_path}")

if __name__ == '__main__':
    raw_path = '/home/zacmero/Documents/mero-vault/5_ Knowledge_Library/raw_book_notes/Snow Crash - Neal Stephenson.md'
    target_path = '/home/zacmero/Documents/mero-vault/5_ Knowledge_Library/Sci-Fi/Snow Crash.md'
    promote_book(raw_path, target_path)
