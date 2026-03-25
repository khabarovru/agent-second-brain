---
type: note
last_accessed: 2026-03-19
relevance: 0.98
tier: active
---
# Wiki-Links Building

## Purpose

Build connections between notes to create a knowledge graph.

## When Saving a Thought

### Step 1: Search for Related Notes

Search thoughts/ for related content:

```
Grep "keyword1" in thoughts/**/*.md
Grep "keyword2" in thoughts/**/*.md
```

Keywords to search:
- Main topic of the thought
- Key entities (people, projects, technologies)
- Domain terms

### Step 2: Check MOC Indexes

Read relevant MOC files:

```
MOC/
├── MOC-ideas.md
├── MOC-projects.md
├── MOC-learnings.md
└── MOC-reflections.md
```

Find related entries.

### Step 3: Link to Goals

Check if thought relates to goals:

```
Read goals/1-yearly-2025.md
Find matching goal areas
```

### Step 4: Add Links to Note (with context)

In the thought file, add **typed relationships** — each link explains WHY it's connected:

**In frontmatter (for graph analysis):**
```yaml
related:
  - "2024 12 15 Voice Agents"
  - "1 Yearly 2026#Ai Development"
```

**In content (inline):**
```markdown
This connects to [[Voice Agents Architecture]] we explored earlier.
```

**In Related section (with context phrases):**
```markdown
## Related
- Voice Agents — extends: real-time TTS pipeline
- Acme Corp — context: NCP campaign uses similar approach
- 1 Yearly 2026#Ai Development — supports: yearly AI skill goal
```

### Relationship Types

Use context phrases after `—` to explain the connection:

| Type | When to use | Example |
|------|------------|---------|
| extends | Builds on another idea | `— extends: adds TTS to voice pipeline` |
| context | Background/origin of idea | `— context: emerged from client project` |
| supports | Aligns with a goal | `— supports: Q1 revenue target` |
| contradicts | Challenges existing note | `— contradicts: previous approach was sync` |
| enables | Makes something possible | `— enables: automated daily reports` |
| requires | Dependency | `— requires: mcp-cli working` |

### Step 5: Update MOC Index

Add new note to appropriate MOC:

```markdown
# MOC: Ideas

## Recent
- 2024 12 20 New Idea — Brief description

## By Topic
### AI & Voice
- 2024 12 20 New Idea
- 2024 12 15 Voice Agents
```

### Step 6: Add Backlinks

In related notes, add backlink to new note if highly relevant.

## Link Format

### Internal Links
```markdown
[[Note Name]]                    # Simple link
[[Note Name|Display Text]]       # With alias
Note Name             # With path
[[Note Name#Section]]            # To heading
```

### Link to Goals
```markdown
1 Yearly 2025#Career & Business
[[goals/3-weekly]] — ONE Big Thing
```

---

## Business Entity Links

### Формат связей

| Тип | Формат | Пример |
|-----|--------|--------|
| Клиент | `Display` | `Acme Corp` |
| Проект | `Display` | `Project Alpha` |
| CRM Lead | `Display` | `TechCo` |

### Где добавлять связи (с typed context)

**В daily file (комментарий):**
```markdown
## 10:30 [voice]
Позвонил в Acme Corp по проекту
<!-- связь: Acme Corp -->
```

**В thoughts (Related section с context phrases):**
```markdown
## Related
- TechCo — context: обсуждение BTL стратегии
- PhoneBrand — extends: SMM стратегия 2026
```

**В задаче Todoist (description):**
```
Description: "Клиент: Acme Corp"
```

---

## Report Section

Track new links created:

```
<b>🔗 Новые связи:</b>
• [[Note A]] ↔ [[Note B]]
• [[New Thought]] → [[Related Project]]
```

## Example Workflow

New thought: "Chatterbox TTS can be used for voice agents"

1. **Search:**
   - Grep "voice" in thoughts/ → finds [[Voice Agents Architecture]]
   - Grep "TTS" in thoughts/ → no results
   - Grep "Chatterbox" → no results

2. **Check MOC:**
   - MOC-learnings.md has "AI & Voice" section

3. **Goals:**
   - 1-yearly-2025.md has "AI Development" goal

4. **Create links:**
   ```yaml
   related:
     - "Voice Agents Architecture"
     - "1 Yearly 2025#Ai Development"
   ```

5. **Update MOC-learnings.md:**
   ```markdown
   ### AI & Voice
   - 2024 12 20 Chatterbox Tts — TTS for voice agents
   ```

6. **Report:**
   ```
   <b>🔗 Новые связи:</b>
   • [[Chatterbox TTS]] ↔ [[Voice Agents Architecture]]
   ```

## Orphan Detection

A note is "orphan" if:
- No incoming links from other notes
- No related notes in frontmatter
- Not listed in any MOC

Flag orphans for review:
```
<b>⚠️ Изолированные заметки:</b>
• Orphan Note
```
