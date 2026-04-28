#!/usr/bin/env python3
"""extract-entities.py — Извлечение сущностей из текста"""

import sys
import json
import re
import os
from pathlib import Path

VAULT = "/volume1/docker/openclaw/.openclaw/workspace/skills/agent-second-brain/vault"
ALIASES_FILE = os.path.join(os.path.dirname(__file__), "aliases.json")


def load_aliases():
    try:
        with open(ALIASES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"people": {}, "objects": {}}


def extract_entities(text, aliases):
    """Find people and objects in text using aliases"""
    text_lower = text.lower()
    found_people = set()
    found_objects = set()

    for canonical, aliases_list in aliases.get("people", {}).items():
        for alias in aliases_list:
            if alias.lower() in text_lower:
                found_people.add(canonical)
                break

    for canonical, aliases_list in aliases.get("objects", {}).items():
        for alias in aliases_list:
            if alias.lower() in text_lower:
                found_objects.add(canonical)
                break

    return list(found_people), list(found_objects)


def search_vault(people, objects, limit=5):
    """Search vault for related notes"""
    related = []
    search_terms = people + objects

    if not search_terms:
        return related

    # Build grep pattern
    pattern = "|".join(re.escape(term.lower()) for term in search_terms)

    # Search all markdown files
    vault_path = Path(VAULT)
    for md_file in vault_path.rglob("*.md"):
        # Skip Гермес folder
        if "/99 Сервис/Гермес/" in str(md_file):
            continue

        try:
            content = md_file.read_text(encoding="utf-8", errors="ignore")
            content_lower = content.lower()

            if re.search(pattern, content_lower):
                # Extract title (first # heading or filename)
                title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
                title = title_match.group(1) if title_match else md_file.stem

                # Find snippets
                snippets = []
                for line in content.split("\n"):
                    if re.search(pattern, line.lower()):
                        clean_line = line.strip().lstrip("#*-|")
                        clean_line = clean_line[:100]
                        if clean_line:
                            snippets.append(clean_line)
                        if len(snippets) >= 2:
                            break

                # Get relative path
                rel_path = md_file.relative_to(VAULT)

                related.append({
                    "file": str(rel_path),
                    "title": title,
                    "snippets": snippets[:2]
                })

                if len(related) >= limit:
                    break

        except Exception:
            continue

    return related


def format_notification(text, people, objects, related):
    """Format notification message"""
    lines = []

    if people:
        lines.append(f"👤 Люди: {', '.join(people)}")

    if objects:
        lines.append(f"🏢 Объекты: {', '.join(objects)}")

    if related:
        lines.append(f"\n🔗 Связанные записи ({len(related)}):")
        for r in related:
            snippet = r["snippets"][0][:60] if r["snippets"] else ""
            lines.append(f"  📄 {r['title']}")
            if snippet:
                lines.append(f"     └ {snippet}...")
    else:
        lines.append("\n🔗 Связанных записей не найдено")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python3 extract-entities.py 'text'"}))
        sys.exit(1)

    text = sys.argv[1]
    aliases = load_aliases()

    people, objects = extract_entities(text, aliases)
    related = search_vault(people, objects)

    result = {
        "people": people,
        "objects": objects,
        "related": related,
        "notification": format_notification(text, people, objects, related)
    }

    # Output as JSON (for scripting) and formatted (for display)
    if "--json" in sys.argv:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["notification"])


if __name__ == "__main__":
    main()
