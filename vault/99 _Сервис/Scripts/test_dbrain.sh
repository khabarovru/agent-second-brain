#!/bin/bash
# Тест d-brain бота после миграции vault

set -e

VAULT_PATH="$HOME/.openclaw/workspace/vault"
BOT_DIR="$HOME/.openclaw/workspace/skills/agent-second-brain"

echo "🧪 Тест d-brain после миграции vault"
echo "======================================"
echo ""

# 1. Проверка структуры vault
echo "1️⃣ Проверка структуры vault..."
if [ ! -d "$VAULT_PATH/80 Ежедневные" ]; then
    echo "❌ Папка '80 Ежедневные' не найдена"
    exit 1
fi
if [ ! -d "$VAULT_PATH/99 _Сервис/Skills/dbrain-processor" ]; then
    echo "❌ SKILL.md не найден в vault"
    exit 1
fi
echo "✅ Структура OK"
echo ""

# 2. Проверка конфигурации
echo "2️⃣ Проверка конфигурации..."
cd "$BOT_DIR"
if ! grep -q "VAULT_PATH=$VAULT_PATH" .env; then
    echo "❌ .env не обновлен"
    exit 1
fi
echo "✅ .env OK"
echo ""

# 3. Проверка Python кода
echo "3️⃣ Проверка кода..."
if ! grep -q "80 Ежедневные" src/d_brain/services/storage.py; then
    echo "❌ storage.py не обновлен"
    exit 1
fi
if ! grep -q "85 Сводки" src/d_brain/services/processor.py; then
    echo "❌ processor.py не обновлен"
    exit 1
fi
echo "✅ Код обновлён"
echo ""

# 4. Тест записи в daily
echo "4️⃣ Тест записи в daily notes..."
TEST_FILE="$VAULT_PATH/80 Ежедневные/test-$(date +%Y-%m-%d).md"
echo "## 99:99 [test]" > "$TEST_FILE"
echo "Тестовая запись" >> "$TEST_FILE"
if [ -f "$TEST_FILE" ]; then
    echo "✅ Запись успешна: $TEST_FILE"
    cat "$TEST_FILE"
    rm "$TEST_FILE"
else
    echo "❌ Не удалось создать файл"
    exit 1
fi
echo ""

# 5. Проверка SKILL.md
echo "5️⃣ Проверка SKILL.md..."
SKILL_FILE="$VAULT_PATH/99 _Сервис/Skills/dbrain-processor/SKILL.md"
if grep -q "60 Цели/" "$SKILL_FILE" && grep -q "80 Ежедневные/" "$SKILL_FILE"; then
    echo "✅ SKILL.md обновлён с новыми путями"
else
    echo "❌ SKILL.md содержит старые пути"
    exit 1
fi
echo ""

echo "🎉 Все тесты пройдены!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Перезапустить бота: cd $BOT_DIR && .venv/bin/python -m d_brain"
echo "2. Отправить голосовое в Telegram: @khabarovru_obsidian_bot"
echo "3. Проверить файл: $VAULT_PATH/80 Ежедневные/$(date +%Y-%m-%d).md"
echo "4. Запустить /process для проверки обработки"
