---
type: note
description: Обработка ежедневных голосовых и текстовых записей из Telegram. Классифицирует контент, создаёт задачи в Todoist, сохраняет мысли в Obsidian, генерирует HTML-отчёт. Интегрирован с бизнес-контекстом (объекты, подрядчики, CRM).
last_accessed: 2026-04-01
relevance: 1.0
tier: active
name: dbrain-processor
depends_on: [graph-builder, todoist-ai, agent-memory, vault-health]
---

# d-brain Processor

Обработка дневниковых записей → задачи (Todoist) + мысли (Obsidian) + HTML-отчёт (Telegram).

## CRITICAL: Формат вывода

**ВСЕГДА возвращай RAW HTML. Без исключений. Без markdown.**

Правила:
1. ВСЕГДА возвращай HTML-отчёт — даже если записи уже обработаны
2. ВСЕГДА используй шаблон ниже — без произвольного текста
3. НИКОГДА не используй markdown (**, ##, ```, -)
4. НИКОГДА не объясняй что делал в plain text — всё в HTML-отчёте

## Todoist — bash-скрипты

**ВСЕГДА используй bash-скрипты. НЕ используй mcp-cli.**

```bash
SCRIPTS="/home/node/.openclaw/agents/second-brain/agent/scripts"

# Найти задачи по лейблу
bash "$SCRIPTS/todoist-find-tasks.sh" '{"labels": ["process-goal"]}'

# Создать задачу
bash "$SCRIPTS/todoist-add-task.sh" '{"content": "Задача", "priority": 2, "due_string": "tomorrow"}'

# Создать задачу (альтернативный скрипт с аргументами)
bash "$SCRIPTS/todoist-create-task.sh" "Название" "Описание" 2 "tomorrow"

# Все активные задачи
bash "$SCRIPTS/todoist-find-tasks.sh" '{}'
```

### Приоритеты:
- 4 = p1 (наивысший)
- 3 = p2 (высокий)
- 2 = p3 (средний)
- 1 = p4 (обычный)

## Processing Flow

1. **Загрузи контекст целей** — прочитай:
   - `vault/60 Цели/3-weekly.md` → ONE Big Thing (секция `## ONE Big Thing`)
   - `vault/60 Цели/2-monthly.md` → Top 3 приоритеты
   - `vault/60 Цели/1-yearly-2026.md` → годовые цели

2. **Загрузи бизнес-контекст** — прочитай:
   - `references/about.md` — профиль владельца
   - `references/business-context.md` — объекты, подрядчики
   - `references/contacts.md` — ключевые контакты

3. **Прочитай дневник** — `vault/20 Ежедневник/Daily Notes/YYYY-MM-DD.md`

4. **Проверь загрузку** — запусти:
   ```bash
   bash "$SCRIPTS/todoist-find-tasks.sh" '{}'
   ```

5. **Проверь process goals**:
   ```bash
   bash "$SCRIPTS/todoist-find-tasks.sh" '{"labels": ["process-goal"]}'
   ```
   Если пусто → создай из целей (см. раздел Process Goals)

6. **Обработай записи** — классифицируй каждую: task / idea / reflection / learning

7. **Создай задачи** в Todoist для всех `task`

8. **Сохрани мысли** в vault для всех `idea/reflection/learning`

9. **Залогируй действия** в дневник (append в `20 Ежедневник/Daily Notes/YYYY-MM-DD.md`)

10. **Сгенерируй HTML-отчёт** и отправь в Telegram

## Process Goals (Шаг 5 детально)

**Если process goals ОТСУТСТВУЮТ — создай автоматически без вопросов:**

```bash
# Заполни из 60 Цели/3-weekly.md и 60 Цели/2-monthly.md
bash "$SCRIPTS/todoist-add-task.sh" '{"content": "2h deep work: [ONE Big Thing]", "due_string": "every weekday at 9am", "priority": 3, "labels": ["process-goal"]}'
bash "$SCRIPTS/todoist-add-task.sh" '{"content": "1 действие/день: [monthly priority]", "due_string": "every weekday", "priority": 2, "labels": ["process-goal"]}'
bash "$SCRIPTS/todoist-add-task.sh" '{"content": "30 мин: [yearly focus]", "due_string": "every day", "priority": 1, "labels": ["process-goal"]}'
```

**Формулировка — ПРОЦЕСС, не результат:**
- ❌ "Закрыть договор по Кампусу" → ✅ "Позвонить по статусу договора Кампус"
- ❌ "Получить КП" → ✅ "Написать Бурлаченко — запросить КП"
- ❌ "Сделать освидетельствование" → ✅ "30 мин: подготовка документов освидетельствование"

## Классификация записей

**Task** = действие + (дедлайн | контекст выполнения)
- "Надо бы...", "Завтра сделать...", "Напомни..."
- Любое упоминание объекта + действия (Кампус + допуск, Шайба + ДС)

**Idea** = креативная мысль, гипотеза, инсайт

**Reflection** = наблюдение, вывод из опыта

**Learning** = урок, правило, важный факт

## Бизнес-контекст

Объекты (из references/business-context.md):
- Кампус, Сириус Арена, Университет, Шайба, Альфа, Гамма, М2, М10, Автодром, Айсберг, Дельта, Омега, Пульсар, Воскресенская, КТ, Сигма, Концертный комплекс

Ключевые термины → типовые задачи:
- "допуск [объект]" → задача на подачу списка сотрудников
- "ДС [объект]" → задача на подписание доп. соглашения
- "освидетельствование" → задача на плановое освидетельствование
- "КП [подрядчик]" → задача на запрос коммерческого предложения

## Приоритет задач

| Условие | Приоритет |
|---------|-----------|
| Совпадает с ONE Big Thing | p2 (priority: 3) |
| Совпадает с месячным приоритетом | p2-p3 |
| Срочно / дедлайн сегодня-завтра | p1 (priority: 4) |
| Совпадает с годовой целью | p3 (priority: 2) |
| Операционное без цели | p4 (priority: 1) |

## Сохранение мыслей

```
vault/00 Входящие/Ideas/YYYY-MM-DD-название.md     ← идеи
vault/90 Карты знаний/Knowledge Base/тема.md        ← знания
```

Формат файла:
```yaml
---
created: YYYY-MM-DD HH:MM
type: idea|reflection|learning
tags: [tag1, tag2]
source: telegram-voice|telegram-text
---
# Название

Содержимое...
```

## Логирование в дневник

После обработки — дописать в `vault/20 Ежедневник/Daily Notes/YYYY-MM-DD.md`:

```
## HH:MM [text]
Обработка ежедневных записей

**Создано задач:** N
- "Название задачи" (id: XXX, p2, дедлайн)

**Сохранено мыслей:** M
- "Название мысли" → category/
```

## HTML Report Template

Возвращай RAW HTML (без markdown, без code blocks):

📊 <b>Обработка за {DATE}</b>

<b>🎯 Текущий фокус:</b>
{ONE_BIG_THING}

<b>📓 Сохранено мыслей:</b> {N}
• {emoji} {title} → {category}/

<b>✅ Создано задач:</b> {M}
• {task} <i>({priority}, {due})</i>

<b>📋 Process Goals:</b>
• {process goal 1} → ✅ активен
• {process goal 2} → ⚠️ просрочен
{N} активных | {M} требуют внимания

<b>📅 Загрузка на неделю:</b>
Пн: {n} | Вт: {n} | Ср: {n} | Чт: {n} | Пт: {n} | Сб: {n} | Вс: {n}

<b>⚠️ Требует внимания:</b>
• {просроченные задачи}

<b>⚡ Топ-3 приоритета:</b>
1. {task}
2. {task}
3. {task}

---
<i>Обработано за {duration}</i>

## Если записи уже обработаны

Если все записи имеют маркер `<!-- ✓ processed -->`:

📊 <b>Статус за {DATE}</b>

<b>🎯 Текущий фокус:</b>
{ONE_BIG_THING}

<b>📋 Process Goals:</b>
• {process goal 1} → {status}
{N} активных | {M} требуют внимания

<b>📅 Загрузка на неделю:</b>
Пн: {n} | Вт: {n} | Ср: {n} | Чт: {n} | Пт: {n} | Сб: {n} | Вс: {n}

<b>⚡ Топ-3 приоритета:</b>
1. {task}
2. {task}
3. {task}

---
<i>Записи уже обработаны ранее</i>

## Разрешённые HTML-теги

<b> — жирный
<i> — курсив
<code> — команды, пути
<s> — зачёркнутый
<u> — подчёркнутый
<a href="url">текст</a> — ссылки

Максимум: 4096 символов.

## References

- references/about.md — профиль владельца
- references/classification.md — правила классификации
- references/business-context.md — объекты, подрядчики
- references/contacts.md — контакты
- references/goals.md — логика привязки к целям
- references/process-goals.md — process vs outcome
- references/rules.md — обязательные правила
- references/todoist.md — детали создания задач
