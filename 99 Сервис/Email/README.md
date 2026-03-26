# Email Processing System

Автоматическая проверка и категоризация входящей почты Gmail.

## Как работает

**Крон:** каждый час (`0 * * * *`)  
**Скрипт:** `agent/scripts/email-check.sh` → `gmail-check.py`  
**Агент:** second-brain (isolated session)

## Настройка

### 1. Создать App Password в Google

1. Открой https://myaccount.google.com/security
2. Включи 2-Step Verification (если ещё не включена)
3. Найди "App passwords" → Создать новый
4. Выбери "Other" → назови "OpenClaw Second Brain"
5. Скопируй 16-значный пароль

### 2. Добавить креды в secrets.json

Файл: `~/.openclaw/agents/second-brain/agent/secrets.json`

```json
{
  "todoist_token": "существующий токен",
  "gmail_user": "your-email@gmail.com",
  "gmail_app_password": "ваш 16-значный app password"
}
```

**Важно:** App Password ≠ основной пароль! Используй только app password из Google Account Settings.

## Категории писем

### 🔴 Срочно (ответ нужен сегодня)
**Триггеры:**
- "urgent", "asap", "today"
- "срочно", "немедленно", "нужен сегодня"
- "deadline today"

**Действия:**
- Создаётся задача в Todoist (p1, deadline: today)
- Уведомление владельцу в Telegram
- Контекст письма → `vault/30 CRM/Email Context/YYYY-MM-DD-urgent.md`

### 🟡 Важно (ответ нужен на неделе)
**Триггеры:**
- "important", "важно", "необходимо"
- "action required", "please respond"
- От известных контактов (проверяется по CRM)

**Действия:**
- Заметка в `vault/00 Входящие/Email/YYYY-MM-DD-subject.md`
- Добавляется в недельный обзор

### 🟢 Информация (прочитать когда удобно)
**Триггеры:**
- Все письма, не попавшие в другие категории
- Обновления от сервисов, уведомления

**Действия:**
- Сохраняется в `vault/00 Входящие/Read Later/`
- Группируется в дайджест (1 раз в день)

### ⚫ Спам/рассылки
**Триггеры:**
- "unsubscribe", "отписаться"
- "newsletter", "рассылка"
- `noreply@`, `no-reply@`, `marketing@`

**Действия:**
- Если >3 письма от одного отправителя → предложение отписки
- Автоматическая архивация (письмо остаётся в Gmail, но не обрабатывается)

## Пример отчёта

```
📧 Проверка почты (14:00 MSK)

🔴 Срочно (2):
• От: boss@company.com
  "Нужен отчёт до конца дня"
  → ✅ Задача создана: "Отчёт для босса" (p1, сегодня)

• От: client@example.com
  "ASAP: Fix production issue"
  → ✅ Задача создана: "Production issue client" (p1, сегодня)

🟡 Важно (1):
• От: colleague@company.com
  "Обсудить архитектуру нового проекта"
  → 📝 Заметка: vault/00 Входящие/Email/2026-03-26-architecture-discussion.md

🟢 Информация (3):
• GitHub: 2 new pull requests
• Telegram: Updates available
• Stack Overflow: Weekly digest

⚫ Спам (5):
• Medium (3 письма) → Предложить отписку?
• LinkedIn notifications (2)
```

## Логи

Все проверки логируются в `vault/99 Сервис/Logs/email-checks.log`:

```
2026-03-26 14:00:15 | Checked: 11 emails | Urgent: 2 | Important: 1 | Info: 3 | Spam: 5
2026-03-26 15:00:22 | Checked: 0 emails | No new mail
```

## Безопасность

✅ **App Password хранится в `secrets.json` (chmod 600)**  
✅ **Подключение через IMAP SSL (порт 993)**  
✅ **Письма остаются в Gmail (не удаляются)**  
✅ **Только чтение INBOX (UNSEEN)**

## Отключение

```bash
# Временно отключить крон
openclaw cron disable 448c7b56-693e-4d2d-9d94-4c32baded067

# Включить обратно
openclaw cron enable 448c7b56-693e-4d2d-9d94-4c32baded067

# Удалить крон
openclaw cron remove 448c7b56-693e-4d2d-9d94-4c32baded067
```

## Доработки

**Планируется:**
- [ ] Автоматическое обновление CRM из подписей писем
- [ ] Извлечение номеров телефонов/адресов из писем
- [ ] Связывание писем с проектами (по ключевым словам)
- [ ] Автоматические ответы на типичные запросы (с подтверждением)
- [ ] Интеграция с календарём (встречи из писем → Google Calendar)
