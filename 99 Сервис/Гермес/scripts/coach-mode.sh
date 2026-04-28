#!/bin/bash
# coach-mode.sh — Коуч-режим
# Активируется: /коуч

VAULT="/volume1/docker/openclaw/.openclaw/workspace/skills/agent-second-brain/vault"
TODOIST_TOKEN="c1f7278f1dd135b6f0dcdf4a01018c70aead351f"

echo "🎯 Коуч-режим"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 1. 📋 Todoist — задачи на сегодня и просроченные
echo "📋 Todoist:"
overdue=$(curl -s "https://api.todoist.com/api/v8/tasks" \
  -H "Authorization: Bearer $TODOIST_TOKEN" \
  -G -d "filter=overdue" 2>/dev/null | jq '.tasks | length' 2>/dev/null || echo "0")
today_tasks=$(curl -s "https://api.todoist.com/api/v8/tasks" \
  -H "Authorization: Bearer $TODOIST_TOKEN" \
  -G -d "filter=today" 2>/dev/null | jq '.tasks | length' 2>/dev/null || echo "0")

if [ "$overdue" -gt 0 ]; then
    echo "   ⚠️  Просрочено: $overdue — шевелись!"
else
    echo "   ✅ Нет просроченных"
fi
echo "   📅 На сегодня: $today_tasks задач"
echo ""

# 2. 🎯 Цели — проверка из vault
echo "🎯 Цели:"
yearly="$VAULT/60 Цели/1-yearly-2026.md"
monthly="$VAULT/60 Цели/2-monthly.md"
weekly="$VAULT/60 Цели/3-weekly.md"

for goal in "$yearly" "$monthly" "$weekly"; do
    if [ -f "$goal" ]; then
        name=$(basename "$goal" .md)
        echo "   → $name"
    fi
done

if [ ! -f "$yearly" ] && [ ! -f "$monthly" ] && [ ! -f "$weekly" ]; then
    echo "   ⚠️  Цели не найдены — пора поставить!"
fi
echo ""

# 3. 📊 Прогресс за неделю
echo "📊 Прогресс за неделю:"
week_ago=$(date -d "7 days ago" +%Y-%m-%d)
completed=$(grep -rl "^created: $week_ago" "$VAULT" 2>/dev/null | grep -v "/99 Сервис/Гермес/" | wc -l)
echo "   📁 Записей за неделю: $completed"
echo ""

# 4. 💡 Рекомендации
echo "💡 Рекомендации:"
if [ "$overdue" -gt 0 ]; then
    echo "   1. Просроченные задачи — закрыть или удалить"
fi
if [ "$today_tasks" -eq 0 ]; then
    echo "   2. Нет задач на сегодня — добавь что-нибудь"
fi
if [ "$completed" -lt 3 ]; then
    echo "   3. Маловато активности — минимум 3 записи в день"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💪 Ты справишься!"
