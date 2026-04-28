---
type: note
description: "- Структура папок (пустые .gitkeep) - Obsidian конфигурация (.obsidian/) - Служебные скрипты (99 Сервис/Scripts/)"
related: 
last_accessed: 2026-03-19
relevance: 0.43
tier: cold
---
# GitHub Setup — Безопасная публикация vault

> Инструкция по настройке публичного GitHub репозитория БЕЗ утечки личных данных.

## 🔒 Политика безопасности

### ✅ Что МОЖНО коммитить:

- Структура папок (пустые .gitkeep)
- Obsidian конфигурация (.obsidian/)
- Служебные скрипты (99 Сервис/Scripts/)
- AgentSkills (99 Сервис/Skills/)
- Документация (README.md, MIGRATION.md и т.д.)

### ❌ Что НИКОГДА не коммитить:

- **Личные заметки:** все .md файлы в 00-95 папках
- **Системные файлы:** MEMORY.md, USER.md, SOUL.md, AGENTS.md, IDENTITY.md, HEARTBEAT.md
- **Секреты:** .env, API ключи, токены, mcp-config.json
- **Attachments:** файлы, фото, документы
- **Obsidian workspace:** .obsidian/workspace.json (содержит открытые заметки)

## 📋 Быстрый старт

### 1. Создай репозиторий на GitHub

```bash
# На GitHub.com:
# 1. New repository
# 2. Имя: vault-second-brain
# 3. Public
# 4. НЕ добавляй README (уже есть локально)
```

### 2. Проверь безопасность

```bash
cd ~/.openclaw/workspace/vault
bash 99\ _Сервис/Scripts/test_git_privacy.sh
```

**Ожидаемый результат:** `✅ Готово к push на GitHub!`

### 3. Инициализируй Git (если ещё не сделано)

```bash
cd ~/.openclaw/workspace/vault
git init
git branch -M main  # переименовать master → main (стандарт GitHub)
```

### 4. Добавь remote и push

```bash
# Замени YOUR_USERNAME на свой GitHub username
git remote add origin https://github.com/YOUR_USERNAME/vault-second-brain.git

# Stage все файлы (личные данные уже игнорируются)
git add -A

# Commit
git commit -m "Initial commit: vault structure + AgentSkills"

# Push
git push -u origin main
```

### 5. Проверь на GitHub

Открой: `https://github.com/YOUR_USERNAME/vault-second-brain`

**Должно быть:**
- ✅ README.md
- ✅ .gitignore
- ✅ Пустые папки (00-95) с .gitkeep
- ✅ 99 Сервис/ с содержимым
- ✅ .obsidian/ (кроме workspace.json)

**НЕ должно быть:**
- ❌ MEMORY.md, USER.md, SOUL.md
- ❌ .md файлов в 80 Ежедневные/, 60 Цели/ и т.д.
- ❌ .env файлов
- ❌ Attachments/

## 🔁 Регулярные обновления

### Обновить Skills/скрипты:

```bash
cd ~/.openclaw/workspace/vault

# Проверить изменения
git status

# Тест безопасности (ОБЯЗАТЕЛЬНО!)
bash 99\ _Сервис/Scripts/test_git_privacy.sh

# Commit
git add 99\ _Сервис/
git commit -m "Update: dbrain-processor skill"

# Push
git push origin main
```

### Добавить новый скрипт:

```bash
# Создать скрипт
vim 99\ _Сервис/Scripts/new_script.sh

# Проверить
bash 99\ _Сервис/Scripts/test_git_privacy.sh

# Commit
git add 99\ _Сервис/Scripts/new_script.sh
git commit -m "Add: new_script.sh"
git push origin main
```

## ⚠️ Опасные команды (НЕ ИСПОЛЬЗОВАТЬ)

```bash
# ❌ git add . (может добавить личные данные)
# ❌ git add -f MEMORY.md (force добавление игнорируемого файла)
# ❌ git commit -a (коммитит все изменения, включая новые файлы)
```

**Безопасный workflow:**
1. Сначала: `bash 99\ _Сервис/Scripts/test_git_privacy.sh`
2. Потом: `git add <конкретные файлы>`
3. Проверка: `git status` (убедись, что НЕТ личных данных)
4. Commit + push

## 🛠️ Troubleshooting

### Проблема: Случайно закоммитил личные данные

**Решение (если ещё НЕ запушил):**
```bash
# Откат последнего коммита (сохраняя изменения)
git reset --soft HEAD~1

# Убери личные файлы из stage
git reset HEAD MEMORY.md USER.md  # пример

# Проверь
git status

# Коммит снова (без личных данных)
git commit -m "..."
```

**Решение (если УЖЕ запушил на GitHub):**
```bash
# КРИТИЧНО: История Git навсегда хранит файлы!
# Нужно переписать историю (опасно):

# 1. Удали файл из истории
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch MEMORY.md" \
  --prune-empty --tag-name-filter cat -- --all

# 2. Force push (перезаписывает GitHub)
git push origin --force --all

# 3. Смени API ключи/токены, которые были в файле!
```

### Проблема: .gitignore не работает

**Проверка:**
```bash
# Показать правила .gitignore для файла
git check-ignore -v MEMORY.md

# Ожидаемый вывод:
# .gitignore:52:MEMORY.md    MEMORY.md
```

**Если уже в Git:**
```bash
# Убрать из Git, но оставить локально
git rm --cached MEMORY.md
git commit -m "Remove sensitive file from Git"
```

### Проблема: Забыл запустить тест перед push

**Откат push:**
```bash
# Откатить локально
git reset --hard HEAD~1

# Откатить на GitHub (опасно!)
git push origin +main  # + означает force
```

## 📊 Мониторинг безопасности

### Автоматический тест перед каждым push

Создай Git hook:
```bash
cat > ~/.openclaw/workspace/vault/.git/hooks/pre-push << 'EOF'
#!/bin/bash
echo "🔒 Running privacy test..."
cd ~/.openclaw/workspace/vault
bash 99\ _Сервис/Scripts/test_git_privacy.sh || exit 1
echo "✅ Privacy test passed"
EOF

chmod +x ~/.openclaw/workspace/vault/.git/hooks/pre-push
```

Теперь каждый `git push` будет автоматически проверять безопасность!

### GitHub Actions (опционально)

Создай `.github/workflows/privacy-check.yml`:
```yaml
name: Privacy Check
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Privacy test
        run: bash 99\ _Сервис/Scripts/test_git_privacy.sh
```

## 🔗 Полезные ссылки

- [GitHub Docs: Ignoring files](https://docs.github.com/en/get-started/getting-started-with-git/ignoring-files)
- [git-filter-repo](https://github.com/newren/git-filter-repo) — безопасная очистка истории
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/) — удаление секретов из истории

## 📞 Контакты

Если случайно запушил секреты:
1. Немедленно смени API ключи/токены
2. Запусти `git filter-branch` (см. выше)
3. Если критично — удали репозиторий и создай новый

---

**ПОМНИ:** Git хранит ВСЮ историю навсегда. Проще предотвратить утечку, чем потом удалять.

✅ **Всегда запускай:** `bash 99\ _Сервис/Scripts/test_git_privacy.sh` перед push!

## Related

- [[index]]
- [[HEARTBEAT]]
- [[MIGRATION]]
- [[Scripts]]
- [[2026-03-19]]
- [[SKILL]]
- [[USER]]
- [[SOUL]]
- [[Все]]
- [[AGENTS]]
- [[Публикация]]
- [[IDENTITY]]
- [[README]]
- [[MEMORY]]
