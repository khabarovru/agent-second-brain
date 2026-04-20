---
type: note
description: "1. Это команда, НЕ заметка 2. Прочитать vault/20 Ежедневник/Daily Notes/2026-03-25.md 3. Посчитать записи по типам"
related: 
last_accessed: 2026-03-28
relevance: 0.91
tier: active
---
# Примеры обработки сообщений

## Пример 0: Команда /status

**Вход:**
📊 Статус

**Обработка:**
1. Это команда, НЕ заметка
2. Прочитать vault/20 Ежедневник/Daily Notes/2026-03-25.md
3. Посчитать записи по типам

**Действия:**
```bash
read vault/20 Ежедневник/Daily Notes/2026-03-25.md
```

**Анализ файла:**
```markdown
## 09:41 - Daily Auto-Upload Setup
[тип: note]

## 09:42 - Testing Reminder  
[тип: task]

## 10:17 - Migration Idea 💡
[тип: idea + task]
```

**Подсчёт:**
- Задачи: 2 (Testing Reminder, Migration Idea checklists)
- Идеи: 1 (Migration Idea)
- Заметки: 1 (Daily Auto-Upload Setup)
- Знания: 0

**Уведомление:**
```
📊 Сегодня (2026-03-25):
✅ Задач: 2
💡 Идей: 1
📝 Заметок: 1
🧠 Знаний: 0

Всего записей: 4
```

---

## Пример 1: Задача из голосового

**Вход:**
🎤 "Надо купить молоко завтра утром перед работой"

**Обработка:**
1. Тип: задача (действие "купить" + дедлайн "завтра утром")
2. Приоритет: p3 (бытовое, не срочное)
3. Дедлайн: tomorrow 09:00

**Действия:**
```bash
exec scripts/todoist-create-task.sh \
  "Купить молоко" \
  "Перед работой" \
  "3" \
  "tomorrow 09:00"

write vault/50 Задачи/Active/2026-03-26-buy-milk.md
```

**Уведомление:**
```
✅ Задача создана: "Купить молоко"
   Приоритет: p3, Дедлайн: завтра 09:00
```

---

## Пример 2: Идея из текста

**Вход:**
"Интересная мысль: можно сделать автоматический дайджест заметок за неделю и отправлять в воскресенье"

**Обработка:**
1. Тип: идея (ключевое слово "интересная мысль", нет действия)
2. Теги: #automation, #digest

**Действия:**
```bash
write vault/00 Входящие/Ideas/2026-03-25-weekly-digest-automation.md
```

**Содержимое файла:**
```markdown
---
created: 2026-03-25 12:45
type: idea
tags: [automation, digest, openclaw]
source: telegram-text
---

# Автоматический недельный дайджест

Идея: создать крон-задачу, которая каждое воскресенье:
1. Собирает все заметки за неделю
2. Группирует по типам (задачи, идеи, знания)
3. Формирует краткий дайджест
4. Отправляет в Telegram

Возможная реализация: OpenClaw cron + sessions_spawn для обработки
```

**Уведомление:**
```
💡 Идея сохранена: "Автоматический недельный дайджест"
   Файл: vault/00 Входящие/Ideas/2026-03-25-weekly-digest-automation.md
```

---

## Пример 3: Заметка с фотографией

**Вход:**
📷 Фото + текст: "Хорошая схема архитектуры second-brain, сохранить для презентации"

**Обработка:**
1. Тип: заметка (факт + контекст использования)
2. Теги: #architecture, #presentation

**Действия:**
```bash
# Сохранить фото
save photo → vault/attachments/2026-03-25-architecture-schema.png

# Создать заметку со ссылкой
write vault/10 Заметки/General/2026-03-25-second-brain-architecture.md
```

**Содержимое файла:**
```markdown
---
created: 2026-03-25 13:15
type: note
tags: [architecture, presentation, second-brain]
source: telegram-photo
attachments: [2026-03-25-architecture-schema.png]
---

# Схема архитектуры Second Brain

![Схема](../attachments/2026-03-25-architecture-schema.png)

Контекст: хорошая схема для презентации второго агента.
```

**Уведомление:**
```
📝 Заметка сохранена: "Схема архитектуры Second Brain"
   + вложение: architecture-schema.png
```

---

## Пример 4: Знание из наблюдения

**Вход:**
"Заметил: когда агенту даёшь конкретные примеры в AGENTS.md, качество ответов сразу растёт. Абстрактные правила работают хуже"

**Обработка:**
1. Тип: знание (обобщённый вывод, урок)
2. Область: agent-development
3. Теги: #openclaw, #prompting, #best-practices

**Действия:**
```bash
# Проверить существующий файл
read vault/90 Карты знаний/Knowledge Base/agent-prompting-best-practices.md

# Дополнить существующий или создать новый
write vault/90 Карты знаний/Knowledge Base/agent-prompting-best-practices.md
```

**Содержимое файла (дополнение):**
```markdown
---
created: 2026-03-15
updated: 2026-03-25
type: knowledge
tags: [openclaw, prompting, best-practices, agents]
---

# Best Practices: Промптинг агентов

## Примеры > Правила

**Урок 25.03.2026:**
Конкретные примеры в AGENTS.md работают лучше абстрактных правил.

**Было:**
```
При обработке задачи определи приоритет по контексту.
```

**Стало:**
```
Приоритеты:
- "срочно", "ASAP" → p1
- "сегодня", "важно" → p2
- обычная задача → p3
- "когда-нибудь" → p4
```

Результат: агент стабильно определяет приоритет, меньше ошибок.

**Правило:** Для каждого сложного решения давай 2-3 примера в AGENTS.md.
```

**Уведомление:**
```
🧠 Знание добавлено: "Примеры > Правила в промптинге"
   Обновлён: vault/90 Карты знаний/Knowledge Base/agent-prompting-best-practices.md
```

---

## Пример 5: Пересланное сообщение

**Вход:**
Пересланное из канала: статья про Obsidian Graph View

**Обработка:**
1. Тип: заметка (внешний контент для изучения)
2. Источник: forwarded
3. Теги: #obsidian, #tools, #to-read

**Действия:**
```bash
write vault/10 Заметки/General/2026-03-25-obsidian-graph-view-article.md
```

**Содержимое файла:**
```markdown
---
created: 2026-03-25 14:00
type: note
tags: [obsidian, tools, to-read]
source: telegram-forward
origin: @obsidian_tips
---

# Статья: Obsidian Graph View

Источник: пересланное из @obsidian_tips

[Ссылка на статью]

Коротко: обзор возможностей визуализации связей в Obsidian.

**TODO:** Прочитать и применить к своему vault.
```

**Уведомление:**
```
📌 Сохранено из @obsidian_tips: "Obsidian Graph View"
   Файл: vault/10 Заметки/General/2026-03-25-obsidian-graph-view-article.md
   Тег: #to-read
```

## Related

- [[TODOIST]]
- [[SCHEMA]]
- [[MIGRATION]]
- [[Scripts]]
- [[2026-03-26]]
- [[2026-03-28]]
- [[2026-03-15]]
- [[todoist]]
- [[TOOLS]]
- [[Все]]
- [[AGENTS]]
- [[architecture]]
- [[Заметка]]
- [[2026-03-25]]
