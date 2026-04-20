---
type: note
title: TOOLS.md - Инструменты Second Brain
description: "Инструменты и настройки Second Brain"
related: 
last_accessed: 2026-04-08
relevance: 0.91
tier: active
---
# TOOLS.md - Инструменты Second Brain

## 🎤 Голосовая транскрипция

**Deepgram** — глобально для всех агентов (OpenClaw config `tools.media.audio.deepgram`)
- Работает через VK/Telegram автоматически — отправь голосовое → получил текст
- Настройки: nova-2, punctuate, smart_format, detectLanguage, ru язык
- **Больше НЕ нужен shell скрипт** — встроено в OpenClaw

### Отправка голосового
1. VK: отправь голосовое → auto transcribed → отвечаю текстом
2. Telegram: отправь голосовое → auto transcribed → отвечаю текстом

---

## 📂 Vault структура

| Папка | Что там |
|-------|---------|
| `00 Входящие/Ideas/` | Необработанные идеи |
| `00 Входящие/Tasks/` | Необработанные задачи |
| `00 Входящие/Notes/` | Необработанные заметки |
| `10 Заметки/General/` | Общие заметки |
| `20 Ежедневник/Daily Notes/` | Дневник |
| `50 Задачи/Active/` | Активные задачи |
| `60 Проекты/` | Проекты |
| `90 Карты знаний/Knowledge Base/` | Знания |

---

## 🔧 Рабочие скрипты

| Скрипт | Папка | Функция |
|--------|-------|---------|
| `extract-entities.py` | `99 Сервис/Skills/entity-extractor/scripts/` | Entity recognition (люди, объекты, связи) |
| `resolve-conflicts.sh` | `99 Сервис/Skills/entity-extractor/scripts/` | Syncthing conflict resolution |
| `todoist-sync-closed.py` | `99 Сервис/Skills/todoist-sync/` | Синхронизация закрытых задач Todoist → vault |

---

## 🚫 Удалённые скрипты (d-brain наследство)

| Скрипт | Почему удалён |
|--------|--------------|
| `vault-status.sh` | Статистика через direct read (я сам считаю) |
| `vault-process.sh` | Обработка через агента |
| `deepgram-transcribe.sh` | Deepgram встроен в OpenClaw |
| `todoist-add-task.sh` | mcp-cli глобально |
| `todoist-create-task.sh` | mcp-cli глобально |
| `todoist-find-tasks.sh` | mcp-cli глобально |
| `email-check.sh` | Не прижился |
| `gmail-check.py` | Не прижился |

---

## 🧠 Паттерны владельца

| Паттерн | Описание |
|---------|---------|
| `vk-text` / `telegram-text` | Текст из канала |
| `vk-voice` / `telegram-voice` | Голосовое |
| `vk-forward` / `telegram-forward` | Пересланное |

### Приоритеты задач
- p1 = срочно, прямо сейчас
- p2 = важно, в ближайшее время
- p3 = обычное
- p4 = когда-нибудь

---

## 📡 Todoist (mcp-cli)

Todoist подключён глобально через mcp-cli. Все агенты могут:

```bash
mcp-cli call todoist add-tasks '{"tasks": [{"content": "Task", "dueString": "tomorrow", "priority": 2}]}'
mcp-cli call todoist find-tasks-by-date '{"startDate": "today"}'
mcp-cli call todoist complete-tasks '{"ids": ["task_id"]}'
mcp-cli call todoist get-overview '{}'
```

**API Key:** `skills.entries.todoist.apiKey` (в OpenClaw config)
**Token:** `c1f7278f1dd135b6f0dcdf4a01018c70aead351f`

---

## 🔗 Интеграции

| Сервис | Статус | Заметки |
|--------|--------|---------|
| Deepgram | ✅ Глобально | Все каналы, все агенты |
| Todoist (mcp-cli) | ✅ Глобально | Все агенты |
| Whisper | ❌ Отключён | Заменён на Deepgram |
| Syncthing | ✅ Работает | Конфликты см. resolve-conflicts.sh |
| Obsidian | ✅ Работает | Markdown vault |

---

## 📝 YAML frontmatter шаблон

```yaml
---
created: YYYY-MM-DD HH:MM
type: [task|idea|note|knowledge]
tags: [tag1, tag2]
source: [vk-text|vk-voice|vk-forward|telegram-text|telegram-voice|telegram-forward]
priority: 1-4  # только для task
related: [["связанная заметка"]]
---

# Название

Содержимое...
```

## Related

- [[TODOIST]]
- [[2026-04-09]]
- [[log]]
- [[entities]]
- [[Люди]]
- [[lessons]]
- [[goals]]
- [[patterns]]
- [[2026-03-26]]
- [[SKILL]]
- [[2026-03-28]]
- [[Home]]
- [[AGENTS]]
- [[2026-03-25]]
- [[MEMORY]]
- [[frontmatter]]
- [[HEARTBEAT]]
- [[2026-04-08]]
- [[Scripts]]
- [[todoist]]
- [[USER]]
- [[Все]]
- [[Заметка]]
