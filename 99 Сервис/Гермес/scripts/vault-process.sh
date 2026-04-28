#!/bin/bash
# vault-process.sh — обработка входящих записей за день
# Активируется: /процесс

VAULT="/volume1/docker/openclaw/.openclaw/workspace/skills/agent-second-brain/vault"
TODAY=$(date +%Y-%m-%d)

echo "📥 Обработка входящих за $(date '+%d.%m.%Y')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Файлы в корне 00 Входящие (необработанные)
unprocessed=$(find "$VAULT/00 Входящие" -maxdepth 1 -name "*.md" -type f 2>/dev/null | wc -l)
if [ "$unprocessed" -gt 0 ]; then
    echo "⚠️  Необработанные в корне 00 Входящие: $unprocessed"
    find "$VAULT/00 Входящие" -maxdepth 1 -name "*.md" -type f 2>/dev/null | while read f; do
        echo "   → $(basename "$f")"
    done
    echo ""
else
    echo "✅ Нет необработанных в корне"
fi

echo ""

# Подсчёт по папкам за сегодня
count_folder() {
    local folder=$1
    local label=$2
    local count
    count=$(find "$folder" -name "*.md" -type f 2>/dev/null | xargs grep -l "^created: $TODAY" 2>/dev/null | wc -l)
    echo "$label: $count"
}

echo "📁 За сегодня:"
count_folder "$VAULT/00 Входящие/Ideas" "   💡 Идеи"
count_folder "$VAULT/00 Входящие/Tasks"  "   ✅ Задачи"
count_folder "$VAULT/00 Входящие/Notes"  "   📝 Заметки"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Сводка готова"
