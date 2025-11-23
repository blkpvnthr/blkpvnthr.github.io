#!/usr/bin/env python3
"""
Auto-generate index.json for every subfolder inside:

Images:
  /Users/abdula1/Library/MobileDocuments/com~apple~CloudDocs/blkpvnthr.github.io/blkpvnthr.github.io/assets/images/

Videos:
  /Users/abdula1/Library/MobileDocuments/com~apple~CloudDocs/blkpvnthr.github.io/blkpvnthr.github.io/assets/videos/

Titles/descriptions are auto-built from filenames.
"""

from pathlib import Path
import json, re

IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".svg")
VIDEO_EXTENSIONS = (".mp4", ".mov", ".webm", ".mkv")

def clean_title(filename: str) -> str:
    name = Path(filename).stem
    name = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', name)
    name = re.sub(r'[-_]+', ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    parts = []
    for w in name.split(' '):
        if w.isupper() and len(w) <= 4:
            parts.append(w)
        else:
            parts.append(w.capitalize())
    return ' '.join(parts)

def make_description(title: str) -> str:
    return f"{title}."

def process_folder(folder: Path, exts):
    print(f"\n📁 Scanning: {folder}")

    if not folder.exists():
        print("  ❌ Folder does not exist, skipped.")
        return

    entries = []

    # 1. Scan top-level files first
    for p in sorted(folder.iterdir(), key=lambda x: x.name.lower()):
        if p.is_file() and p.suffix.lower() in exts:
            title = clean_title(p.name)
            entries.append({
                "src": p.name,
                "title": title,
                "description": make_description(title)
            })

    # 2. If no top-level items, check subfolders
    if not entries:
        for sub in sorted(folder.iterdir(), key=lambda x: x.name.lower()):
            if sub.is_dir():
                for p in sorted(sub.iterdir(), key=lambda x: x.name.lower()):
                    if p.is_file() and p.suffix.lower() in exts:
                        rel = f"{sub.name}/{p.name}"
                        title = clean_title(p.name)
                        entries.append({
                            "src": rel,
                            "title": title,
                            "description": make_description(title)
                        })

    if not entries:
        print("  ⚠️ No media files found.")
        return

    index_file = folder / "index.json"
    with index_file.open("w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

    print(f"  ✅ Wrote {len(entries)} entries → {index_file}")

def main():
    base_images = Path("/Users/abdula1/Library/MobileDocuments/com~apple~CloudDocs/blkpvnthr.github.io/blkpvnthr.github.io/assets/images/")
    base_videos = Path("/Users/abdula1/Library/MobileDocuments/com~apple~CloudDocs/blkpvnthr.github.io/blkpvnthr.github.io/assets/videos/")

    print("🚀 Generating index.json for all media folders...")

    # Process all subfolders under images
    for folder in sorted(base_images.iterdir(), key=lambda x: x.name.lower()):
        if folder.is_dir():
            process_folder(folder, IMAGE_EXTENSIONS)

    # Process all subfolders under videos
    for folder in sorted(base_videos.iterdir(), key=lambda x: x.name.lower()):
        if folder.is_dir():
            process_folder(folder, VIDEO_EXTENSIONS)

    print("\n🎉 Done! All index.json files generated.\n")

if __name__ == "__main__":
    main()
