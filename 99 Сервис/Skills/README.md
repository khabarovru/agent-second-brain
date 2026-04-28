---
type: note
description: "Все скрипты находятся в 99 Сервис/Skills/ и автоматизируют обслуживание Obsidian vault."
last_accessed: 2026-03-20
relevance: 0.45
tier: cold
---
# Инструкция по maintenance-скриптам vault

Все скрипты находятся в `99 Сервис/Skills/` и автоматизируют обслуживание Obsidian vault.

---

## 📊 graph-builder — Построение графа знаний

### build_graph.py
**Что делает:** Сканирует все .md файлы, парсит wikilinks, создаёт `.graph/vault-graph.json` со статистикой.

**Запуск:**
```bash
cd vault
python3 99\ _Сервис/Skills/graph-builder/scripts/build_graph.py .
```

**Когда запускать:** Перед запуском vault-health скриптов (они требуют vault-graph.json).

**Автоматизация:** Можно настроить cron (раз в неделю).

**Результат:**
- `.graph/vault-graph.json` — граф ссылок
- Статистика: total files, links, orphans, broken links

---

### analyze.py
**Что делает:** Анализирует граф и предлагает новые wikilinks на основе упоминаний в тексте.

**Запуск:**
```bash
cd vault
python3 99\ _Сервис/Skills/graph-builder/scripts/analyze.py . --html
```

**Когда запускать:** Для поиска неявных связей между заметками.

**Автоматизация:** Ручной запуск по запросу.

---

## 🧠 agent-memory — Управление памятью (Ebbinghaus decay)

### memory-engine.py

**Что делает:** Управляет relevance и tier файлов по модели Ebbinghaus (забывание со временем).

**Команды:**

#### scan
Проверяет vault без изменений:
```bash
python3 99\ _Сервис/Skills/agent-memory/scripts/memory-engine.py scan .
```

#### init
Добавляет YAML frontmatter файлам без него:
```bash
python3 99\ _Сервис/Skills/agent-memory/scripts/memory-engine.py init .
```

#### decay
Обновляет relevance и tier для всех файлов (забывание):
```bash
python3 99\ _Сервис/Skills/agent-memory/scripts/memory-engine.py decay .
```

#### stats
Показывает health metrics и tier distribution:
```bash
python3 99\ _Сервис/Skills/agent-memory/scripts/memory-engine.py stats .
```

#### creative N
Возвращает N случайных файлов из cold/archive для вдохновения:
```bash
python3 99\ _Сервис/Skills/agent-memory/scripts/memory-engine.py creative 5 .
```

#### touch <file>
Обновляет файл, возвращает в active tier:
```bash
python3 99\ _Сервис/Skills/agent-memory/scripts/memory-engine.py touch "path/to/file.md"
```

**Автоматизация:** 
- `decay` — cron раз в неделю (воскресенье ночью)
- `init` — только при добавлении новых файлов без frontmatter
- `stats` — для мониторинга по запросу

**Tier система:**
- **active** (<7 дней) — свежие записи
- **warm** (7-21 день) — недавние
- **cold** (21-60 дней) — старые, но не забытые
- **archive** (>60 дней) — давно не использовались

---

## 🏥 vault-health — Здоровье vault

### generate_moc.py
**Что делает:** Генерирует Maps of Content (MOC) для доменов (business, projects).

**Запуск:**
```bash
cd vault
python3 99\ _Сервис/Skills/vault-health/scripts/generate_moc.py
```

**Автоматизация:** Раз в месяц или после большого добавления файлов.

**Результат:** Создаёт/обновляет `90 Карты знаний/MOC-{domain}.md` со списком файлов.

---

### add_descriptions.py
**Что делает:** Добавляет поле `description` в frontmatter файлам без него (на основе первого параграфа).

**Запуск (dry-run):**
```bash
cd vault
python3 99\ _Сервис/Skills/vault-health/scripts/add_descriptions.py
```

**Применить изменения:**
```bash
python3 99\ _Сервис/Skills/vault-health/scripts/add_descriptions.py --apply
```

**Автоматизация:** Ручной запуск после добавления новых файлов.

**Требует:** `vault-graph.json` (запустить `build_graph.py` сначала).

---

### fix_links.py
**Что делает:** Исправляет битые wikilinks:
- Удаляет trailing backslashes (`[[link\]]` → `[[link]]`)
- Убирает ссылки на вложения/Excel/PDF
- Обрабатывает слишком длинные пути (>255 символов)

**Запуск (dry-run):**
```bash
cd vault
python3 99\ _Сервис/Skills/vault-health/scripts/fix_links.py
```

**Применить изменения:**
```bash
python3 99\ _Сервис/Skills/vault-health/scripts/fix_links.py --apply
```

**Автоматизация:** Ручной запуск при появлении большого количества broken links.

**Требует:** `vault-graph.json`.

**⚠️ Исправление:** Добавлена обработка `OSError` для файлов с именами >255 символов.

---

### connect_orphans.py
**Что делает:** Подключает orphan файлы (без входящих/исходящих ссылок) к `MEMORY.md`.

**Запуск (dry-run):**
```bash
cd vault
python3 99\ _Сервис/Skills/vault-health/scripts/connect_orphans.py
```

**Применить изменения:**
```bash
python3 99\ _Сервис/Skills/vault-health/scripts/connect_orphans.py --apply
```

**Автоматизация:** Раз в неделю после `fix_links.py`.

**Требует:** `vault-graph.json`.

---

## 🔄 Рекомендуемый порядок запуска

### Еженедельное обслуживание (воскресенье):
```bash
cd ~/.openclaw/workspace/skills/agent-second-brain/vault

# 1. Построить граф
python3 99\ _Сервис/Skills/graph-builder/scripts/build_graph.py .

# 2. Обновить память (забывание)
python3 99\ _Сервис/Skills/agent-memory/scripts/memory-engine.py decay .

# 3. Исправить битые ссылки
python3 99\ _Сервис/Skills/vault-health/scripts/fix_links.py --apply

# 4. Подключить orphans
python3 99\ _Сервис/Skills/vault-health/scripts/connect_orphans.py --apply

# 5. Проверить статистику
python3 99\ _Сервис/Skills/agent-memory/scripts/memory-engine.py stats .
```

### Ежемесячное обслуживание:
```bash
# 1. Добавить описания новым файлам
python3 99\ _Сервис/Skills/vault-health/scripts/add_descriptions.py --apply

# 2. Обновить MOC
python3 99\ _Сервис/Skills/vault-health/scripts/generate_moc.py

# 3. Проверить граф на новые связи
python3 99\ _Сервис/Skills/graph-builder/scripts/analyze.py . --html
```

---

## 📁 Структура vault

```
vault/
├── 00 Входящие/           # Inbox
├── 10 Заметки/            # Основные заметки (было thoughts/)
├── 20 Ежедневник/         # Daily entries
├── 35 Проекты/            # Projects
├── 40 Объекты/            # Objects/Entities
├── 50 Задачи/             # Tasks
├── 60 Цели/               # Goals (было goals/)
├── 70 Люди/               # People/Contacts (было contacts/)
├── 80 Ежедневные/         # Daily logs
├── 80 Сводки/             # Summaries (было summaries/)
├── 90 Карты знаний/       # MOC (Maps of Content)
├── 95 Файлы/              # Files/Attachments (игнорируется скриптами)
└── 99 Сервис/
    ├── Skills/
    │   ├── graph-builder/
    │   │   ├── scripts/
    │   │   │   ├── build_graph.py    # ⭐ Создание vault-graph.json
    │   │   │   └── analyze.py         # Поиск неявных связей
    │   │   └── SKILL.md
    │   ├── agent-memory/
    │   │   ├── scripts/
    │   │   │   └── memory-engine.py   # ⭐ Управление памятью (decay)
    │   │   └── SKILL.md
    │   ├── vault-health/
    │   │   ├── scripts/
    │   │   │   ├── generate_moc.py    # Создание MOC
    │   │   │   ├── add_descriptions.py # Описания в frontmatter
    │   │   │   ├── fix_links.py       # ⭐ Исправление битых ссылок
    │   │   │   └── connect_orphans.py # ⭐ Подключение orphans
    │   │   └── SKILL.md
    │   └── README.md                  # ← Эта инструкция
    └── Организация Обсидиан/
```

**Маппинг старых путей → новые:**
- `thoughts/` → `10 Заметки/`
- `goals/` → `60 Цели/`
- `contacts/` → `70 Люди/`
- `summaries/` → `80 Сводки/`
- `MOC/` → `90 Карты знаний/`
```

---

## 🤖 Автоматизация через OpenClaw cron

Пример настройки недельного обслуживания:

```bash
openclaw cron add --name "Vault Weekly Maintenance" \
  --schedule '{"kind":"cron","expr":"0 3 * * 0"}' \
  --agent dbrain-processor \
  --task "Запусти все скрипты vault maintenance в порядке: build_graph, decay, fix_links, connect_orphans, stats" \
  --delivery announce
```

---

## 📊 Текущая статистика (2026-03-20)

- **Файлов:** 423 (100% с YAML frontmatter)
- **Ссылок:** 1692
- **Broken links:** 1181 (исправлено 369)
- **Orphans:** 4 (подключено 57)
- **Memory tiers:**
  - Active: 73 (17.3%)
  - Warm: 189 (44.7%)
  - Cold: 4 (0.9%)
  - Archive: 157 (37.1%)
- **Active context:** 242 KB (~62K токенов)

---

**Все скрипты работают! Vault готов к ежедневному использованию.** 🎉
