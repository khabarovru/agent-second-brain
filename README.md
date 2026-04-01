---
type: note
last_accessed: 2026-03-19
relevance: 0.98
tier: active
---
# Second Brain Vault

> Структурированный Obsidian vault для работы с d-brain ботом и OpenClaw агентами.
[[99 Сервис/Организация Обсидиан/Организация Обсидиан|Организация Обсидиан]]

## 📂 Структура

```
vault/
├── 00 Входящие/         # Inbox для новых идей, Web Clipper
├── 10 Заметки/          # Основные заметки
├── 20 Ежедневник/       # Ручные дневниковые записи
├── 30 Проекты/          # Активные проекты
├── 40 Объекты/          # Объекты работы (лифты, здания и т.д.)
├── 50 Задачи/           # Задачи из Todoist (опционально)
├── 60 Цели/             # Goals (yearly/monthly/weekly)
├── 70 Люди/             # Контакты, заметки о людях
├── 80 Ежедневные/       # Daily notes от бота (голосовые + текст)
├── 80 Сводки/           # Weekly summaries
├── 90 Карты знаний/     # MOC (Maps of Content)
├── 95 Файлы/            # Attachments, документы
└── 99 Сервис/          # Служебные файлы
    ├── Skills/          # AgentSkills (dbrain-processor и др.)
    ├── Scripts/         # Вспомогательные скрипты
    └── Шаблоны/         # Obsidian templates
```

## 🤖 Интеграция с d-brain

**d-brain** — Telegram-бот для голосового дневника с обработкой через OpenClaw + Todoist.

### Основные возможности:

- **Голосовые заметки:** Отправь голосовое → расшифровка (Deepgram) → `80 Ежедневные/YYYY-MM-DD.md`
- **Автообработка:** `/process` → классификация + создание задач в Todoist
- **Weekly digest:** `/weekly` → обзор недели + alignment с целями

### Агенты:

- `dbrain-processor` — обработка daily notes
- `todoist-ai` — создание умных задач
- `graph-builder` — построение графа знаний
- `vault-health` — поддержание порядка в vault

## 🛠️ Установка

1. **Склонируй репозиторий:**
   ```bash
   git clone https://github.com/yourusername/vault-second-brain.git ~/vault
   ```

2. **Открой в Obsidian:**
   - Настройки → Open another vault → Open folder as vault
   - Выбери папку `~/vault`

3. **Настрой d-brain бота (опционально):**
   - См. документацию: [agent-second-brain](https://github.com/yourusername/agent-second-brain)

## 🔒 Безопасность

**Этот репозиторий содержит ТОЛЬКО:**
- ✅ Структуру папок (пустые .gitkeep)
- ✅ Obsidian конфигурацию (.obsidian/)
- ✅ Служебные скрипты (99 Сервис/)
- ✅ AgentSkills (SKILL.md файлы)

**НИКОГДА не коммитятся:**
- ❌ Личные заметки (00-95 папки)
- ❌ MEMORY.md, USER.md, IDENTITY.md
- ❌ API ключи (.env, mcp-config.json)
- ❌ Attachments, файлы проектов

См. `.gitignore` для деталей.

## 📦 Плагины Obsidian

**Обязательные:**
- [Templater](https://github.com/SilentVoid13/Templater) — шаблоны daily notes
- [Dataview](https://github.com/blacksmithgu/obsidian-dataview) — запросы к заметкам
- [Calendar](https://github.com/liamcain/obsidian-calendar-plugin) — навигация по daily notes

**Рекомендуемые:**
- [Auto Note Mover](https://github.com/farux/obsidian-auto-note-mover) — автосортировка заметок
- [Periodic Notes](https://github.com/liamcain/obsidian-periodic-notes) — weekly/monthly notes
- [Tasks](https://github.com/obsidian-tasks-group/obsidian-tasks) — управление задачами

Полный список: `.obsidian/community-plugins.json`

## 🚀 Быстрый старт

1. **Создай первую заметку:**
   - `Cmd/Ctrl + N` → новая заметка
   - Сохрани в `10 Заметки/`

2. **Настрой цели:**
   - `60 Цели/0-vision-3y.md` — долгосрочная vision
   - `60 Цели/1-yearly-2026.md` — цели на год
   - `60 Цели/3-weekly.md` — ONE Big Thing на неделю

3. **Запусти d-brain (если настроен):**
   - Отправь голосовое в Telegram
   - Проверь `80 Ежедневные/YYYY-MM-DD.md`

## 📚 Документация

- [MIGRATION.md](99%20_Сервис/MIGRATION.md) — миграция из старой структуры
- [Skills/dbrain-processor/SKILL.md](99%20_Сервис/Skills/dbrain-processor/SKILL.md) — агент обработки

## 🤝 Вклад

Этот vault — личный проект, но если хочешь улучшить структуру/скрипты:

1. Fork репозиторий
2. Создай feature branch (`git checkout -b feature/awesome-script`)
3. Commit изменения (`git commit -m 'Add awesome script'`)
4. Push в branch (`git push origin feature/awesome-script`)
5. Открой Pull Request

## 📄 Лицензия

MIT License — используй как хочешь, но без гарантий.

## 🙏 Благодарности

- [Obsidian](https://obsidian.md) — лучший инструмент для PKM
- [OpenClaw](https://openclaw.ai) — AI-агенты на стероидах
- [Building a Second Brain](https://www.buildingasecondbrain.com) — методология

---

**Автор:** Краб 🦀  
**Дата:** 2026-03-19
