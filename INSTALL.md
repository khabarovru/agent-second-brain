# Quick Install (OpenClaw)

Минимальная инструкция для установки agent-second-brain на систему с OpenClaw.

## Предварительные требования

- OpenClaw установлен и работает (`openclaw status`)
- Python 3.11+ и `uv` установлены
- Telegram бот создан через @BotFather
- API ключи: Deepgram (транскрипция), Todoist (задачи)

## Установка

### 1. Клонировать репозиторий

```bash
cd ~/.openclaw/workspace/skills/
git clone https://github.com/khabarovru/agent-second-brain.git
cd agent-second-brain
```

### 2. Настроить окружение

```bash
# Копировать шаблон .env
cp .env.example .env

# Заполнить своими токенами
nano .env
```

Заполнить:
```bash
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
DEEPGRAM_API_KEY=your_deepgram_key
TODOIST_API_TOKEN=your_todoist_token  # НЕ API_KEY!
ALLOWED_USER_IDS=[your_telegram_user_id]
VAULT_PATH=/home/YOUR_USER/.openclaw/workspace/skills/agent-second-brain/vault
```

### 3. Установить зависимости

```bash
uv sync
```

### 4. Добавить агентов в OpenClaw

```bash
openclaw config patch << 'EOF'
{
  agents: {
    list: [
      {
        id: 'main',
        subagents: {
          allowAgents: ['dbrain-processor', 'goal-aligner']
        }
      },
      {
        id: 'dbrain-processor',
        name: 'dbrain-processor',
        workspace: '/home/YOUR_USER/.openclaw/workspace/skills/agent-second-brain/vault',
        agentDir: '/home/YOUR_USER/.openclaw/agents/dbrain-processor/agent',
        model: 'openrouter/free'
      },
      {
        id: 'goal-aligner',
        name: 'goal-aligner',
        workspace: '/home/YOUR_USER/.openclaw/workspace/skills/agent-second-brain/vault',
        agentDir: '/home/YOUR_USER/.openclaw/agents/goal-aligner/agent',
        model: 'openrouter/free'
      }
    ]
  }
}
EOF
```

**Замените `YOUR_USER` на ваше имя пользователя!**

### 5. Добавить TODOIST_API_KEY в .env

mcp-cli ожидает именно `TODOIST_API_KEY`, а не `TODOIST_API_TOKEN`:

```bash
echo "TODOIST_API_KEY=$(grep TODOIST_API_TOKEN .env | cut -d= -f2)" >> .env
```

### 6. Установить systemd services

```bash
# Исправить пути в service файлах (заменить YOUR_USER)
sed -i "s|/home/khabarovru|/home/YOUR_USER|g" deploy/*.service
sed -i "s|User=khabarovru|User=YOUR_USER|g" deploy/*.service

# Копировать в systemd
sudo cp deploy/*.service deploy/*.timer /etc/systemd/system/

# Перезагрузить systemd
sudo systemctl daemon-reload

# Включить и запустить
sudo systemctl enable --now d-brain-bot.service
sudo systemctl enable d-brain-process.timer
sudo systemctl enable d-brain-weekly.timer
```

### 7. Проверить статус

```bash
# OpenClaw
openclaw status

# d-brain бот
systemctl status d-brain-bot.service

# Timers
systemctl list-timers | grep d-brain

# Telegram бот логи
sudo journalctl -u d-brain-bot -f
```

### 8. Тест в Telegram

1. Найти бота по username
2. Отправить `/start`
3. Отправить голосовое сообщение
4. Проверить, что запись появилась в `vault/daily/YYYY-MM-DD.md`

## Структура проекта

```
~/.openclaw/workspace/skills/agent-second-brain/
├── vault/                    # Obsidian vault
│   ├── daily/               # Ежедневные записи
│   ├── goals/               # Цели (yearly, monthly, weekly)
│   ├── thoughts/            # Идеи, заметки
│   ├── .claude/
│   │   ├── skills/         # Skills для агентов
│   │   ├── rules/          # Форматирование
│   │   └── agents/         # Шаблоны агентов
│   └── MEMORY.md           # Долгосрочная память
├── scripts/
│   ├── process.sh          # Ежедневная обработка (21:00)
│   └── weekly.py           # Недельный дайджест (пятница 06:00)
├── deploy/                  # systemd services
└── .env                     # Токены (НЕ коммитить!)
```

## Автоматика

После установки работает автоматически:

- **Telegram бот** — всегда онлайн (systemd service)
- **21:00 UTC** — обработка daily файлов → задачи в Todoist + отчёт
- **Пятница 06:00** — недельный дайджест

## Команды бота

- `/start` — приветствие
- `/status` — статистика дня
- `/process` — обработать записи прямо сейчас
- `/weekly` — недельный отчёт

## Troubleshooting

### Бот не отвечает

```bash
# Проверить логи
sudo journalctl -u d-brain-bot -n 50

# Проверить токен
cat .env | grep TELEGRAM_BOT_TOKEN
```

### Todoist не создаёт задачи

```bash
# Тест mcp-cli
cd ~/.openclaw/workspace/skills/agent-second-brain
export $(cat .env | xargs)
mcp-cli call todoist get-overview '{}'
```

### OpenClaw агент не работает

```bash
# Проверить конфигурацию
openclaw config get | grep -A 10 dbrain-processor

# Проверить allowAgents
openclaw config get | grep -A 5 "subagents"
```

## Ссылки

- [Полный README](README.md)
- [Русская документация](README.ru.md)
- [VPS setup guide](docs/vps-setup.md)
- [Upstream репозиторий](https://github.com/smixs/agent-second-brain)
