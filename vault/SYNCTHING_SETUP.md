# Syncthing Setup — Синхронизация vault

> Инструкция по настройке Syncthing для синхронизации vault между Windows ПК и сервером OpenClaw.

## 🎯 Цель

**Двусторонняя синхронизация:**
- **Windows ПК → Сервер:** Рабочие заметки (00-95 папки), системные файлы (MEMORY.md и т.д.)
- **Сервер → Windows ПК:** Skills (99 _Сервис/), обновления от бота
- **Обе стороны:** Obsidian конфигурация (.obsidian/)

## 📋 Предварительные требования

- ✅ Syncthing установлен на обеих сторонах
- ✅ Устройства уже добавлены друг к другу

**ID устройств:**
- **Windows ПК (router):** `5ULBLRJ-2OLQ57T-JOUGJL7-GLEWX63-GXKY6VP-I7HLVFA-GRLCUYZ-T3B24QD`
- **Сервер (n100):** `IIHPVBO-KEAR4XF-BMEDNK4-EUHDZIY-MDCY544-YW7W2MM-DOR5A6S-LPLHKQA`

## 🔧 Настройка на Windows ПК

### 1. Открой Syncthing Web UI

```
http://localhost:8384
```

### 2. Добавь папку

1. **Add Folder** (правая панель)

2. **General:**
   - **Folder Label:** `Vault Second Brain`
   - **Folder ID:** `vault-second-brain` ⚠️ **ВАЖНО:** точно как здесь!
   - **Folder Path:** `C:\Users\habarov.db\Documents\__Для Обсидиан\vault_second_brain`

3. **Sharing:**
   - ✅ **Share with device:** `n100` (сервер)

4. **File Versioning:**
   - **Type:** `Staggered`
   - **Max Age:** `30` days
   - **Clean Out After:** `0` (никогда не удалять)

5. **Advanced:**
   - **Folder Type:** `Send & Receive`
   - **Rescan Interval:** `60` seconds
   - **File Pull Order:** `Random`
   - **Ignore Permissions:** ☐ (не включать — нужны права для скриптов)
   - **Watch for Changes:** ✅
   - **Ignore Patterns:** (оставить пустым — загрузится с сервера)

6. **Save**

### 3. Дождись подтверждения с сервера

Syncthing покажет уведомление на Windows ПК:
```
Device 'n100' wants to share folder 'Vault Second Brain'
```

**Нажми:** `Add` (подтвердить)

## 🔧 Настройка на сервере (n100)

### 1. Открой Syncthing Web UI

```
http://192.168.1.81:8384
```

Логин: `khabarovru`  
Пароль: (спроси у админа)

### 2. Добавь папку

1. **Add Folder** (правая панель)

2. **General:**
   - **Folder Label:** `Vault Second Brain`
   - **Folder ID:** `vault-second-brain` ⚠️ **ВАЖНО:** точно как на ПК!
   - **Folder Path:** `/home/khabarovru/.openclaw/workspace/skills/agent-second-brain/vault`

3. **Sharing:**
   - ✅ **Share with device:** `router` (Windows ПК)

4. **File Versioning:**
   - **Type:** `Staggered`
   - **Max Age:** `30` days

5. **Advanced:**
   - **Folder Type:** `Send & Receive`
   - **Ignore Permissions:** ☐ (не включать)
   - **Watch for Changes:** ✅

6. **Save**

### 3. Дождись подтверждения от Windows ПК

Syncthing покажет уведомление на сервере:
```
Device 'router' wants to share folder 'Vault Second Brain'
```

**Нажми:** `Add` (подтвердить)

## 🔍 Проверка синхронизации

### 1. Статус на обеих сторонах

**Syncthing UI → Folders → Vault Second Brain:**
- Статус должен быть: `Up to Date` или `Syncing`
- Количество файлов примерно одинаковое

### 2. Тест файла

**На Windows ПК:**
```
echo "test syncthing" > vault_second_brain\test-sync.txt
```

**Проверь на сервере (через 1-2 минуты):**
```bash
cat ~/.openclaw/workspace/skills/agent-second-brain/vault/test-sync.txt
```

Должен вывести: `test syncthing`

**Удали тестовый файл:**
```bash
rm ~/.openclaw/workspace/skills/agent-second-brain/vault/test-sync.txt
```

(Удаление синхронизируется обратно на ПК)

## 📁 Что синхронизируется

### ✅ Синхронизируется:

- **Заметки:** 00-95 папки (рабочие проекты, объекты, задачи и т.д.)
- **Skills:** 99 _Сервис/Skills/ (AgentSkills для бота)
- **Scripts:** 99 _Сервис/Scripts/ (вспомогательные скрипты)
- **Документация:** 99 _Сервис/*.md
- **Obsidian конфигурация:** .obsidian/ (плагины, темы, настройки)
- **Системные файлы:** MEMORY.md, USER.md, SOUL.md, AGENTS.md и т.д.
- **README.md** и другая документация

### ❌ НЕ синхронизируется (см. `.stignore`):

- **.git/** — Git репозиторий (только на сервере)
- **.obsidian/workspace.json** — персональный для каждого устройства
- **.obsidian/cache/** — кеш (пересоздаётся локально)
- **Временные файлы:** .DS_Store, Thumbs.db, *.tmp, *.swp
- **Syncthing служебные:** .stfolder/, .stversions/

## 🔄 Как работает синхронизация

### Направление sync

**Тип: Send & Receive (двусторонний)**

- Windows ПК изменяет заметку → синхронизируется на сервер
- Сервер обновляет Skills → синхронизируется на ПК
- Конфликты разрешаются автоматически (создаётся `.sync-conflict` файл)

### Versioning (версионирование)

- **Staggered Versioning:** старые версии файлов сохраняются 30 дней
- Путь к версиям: `.stversions/` (в корне vault)
- Можно откатить файл если что-то сломалось

### Conflict Resolution (разрешение конфликтов)

Если файл изменился на обеих сторонах одновременно:
1. Syncthing сохраняет обе версии
2. Новый файл называется: `file.sync-conflict-YYYYMMDD-HHMMSS.ext`
3. Вручную выбери нужную версию и удали `.sync-conflict`

## 🛠️ Troubleshooting

### Проблема: Папка не синхронизируется

**Проверь:**
1. Статус устройства: должен быть `Connected`
2. Folder ID одинаковый на обеих сторонах
3. Путь к папке правильный (существует на обеих сторонах)
4. Права доступа: пользователь может писать в папку

**Логи:**
- Syncthing UI → Actions → Logs
- Ищи ошибки связанные с `vault-second-brain`

### Проблема: Конфликты файлов

**Если появились `.sync-conflict` файлы:**

1. Открой оба файла (оригинал + conflict)
2. Сравни содержимое
3. Объедини вручную если нужно
4. Удали `.sync-conflict` файл

**Предотвращение:**
- Не редактируй один файл на обеих сторонах одновременно
- Дождись синхронизации (статус `Up to Date`) перед редактированием

### Проблема: Syncthing медленный

**Оптимизация:**

1. **Уменьши Rescan Interval:** 60 → 300 секунд (если изменения редкие)
2. **File Pull Order:** Random → By Name (предсказуемая очередь)
3. **Игнорируй большие файлы:** Добавь в `.stignore`:
   ```
   *.mp4
   *.avi
   *.iso
   ```

### Проблема: Высокая загрузка CPU

**Причина:** File Watcher на большом количестве файлов

**Решение:**
- Отключи **Watch for Changes** в Advanced
- Syncthing будет сканировать папку каждые 60 секунд вместо мгновенного отслеживания

## 📖 Документация

- **Syncthing Docs:** https://docs.syncthing.net/
- **Ignore Patterns:** https://docs.syncthing.net/users/ignoring.html
- **Versioning:** https://docs.syncthing.net/users/versioning.html
- **.stignore:** `vault/.stignore` (правила игнорирования)

## 🔐 Безопасность

- **Шифрование:** Syncthing использует TLS для передачи данных
- **Локальная сеть:** Трафик идёт напрямую (ПК ↔ Сервер), без облака
- **Приватность:** Никакие данные не отправляются третьим лицам
- **Пароли:** Syncthing Web UI защищён паролем

---

**Настройка завершена!** 🎉

Vault теперь синхронизируется между Windows ПК и сервером OpenClaw.
