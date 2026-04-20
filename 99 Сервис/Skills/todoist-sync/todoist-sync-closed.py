#!/usr/bin/env python3
"""
Синхронизация закрытых задач Todoist → Obsidian vault.
Ищет закрытые задачи за последние N дней и помечает их в vault.
Usage: python3 todoist-sync-closed.py [days=1]
"""
import sys
import json
import os
import re
import urllib.request
import urllib.error
from datetime import datetime, timedelta

SECRETS_FILE = '/home/khabarovru/.openclaw/agents/second-brain/agent/secrets.json'
VAULT_PATH = '/home/khabarovru/.openclaw/agents/second-brain/vault'
SYNC_STATE_FILE = '/home/khabarovru/.openclaw/agents/second-brain/agent/todoist-sync-state.json'

def get_token():
    with open(SECRETS_FILE, 'r') as f:
        return json.load(f)['todoist_token']

def api_request(url, token, method='GET', data=None):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode()}", file=sys.stderr)
        return None

def load_sync_state():
    if os.path.exists(SYNC_STATE_FILE):
        with open(SYNC_STATE_FILE, 'r') as f:
            return json.load(f)
    return {'synced_task_ids': [], 'last_sync': None}

def save_sync_state(state):
    with open(SYNC_STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def find_task_in_vault(task_content, task_id):
    """Ищет задачу в vault по содержимому или todoist_id"""
    search_dirs = [
        os.path.join(VAULT_PATH, '50 Задачи'),
        os.path.join(VAULT_PATH, '20 Ежедневник', 'Daily Notes'),
    ]
    found = []
    for search_dir in search_dirs:
        if not os.path.exists(search_dir):
            continue
        for root, dirs, files in os.walk(search_dir):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for fname in files:
                if not fname.endswith('.md'):
                    continue
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    # Ищем по todoist_id в frontmatter
                    if f'todoist_id: {task_id}' in content:
                        found.append(fpath)
                    # Или по содержимому задачи (нечёткий поиск)
                    elif task_content.lower()[:30] in content.lower():
                        found.append(fpath)
                except Exception:
                    pass
    return found

def mark_task_closed_in_vault(fpath, task_content):
    """Помечает задачу закрытой в файле vault"""
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Меняем status: open → closed в frontmatter
        updated = re.sub(r'^(status:\s*)open', r'\1closed', content, flags=re.MULTILINE)
        # Или добавляем closed_at если нет status
        if 'status:' not in updated:
            updated = updated.replace('---\n\n#', f'---\nstatus: closed\nclosed_at: {datetime.now().strftime("%Y-%m-%d")}\n\n#')

        # Помечаем чекбокс если есть
        updated = re.sub(
            r'- \[ \] ' + re.escape(task_content[:20]),
            f'- [x] {task_content[:20]}',
            updated
        )

        if updated != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(updated)
            return True
    except Exception as e:
        print(f"Ошибка обновления {fpath}: {e}", file=sys.stderr)
    return False

def main():
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    token = get_token()
    state = load_sync_state()
    synced_ids = set(state.get('synced_task_ids', []))

    # Получаем закрытые задачи из Todoist (completed)
    since = (datetime.utcnow() - timedelta(days=days)).strftime('%Y-%m-%dT%H:%M:%SZ')
    result = api_request(
        'https://api.todoist.com/api/v2/tasks?completed=true',
        token
    )

    if not result:
        print("❌ Не удалось получить закрытые задачи из Todoist")
        sys.exit(1)

    tasks = result.get('results', [])
    print(f"📋 Найдено закрытых задач: {len(tasks)}")

    updated_count = 0
    for task in tasks:
        task_id = task.get('id') or task.get('task_id')
        task_content = task.get('content', '')

        if str(task_id) in synced_ids:
            continue

        vault_files = find_task_in_vault(task_content, task_id)
        if vault_files:
            for fpath in vault_files:
                if mark_task_closed_in_vault(fpath, task_content):
                    rel = os.path.relpath(fpath, VAULT_PATH)
                    print(f"✅ Закрыта в vault: {rel} ← {task_content[:50]}")
                    updated_count += 1
            synced_ids.add(str(task_id))

    state['synced_task_ids'] = list(synced_ids)[-500:]  # храним последние 500
    state['last_sync'] = datetime.utcnow().isoformat()
    save_sync_state(state)

    print(f"\n🔄 Обновлено записей в vault: {updated_count}")

if __name__ == '__main__':
    main()
