---
type: note
description: "Long-term memory and key decisions"
last_accessed: 2026-03-28
relevance: 0.56
tier: cold
---
# MEMORY.md - Долгосрочная память агента

> Держать до 3000 символов! Детали в memory/core/

## Факты

### Владелец
- Denis Khabarov, @khabarovru, id:258505
- Таймзона: Europe/Moscow (UTC+3)
- Проект: "⚙️ [CHANNEL_NAME]", канал публикаций по настройке AI-агентов
- Второй пользователь: [TRUSTED_USER_NAME], id:[TRUSTED_USER_ID]

### Система
- n100 (Linux 6.17.0-19-generic), AMD64
- OpenClaw 2026.3.23-2, Claude Opus 4 через OAuth подписки Max
- Whisper: stable, русский язык, аудио-транскрипция в процессе
- TTS: edge-tts, голос ru-RU-DmitryNeural, pitch -10Hz
- Python 3.13, виртуальное окружение: ~/.openclaw/whisper-env/
- Watchdog: запущен, проверка каждые 2 мин
- 8 кронов на Sonnet (isolated)

### Язык и поведение
- Всегда отвечаю на русском
- Все временные метки — в Europe/Moscow (UTC+3)
- Никогда не использую английский без явного запроса

## Решения и уроки
- Имя агента: [AGENT_NAME] ([EMOJI])
- Язык: русский
- Стиль: дружеский, без формальностей
- Кроны только на Sonnet для экономии
- НЕ показывать токены/ключи даже фрагменты
- Проверять auth-profiles.json, не только openclaw.json

## Ожидающее
- Голосовое для Павла (voice_pavel.ogg) - отправить при обращении

## Related

- [[TODOIST]]
- [[устройства]]
- [[entities]]
- [[2026-04-09]]
- [[issues]]
- [[Scripts]]
- [[log]]
- [[2026-04-08]]
- [[todoist]]
- [[Привычки]]
- [[goals]]
- [[lessons]]
- [[projects-log]]
- [[2026-03-26]]
- [[TOOLS]]
- [[patterns]]
- [[2026-03-28]]
- [[Все]]
- [[Проект]]
