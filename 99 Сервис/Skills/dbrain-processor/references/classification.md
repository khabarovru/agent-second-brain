---
type: reference
description: "Entry Classification — домены, приоритеты, маршрутизация"
last_accessed: 2026-04-09
relevance: 0.74
tier: warm
---

# Entry Classification — классификация входящих записей

## Домены → Категории

### Client Work
Брифы, стратегии, креатив, кампании, KPI, предложения

**Keywords:** клиент, бриф, презентация, дедлайн, KPI, КП, договор

**→ Category:** task (p1-p2) → Todoist

### AI & Tech
Инструменты, модели, промпты, пайплайны, агенты

**Keywords:** GPT, Claude, модель, агент, API, пайплайн, автоматизация, интеграция, OpenClaw

**→ Category:** learning или idea → `10 Заметки/`

### Product
Идеи, гипотезы, MVP, юнит-экономика

**Keywords:** продукт, SaaS, MVP, гипотеза, монетизация, юнит-экономика

**→ Category:** idea или project → `10 Заметки/`

### Ops (Company Operations)
Команда, процессы, автоматизация, найм, управление, финансы

**Keywords:** команда, найм, процесс, HR, финансы, агентство

**→ Category:** task или project (зависит от срочности)

### Content
Посты, идеи, тезисы

**Keywords:** пост, LinkedIn, контент, тезис, статья

**→ Category:** idea → `00 Входящие/Ideas/` или task если с дедлайном

### Personal
Здоровье, привычки, отношения, семья

**Keywords:** здоровье, вес, зал, привычка, семья, отдых

**→ Category:** task → Coach agent

---

## Дерево решений

```
Входящее содержит...
│
├─ Client brand или deadline?
│   → TASK (p1-p2)
│
├─ Operational/urgent?
│   (нужно сделать, не забыть, позвонить, встреча)
│   → TASK (p2-p3)
│
├─ AI/tech learning?
│   → LEARNING
│
├─ Product/SaaS idea?
│   → IDEA или PROJECT
│
├─ Personal (health, habits)?
│   → TASK → Coach agent
│
└─ Content idea?
    → IDEA
```

## CRM Status Keywords

| Keywords | Интерпретация |
|----------|---------------|
| "подписали", "выиграли", "получили" | Позитивный исход → обновить CRM |
| "отказали", "проиграли" | Негативный исход → записать как урок |
| "отправили КП", "подали" | В процессе → обновить CRM |
| "ждём ответ", "на рассмотрении" | Ожидание → проверить через N дней |

## Повышение приоритета

Если запись связана с целями:

| Связь | Default | Boost to |
|-------|---------|----------|
| ONE Big Thing (weekly) | p3 | p2 |
| Monthly priority | p3 | p2-p3 |
| Yearly goal | p4 | p3 |
| Нет связи | p4 | p4 |

## Output Locations

| Category | Destination | Priority |
|----------|-------------|----------|
| task (client) | Todoist | p1-p2 |
| task (ops) | Todoist | p2-p3 |
| task (personal) | Coach/Todoist | p2-p3 |
| idea | `00 Входящие/Ideas/` | — |
| learning | `10 Заметки/` | — |
| project | `60 Проекты/` | — |

## File Naming

```
{date}-short-title.md
```

Examples:
```
2026-04-09-saas-pricing-model.md
2026-04-09-claude-agent-pipeline.md
2026-04-09-client-Шайба-followup.md
```

## Anti-Patterns

❌ Абстрактные рассуждения без Next Action  
❌ Академическая теория без применения  
❌ Повторы без синтеза  
❌ Задачи типа "подумать о..."  
❌ Хаотичные списки без приоритетов

## MOC Updates

После создания файла добавить ссылку в:
```
90 Карты знаний/MOC-{category}.md
```

---

_Обновлено: 2026-04-09 (адаптировано из smixs/agent-second-brain)_

## Related

- [[TODOIST]]
- [[EXAMPLES]]
- [[patterns]]
- [[todoist]]
- [[2026-04-09]]
- [[Привычки]]
