---
type: note
description: "vault/ ├── daily/ # голосовые + текст от бота ├── weekly/ # недельные дайджесты"
related: 
last_accessed: 2026-03-19
relevance: 0.43
tier: cold
---
# Миграция second-brain в рабочий vault

**Дата:** 2026-03-19  
**Автор:** Краб 🦀

## Что изменилось

### Структура папок

**До миграции:**
```
vault/
├── daily/          # голосовые + текст от бота
├── weekly/         # недельные дайджесты
├── goals/          # цели
└── summaries/      # обработанные записи
```

**После миграции:**
```
vault/
├── 80 Ежедневные/  # daily notes (голосовые + текст)
├── 80 Сводки/      # weekly summaries
├── 60 Цели/        # goals (yearly/monthly/weekly)
├── 50 Задачи/      # Todoist tasks (опционально)
└── 99 Сервис/
    ├── Skills/     # SKILL.md файлы (dbrain-processor и др.)
    └── Scripts/    # вспомогательные скрипты
```

### Обновлённые пути

| Компонент | Старый путь | Новый путь |
|-----------|------------|-----------|
| Daily notes | `vault/daily/` | `vault/80 Ежедневные/` |
| Summaries | `vault/summaries/` | `vault/80 Сводки/` |
| Goals | `vault/goals/` | `vault/60 Цели/` |
| Skills | `vault/.claude/skills/` | `vault/99 Сервис/Skills/` |

### Изменённые файлы

1. **`src/d_brain/config.py`**
   - `vault_path` → `~/.openclaw/workspace/vault`
   - `daily_path` → `80 Ежедневные`
   - Добавлены: `weekly_path`, `tasks_path`, `goals_path`, `skills_path`

2. **`src/d_brain/services/storage.py`**
   - `self.daily_path = vault / "daily"` → `vault / "80 Ежедневные"`

3. **`src/d_brain/services/processor.py`**
   - Все упоминания `goals/`, `daily/`, `summaries/` обновлены
   - `_load_skill_content()` → читает из `99 Сервис/Skills/`

4. **`.env`**
   - `VAULT_PATH=/home/khabarovru/.openclaw/workspace/vault`

5. **`99 Сервис/Skills/dbrain-processor/SKILL.md`**
   - Все пути обновлены через `sed`:
     - `daily/` → `80 Ежедневные/`
     - `goals/` → `60 Цели/`
     - `summaries/` → `80 Сводки/`

## Миграция данных

**Скопировано автоматически:**
- `vault/daily/*.md` → `vault/80 Ежедневные/`
- `vault/summaries/*` → `vault/80 Сводки/`
- `vault/goals/*` → `vault/60 Цели/`
- `vault/.claude/skills/*` → `vault/99 Сервис/Skills/`
- Системные файлы (AGENTS.md, SOUL.md, USER.md и т.д.) → корень vault

**НЕ скопировано (old vault остался):**
- `vault/blog/`, `vault/MOC/`, `vault/thoughts/` — можно перенести позже вручную

## Тестирование

Запустить тест:
```bash
bash ~/.openclaw/workspace/vault/99\ _Сервис/Scripts/test_dbrain.sh
```

Проверяет:
- ✅ Структура папок
- ✅ Конфигурация (.env)
- ✅ Обновления кода (Python)
- ✅ Запись в daily notes
- ✅ SKILL.md с новыми путями

## Запуск после миграции

1. **Перезапустить бота:**
   ```bash
   cd ~/.openclaw/workspace/skills/agent-second-brain
   pkill -f "python -m d_brain"  # убить старый процесс
   .venv/bin/python -m d_brain   # запустить новый
   ```

2. **Проверить логи:**
   ```bash
   tail -f ~/d-brain-bot.log
   ```

3. **Отправить тестовое голосовое в Telegram:**
   - Бот: `@khabarovru_obsidian_bot`
   - Проверить файл: `vault/80 Ежедневные/2026-03-19.md`

4. **Тест /process:**
   - Команда: `/process` в Telegram
   - Проверить логи агента `dbrain-processor`

## Следующие шаги

### Синхронизация с рабочим ПК

**Вариант А (ручное копирование):**
```bash
# На Windows ПК
rsync -avz --delete \
  "C:\Users\habarov.db\Documents\__Для Обсидиан\vault_second_brain/" \
  khabarovru@n100:~/.openclaw/workspace/vault/
```

**Вариант Б (Syncthing):**
1. Установить Syncthing на Windows ПК
2. Настроить sync:
   - Windows: `C:\Users\habarov.db\Documents\__Для Обсидиан\vault_second_brain`
   - OpenClaw: `/home/khabarovru/.openclaw/workspace/vault`
3. Исключить из sync: `.obsidian/workspace.json`, `attachments/`

### Дополнительная настройка Obsidian

1. **Auto Note Mover:**
   - Настроить правило: заметки от бота → `80 Ежедневные/`

2. **Templater:**
   - Создать шаблоны для daily notes в `99 Сервис/Шаблоны/`

3. **Dataview:**
   - Обновить запросы, если используют старые пути (`daily/`, `goals/`)

## Откат (если что-то сломалось)

**Восстановить старую структуру:**
```bash
# 1. Вернуть старый VAULT_PATH в .env
echo "VAULT_PATH=/home/khabarovru/.openclaw/workspace/skills/agent-second-brain/vault" \
  > ~/.openclaw/workspace/skills/agent-second-brain/.env

# 2. Откатить config.py
cd ~/.openclaw/workspace/skills/agent-second-brain
git checkout src/d_brain/config.py src/d_brain/services/storage.py src/d_brain/services/processor.py

# 3. Перезапустить бота
pkill -f "python -m d_brain"
.venv/bin/python -m d_brain
```

## Контакты

- **Vault:** `/home/khabarovru/.openclaw/workspace/vault`
- **Bot code:** `/home/khabarovru/.openclaw/workspace/skills/agent-second-brain`
- **Telegram:** `@khabarovru_obsidian_bot`
- **Logs:** `~/d-brain-bot.log`

---

✅ **Миграция завершена:** 2026-03-19 08:24 UTC

## Related

- [[TODOIST]]
- [[log]]
- [[Scripts]]
- [[2026-03-19]]
- [[SKILL]]
- [[goals]]
- [[todoist]]
- [[USER]]
- [[Home]]
- [[SOUL]]
- [[Все]]
- [[AGENTS]]
- [[Шаблоны]]
