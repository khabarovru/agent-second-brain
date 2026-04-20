#!/usr/bin/env python3
"""
Извлечение людей и объектов из текста задачи + поиск связанных записей в vault.
Usage: python3 extract-entities.py "текст задачи"
Output: JSON с найденными людьми, объектами и связанными записями
"""
import sys
import json
import os
import re

ALIASES_FILE = '/home/khabarovru/.openclaw/agents/second-brain/agent/aliases.json'
# scripts/ → Skills/entity-extractor/ → Skills/ → 99 Сервис/ → vault/
_SCRIPT_REAL = os.path.realpath(__file__)
_VAULT_PATH = '/home/khabarovru/.openclaw/agents/second-brain/vault'

def load_aliases():
    with open(ALIASES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_entities(text, aliases):
    found_people = []
    found_objects = []
    found_orgs = []
    text_lower = text.lower()

    for canonical, data in aliases['people'].items():
        for alias in data['aliases']:
            if alias.lower() in text_lower:
                if canonical not in found_people:
                    found_people.append(canonical)
                break

    for canonical, data in aliases['objects'].items():
        for alias in data['aliases']:
            if alias.lower() in text_lower:
                if canonical not in found_objects:
                    found_objects.append(canonical)
                break

    for canonical, data in aliases.get('organizations', {}).items():
        for alias in data['aliases']:
            if alias.lower() in text_lower:
                if canonical not in found_orgs:
                    found_orgs.append(canonical)
                break

    return found_people, found_objects, found_orgs

def find_related_in_vault(people, objects, aliases, orgs=None):
    """Ищет связанные записи в vault по людям и объектам."""
    related = []
    search_terms = set()

    for person in people:
        data = aliases['people'].get(person, {})
        for a in data.get('aliases', [person]):
            search_terms.add(a.lower())

    for obj in objects:
        data = aliases['objects'].get(obj, {})
        for a in data.get('aliases', [obj]):
            search_terms.add(a.lower())

    for org in (orgs or []):
        data = aliases.get('organizations', {}).get(org, {})
        for a in data.get('aliases', [org]):
            search_terms.add(a.lower())

    search_dirs = [
        os.path.join(_VAULT_PATH, '50 Задачи'),
        os.path.join(_VAULT_PATH, '20 Ежедневник', 'Daily Notes'),
        os.path.join(_VAULT_PATH, '30 Проекты'),
        os.path.join(_VAULT_PATH, '35 Проекты'),
        os.path.join(_VAULT_PATH, '10 Заметки'),
    ]

    HIGH_PRIORITY_PATTERNS = [
        r'счет', r'акт', r'оплат', r'эдо', r'задач', r'todo',
        r'\[ \]', r'\[x\]', r'дедлайн', r'срок', r'до\s+\d', r'p[1-4]',
        r'договор', r'подписан', r'отправил', r'напомни'
    ]

    seen_files = set()
    scored = []

    for search_dir in search_dirs:
        if not os.path.exists(search_dir):
            continue
        for root, dirs, files in os.walk(search_dir):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for fname in sorted(files, reverse=True):
                if not fname.endswith('.md'):
                    continue
                fpath = os.path.join(root, fname)
                if fpath in seen_files:
                    continue
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    content = ''.join(lines)
                    content_lower = content.lower()

                    matched_term = None
                    for term in search_terms:
                        if term in content_lower:
                            matched_term = term
                            break

                    if not matched_term:
                        continue

                    seen_files.add(fpath)
                    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
                    title = title_match.group(1) if title_match else fname.replace('.md', '')

                    score = 0
                    for pat in HIGH_PRIORITY_PATTERNS:
                        if re.search(pat, content_lower):
                            score += 1
                    if re.match(r'\d{4}-\d{2}-\d{2}', fname):
                        score += 3
                    if matched_term in fname.lower():
                        score += 2
                    связано_count = content_lower.count('связано:')
                    if связано_count > 2:
                        score -= связано_count

                    snippets = []
                    for i, line in enumerate(lines):
                        if matched_term in line.lower():
                            snippet = line.strip()
                            if not snippet or snippet.startswith('---') or len(snippet) < 5:
                                continue
                            if snippet.startswith('Связано:') or snippet.startswith('thoughts/'):
                                continue
                            if snippet not in snippets:
                                snippets.append(snippet)
                            if len(snippets) >= 3:
                                break

                    rel_path = os.path.relpath(fpath, _VAULT_PATH)
                    scored.append({
                        'file': rel_path,
                        'title': title,
                        'snippets': snippets[:2],
                        'matched_term': matched_term,
                        'score': score
                    })

                except Exception:
                    pass

    scored.sort(key=lambda x: x['score'], reverse=True)
    for item in scored:
        item.pop('score', None)
    return scored[:10]

def get_person_card_path(canonical, aliases):
    data = aliases['people'].get(canonical, {})
    return data.get('file', f"70 Люди/{canonical.lower().replace(' ', '_').replace('.', '')}.md")

def get_object_card_path(canonical, aliases):
    data = aliases['objects'].get(canonical, {})
    return data.get('file', f"40 Объекты/{canonical.lower().replace(' ', '_')}.md")

def format_for_notification(people, objects, related, orgs=None):
    lines = []
    if people:
        lines.append(f"👤 Люди: {', '.join(people)}")
    if objects:
        lines.append(f"🏢 Объекты: {', '.join(objects)}")
    if orgs:
        lines.append(f"🏭 Организации: {', '.join(orgs)}")
    if related:
        lines.append(f"\n🔗 Связанные записи ({len(related)}):")
        for r in related[:5]:
            lines.append(f"  📄 {r['title']}")
            for s in r['snippets'][:2]:
                if len(s) > 80:
                    s = s[:77] + '...'
                lines.append(f"     └ {s}")
    else:
        if people or objects or orgs:
            lines.append("\n🔗 Связанных записей не найдено")
    return '\n'.join(lines)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({'people': [], 'objects': [], 'related': [], 'notification': ''}))
        sys.exit(0)

    text = ' '.join(sys.argv[1:])
    aliases = load_aliases()
    people, objects, orgs = find_entities(text, aliases)
    related = find_related_in_vault(people, objects, aliases, orgs)

    result = {
        'people': people,
        'objects': objects,
        'organizations': orgs,
        'related': related,
        'people_files': {p: get_person_card_path(p, aliases) for p in people},
        'objects_files': {o: get_object_card_path(o, aliases) for o in objects},
        'notification': format_for_notification(people, objects, related, orgs)
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
