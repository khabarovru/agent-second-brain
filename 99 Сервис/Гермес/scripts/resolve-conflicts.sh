#!/bin/bash
# resolve-conflicts.sh — Автоматическое разрешение конфликтов Syncthing
# Оставляет более новый файл (оригинал или конфликт)

VAULT="/volume1/docker/openclaw/.openclaw/workspace/skills/agent-second-brain/vault"
DRY_RUN=false

if [ "$1" == "--dry-run" ] || [ "$1" == "-n" ]; then
    DRY_RUN=true
    echo "🔍 Тестовый режим (без изменений)"
fi

echo "🔧 Разрешение конфликтов Syncthing"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ "$DRY_RUN" == true ]; then
    echo "📁 Vault: $VAULT"
    echo ""
fi

kept=0
updated=0
renamed=0
errors=0

# Find all conflict files
while IFS= read -r conflict_file; do
    # Extract original filename (remove .sync-conflict* part)
    # Format: filename.sync-conflict-YYYYMMDD-HHMMSS-xxxxxx.ext
    dirname=$(dirname "$conflict_file")
    basename=$(basename "$conflict_file")
    
    # Get the part before .sync-conflict
    original_name=$(echo "$basename" | sed -E 's/\.sync-conflict-[0-9]{8}-[0-9]{6}-[a-zA-Z0-9]+\././')
    original_path="$dirname/$original_name"
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📄 Конфликт: $basename"
    echo "   Оригинал: $original_name"
    
    if [ -f "$original_path" ]; then
        # Both exist — compare dates
        conflict_mtime=$(stat -c %Y "$conflict_file" 2>/dev/null)
        original_mtime=$(stat -c %Y "$original_path" 2>/dev/null)
        
        if [ "$conflict_mtime" -gt "$original_mtime" ]; then
            # Conflict is newer — update original
            if [ "$DRY_RUN" == true ]; then
                echo "   → Будет ОБНОВЛЁН из конфликта (конфликт новее)"
                updated=$((updated + 1))
            else
                cp "$conflict_file" "$original_path" && rm "$conflict_file"
                echo "   → ОБНОВЛЁН из конфликта ✓"
                updated=$((updated + 1))
            fi
        else
            # Original is newer — keep original, remove conflict
            if [ "$DRY_RUN" == true ]; then
                echo "   → Будет УДАЛЁН конфликт (оригинал новее)"
                kept=$((kept + 1))
            else
                rm "$conflict_file"
                echo "   → КОНФЛИКТ УДАЛЁН ✓"
                kept=$((kept + 1))
            fi
        fi
    else
        # No original — rename conflict to original
        if [ "$DRY_RUN" == true ]; then
            echo "   → Будет ПЕРЕИМЕНОВАН в оригинал (оригинала нет)"
            renamed=$((renamed + 1))
        else
            mv "$conflict_file" "$original_path"
            echo "   → ПЕРЕИМЕНОВАН в оригинал ✓"
            renamed=$((renamed + 1))
        fi
    fi
done < <(find "$VAULT" -name "*.sync-conflict*" -type f 2>/dev/null)

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Результат:"
echo "   Оставлено оригиналов: $kept"
echo "   Обновлено из конфликтов: $updated"
echo "   Переименовано: $renamed"
echo "   Ошибок: $errors"
echo ""
if [ "$DRY_RUN" == true ]; then
    echo "🔍 Это был тестовый прогон. Для реальных изменений запустите без --dry-run"
else
    echo "✅ Готово"
fi
