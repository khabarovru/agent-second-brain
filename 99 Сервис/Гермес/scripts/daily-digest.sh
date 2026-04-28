#!/bin/bash
# daily-digest.sh — дневной дайджест
# Активируется: /дейли

VAULT="/volume1/docker/openclaw/.openclaw/workspace/skills/agent-second-brain/vault"
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)
TODAY=$(date +%Y-%m-%d)

echo "📅 Дайджест за $(date -d "yesterday" '+%d.%m.%Y')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 1. 📥 Входящие за вчера
echo "📥 Входящие за вчера:"
for type in "ideas" "tasks" "notes"; do
    case $type in
        ideas)  label="💡 Идеи"   ;;
        tasks)  label="✅ Задачи" ;;
        notes)  label="📝 Заметки" ;;
    esac
    
    count=$(find "$VAULT/00 Входящие/$type" -name "*.md" -type f 2>/dev/null | xargs grep -l "^created: $YESTERDAY" 2>/dev/null | wc -l)
    
    if [ "$count" -gt 0 ]; then
        echo "  $label: $count"
        find "$VAULT/00 Входящие/$type" -name "*.md" -type f 2>/dev/null | xargs grep -l "^created: $YESTERDAY" 2>/dev/null | while read f; do
            title=$(grep "^# " "$f" 2>/dev/null | head -1 | sed 's/^# //')
            [ -z "$title" ] && title=$(basename "$f" .md)
            echo "     → $title"
        done
    else
        echo "  $label: 0"
    fi
done
echo ""

# 2. 📅 Превью дневника
daily_note="$VAULT/20 Ежедневник/Daily Notes/$YESTERDAY.md"
if [ -f "$daily_note" ]; then
    echo "📅 Дневник $YESTERDAY:"
    preview=$(head -c 500 "$daily_note" | tail -c 500)
    # Убираем frontmatter
    preview=$(echo "$preview" | sed '1,/^---$/d' | sed '/^---$/d' | sed 's/^# //' | head -20)
    echo "$preview" | head -10
    if [ ${#preview} -eq 500 ]; then
        echo "..."
    fi
else
    echo "📅 Дневник $YESTERDAY: (пусто)"
fi
echo ""

# 3. 📁 Новые заметки в vault за вчера
echo "📁 Новые заметки за день:"
total_new=$(grep -rl "^created: $YESTERDAY" "$VAULT" 2>/dev/null | grep -v "/99 Сервис/Гермес/" | wc -l)
if [ "$total_new" -gt 0 ]; then
    echo "   Всего: $total_new"
    grep -rl "^created: $YESTERDAY" "$VAULT" 2>/dev/null | grep -v "/99 Сервис/Гермес/" | while read f; do
        folder=$(dirname "$f" | xargs basename)
        echo "   → [$folder] $(basename "$f" .md)"
    done
else
    echo "   Нет новых заметок"
fi
echo ""

# 4. 📋 Todoist
echo "📋 Todoist:"
echo "   → Открой приложение и проверь задачи на сегодня"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧠 Дайджест готов"
