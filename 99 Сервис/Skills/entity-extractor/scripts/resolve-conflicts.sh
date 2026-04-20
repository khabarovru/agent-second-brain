#!/bin/bash
# Автоматическое разрешение конфликтов Syncthing
# Логика: оставляем более новый файл (оригинал или конфликт)
# Usage: ./resolve-conflicts.sh [--dry-run]

VAULT="/home/khabarovru/.openclaw/agents/second-brain/vault"
DRY_RUN=0
[ "$1" = "--dry-run" ] && DRY_RUN=1

kept_orig=0
kept_conflict=0
errors=0

while IFS= read -r conflict; do
  # Восстанавливаем путь оригинала
  original_base=$(echo "$conflict" | sed 's/\.sync-conflict[^.]*\.[^.]*$//')
  ext="${conflict##*.}"
  original="${original_base}.${ext}"

  if [ ! -f "$original" ]; then
    # Нет оригинала - переименовываем конфликт в оригинал
    if [ $DRY_RUN -eq 0 ]; then
      mv "$conflict" "$original" 2>/dev/null && echo "RESTORED: $(basename $original)" || ((errors++))
    else
      echo "[DRY] WOULD RESTORE: $(basename $original)"
    fi
    continue
  fi

  orig_time=$(stat -c %Y "$original" 2>/dev/null)
  conf_time=$(stat -c %Y "$conflict" 2>/dev/null)

  if [ "$orig_time" -ge "$conf_time" ]; then
    # Оригинал новее или одинаковый - удаляем конфликт
    if [ $DRY_RUN -eq 0 ]; then
      rm "$conflict" && ((kept_orig++))
    else
      echo "[DRY] KEEP ORIGINAL: $(basename $original)"
    fi
  else
    # Конфликт новее - заменяем оригинал
    if [ $DRY_RUN -eq 0 ]; then
      cp "$conflict" "$original" && rm "$conflict" && ((kept_conflict++)) && echo "UPDATED from conflict: $(basename $original)"
    else
      echo "[DRY] WOULD USE CONFLICT: $(basename $original)"
    fi
  fi

done < <(find "$VAULT" -name "*.sync-conflict*" 2>/dev/null)

total=$((kept_orig + kept_conflict))

# Ничего не делали — молча exit 0
[ $kept_orig -eq 0 ] && [ $kept_conflict -eq 0 ] && [ $errors -eq 0 ] && exit 0

echo "---"
echo "Оставлено оригиналов: $kept_orig"
echo "Обновлено из конфликтов: $kept_conflict"
echo "Ошибок: $errors"
