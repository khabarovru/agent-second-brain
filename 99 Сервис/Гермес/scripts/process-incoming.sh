#!/bin/bash
# process-incoming.sh — Обработка входящих файлов
# Для каждого файла в 00 Входящие — показать содержимое и предложить действия

VAULT="/volume1/docker/openclaw/.openclaw/workspace/skills/agent-second-brain/vault"
TODOIST_TOKEN="c1f7278f1dd135b6f0dcdf4a01018c70aead351f"

DRY_RUN=false
if [ "$1" == "--dry-run" ] || [ "$1" == "-n" ]; then
    DRY_RUN=true
    echo "🔍 Тестовый режим (без изменений)"
fi

echo "📥 Обработка входящих"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

count=0
processed=0
errors=0

# Find all markdown files in 00 Входящие (including subfolders)
while IFS= read -r file; do
    count=$((count + 1))
    
    # Get filename and frontmatter
    basename=$(basename "$file")
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📄 $basename"
    
    # Check if already processed
    if grep -q "todoist_id:" "$file" 2>/dev/null; then
        echo "   ⏭ Уже обработано (есть todoist_id)"
        continue
    fi
    
    # Extract title
    title=$(grep "^# " "$file" 2>/dev/null | head -1 | sed 's/^# //')
    if [ -z "$title" ]; then
        title="$basename"
    fi
    echo "   Заголовок: $title"
    
    # Extract priority
    priority=$(grep "^priority:" "$file" 2>/dev/null | head -1 | sed 's/priority: //' | tr -d ' ')
    if [ -z "$priority" ]; then
        priority="4"
    fi
    echo "   Приоритет: $priority"
    
    # Extract due
    due=$(grep "^due:" "$file" 2>/dev/null | head -1 | sed 's/due: //' | tr -d ' ')
    echo "   Дедлайн: ${due:-не указан}"
    
    # Extract type
    type=$(grep "^type:" "$file" 2>/dev/null | head -1 | sed 's/type: //' | tr -d ' ')
    if [ "$type" == "task" ]; then
        # Convert priority 1-4 to Todoist p1-p4
        todoist_p=$(echo {4,3,2,1} | tr ' ' '\n' | head -n $((5 - priority)) | tail -1)
        case $priority in
            1) tp="p1 (срочно)" ;;
            2) tp="p2 (важно)" ;;
            3) tp="p3" ;;
            *) tp="p4 (обычное)" ;;
        esac
        echo "   → Todoist: $tp"
        
        if [ "$DRY_RUN" == false ]; then
            # Create in Todoist
            result=$(curl -s -X POST "https://api.todoist.com/api/v1/tasks" \
                -H "Authorization: Bearer $TODOIST_TOKEN" \
                -H "Content-Type: application/json" \
                -d "{\"content\": \"$title\", \"priority\": $((5 - priority))}")
            
            task_id=$(echo "$result" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
            
            if [ -n "$task_id" ]; then
                # Add todoist_id to frontmatter
                sed -i "s/^type: task$/type: task\ntodoist_id: \"$task_id\"/" "$file"
                echo "   ✅ Создана в Todoist (ID: $task_id)"
                processed=$((processed + 1))
            else
                echo "   ❌ Ошибка создания: $result"
                errors=$((errors + 1))
            fi
        else
            echo "   [Тест] Будет создана в Todoist"
        fi
    else
        echo "   → Не задача (type: ${type:-unknown})"
    fi
    echo ""
    
done < <(find "$VAULT/00 Входящие" -name "*.md" -type f 2>/dev/null)

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Результат:"
echo "   Найдено: $count"
echo "   Обработано: $processed"
echo "   Ошибок: $errors"
echo ""
if [ "$DRY_RUN" == true ]; then
    echo "🔍 Тестовый прогон завершён"
fi
