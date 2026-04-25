#!/usr/bin/env python3
"""
Двухсторонняя синхронизация между Obsidian vault и Todoist.

Vault → Todoist: создаёт задачи из vault без todoist_id
Vault ← Todoist: обновляет vault при изменениях в Todoist (приоритет, дедлайн, закрытие)

Usage: python3 todoist-sync-full.py [--dry-run]
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
STATE_FILE = '/home/khabarovru/.openclaw/agents/second-brain/agent/todoist-sync-state.json'

# ID проекта для задач (Work)
DEFAULT_PROJECT_ID = '6CrgJfgjMh6M2p7Q'

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
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode()}", file=sys.stderr)
        return None

def api_post(url, token, data=None):
    return api_request(url, token, method='POST', data=data)

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {'synced_ids': [], 'last_sync': None}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def priority_to_p(p):
    """Map vault priority (1-4) to Todoist p1-p4"""
    mapping = {1: 4, 2: 3, 3: 2, 4: 1}
    return mapping.get(p, 3)

def p_to_priority(p):
    """Map Todoist p1-p4 to vault priority (1-4)"""
    mapping = {4: 1, 3: 2, 2: 3, 1: 4}
    return mapping.get(p, 3)

def parse_frontmatter(content):
    """Парсит frontmatter из markdown файла"""
    fm = {}
    if content.startswith('---'):
        end = content.find('\n---', 4)
        if end != -1:
            fm_text = content[3:end].strip()
            for line in fm_text.split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    fm[key.strip()] = val.strip().strip('"')
    return fm

def get_tasks_from_vault():
    """Находит все активные задачи в vault"""
    tasks = []
    search_dirs = [
        os.path.join(VAULT_PATH, '50 Задачи', 'Active'),
        os.path.join(VAULT_PATH, '00 Входящие', 'Tasks'),
    ]
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
                    
                    fm = parse_frontmatter(content)
                    if fm.get('status') == 'closed':
                        continue
                    
                    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                    title = match.group(1).strip() if match else fname[:-3]
                    
                    task = {
                        'path': fpath,
                        'title': title,
                        'priority': int(fm.get('priority', 3)),
                        'due': fm.get('due', ''),
                        'todoist_id': fm.get('todoist_id', ''),
                        'created': fm.get('created', ''),
                        'content': content
                    }
                    tasks.append(task)
                except Exception as e:
                    print(f"Ошибка чтения {fpath}: {e}", file=sys.stderr)
    return tasks

def create_todoist_task(token, title, priority, due, project_id=DEFAULT_PROJECT_ID):
    """Создаёт задачу в Todoist"""
    data = {
        'content': title,
        'priority': priority,
        'project_id': project_id
    }
    if due:
        data['due_date'] = due
    
    result = api_post('https://api.todoist.com/api/v2/tasks', token, data)
    return result

def update_todoist_task(token, task_id, priority=None, due=None, content=None):
    """Обновляет задачу в Todoist"""
    data = {}
    if priority is not None:
        data['priority'] = priority
    if due is not None:
        data['due_date'] = due if due else ''
    if content is not None:
        data['content'] = content
    
    if data:
        api_post(f'https://api.todoist.com/api/v2/tasks/{task_id}', token, data)

def get_active_todoist_tasks(token):
    """Получает все активные задачи из Todoist"""
    result = api_request(f'https://api.todoist.com/api/v2/tasks?project_id={DEFAULT_PROJECT_ID}', token)
    if not result:
        return []
    # v2 API returns {"results": [...]}
    tasks = result.get('results', [])
    return tasks

def close_todoist_task(token, task_id):
    """Закрывает задачу в Todoist"""
    api_post(f'https://api.todoist.com/api/v2/tasks/{task_id}/close', token, None)

def update_vault_file(fpath, todoist_id=None, status=None, priority=None, due=None):
    """Обновляет frontmatter файла vault"""
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updates = []
        if todoist_id is not None:
            updates.append(('todoist_id', todoist_id))
        if status is not None:
            updates.append(('status', status))
        if priority is not None:
            updates.append(('priority', str(priority)))
        if due is not None:
            updates.append(('due', due))
        
        if not updates:
            return False
        
        if content.startswith('---'):
            end = content.find('\n---', 4)
            if end != -1:
                fm_section = content[3:end]
                rest = content[end+4:]
                
                for key, val in updates:
                    pattern = rf'^({key}:\s*).+$'
                    if re.search(pattern, fm_section, re.MULTILINE):
                        fm_section = re.sub(pattern, rf'\1{val}', fm_section, flags=re.MULTILINE)
                    else:
                        fm_section += f'\n{key}: {val}'
                
                content = '---\n' + fm_section + '\n---' + rest
            else:
                fm_lines = ['---'] + [f'{k}: {v}' for k, v in updates] + ['---', '', content]
                content = '\n'.join(fm_lines)
        else:
            fm_lines = ['---'] + [f'{k}: {v}' for k, v in updates] + ['---', '', content]
            content = '\n'.join(fm_lines) + '\n'
        
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Ошибка обновления {fpath}: {e}", file=sys.stderr)
        return False

def main():
    dry_run = '--dry-run' in sys.argv
    token = get_token()
    state = load_state()
    
    print("🔄 Двухсторонняя синхронизация Todoist ↔ Vault")
    print(f"   Режим: {'Тестовый' if dry_run else 'Рабочий'}")
    print()
    
    # ========== Vault → Todoist ==========
    print("📤 Vault → Todoist")
    print("-" * 40)
    
    vault_tasks = get_tasks_from_vault()
    print(f"   Найдено активных задач в vault: {len(vault_tasks)}")
    
    created_count = 0
    for task in vault_tasks:
        if task['todoist_id']:
            print(f"   ⏭️  Уже синхронизирован: {task['title'][:40]}")
            continue
        
        print(f"   ➕ Создание: {task['title'][:50]}")
        if not dry_run:
            result = create_todoist_task(
                token,
                task['title'],
                priority_to_p(task['priority']),
                task['due']
            )
            if result and 'id' in result:
                todoist_id = result['id']
                update_vault_file(task['path'], todoist_id=todoist_id)
                print(f"      ✅ Создан, ID: {todoist_id}")
                created_count += 1
            else:
                print(f"      ❌ Ошибка: {result}")
        else:
            print(f"      [dry-run]")
    
    print(f"   Создано новых задач: {created_count}")
    print()
    
    # ========== Todoist → Vault ==========
    print("📥 Todoist → Vault")
    print("-" * 40)
    
    todoist_tasks = get_active_todoist_tasks(token)
    if not todoist_tasks:
        print("   ❌ Не удалось получить задачи из Todoist")
    else:
        print(f"   Найдено активных задач в Todoist: {len(todoist_tasks)}")
        
        vault_by_tid = {t['todoist_id']: t for t in vault_tasks if t['todoist_id']}
        
        updated_count = 0
        for tt in todoist_tasks:
            tid = str(tt.get('id', ''))
            if not tid:
                continue
            
            if tid in vault_by_tid:
                vt = vault_by_tid[tid]
                
                changed = False
                new_priority = None
                new_due = None
                
                # Priority
                todoist_p = tt.get('priority', 3)
                vault_p = vt['priority']
                expected_vault_p = p_to_priority(todoist_p)
                if expected_vault_p != vault_p:
                    new_priority = expected_vault_p
                    changed = True
                
                # Due date - v2 API returns dict with 'date' key
                todoist_due = tt.get('due', {})
                if isinstance(todoist_due, dict):
                    todoist_due_str = todoist_due.get('date', '') or ''
                else:
                    todoist_due_str = str(todoist_due) if todoist_due else ''
                
                if todoist_due_str:
                    # Normalize to YYYY-MM-DD
                    if 'T' in todoist_due_str:
                        todoist_due_str = todoist_due_str[:10]
                    if todoist_due_str != vt['due']:
                        new_due = todoist_due_str
                        changed = True
                
                if changed:
                    print(f"   🔄 Обновление: {vt['title'][:40]}")
                    if not dry_run:
                        update_vault_file(vt['path'], priority=new_priority, due=new_due)
                    print(f"      priority: {vault_p} → {new_priority}, due: {vt['due'] or 'none'} → {new_due or 'none'}")
                    updated_count += 1
        
        print(f"   Обновлено задач в vault: {updated_count}")
    
    if not dry_run:
        state['last_sync'] = datetime.utcnow().isoformat()
        save_state(state)
    
    print()
    print(f"✅ Синхронизация завершена")
    print(f"   Последняя синхронизация: {state.get('last_sync', 'никогда')}")

if __name__ == '__main__':
    main()