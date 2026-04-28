---
type: reference
description: "Process Goals — отличие process от outcome goals, stale detection, rechecking"
last_accessed: 2026-04-09
relevance: 0.74
tier: warm
---

# Process Goals — продвинутая логика работы с целями

## Outcome vs Process Goals

**Outcome goals** — ЧТО хочешь достичь:
- "Закрыть сделку"
- "Запустить продукт"

**Process goals** — КАК это делаешь:
- "2h deep work на MVP каждое утро"
- "3 follow-up письма в день"

### Почему Process работает лучше

1. **Контроль** — контролируешь действия, не результат
2. **Уверенность** — превращает вызов в конкретные шаги
3. **Фокус** — ясно что делать каждый день

## Трансформация

| Outcome | Process |
|---------|---------|
| "Закрыть сделку с клиентом" | "1 follow-up в день клиенту" |
| "Запустить продукт" | "2h deep work на MVP каждое утро" |
| "Привлечь 10 клиентов" | "5 outreach сообщений в день" |

## Rechecking — Проверка целей

**При каждой обработке входящих:**

1. Прочитать `60 Цели/3-weekly.md` → ONE Big Thing
2. Прочитать `60 Цели/2-monthly.md` → Top 3 priorities
3. Прочитать `60 Цели/1-yearly-2026.md` → годовые цели

**Для каждой новой задачи спросить:**
- Связана с ONE Big Thing? → добавить `→ Weekly focus`
- Связана с monthly priority? → добавить `→ Monthly: [название]`
- Связана с yearly goal? → добавить `→ Goal: [название]`

## Stale Detection — Определение застоявшихся целей

**Автоматическая проверка (cron job):**

| Без активности | Статус | Действие |
|----------------|--------|----------|
| 0-7 дней | 🟢 Active | Всё ок |
| 8-14 дней | 🟡 Warm | Проверить актуальность |
| 15-30 дней | 🟠 Stale | Спросить: "Это ещё важно?" |
| 30+ дней | 🔴 Dormant | Предложить архивировать |

**Как определять активность:**
- Task создан → цель "active"
- Заметка/мысль сохранена → цель "active"
- Ссылка на цель в новом файле → цель "active"

## Anti-Patterns

❌ "Поработать над проектом" (сколько? когда?)  
❌ "4h deep work 5 дней в неделю" (неSustainable)  
❌ "Подумать о стратегии" (не измеримо)

✅ Конкретное действие + время/частота + измеримость

## Пример обработки

```
Входящее: "Нужно закрыть сделку с Шайбой"

BAD: Создать задачу "Закрыть сделку с Шайбой" p1
→ Неясно, создаёт тревогу, непонятно что делать

GOOD: Создать задачу "Отправить follow-up в Шайбу с обновлённым КП" p1 due:tomorrow
→ Конкретно, выполнимо, подконтрольно
```

## Todoist Integration

Process goals → recurring tasks:

| Process | dueString |
|---------|-----------|
| "каждое утро" | `every day at 6am` |
| "каждый день" | `every day` |
| "3 раза в неделю" | `every monday, wednesday, friday` |
| "раз в неделю" | `every week` |
| "до пятницы" | `friday` (one-time) |

## Формат цели в YAML

```yaml
---
type: goal
goal_type: [outcome|process]
area: [career|health|relationships|growth|finance]
status: [active|warm|stale|dormant]
last_activity: YYYY-MM-DD
tier: active
---

# Название цели

## Outcome
[Что хотим достичь]

## Process
[Конкретные шаги]

## Progress
- [ ] Milestone 1
- [ ] Milestone 2
```

---

_Обновлено: 2026-04-09 (адаптировано из smixs/agent-second-brain)_

## Related

- [[TODOIST]]
- [[patterns]]
- [[todoist]]
- [[2026-04-09]]
- [[3-weekly]]
- [[1-yearly-2026]]
- [[goals]]
- [[Заметка]]
- [[2-monthly]]
