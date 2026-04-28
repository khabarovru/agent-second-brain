#!/bin/bash
# vault-status.sh — статистика vault за сегодня
# Показывает количество идей, задач и заметок созданных за день

VAULT="/volume1/docker/openclaw/.openclaw/workspace/skills/agent-second-brain/vault"
TODAY=$(date +%Y-%m-%d)

echo "📊 Статистика за $(date '+%d.%m.%Y')"
echo "━━━━━━━━━━━━━━━━━━━━━━━"

# Подсчёт по типам
tasks=$(grep -rl "^created: $TODAY" "$VAULT" 2>/dev/null | xargs grep -l "^type: task" 2>/dev/null | wc -l)
ideas=$(grep -rl "^created: $TODAY" "$VAULT" 2>/dev/null | xargs grep -l "^type: idea" 2>/dev/null | wc -l)
notes=$(grep -rl "^created: $TODAY" "$VAULT" 2>/dev/null | xargs grep -l "^type: note" 2>/dev/null | wc -l)
knowledge=$(grep -rl "^created: $TODAY" "$VAULT" 2>/dev/null | xargs grep -l "^type: knowledge" 2>/dev/null | wc -l)

total=$((tasks + ideas + notes + knowledge))

echo "✅ Задачи (tasks):    $tasks"
echo "💡 Идеи (ideas):     $ideas"
echo "📝 Заметки (notes):  $notes"
echo "🧠 Знания (knowledge): $knowledge"
echo "━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 Всего:             $total"
