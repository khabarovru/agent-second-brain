---
type: home
title: 🏠 Home
description: "TABLE WITHOUT ID choice(tier = \"active\", \"🔴\", choice(tier = \"warm\", \"🟡\", choice(tier = \"cold\", \"🔵\", \"⚫\"))) + \" \" + round(relevance * 100) + \"%\" AS..."
tags: [dashboard]
last_accessed: 2026-04-05
relevance: 0.91
tier: active
---

# 🏠 Denis Khabarov — Second Brain

## 🔥 Горячие заметки

> Топ-20 по яркости (Эббингауз). Чем выше % — тем свежее в памяти.

```dataview
TABLE WITHOUT ID
  choice(tier = "active", "🔴", choice(tier = "warm", "🟡", choice(tier = "cold", "🔵", "⚫"))) + " " + round(relevance * 100) + "%" AS "Яркость",
  file.link AS "Заметка",
  last_accessed AS "Доступ"
FROM "10 Заметки" OR "00 Входящие" OR "70 Люди" OR "50 Задачи"
WHERE relevance != null AND file.name != "MOC-tasks" AND file.name != "MOC-contacts"
SORT relevance DESC
LIMIT 20
```

---

## ✅ Активные задачи

```dataview
TABLE WITHOUT ID
  file.link AS "Задача",
  due_date AS "Дедлайн",
  priority AS "P"
FROM "50 Задачи/Active"
SORT due_date ASC
LIMIT 10
```

---

## 📥 Входящие

```dataview
TABLE WITHOUT ID
  file.link AS "Запись",
  file.ctime AS "Добавлено"
FROM "00 Входящие"
SORT file.ctime DESC
LIMIT 7
```

---

## 📅 Дневник

```dataview
LIST
FROM "20 Ежедневник/Daily Notes"
SORT file.name DESC
LIMIT 5
```

---

## 🎯 Цели

```dataview
LIST
FROM "60 Цели"
WHERE file.name != "MOC-goals" AND file.name != "1-yearly-YYYY"
SORT file.name ASC
```

## Related

- [[Люди]]
- [[MOC-goals]]
- [[MOC-tasks]]
- [[1-yearly-YYYY]]
- [[goals]]
- [[Заметка]]
- [[MOC-contacts]]
- [[contacts]]
