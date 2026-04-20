---
type: note
description: "- Session lock решается изоляцией агента, а не флагом --local - Каждый агент (main, dbrain-processor) = отдельный workspace - MCP конфигурация..."
last_accessed: 2026-04-06
relevance: 0.91
tier: active
---
# OpenClaw — Уроки и правила

## Изоляция агентов
- **Session lock решается изоляцией агента**, а не флагом `--local`
- Каждый агент (main, dbrain-processor) = отдельный workspace
- MCP конфигурация per-agent через копирование `mcp-config.json`

## Модели и экономия
- **Haiku вместо Sonnet:** ~12x экономия для рутинных задач
- Fallback цепочка: haiku → sonnet-4-5 → openrouter/free
- Default модель: `anthropic/claude-3-5-haiku-20241022`

## Память (Memory Kit)
- **FTS (full-text search) работает без API** — достаточно для базового поиска
- OpenAI embeddings требуют баланса → альтернатива: Gemini
- WAL mode обязателен для SQLite: `PRAGMA journal_mode=WAL;`
- Кроны isolated, видят историю через `sessions.visibility = "agent"`

## Диагностика
- **agent-doctor — мастхэв** для проверки:
  - WAL mode
  - memorySearch конфиг
  - база памяти (chunks count)
  - Gateway bind security

## Структура скиллов
- `.claude/skills/` — стандартный путь для Claude Code/Codex
- Skill path: 20KB инструкций в SKILL.md
- Skill install: `openclaw skills install <url>`

## Конфигурация
- **Gateway bind = "lan"** для доступа с локальных устройств
- **Telegram native commands:** отключены (`native: false`) для чистого меню
- **Cron модель:** claude-sonnet-4-5 (дешевле sonnet-4-6)

## Obsidian CLI
- Требует точного пути vault, не читает конфиг автоматически
- Установка: `npm install -g obsidian-cli`
- Конфиг: `~/.config/obsidian/obsidian.json`

## Related

- [[2026-04-06]]
- [[SKILL]]
- [[COMMANDS]]
- [[MEMORY]]
