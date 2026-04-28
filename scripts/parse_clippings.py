#!/usr/bin/env python3
import os
import hashlib
import re
from pathlib import Path

# Paths
VAULT_ROOT = Path(os.environ.get("VAULT_ROOT", "/home/zacmero/Documents/mero-vault"))
RAW_NOTES_DIR = VAULT_ROOT / "5_ Knowledge_Library" / "raw_book_notes"
CLIPPINGS_FILE = RAW_NOTES_DIR / "My Clippings.txt"

def get_hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def parse_clippings(file_path):
    if not file_path.exists():
        print(f"Clippings file not found at {file_path}")
        return []

    with open(file_path, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    # Kindle separates clippings with ==========
    raw_clippings = content.split('==========')
    clippings = []

    for raw in raw_clippings:
        lines = [line.strip() for line in raw.split('\n') if line.strip()]
        if len(lines) >= 3:
            # First line: Title (Author)
            title_line = lines[0]
            # Sometimes it's Title (Author), sometimes just Title
            match = re.match(r'^(.*)\s\((.*?)\)$', title_line)
            if match:
                title = match.group(1).strip()
                author = match.group(2).strip()
            else:
                title = title_line.strip()
                author = "Unknown"
            
            # Second line: Meta info (Page, Location, Date)
            meta = lines[1]
            
            # Remaining lines: The actual highlighted text or note
            text = "\n".join(lines[2:])
            
            # Clean up title for filename (remove invalid characters)
            safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
            
            clipping_hash = get_hash(f"{title}{meta}{text}")
            
            clippings.append({
                'title': safe_title,
                'author': author,
                'meta': meta,
                'text': text,
                'hash': clipping_hash
            })

    return clippings

def process_clippings():
    if not RAW_NOTES_DIR.exists():
        RAW_NOTES_DIR.mkdir(parents=True, exist_ok=True)

    clippings = parse_clippings(CLIPPINGS_FILE)
    if not clippings:
        return

    # Group by book
    books = {}
    for clip in clippings:
        if clip['title'] not in books:
            books[clip['title']] = []
        books[clip['title']].append(clip)

    added_count = 0

    for title, clips in books.items():
        book_file = RAW_NOTES_DIR / f"{title}.md"
        existing_content = ""
        
        if book_file.exists():
            with open(book_file, 'r', encoding='utf-8') as f:
                existing_content = f.read()
        else:
            # Create a nice header for new books
            existing_content = f"# {title}\n\n*Raw Kindle Highlights*\n\n"

        new_content = ""
        for clip in clips:
            hash_marker = f"<!-- hash: {clip['hash']} -->"
            if hash_marker not in existing_content:
                # Format the clipping nicely
                new_content += f"{hash_marker}\n"
                new_content += f"> {clip['text']}\n"
                new_content += f"> *{clip['meta']}*\n\n"
                added_count += 1

        if new_content:
            with open(book_file, 'a', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Added {new_content.count('<!-- hash:')} new clippings to '{title}'")

    print(f"Processing complete. Added {added_count} new clippings across {len(books)} books.")

if __name__ == "__main__":
    process_clippings()
