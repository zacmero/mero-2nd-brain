#!/usr/bin/env python3
import os
import hashlib
import re
from pathlib import Path

# --- CONFIGURATION ---
# The root of the git repository on the VPS host.
REPO_ROOT = Path("/home/ubuntu/mero-2nd-brain")
# The path to the directory that is ACTUALLY synced by Docker.
VAULT_ROOT_ON_HOST = REPO_ROOT / "vps-infra" / "data" / "vault"
# The destination for the processed clippings file inside the vault.
RAW_NOTES_DIR = VAULT_ROOT_ON_HOST / "5_ Knowledge_Library" / "raw_book_notes"
CLIPPINGS_FILE_IN_VAULT = RAW_NOTES_DIR / "My Clippings.txt"

def get_hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def parse_clippings(file_path):
    if not file_path.exists():
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
            title = match.group(1).strip() if match else title_line.strip()
            author = match.group(2).strip() if match else "Unknown"
            
            meta, text = lines[1], "\n".join(lines[2:])
            safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
            clipping_hash = get_hash(f"{title}{meta}{text}")
            clippings.append({'title': safe_title, 'author': author, 'meta': meta, 'text': text, 'hash': clipping_hash})
    return clippings

def main():
    if not CLIPPINGS_FILE_IN_VAULT.exists() or CLIPPINGS_FILE_IN_VAULT.stat().st_size == 0:
        print("No new clippings to process.")
        return

    clippings = parse_clippings(CLIPPINGS_FILE_IN_VAULT)
    
    # Organize clippings by book
    books = {}
    for clip in clippings:
        books.setdefault(clip['title'], []).append(clip)

    for title, clips in books.items():
        book_file = RAW_NOTES_DIR / f"{title}.md"
        
        # Build the new content for the book
        new_content = f"# {title}\n\n*Raw Kindle Highlights*\n\n"
        for clip in clips:
            new_content += f"<!-- hash: {clip['hash']} -->\n"
            new_content += f"> {clip['text']}\n"
            new_content += f"> *{clip['meta']}*\n\n"
        
        # Atomically update the file
        book_file.write_text(new_content, encoding='utf-8')
        print(f"Synced {len(clips)} highlights to '{title}'")
    
    # Truncate raw file to signal completion while keeping it for embeds
    open(CLIPPINGS_FILE_IN_VAULT, 'w').close()
    print("Processing complete and raw file cleared.")

if __name__ == "__main__":
    main()
