---
type: note
description: "- Путь: /home/khabarovru/.openclaw/workspace/skills/agent-second-brain/ - Бот: @khabarovru_obsidian_bot (Telegram) - Цель: Голосовой дневник с..."
last_accessed: 2026-04-06
relevance: 0.91
tier: active
---
# d-brain бот — Архитектурные решения

## Проект: agent-second-brain
- **Путь:** `/home/khabarovru/.openclaw/workspace/skills/agent-second-brain/`
- **Бот:** `@khabarovru_obsidian_bot` (Telegram)
- **Цель:** Голосовой дневник с автоматической обработкой

## Архитектура
```
Telegram → d-brain bot (aiogram)
           ↓
    Deepgram (транскрипция голосовых)
           ↓
    vault/daily/YYYY-MM-DD.md (сырые записи)
           ↓
    /process → OpenClaw agent "dbrain-processor"
           ↓
    MCP Todoist + Obsidian vault
```

## Ключевые решения

### 1. Изоляция обработки
- **Агент:** `dbrain-processor` (отдельный workspace)
- **Почему:** Session lock при одновременной работе main + bot
- **Результат:** Нет конфликтов, бот и основной чат независимы

### 2. Без git
- **Решение:** Убраны `git.commit_and_push()` из `/process` и `/weekly`
- **Почему:** Проект локальный, автокоммиты не нужны
- **Результат:** Никаких push на GitHub, всё остаётся на сервере

### 3. MCP Todoist
- **Переменная:** `TODOIST_API_TOKEN` (не `TODOIST_API_KEY`)
- **Конфиг:** `~/.openclaw/agents/dbrain-processor/mcp-config.json`
- **Skill path:** `.claude/skills/dbrain-processor/SKILL.md`

### 4. Экономия на моделях
- **Primary:** `claude-3-5-haiku-20241022` (~12x дешевле Sonnet)
- **Для сложных задач:** fallback на sonnet-4-5
- **Кроны:** sonnet-4-5 (баланс цена/качество)

## Команды бота
- `/start` — приветствие + клавиатура
- `/status` — статистика дня
- `/process` — обработка записей через OpenClaw
- `/weekly` — недельный дайджест

## Что НЕ делать
- ❌ Не запускать бота с `--local` (нарушает изоляцию)
- ❌ Не возвращать git commit (проект задуман локальным)
- ❌ Не менять путь к skill (`.claude/skills` правильный)
- ❌ Не использовать `TODOIST_API_KEY` (правильно: `TODOIST_API_TOKEN`)

## Технические детали
- **Бот запуск:** `.venv/bin/python -m d_brain`
- **Логи:** `~/d-brain-bot.log`
- **Vault:** `~/.openclaw/workspace/skills/agent-second-brain/vault/`
- **Gateway port:** 18789 (LAN bind)

## Related

- [[TODOIST]]
- [[log]]
- [[2026-04-06]]
- [[SKILL]]
- [[todoist]]
- [[GITHUB]]
- [[Home]]
- [[AGENTS]]
- [[Проект]]
