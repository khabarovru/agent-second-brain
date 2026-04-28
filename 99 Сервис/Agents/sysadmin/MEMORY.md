---
type: note
last_accessed: 2026-04-09
relevance: 0.74
tier: warm
---
# MEMORY.md - Сисадмин 🖥️

## HA-конфигурация (Xpenology 192.168.1.134)

### Файлы
- `/volume1/docker/homeassistant/configuration.yaml`
- `/volume1/docker/homeassistant/automations.yaml`

### Что настроено

**configuration.yaml:**
- `system_log: fire_event: true` — для счётчиков ошибок/предупреждений
- `counter: error_counter, warning_counter, restart_counter` (initial: 0)
- `rest_command: ha_notify_sysadmin` → webhook на n100:18899
- `http: use_x_forwarded_for: true, trusted_proxies`

**automations.yaml (4 шт):**
- `sysadmin_error_counter` — ловит system_log_event ERROR → counter.error_counter
- `sysadmin_warning_counter` — ловит system_log_event WARNING → counter.warning_counter  
- `sysadmin_ha_start_notify` — homeassistant.start → notify.mobile_app_denis_phone + restart_counter++
- `sysadmin_ha_stop_notify` — homeassistant.shutdown → notify.mobile_app_denis_phone

### SSH-доступ
- Хост: 192.168.1.134
- Пользователь: khabarovru
- Пароль: 13spartahN
- HA config: /volume1/docker/homeassistant/

### Важно
- ping интеграция НЕ поддерживает YAML — настраивать через UI
- counter.increment использует `target.entity_id:` (не `entity_id:` напрямую)
- template sensor denis_home уже есть в template.yaml (не дублировать в configuration.yaml)

## HA-конфигурация (Xpenology 192.168.1.134)

### Файлы
- `/volume1/docker/homeassistant/configuration.yaml`
- `/volume1/docker/homeassistant/automations.yaml` (17 automations)
- `/volume1/docker/homeassistant/binary_sensor.yaml` (пустой, ping только через UI)

### counters (initial: 0)
- error_counter, warning_counter, restart_counter, badlogin_counter, triggered_automations, executed_scripts

### utility_meter
- error_counter_hourly, warning_counter_hourly (cycle: hourly)

### sensors (command_line)
- sensor.public_ip — внешний IP (curl api.ipify.org)
- sensor.openwrt_ping — пинг 192.168.1.1

### helpers
- input_boolean.ha_shutdown, input_boolean.system_silent_mode
- input_number.main_volume, battery_low_level_zb, battery_low_level_bt

### rest_command
- ha_notify_sysadmin → webhook n100:18899

### Что настроено (automations)
1. sysadmin_error_counter — счётчик ERROR
2. sysadmin_warning_counter — счётчик WARNING
3. sysadmin_triggered_automations_counter — счётчик triggered automations
4. sysadmin_executed_scripts — счётчик запущенных скриптов
5. sysadmin_ha_start_notify — старт HA
6. sysadmin_ha_stop_notify — стоп HA
7. sysadmin_new_day — 00:00 отчёт + сброс счётчиков
8. sysadmin_login_failure — ловит http-login, ip-ban
9. sysadmin_critical_error — FATAL/CRITICAL
10. sysadmin_automation_error — ошибки automations/scripts
11. sysadmin_ip_blocked — блокировка IP
12. sysadmin_config_error_notification — ошибки конфигурации
13. sysadmin_database_purge — 02:00 очистка БД
14. sysadmin_error_per_hour — >100 ошибок/час
15. sysadmin_warning_per_hour — >100 предупреждений/час
16. sysadmin_dark_mode — режим тишины
17. sysadmin_new_device_tracker — новые устройства
18. sysadmin_automation_reloaded — automation перезагружена
19. sysadmin_scripts_reloaded — scripts перезагружены
20. sysadmin_battery_level_check — 20:30 проверка батарей
21. sysadmin_groups_rebuild — перестроение групп каждый час
22. sysadmin_public_ip_change — смена внешнего IP
23. sysadmin_openwrt_ping — роутер недоступен

### SSH-доступ
- Хост: 192.168.1.134
- Пользователь: khabarovru
- Пароль: 13spartahN
- HA config: /volume1/docker/homeassistant/

### Важно
- ping binary_sensor — ТОЛЬКО через UI (Настройки → Devices → Helpers)
- counter.increment использует `target.entity_id:`
- template sensor denis_home — в template.yaml
- command_line sensors: platform: command_line (НЕ command_line: напрямую)

## Последние события

### 2026-04-09
- Создан агент Сисадмин
- Настроен бот @Sysadmin_khabarovru_bot (токен: 8676067553:AAGJJfdCHFDB3N2sAKoSrkseJXXSd4DDK3Q)
- Настроены 23 automations и все helpers для HA
- Настроен мониторинг OpenWrt роутера и внешнего IP

## Known Issues

- presence_pack.yaml вызывал ошибки формата — исправлено разделением на binary_sensor.yaml, template.yaml, group.yaml
- Packages в HA работают через !include_dir_merge_named, но лучше использовать !include для отдельных доменов

## Counter entities (нужны для автоматизаций)

При старте automations.yaml нужно создать:
- counter.error_counter
- counter.warning_counter
- counter.restart_counter
- counter.triggered_automations

## Правило Gateway Restart
Только **Краб** или **Сисадмин** могут рестартить gateway. Только после согласования с владельцем (Denis).

## Правило последнего сообщения
Сообщение агента всегда должно быть последним в чате. Если видно сообщение от Дениса последним и не ясно что делать — спросить.

## Удаление LKDS автоматизаций (2026-04-09 19:57 UTC)
- Удалены 2 отключённые LKDS автоматизации: утренний и вечерний отчёты.

## Роутер Keenetic (192.168.1.1)
- **Логин**: khabarovru
- **Пароль**: 13spartahN
- **SSH**: возможно на порту 22 (проверить после сохранения)


## Важно: работа с роутером (192.168.1.1)
- ВСЕГДА описывать каждое изменение ДО выполнения
- ВСЕГДА спрашивать подтверждение перед применением
- Не применять изменения без явного согласия пользователя
