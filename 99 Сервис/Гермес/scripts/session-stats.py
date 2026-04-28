#!/usr/bin/env python3
"""session-stats.py — Статистика взаимодействий за период"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

VAULT = "/volume1/docker/openclaw/.openclaw/workspace/skills/agent-second-brain/vault"
SESSIONS_DIR = f"{VAULT}/.sessions"


def get_sessions(user_id="default"):
    """Read session file"""
    session_file = Path(SESSIONS_DIR) / f"{user_id}.jsonl"
    if not session_file.exists():
        return []
    
    entries = []
    with open(session_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    entries.append(json.loads(line))
                except:
                    continue
    return entries


def get_stats(days=7):
    """Get stats for last N days"""
    entries = get_sessions()
    
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    recent = [e for e in entries if e.get("ts", "") >= cutoff]
    
    stats = {"voice": 0, "text": 0, "command": 0, "forward": 0, "photo": 0, "other": 0}
    total_chars = 0
    total_duration = 0
    
    for e in recent:
        t = e.get("type", "unknown")
        if t in stats:
            stats[t] += 1
        else:
            stats["other"] += 1
        
        if "text" in e:
            total_chars += len(e.get("text", ""))
        if "duration" in e:
            total_duration += e.get("duration", 0)
    
    return stats, total_chars, total_duration, len(recent)


def main():
    days = 7
    if len(sys.argv) > 1:
        try:
            days = int(sys.argv[1])
        except:
            pass
    
    print(f"📊 Статистика за {days} дней")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    stats, chars, duration, total = get_stats(days)
    
    print(f"📝 Текстовых:    {stats['text']}")
    print(f"🎤 Голосовых:    {stats['voice']}")
    print(f"⚡ Команд:       {stats['command']}")
    print(f"🔄 Пересланных: {stats['forward']}")
    print(f"🖼 Фото:        {stats['photo']}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📦 Всего:        {total}")
    
    if chars > 0:
        print(f"📊 Символов:     {chars:,}")
    if duration > 0:
        mins = duration // 60
        secs = duration % 60
        print(f"⏱  Голоса:       {mins}м {secs}с")


if __name__ == "__main__":
    main()
