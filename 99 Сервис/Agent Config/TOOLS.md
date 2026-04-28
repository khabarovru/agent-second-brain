---
type: note
description: "- Движок: mlx-whisper (Apple Silicon GPU) - Скрипт: ~/.openclaw/whisper-env/bin/python3 ~/.openclaw/whisper-env/transcribe.py <файл> ru - Модель..."
related: 
last_accessed: 2026-03-28
relevance: 0.56
tier: cold
---
# TOOLS.md - Локальные настройки

## Whisper (STT)
- Движок: mlx-whisper (Apple Silicon GPU)
- Скрипт: ~/.openclaw/whisper-env/bin/python3 ~/.openclaw/whisper-env/transcribe.py <файл> ru
- Модель: mlx-community/whisper-small-mlx
- Скорость: ~1.5 сек на короткое сообщение

## TTS (голосовые ответы)
- Движок: edge-tts (Microsoft, бесплатно)
- Голос: ru-RU-DmitryNeural (мужской, пониженный тон)
- Команда: ~/.openclaw/whisper-env/bin/edge-tts --voice "ru-RU-DmitryNeural" --pitch="-10Hz" --rate="-5%" --text "текст" --write-media output.mp3
- Потом конвертация: ffmpeg -y -i output.mp3 -c:a libopus -b:a 64k output.ogg

## Напоминания
Все напоминания → sessionTarget: "isolated" + payload.kind: "agentTurn"
НИКОГДА sessionTarget: "main" + systemEvent!

## Погода Сочи
- Скилл: `skills/weather-sochi/`
- Скрипты: `fetch_weather.sh` (сбор данных) + `format_report.py` (форматирование)
- Крон: каждый день в 07:00 МСК (ID: 8ce94ffc-a96e-4eb6-8f46-542f85a2fb01)
- Источники: Open-Meteo (температура, ветер, давление, влажность) + NOAA (магнитное поле)
- Формат: полный отчет с рекомендациями одежды, зонтом, качеством воздуха, температурой моря

## После обновления OpenClaw
1. Запустить: scripts/post-update-check.sh
2. Или сказать: "продиагностируй себя" (Agent Doctor)
3. Скилл: skills/agent-doctor/SKILL.md

НЕ openclaw gateway restart из сессии!
Mac: launchctl kickstart -k gui/$(id -u) ai.openclaw.gateway

## Маршрутизация моделей
- Мощная (Opus): разговор, стратегия, тексты
- Быстрая (Sonnet): данные, черновики, кроны
Кроны: полное имя модели (anthropic/claude-sonnet-4-6)
SQLite WAL обязателен!

## Браузеры

### 1. Google Chrome (основной)
- Путь: /Applications/Google Chrome.app
- Для: проверка лимитов Claude, интерфейсы, сайты с авторизацией
- Профиль openclaw для сохранения куки и сессий
- Запуск: open -a "Google Chrome" или через agent-browser --executable-path

### 2. agent-browser (Chromium, автоматизация)
- Путь: /opt/homebrew/bin/agent-browser
- Для: сложные автоматизации, Accessibility Tree, скриншоты с номерами
- Workflow: open → snapshot -i → click @e1 → fill @e2 "text"

### 3. Lightpanda (ультралёгкий headless)
- Путь: scripts/lightpanda
- Для: быстрый парсинг текста, HTML для субагентов/кронов
- 11x быстрее Chrome, 9x меньше памяти
- Пример: scripts/lightpanda fetch --dump markdown https://example.com

## Агент-доктор (Doktor[AGENT_NAME])
- Папка: ~/Desktop/agent-doctor/
- Бот: @Doktor[AGENT_NAME]_bot
- Движок: ClaudeClaw (Claude Code CLI)
- Сервис: com.claudeclaw.doctor (LaunchAgent)
- Логи: ~/Desktop/agent-doctor/logs/
- Перезапуск: launchctl kickstart -k gui/$(id -u) com.claudeclaw.doctor
- Работает по подписке Max (claude login)
- У меня полный доступ к его папке, у него - к моей

## Obsidian Vault

### Путь
`/home/khabarovru/.openclaw/agents/second-brain/vault`

### Скрипты обслуживания (Python 3)
Все исполняемые, только stdlib (внешних пакетов не требуется):

#### Graph Builder
- `99 Сервис/Skills/graph-builder/scripts/build_graph.py` — построение графа связей
- `99 Сервис/Skills/graph-builder/scripts/analyze.py` — анализ и предложения связей

#### Vault Health
- `99 Сервис/Skills/vault-health/scripts/generate_moc.py` — генерация MOC
- `99 Сервис/Skills/vault-health/scripts/add_descriptions.py` — добавление описаний в frontmatter
- `99 Сервис/Skills/vault-health/scripts/fix_links.py` — исправление битых ссылок
- `99 Сервис/Skills/vault-health/scripts/connect_orphans.py` — подключение orphan файлов

#### Agent Memory
- `99 Сервис/Skills/agent-memory/scripts/memory-engine.py` — управление памятью (Ebbinghaus curve)

### Автоматическое обслуживание (cron)

#### Еженедельно (понедельник 02:00 MSK)
```bash
# ID: 427c4907-4af4-46dd-85ba-2922d058a339
# Обновление графа + memory decay
build_graph.py + memory-engine.py decay + stats
```

#### Еженедельно (вторник 04:00 MSK)
```bash
# ID: 2fde2adb-b6ff-47e5-838c-51e8d38fe720
# Проверка frontmatter
memory-engine.py scan + init (если нужно)
```

#### Ежемесячно (1-е число 03:00 MSK)
```bash
# ID: 23a15a5a-5c41-4b47-8506-5f459128d296
# Исправление ссылок + orphans + MOC
fix_links.py --apply + connect_orphans.py --apply + generate_moc.py + build_graph.py
```

### Ручное обслуживание
```bash
cd /home/khabarovru/.openclaw/agents/second-brain/vault

# Анализ и предложения связей
python3 "99 Сервис/Skills/graph-builder/scripts/analyze.py" > ~/Desktop/link-suggestions.md

# Добавление описаний в frontmatter
python3 "99 Сервис/Skills/vault-health/scripts/add_descriptions.py" --apply

# Проверка здоровья памяти
python3 "99 Сервис/Skills/agent-memory/scripts/memory-engine.py" stats .

# Случайные карточки (creative prompts)
python3 "99 Сервис/Skills/agent-memory/scripts/memory-engine.py" creative 5 .
```

### Статистика (актуально на 2026-03-25)
- 468 файлов, 0 без frontmatter ✅
- 351 файл в графе, 1710 связей
- 59 orphan файлов (большинство из .stversions)
- 1203 битых ссылки (требуют ручного аудита)
- Tier distribution: active 18%, warm 44%, cold 1%, archive 36%

### obsidian-cli
```bash
# Установлен через Homebrew
obsidian-cli --version

# Vault по умолчанию: vault (/home/khabarovru/.openclaw/agents/second-brain/vault)

# Поиск по названиям заметок
obsidian-cli search "query"

# Поиск по содержимому
obsidian-cli search-content "query"

# Создание заметки
obsidian-cli create "Folder/New note" --content "..." --open

# Переименование/перемещение (обновляет ссылки!)
obsidian-cli move "old/path/note" "new/path/note"

# Удаление
obsidian-cli delete "path/note"
```
