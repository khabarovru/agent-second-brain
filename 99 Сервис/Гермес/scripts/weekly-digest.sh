#!/bin/bash
# weekly-digest.sh — Недельный дайджест

VAULT="/volume1/docker/openclaw/.openclaw/workspace/skills/agent-second-brain/vault"
WEEK_AGO=$(date -d "7 days ago" +%Y-%m-%d)
TODAY=$(date +%Y-%m-%d)

echo "📊 Недельный дайджест"
echo "$(date -d "$WEEK_AGO" '+%d.%m') - $(date '+%d.%m.%Y')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 1. Подсчёт новых записей за неделю
echo "📁 Новые записи:"
total=$(grep -rl "^created: $WEEK_AGO" "$VAULT" 2>/dev/null | grep -v "/99 Сервис/Гермес/" | wc -l)
tasks=$(grep -rl "^created: $WEEK_AGO" "$VAULT" 2>/dev/null | xargs grep -l "^type: task" 2>/dev/null | wc -l)
ideas=$(grep -rl "^created: $WEEK_AGO" "$VAULT" 2>/dev/null | xargs grep -l "^type: idea" 2>/dev/null | wc -l)
notes=$(grep -rl "^created: $WEEK_AGO" "$VAULT" 2>/dev/null | xargs grep -l "^type: note" 2>/dev/null | wc -l)

echo "   ✅ Задач: $tasks"
echo "   💡 Идей: $ideas"
echo "   📝 Заметок: $notes"
echo "   📦 Всего: $total"
echo ""

# 2. Цели — прогресс
echo "🎯 Цели:"
yearly="$VAULT/60 Цели/1-yearly-2026.md"
if [ -f "$yearly" ]; then
    # Count unchecked tasks
    unchecked=$(grep -c "^\- \[ \]" "$yearly" 2>/dev/null || echo "0")
    checked=$(grep -c "^\- \[x\]" "$yearly" 2>/dev/null || echo "0")
    echo "   Годовые: $checked выполнено, $unchecked осталось"
fi
echo ""

# 3. Время дня — когда активнее всего
echo "⏰ Активность:"
# Count entries by hour (rough)
hours_file=$(mktemp)
grep -rh "^created:" "$VAULT" 2>/dev/null | grep -oE "[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}" | cut -d' ' -f2 | cut -d':' -f1 | sort | uniq -c | sort -rn > "$hours_file"
if [ -s "$hours_file" ]; then
    top_hour=$(head -1 "$hours_file" | awk '{print $2}')
    top_count=$(head -1 "$hours_file" | awk '{print $1}')
    echo "   Пик активности: $top_hour:00 ($top_count записей)"
else
    echo "   Нет данных"
fi
rm -f "$hours_file"
echo ""

# 4. Популярные темы
echo "📌 Популярные темы:"
# Extract most common words (excluding stop words)
topics=$(grep -rh "^tags:" "$VAULT" 2>/dev/null | grep -oE "\[([^\]]+)\]" | tr -d '[]' | tr ',' '\n' | tr -d ' ' | sort | uniq -c | sort -rn | head -5)
if [ -n "$topics" ]; then
    echo "$topics" | head -5 | while read count tag; do
        echo "   #$tag ($count)"
    done
else
    echo "   Нет данных"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💪 Продолжай в том же духе!"
