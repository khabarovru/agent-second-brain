---
type: note
last_accessed: 2026-04-09
relevance: 0.74
tier: warm
---
# HEARTBEAT.md - Сисадмин

Проверяй каждые 5 минут:
1. Есть ли новые алерты в Home Assistant (system_log)
2. Не появились ли новые предупреждения конфигурации
3. Статус Docker-контейнеров на Xpenology

Команда проверки:
```bash
ssh -o ConnectTimeout=10 khabarovru@192.168.1.134 "/usr/local/bin/docker ps --format '{{.Names}}: {{.Status}}'" 2>/dev/null
```

Если что-то не так — доложи в Telegram.
