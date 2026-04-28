#!/usr/bin/env python3
import os
import hashlib
import re
from pathlib import Path
import shutil

# --- CONFIGURATION ---
VAULT_ROOT = Path(os.environ.get("VAULT_ROOT", "/mero-2nd-brain"))
RAW_NOTES_DIR = VAULT_ROOT / "5_ Knowledge_Library" / "raw_book_notes"
CLIPPINGS_FILE_IN_VAULT = RAW_NOTES_DIR / "My Clippings.txt"
INCOMING_CLIPPINGS_PATH = Path.home() / "My_Clippings.txt" # Using underscore to be safe

def get_hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def parse_clippings(file_path):
    if not file_path.exists():
        print(f"Clippings file not found at {file_path}")
        return []

    with open(file_path, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    raw_clippings = content.split('==========')
    clippings = []
    for raw in raw_clippings:
        lines = [line.strip() for line in raw.split('\n') if line.strip()]
        if len(lines) >= 3:
            title_line = lines[0]
            match = re.match(r'^(.*)\s\((.*?)\)$', title_line)
            if match:
                title, author = match.group(1).strip(), match.group(2).strip()
            else:
                title, author = title_line.strip(), "Unknown"
            
            meta, text = lines[1], "\n".join(lines[2:])
            safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
            clipping_hash = get_hash(f"{title}{meta}{text}")
            clippings.append({'title': safe_title, 'author': author, 'meta': meta, 'text': text, 'hash': clipping_hash})
    return clippings

def main():
    if not INCOMING_CLIPPINGS_PATH.exists():
        print("No new clippings file found in home directory. Nothing to do.")
        return

    print(f"Found incoming clippings at {INCOMING_CLIPPINGS_PATH}")
    if not RAW_NOTES_DIR.exists():
        RAW_NOTES_DIR.mkdir(parents=True, exist_ok=True)
    
    shutil.move(INCOMING_CLIPPINGS_PATH, CLIPPINGS_FILE_IN_VAULT)
    print(f"Moved clippings into vault at {CLIPPINGS_FILE_IN_VAULT}")

    clippings = parse_clippings(CLIPPINGS_FILE_IN_VAULT)
    if not clippings:
        return

    books = {}
    for clip in clippings:
        books.setdefault(clip['title'], []).append(clip)

    for title, clips in books.items():
        book_file = RAW_NOTES_DIR / f"{title}.md"
        existing_content = book_file.read_text(encoding='utf-8') if book_file.exists() else f"# {title}\n\n*Raw Kindle Highlights*\n\n"
        
        new_highlights = []
        for clip in clips:
            hash_marker = f"<!-- hash: {clip['hash']} -->"
            if hash_marker not in existing_content:
                new_highlights.append(f"{hash_marker}\n> {clip['text']}\n> *{clip['meta']}*\n\n")
        
        if new_highlights:
            with open(book_file, 'a', encoding='utf-8') as f:
                f.write("".join(new_highlights))
            print(f"Added {len(new_highlights)} new clippings to '{title}'")
    
    print("Processing complete.")

if __name__ == "__main__":
    main()
