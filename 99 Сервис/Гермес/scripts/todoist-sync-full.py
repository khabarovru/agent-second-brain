#!/usr/bin/env python3
"""todoist-sync-full.py — Двухсторонняя синхронизация Obsidian ↔ Todoist"""

import os
import sys
import json
import re
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

VAULT = "/volume1/docker/openclaw/.openclaw/workspace/skills/agent-second-brain/vault"
STATE_FILE = os.path.join(os.path.dirname(__file__), "todoist-sync-state.json")
TODOIST_TOKEN = "c1f7278f1dd135b6f0dcdf4a01018c70aead351f"
TODOIST_API = "https://api.todoist.com/api/v1"
TODOIST_PROJECT = "6CrgJfgjMh6M2p7Q"  # Inbox / Work

DRY_RUN = "--dry-run" in sys.argv


def api_request(method, endpoint, data=None):
    """Make Todoist API request"""
    cmd = [
        "curl", "-s", "-X", method,
        f"{TODOIST_API}/{endpoint}",
        "-H", f"Authorization: Bearer {TODOIST_TOKEN}",
        "-H", "Content-Type: application/json"
    ]
    if data:
        cmd += ["-d", json.dumps(data)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout) if result.stdout else {}


def get_frontmatter(content):
    """Extract frontmatter dict from markdown content"""
    fm = {}
    if content.startswith("---"):
        end = content.find("---\n", 3)
        if end > 0:
            fm_text = content[3:end]
            for line in fm_text.strip().split("\n"):
                if ":" in line:
                    key, val = line.split(":", 1)
                    fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm, content


def update_frontmatter(content, fm):
    """Update frontmatter in markdown content"""
    if content.startswith("---"):
        end = content.find("---\n", 3)
        if end > 0:
            fm_lines = []
            for k, v in fm.items():
                fm_lines.append(f'{k}: "{v}"')
            return "---\n" + "\n".join(fm_lines) + "\n---\n" + content[end + 4:]
    return content


def read_file(path):
    """Read file content"""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    """Write file content"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def parse_due(date_str):
    """Parse date string to Todoist due format"""
    if not date_str:
        return None
    
    date_str = date_str.strip()
    today = datetime.now().date()
    
    # Already YYYY-MM-DD
    if re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        return {"date": date_str}
    
    # Relative dates
    if date_str in ["today", "сегодня"]:
        return {"date": today.isoformat()}
    if date_str in ["tomorrow", "завтра"]:
        return {"date": (today + timedelta(days=1)).isoformat()}
    if date_str in ["next monday", "следующий понедельник"]:
        days_ahead = 7 - today.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return {"date": (today + timedelta(days=days_ahead)).isoformat()}
    
    # "in X days"
    m = re.match(r"in (\d+) days?", date_str.lower())
    if m:
        days = int(m.group(1))
        return {"date": (today + timedelta(days=days)).isoformat()}
    
    return None


def priority_to_todoist(p):
    """Convert vault priority (1-4) to Todoist (p1-p4)"""
    # p1=urgent (highest), p4=lowest (normal)
    # Vault 1=highest → Todoist p1, Vault 4=lowest → Todoist p4
    return {1: 4, 2: 3, 3: 2, 4: 1}.get(p, 1)


def priority_from_todoist(p):
    """Convert Todoist priority to vault (1-4)"""
    return {4: 1, 3: 2, 2: 3, 1: 4}.get(p, 4)


def vault_to_todoist():
    """Sync vault tasks to Todoist"""
    print("\n📤 Vault → Todoist")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    created = 0
    updated = 0
    skipped = 0
    
    folders = [
        f"{VAULT}/50 Задачи/Active",
        f"{VAULT}/00 Входящие/Tasks"
    ]
    
    for folder in folders:
        if not os.path.exists(folder):
            continue
        
        for md_file in Path(folder).glob("*.md"):
            content = read_file(str(md_file))
            fm, body = get_frontmatter(content)
            
            # Skip if already has todoist_id
            if fm.get("todoist_id"):
                skipped += 1
                continue
            
            # Get task info
            title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else md_file.stem
            
            # Get priority
            priority = int(fm.get("priority", 4))
            
            # Get due date
            due = parse_due(fm.get("due", ""))
            
            # Build task data
            task_data = {
                "content": title,
                "project_id": TODOIST_PROJECT,
                "priority": priority_to_todoist(priority)
            }
            if due:
                task_data["due_string"] = due["date"]
            
            print(f"  {'➕' if not DRY_RUN else '🔍'} {title[:50]}")
            
            if DRY_RUN:
                print(f"      priority={priority}, due={due}")
            else:
                result = api_request("POST", "tasks", task_data)
                if result.get("id"):
                    fm["todoist_id"] = result["id"]
                    new_content = update_frontmatter(body, fm)
                    write_file(str(md_file), new_content)
                    print(f"      → создан (ID: {result['id']})")
                    created += 1
                else:
                    print(f"      → ОШИБКА: {result}")
    
    print(f"\n  Создано: {created}, Пропущено: {skipped}")
    return created


def todoist_to_vault():
    """Sync Todoist tasks to vault"""
    print("\n📥 Todoist → Vault")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    updated = 0
    not_found = 0
    
    # Get active tasks from Todoist
    tasks = api_request("GET", f"tasks?project_id={TODOIST_PROJECT}")
    if isinstance(tasks, dict):
        tasks = tasks.get("results", []) if "results" in tasks else tasks.get("tasks", [])
    elif not isinstance(tasks, list):
        tasks = []
    
    # Load state
    state = {}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
    
    for task in tasks:
        task_id = str(task.get("id", ""))
        
        # Find file with this todoist_id
        found = False
        for folder in ["50 Задачи/Active", "00 Входящие/Tasks"]:
            folder_path = f"{VAULT}/{folder}"
            if not os.path.exists(folder_path):
                continue
            for md_file in Path(folder_path).glob("*.md"):
                content = read_file(str(md_file))
                fm, body = get_frontmatter(content)
                if fm.get("todoist_id") == task_id:
                    # Update priority and due
                    changed = False
                    
                    # Priority
                    todoist_p = task.get("priority", 1)
                    vault_p = priority_from_todoist(todoist_p)
                    if str(fm.get("priority", "")) != str(vault_p):
                        fm["priority"] = str(vault_p)
                        changed = True
                    
                    # Due date
                    due = task.get("due", {})
                    due_date = due.get("date", "") if due else ""
                    if due_date and fm.get("due") != due_date:
                        fm["due"] = due_date
                        changed = True
                    
                    if changed:
                        new_content = update_frontmatter(body, fm)
                        write_file(str(md_file), new_content)
                        print(f"  ✅ {task.get('content', '')[:50]}")
                        print(f"      priority={vault_p}, due={due_date}")
                        updated += 1
                    found = True
                    break
            if found:
                break
        
        if not found:
            not_found += 1
    
    print(f"\n  Обновлено: {updated}, Не найдено в vault: {not_found}")
    return updated


def main():
    print("📋 Todoist Sync (Obsidian ↔ Todoist)")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    if DRY_RUN:
        print("🔍 Режим: тестовый (без изменений)")
    else:
        print("⚙️  Режим: рабочий")
    
    # Vault → Todoist
    vault_to_todoist()
    
    # Todoist → Vault
    todoist_to_vault()
    
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("✅ Синхронизация завершена")


if __name__ == "__main__":
    main()
