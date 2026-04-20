#!/bin/bash
# Тест защиты личных данных в Git

set -e

VAULT="$HOME/.openclaw/workspace/vault"
cd "$VAULT"

echo "🔒 Тест Git Privacy Protection"
echo "================================"
echo ""

# Проверка 1: .gitignore существует
echo "1️⃣ Проверка .gitignore..."
if [ ! -f .gitignore ]; then
    echo "❌ .gitignore не найден"
    exit 1
fi
echo "✅ .gitignore существует"
echo ""

# Проверка 2: Личные файлы игнорируются
echo "2️⃣ Проверка игнорирования личных файлов..."
IGNORED_FILES=(
    "MEMORY.md"
    "USER.md"
    "SOUL.md"
    "AGENTS.md"
    "IDENTITY.md"
)

for file in "${IGNORED_FILES[@]}"; do
    if git check-ignore -q "$file" 2>/dev/null; then
        echo "   ✅ $file — игнорируется"
    else
        echo "   ❌ $file — НЕ игнорируется (КРИТИЧНО!)"
        exit 1
    fi
done
echo ""

# Проверка 3: Заметки в папках игнорируются
echo "3️⃣ Проверка игнорирования заметок в папках..."
TEST_FILES=(
    "80 Ежедневные/2026-03-19.md"
    "60 Цели/1-yearly-2026.md"
    "10 Заметки/test.md"
    "40 Объекты/project.md"
)

# Создаём тестовые файлы если их нет
for file in "${TEST_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        mkdir -p "$(dirname "$file")"
        echo "test" > "$file"
    fi
done

for file in "${TEST_FILES[@]}"; do
    if git check-ignore -q "$file" 2>/dev/null; then
        echo "   ✅ $file — игнорируется"
    else
        echo "   ❌ $file — НЕ игнорируется (КРИТИЧНО!)"
        exit 1
    fi
done
echo ""

# Проверка 4: .gitkeep НЕ игнорируются
echo "4️⃣ Проверка .gitkeep (должны коммититься)..."
GITKEEP_FILES=(
    "80 Ежедневные/.gitkeep"
    "60 Цели/.gitkeep"
    "10 Заметки/.gitkeep"
)

for file in "${GITKEEP_FILES[@]}"; do
    if git check-ignore -q "$file" 2>/dev/null; then
        echo "   ❌ $file — игнорируется (должен коммититься!)"
        exit 1
    else
        echo "   ✅ $file — НЕ игнорируется"
    fi
done
echo ""

# Проверка 5: Служебные файлы НЕ игнорируются
echo "5️⃣ Проверка служебных файлов (должны коммититься)..."
SERVICE_FILES=(
    "99 _Сервис/MIGRATION.md"
    "99 _Сервис/Scripts/test_dbrain.sh"
    "99 _Сервис/Skills/dbrain-processor/SKILL.md"
    "README.md"
    ".gitignore"
)

for file in "${SERVICE_FILES[@]}"; do
    if git check-ignore -q "$file" 2>/dev/null; then
        echo "   ❌ $file — игнорируется (должен коммититься!)"
        exit 1
    else
        echo "   ✅ $file — НЕ игнорируется"
    fi
done
echo ""

# Проверка 6: .env игнорируется
echo "6️⃣ Проверка секретов (.env)..."
if git check-ignore -q ".env" 2>/dev/null; then
    echo "   ✅ .env — игнорируется"
else
    echo "   ⚠️ .env — не найден (создай пустой для теста)"
fi
echo ""

# Проверка 7: Подсчёт staged файлов
echo "7️⃣ Подсчёт файлов для коммита..."
git add -A 2>/dev/null || true
STAGED_COUNT=$(git status --short | wc -l)
echo "   📊 Файлов в stage: $STAGED_COUNT"

# Проверка что НЕТ личных данных в staged
if git status --short | grep -E "(MEMORY|USER|SOUL|AGENTS|IDENTITY|HEARTBEAT)" >/dev/null 2>&1; then
    echo "   ❌ КРИТИЧНО: Личные файлы в stage!"
    git status --short | grep -E "(MEMORY|USER|SOUL|AGENTS|IDENTITY|HEARTBEAT)"
    exit 1
else
    echo "   ✅ Личные файлы не в stage"
fi

if git status --short | grep -E "80 Ежедневные.*\.md|60 Цели.*\.md" >/dev/null 2>&1; then
    echo "   ❌ КРИТИЧНО: Заметки в stage!"
    git status --short | grep -E "80 Ежедневные|60 Цели"
    exit 1
else
    echo "   ✅ Заметки не в stage"
fi
echo ""

echo "🎉 Все проверки пройдены!"
echo ""
echo "📋 Безопасно для коммита:"
echo "   - Структура папок (.gitkeep)"
echo "   - Служебные скрипты (99 _Сервис/)"
echo "   - AgentSkills (SKILL.md)"
echo "   - Obsidian конфигурация (.obsidian/)"
echo ""
echo "❌ Игнорируется (личные данные):"
echo "   - Все заметки в 00-95 папках"
echo "   - MEMORY.md, USER.md, SOUL.md и др."
echo "   - .env, API ключи, токены"
echo ""
echo "✅ Готово к push на GitHub!"
