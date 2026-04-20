---
type: note
description: "vault/ ├── 00 Входящие/ # Inbox для новых идей, Web Clipper ├── 10 Заметки/ # Основные заметки"
last_accessed: 2026-04-01
relevance: 0.91
tier: active
---
# Second Brain Vault 🧠

> Структурированный Obsidian vault для работы с OpenClaw агентом Second Brain.

## 📂 Структура

```
vault/
├── 00 Входящие/         # Inbox для новых идей, Web Clipper
├── 10 Заметки/          # Основные заметки
├── 20 Ежедневник/       # Дневниковые записи
├── 35 Проекты/          # Активные проекты
├── 40 Объекты/          # Объекты работы
├── 50 Задачи/           # Задачи (Todoist)
├── 60 Цели/             # Цели: год / месяц / неделя
├── 70 Люди/             # Контакты и заметки о людях
├── 80 Сводки/           # Недельные дайджесты
├── 85 Сводки/           # Итоговые сводки
├── 90 Карты знаний/     # MOC (Maps of Content)
├── 95 Файлы/            # Вложения, документы
└── 99 Сервис/           # Служебные файлы
    ├── Skills/          # AgentSkills для OpenClaw
    ├── Scripts/         # Вспомогательные скрипты
    └── Шаблоны/         # Obsidian templates
```

## 🤖 Интеграция с OpenClaw

**Second Brain** — AI-агент в OpenClaw для захвата и обработки мыслей через Telegram.

### Основные возможности:

- **Голосовые и текстовые заметки** → автоклассификация → сохранение в vault
- **Транскрипция голоса** через Whisper (локально)
- **Автообработка:** `/process` → классификация + создание задач в Todoist
- **Недельный дайджест:** `/weekly` → обзор недели
- **Память по Эббингаузу** — заметки тускнеют со временем без обращения

### AgentSkills:

- `todoist-ai` — создание умных задач
- `graph-builder` — построение графа знаний
- `vault-health` — поддержание порядка в vault
- `agent-memory` — движок памяти (Эббингауз)

## 🛠️ Установка

1. **Склонируй репозиторий:**
   ```bash
   git clone https://github.com/yourusername/vault-second-brain.git ~/vault
   ```

2. **Открой в Obsidian:**
   - Settings → Open another vault → Open folder as vault
   - Выбери папку `~/vault`

3. **Подключи OpenClaw агента:**
   - Установи [OpenClaw](https://openclaw.ai)
   - Настрой агент `second-brain` с workspace на эту папку

## 🔒 Безопасность

**Этот репозиторий содержит ТОЛЬКО:**
- ✅ Структуру папок (пустые `.gitkeep`)
- ✅ Obsidian конфигурацию (`.obsidian/`)
- ✅ Служебные скрипты (`99 Сервис/`)
- ✅ AgentSkills (`SKILL.md` файлы)

**НИКОГДА не коммитятся:**
- ❌ Личные заметки (папки 00–95)
- ❌ `MEMORY.md`, `USER.md`, `SOUL.md`, `AGENTS.md`
- ❌ API ключи, `.env`, `mcp-config.json`
- ❌ Вложения и файлы проектов

См. `.gitignore` для деталей.

## 📦 Плагины Obsidian

**Обязательные:**
- [Dataview](https://github.com/blacksmithgu/obsidian-dataview) — запросы к заметкам (нужен для `Home.md`)
- [Templater](https://github.com/SilentVoid13/Templater) — шаблоны

**Рекомендуемые:**
- [Calendar](https://github.com/liamcain/obsidian-calendar-plugin) — навигация по дневнику
- [Tasks](https://github.com/obsidian-tasks-group/obsidian-tasks) — управление задачами

Полный список: `.obsidian/community-plugins.json`

## 🚀 Быстрый старт

1. **Открой `Home.md`** — дашборд с горячими заметками, задачами и входящими
2. **Настрой цели** в `60 Цели/`
3. **Отправь голосовое или текст** агенту в Telegram — всё остальное он сделает сам

## 📄 Лицензия

MIT License

---

**Автор:** Denis Khabarov  
**Обновлено:** 2026-04-01

## Related

- [[TODOIST]]
- [[2026-04-09]]
- [[secrets]]
- [[log]]
- [[Люди]]
- [[CHANGELOG]]
- [[2026-03-19]]
- [[TOOLS]]
- [[execute]]
- [[patterns]]
- [[frontmatter]]
- [[entities]]
- [[goals]]
- [[2026-03-20]]
- [[Организация Обсидиан]]
- [[links]]
- [[contacts]]
- [[SYSTEM]]
- [[2026-03-26]]
- [[Все]]
- [[architecture]]
- [[Заметка]]
- [[Scripts]]
- [[SKILL]]
- [[todoist]]
- [[GITHUB]]
- [[USER]]
- [[Home]]
- [[SOUL]]
- [[AGENTS]]
- [[Шаблоны]]
- [[MEMORY]]
