# Handoff — 2026-03-26 18:00 UTC (21:00 MSK)

## Тема
Настройка агента-секретаря — структура папок и workflow для проверки документов.

## Решения
- **Создали структуру папок:**
  - `inbox/` — входящие файлы на проверку (.docx, .xlsx, .pdf)
  - `output/` — отчёты агента (формат `YYYY-MM-DD_имя-файла_report.md`)
  - `templates/` — шаблоны договоров/актов для сверки
  - `scripts/` — парсеры (parse_pdf.py, parse_docx.py, parse_xlsx.py)
  - `skills/` — специализированные скиллы
  - `memory/` — lessons, patterns, projects-log

- **Обновили AGENTS.md** — добавили описание workflow:
  1. Файл в inbox
  2. Парсинг через scripts или pdf tool
  3. Проверка по 4 направлениям (правовая, факты, структура, язык)
  4. Отчёт в output
  5. Запись в memory/projects-log.md

## TODO
- [ ] Закинуть шаблоны договоров в `templates/`
- [ ] Протестировать workflow: файл → inbox → проверка → отчёт в output
- [ ] Настроить автоматическую обработку файлов из Telegram (если нужно)

## Файлы
- `~/.openclaw/agents/secretary/agent/AGENTS.md` — обновлён workflow
- `~/.openclaw/agents/secretary/agent/inbox/` — входящие файлы
- `~/.openclaw/agents/secretary/agent/output/` — результаты проверок
- `~/.openclaw/agents/secretary/agent/templates/` — шаблоны для сверки

## Контекст
Пользователь хотел структурировать работу агента-секретаря. Сделали систему папок по образцу "inbox → обработка → output". Агент теперь будет складывать отчёты в output, а шаблоны для сверки — в templates. Следующий шаг — наполнить templates образцами документов и протестировать полный цикл.

## Черновики
(Нет незавершённого текста)
