# Vault Migration — Новая структура

> **Дата миграции:** 2026-03-19  
> **Причина:** Объединение второго мозга (d-brain) с рабочим Obsidian vault

## 🔄 Что изменилось

### ❌ Старая структура (удалена):
```
agent-second-brain/
├── vault/              # Локальный vault внутри репозитория
│   ├── daily/          # Daily notes от бота
│   ├── goals/          # Goals
│   ├── summaries/      # Weekly summaries
│   └── .claude/skills/ # AgentSkills
└── src/d_brain/        # Код бота
```

### ✅ Новая структура:
```
~/.openclaw/workspace/
├── vault/              # Глобальный vault (ВНЕ репозитория agent-second-brain)
│   ├── 80 Ежедневные/  # Daily notes
│   ├── 60 Цели/        # Goals
│   ├── 85 Сводки/      # Weekly summaries
│   ├── 99 _Сервис/
│   │   └── Skills/     # AgentSkills (dbrain-processor и др.)
│   └── 00-95/          # Рабочие папки (Объекты, Проекты и т.д.)
└── skills/agent-second-brain/
    └── src/d_brain/    # Код бота (остался здесь)
```

## 🎯 Зачем это нужно

1. **Объединение с рабочим vault:**
   - Рабочий ПК: структурированный Obsidian vault (лифтовые проекты)
   - d-brain: голосовые заметки + автоматизация
   - Итог: Один vault для всего

2. **Разделение кода и данных:**
   - **Код бота** (`agent-second-brain/`) → на GitHub
   - **Личный vault** (`~/.openclaw/workspace/vault/`) → локально (или приватный репо)

3. **Гибкость:**
   - Vault можно синхронизировать через Syncthing (Windows ↔ OpenClaw)
   - Бот работает с любым vault (путь в `.env`)

## 📋 Что делать после clone

### 1. Установи бота (как раньше):
```bash
cd agent-second-brain
python -m venv .venv
.venv/bin/pip install -e .
```

### 2. Настрой .env:
```bash
cp .env.example .env
vim .env

# Укажи:
TELEGRAM_BOT_TOKEN=your_token
DEEPGRAM_API_KEY=your_key
VAULT_PATH=/home/username/.openclaw/workspace/vault  # ← НОВЫЙ ПУТЬ
```

### 3. Создай vault (если ещё нет):

**Вариант А: Склонируй готовый vault (рекомендуется):**
```bash
# TODO: Опубликовать vault-second-brain как отдельный репозиторий
git clone https://github.com/khabarovru/vault-second-brain.git ~/.openclaw/workspace/vault
```

**Вариант Б: Создай пустой:**
```bash
mkdir -p ~/.openclaw/workspace/vault
# Структура создастся автоматически при первом запуске бота
```

### 4. Запусти бота:
```bash
cd agent-second-brain
.venv/bin/python -m d_brain
```

## 🔗 Связь между репозиториями

| Репозиторий | Содержимое | GitHub |
|-------------|-----------|--------|
| **agent-second-brain** | Код бота (Python) | Публичный |
| **vault-second-brain** | Структура vault + Skills | Публичный (без личных данных) |
| **Локальный vault** | Личные заметки + данные | НЕ на GitHub |

## 📄 Документация

- **Бот:** [README.md](README.md) — установка и настройка d-brain
- **Vault:** см. `~/.openclaw/workspace/vault/README.md` (после clone)
- **Миграция:** `~/.openclaw/workspace/vault/99 _Сервис/MIGRATION.md`

## ⚠️ Важно

**НЕ КОММИТИТЬ личный vault в agent-second-brain!**

Старая папка `vault/` в репозитории игнорируется через `.gitignore`.  
Если случайно создал — удали:
```bash
cd agent-second-brain
rm -rf vault/  # Удалить ЛОКАЛЬНО (не на GitHub)
git rm -r --cached vault/  # Удалить из Git (если закоммитил)
```

---

**Версия:** 2.0 (после миграции 2026-03-19)  
**Автор:** Краб 🦀
