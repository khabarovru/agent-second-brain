---
type: note
last_accessed: 2026-04-09
relevance: 0.74
tier: warm
---
# TOOLS.md - Инструменты Сисадмина

## Основные команды

### SSH на Xpenology
```bash
ssh khabarovru@192.168.1.134 "[команда]"
```

### SSH на OpenWrt
```bash
ssh root@192.168.1.1 "[команда]"
```

### Проверка Docker контейнеров
```bash
ssh khabarovru@192.168.1.134 "docker ps"
```

### Логи Home Assistant
```bash
ssh khabarovru@192.168.1.134 "tail -100 /volume1/@appdata/ContainerManager/all_shares/docker/homeassistant/home-assistant.log"
```

### Проверка SMART дисков
```bash
ssh khabarovru@192.168.1.134 "smartctl -a /dev/sda" 2>/dev/null
```

## API Home Assistant

Токен можно получить из .storage файлов или запросить через UI.
