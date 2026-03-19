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
agent-second-brain/
├── vault/              # Vault с новой нумерацией папок
│   ├── 80 Ежедневные/  # Daily notes (вместо daily/)
│   ├── 60 Цели/        # Goals (вместо goals/)
│   ├── 85 Сводки/      # Weekly summaries (вместо summaries/)
│   ├── 99 _Сервис/
│   │   └── Skills/     # AgentSkills (вместо .claude/skills/)
│   └── 00-95/          # Рабочие папки (Объекты, Проекты и т.д.)
└── src/d_brain/        # Код бота
```

**Vault теперь В РЕПОЗИТОРИИ,** но личные данные (содержимое 00-95 папок) игнорируются через `.gitignore`.  
На GitHub коммитится только структура (.gitkeep) + служебные файлы (Skills, Scripts).

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
VAULT_PATH=$PWD/vault  # ← Vault теперь в репозитории
```

### 3. Vault уже включён!

Vault теперь часть репозитория (папка `vault/`).  
Структура с пустыми папками уже на месте, агенты тоже.

### 4. Запусти бота:
```bash
cd agent-second-brain
.venv/bin/python -m d_brain
```

## 🔒 Безопасность на GitHub

Vault включён в репозиторий, но **личные данные НЕ коммитятся:**

| Что | GitHub |
|-----|--------|
| Структура папок (.gitkeep) | ✅ Да |
| Skills, Scripts, документация | ✅ Да |
| Obsidian конфигурация | ✅ Да |
| Личные заметки (00-95 папки) | ❌ Нет (игнорируются) |
| MEMORY.md, USER.md и т.д. | ❌ Нет (игнорируются) |
| .env, API ключи | ❌ Нет (игнорируются) |

См. `vault/.gitignore` для деталей.

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
