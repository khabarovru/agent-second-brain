---
type: note
description: "dbrain-processor references — инструкции для обработки входящих"
last_accessed: 2026-04-09
relevance: 0.74
tier: warm
---

# dbrain-processor References

Справочные материалы для обработки входящих записей.

## Файлы

| Файл | Назначение |
|------|------------|
| [[process-goals]] | Process vs Outcome goals, stale detection, rechecking |
| [[classification]] | Классификация входящих по доменам и категориям |
| [[goals]] | Интеграция с целями Denis |
| [[business-context]] | CRM структура, метрики, статусы сделок |

## Использование

При обработке входящей записи:

1. **Классификация** → прочитай `classification.md`
   - Определи домен (client/AI/product/ops/content/personal)
   - Выбери категорию и приоритет

2. **Проверка целей** → прочитай `process-goals.md`
   - Связана ли запись с ONE Big Thing?
   - Обновить статус активности цели

3. **CRM** → прочитай `business-context.md`
   - Упомянут ли клиент?
   - Обновить статус сделки

## Структура

```
references/
├── README.md          ← этот файл
├── classification.md  ← дерево решений
├── process-goals.md   ← работа с целями
├── goals.md           ← интеграция целей
└── business-context.md ← CRM контекст
```

---

_Обновлено: 2026-04-09_
