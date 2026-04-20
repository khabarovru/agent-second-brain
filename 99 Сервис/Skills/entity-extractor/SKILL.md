---
type: note
description: "Извлечение сущностей (люди, объекты, организации) из текста и поиск связанных записей в vault. Использует aliases.json для распознавания."
last_accessed: 2026-04-08
relevance: 0.91
tier: active
name: entity-extractor
---

# entity-extractor

## Scripts

### extract-entities.py
```bash
python3 extract-entities.py "текст задачи"
```
Извлекает из текста людей и объекты через aliases.json, ищет связанные записи в vault.

**Input:** текст (аргументы командной строки)
**Output:** JSON с people, objects, organizations, related, notification

### resolve-conflicts.sh
```bash
./resolve-conflicts.sh [--dry-run]
```
Автоматическое разрешение Syncthing конфликтов. Оставляет более новый файл.

## Aliases
- Файл: `agent/aliases.json`
- Содержит people, objects, organizations с каноническими именами и алиасами
- Алиасы намеренно созданы владельцем — НЕ УДАЛЯТЬ

## Важно
- `agent/aliases.json` — ценный domain knowledge, не удалять
- `agent/scripts/extract-entities.py` — specialized entity recognition, рабочий
- `agent/scripts/resolve-conflicts.sh` — Syncthing conflict resolution, рабочий
