"""
Rebuild files/photos/photos.json from the images in this folder.
Run from the repo root:

    python files/photos/update_manifest.py

Filenames are expected to follow: Year-Place-Title.jpg (Title optional).
"""

from __future__ import annotations

import json
from pathlib import Path


def build_manifest(folder: Path) -> list[dict]:
    photos = []
    for path in sorted(folder.glob("*")):
        if not path.is_file():
            continue

        stem = path.stem
        parts = stem.split("-")
        if len(parts) >= 3:
            year, place = parts[0], parts[1]
            title = "-".join(parts[2:])
        elif len(parts) == 2:
            year, place = parts[0], parts[1]
            title = ""
        else:
            year, place, title = "", "", stem

        photos.append(
            {
                "file": path.name,
                "year": year,
                "place": place,
                "title": title.replace("_", " ").strip(),
            }
        )
    return photos


def main() -> None:
    folder = Path(__file__).parent
    manifest = build_manifest(folder)
    out = folder / "photos.json"
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(f"Wrote {len(manifest)} entries to {out}")


if __name__ == "__main__":
    main()
