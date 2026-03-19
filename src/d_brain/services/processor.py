"""openclaw processing service."""

import logging
import os
import subprocess
from datetime import date
from pathlib import Path
from typing import Any

from d_brain.services.session import SessionStore

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 1200  # 20 minutes


class ClaudeProcessor:
    """Service for triggering Openclaw Code processing."""

    def __init__(self, vault_path: Path, todoist_api_key: str = "") -> None:
        self.vault_path = Path(vault_path)
        self.todoist_api_key = todoist_api_key
        self._mcp_config_path = (self.vault_path.parent / "mcp-config.json").resolve()

    def _load_skill_content(self) -> str:
        """Load dbrain-processor skill content for inclusion in prompt.

        NOTE: @vault/ references don't work in --print mode,
        so we must include skill content directly in the prompt.
        """
        skill_path = self.vault_path / "99 _Сервис" / "Skills" / "dbrain-processor" / "SKILL.md"
        if skill_path.exists():
            return skill_path.read_text()
        return ""

    def _load_todoist_reference(self) -> str:
        """Load Todoist reference for inclusion in prompt."""
        ref_path = self.vault_path / "99 _Сервис" / "Skills" / "dbrain-processor" / "references" / "todoist.md"
        if ref_path.exists():
            return ref_path.read_text()
        return ""

    def _get_session_context(self, user_id: int) -> str:
        """Get today's session context for openclaw.

        Args:
            user_id: Telegram user ID

        Returns:
            Recent session entries formatted for inclusion in prompt.
        """
        if user_id == 0:
            return ""

        session = SessionStore(self.vault_path)
        today_entries = session.get_today(user_id)
        if not today_entries:
            return ""

        lines = ["=== TODAY'S SESSION ==="]
        for entry in today_entries[-10:]:
            ts = entry.get("ts", "")[11:16]  # HH:MM from ISO
            entry_type = entry.get("type", "unknown")
            text = entry.get("text", "")[:80]
            if text:
                lines.append(f"{ts} [{entry_type}] {text}")
        lines.append("=== END SESSION ===\n")
        return "\n".join(lines)

    def _html_to_markdown(self, html: str) -> str:
        """Convert Telegram HTML to Obsidian Markdown."""
        import re

        text = html
        # <b>text</b> → **text**
        text = re.sub(r"<b>(.*?)</b>", r"**\1**", text)
        # <i>text</i> → *text*
        text = re.sub(r"<i>(.*?)</i>", r"*\1*", text)
        # <code>text</code> → `text`
        text = re.sub(r"<code>(.*?)</code>", r"`\1`", text)
        # <s>text</s> → ~~text~~
        text = re.sub(r"<s>(.*?)</s>", r"~~\1~~", text)
        # Remove <u> (no Markdown equivalent, just keep text)
        text = re.sub(r"</?u>", "", text)
        # <a href="url">text</a> → [text](url)
        text = re.sub(r'<a href="([^"]+)">([^<]+)</a>', r"[\2](\1)", text)

        return text

    def _save_weekly_summary(self, report_html: str, week_date: date) -> Path:
        """Save weekly summary to 85 Сводки/YYYY-WXX-summary.md."""
        # Calculate ISO week number
        year, week, _ = week_date.isocalendar()
        filename = f"{year}-W{week:02d}-summary.md"
        summary_path = self.vault_path / "85 Сводки" / filename

        # Convert HTML to Markdown for Obsidian
        content = self._html_to_markdown(report_html)

        # Add frontmatter
        frontmatter = f"""---
date: {week_date.isoformat()}
type: weekly-summary
week: {year}-W{week:02d}
---

"""
        summary_path.write_text(frontmatter + content)
        logger.info("Weekly summary saved to %s", summary_path)
        return summary_path

    def _update_weekly_moc(self, summary_path: Path) -> None:
        """Add link to new summary in MOC-weekly.md."""
        moc_path = self.vault_path / "MOC" / "MOC-weekly.md"
        if moc_path.exists():
            content = moc_path.read_text()
            link = f"- [[summaries/{summary_path.name}|{summary_path.stem}]]"
            # Insert after "## Previous Weeks" if not already there
            if summary_path.stem not in content:
                content = content.replace(
                    "## Previous Weeks\n",
                    f"## Previous Weeks\n\n{link}\n",
                )
                moc_path.write_text(content)
                logger.info("Updated MOC-weekly.md with link to %s", summary_path.stem)

    def _run_goal_aligner(self) -> str:
        """Run goal-aligner agent to check task↔goal alignment.

        Returns:
            Alignment report as plain text (not HTML).
        """
        logger.info("Running goal-aligner check...")

        prompt = """Проверь alignment между активными задачами в Todoist и целями из 60 Цели/*.

WORKFLOW:
1. Прочитай все цели: 60 Цели/0-vision-3y.md, 60 Цели/1-yearly-YYYY.md, 60 Цели/2-monthly.md, 60 Цели/3-weekly.md
2. Получи активные задачи через mcp__todoist__find-tasks (limit: 50)
3. Классифицируй каждую задачу:
   - ✅ Aligned — явно связана с целью
   - 🔶 Possibly aligned — похожие keywords
   - ❌ Orphan — нет связи с целями
4. Найди stale goals (без активности 7+ дней)

OUTPUT FORMAT (plain text for inclusion in weekly digest):
```
🎯 Goal Alignment Check

📋 Orphan Tasks (not aligned):
• Task name — suggest: Goal X
• Task name — suggest: Goal Y
(or "✅ All tasks aligned")

🎯 Stale Goals (no activity 7+ days):
• Goal name — 12 days idle
(or "✅ All goals active")

📊 Distribution:
• Goal A: 5 tasks
• Goal B: 3 tasks
• No goal: 2 tasks

💡 Recommendations:
- Start: [goal to focus on]
- Stop: [tasks not aligned]
- Continue: [aligned work]
```

CRITICAL: Вернуть ТОЛЬКО текст отчёта, без Markdown форматирования вокруг."""

        try:
            env = os.environ.copy()
            if self.todoist_api_key:
                env["TODOIST_API_TOKEN"] = self.todoist_api_key

            result = subprocess.run(
                [
                    "openclaw",
                    "agent",
                    "--agent", "goal-aligner",
                    "--session-id", "goal-aligner-session",
                    "-m", prompt,
                ],
                cwd=self.vault_path,
                capture_output=True,
                text=True,
                timeout=180,  # 3 minutes should be enough
                check=False,
                env=env,
            )

            if result.returncode != 0:
                logger.warning("Goal aligner failed: %s", result.stderr)
                return "(Goal alignment check failed — skipping)"

            return result.stdout.strip()

        except subprocess.TimeoutExpired:
            logger.warning("Goal aligner timed out")
            return "(Goal alignment check timed out)"
        except Exception as e:
            logger.warning("Goal aligner error: %s", e)
            return "(Goal alignment check unavailable)"

    def process_daily(self, day: date | None = None) -> dict[str, Any]:
        """Process daily file with openclaw.

        Args:
            day: Date to process (default: today)

        Returns:
            Processing report as dict
        """
        if day is None:
            day = date.today()

        daily_file = self.vault_path / "daily" / f"{day.isoformat()}.md"

        if not daily_file.exists():
            logger.warning("No daily file for %s, creating empty one", day)
            daily_file.parent.mkdir(parents=True, exist_ok=True)
            daily_file.write_text(f"# {day.isoformat()}\n\n")
            # Return early if file was just created empty
            return {
                "error": f"No entries yet for {day}. Daily file created.",
                "processed_entries": 0,
            }

        # Load skill content directly (@ references don't work in --print mode)
        skill_content = self._load_skill_content()

        prompt = f"""Сегодня {day}. Выполни ежедневную обработку.

=== SKILL INSTRUCTIONS ===
{skill_content}
=== END SKILL ===

ПЕРВЫМ ДЕЛОМ: вызови mcp__todoist__user-info чтобы убедиться что MCP работает.

CRITICAL MCP RULE:
- ТЫ ИМЕЕШЬ ДОСТУП к mcp__todoist__* tools — ВЫЗЫВАЙ ИХ НАПРЯМУЮ
- НИКОГДА не пиши "MCP недоступен" или "добавь вручную"
- Для задач: вызови mcp__todoist__add-tasks tool
- Если tool вернул ошибку — покажи ТОЧНУЮ ошибку в отчёте

CRITICAL OUTPUT FORMAT:
- Return ONLY raw HTML for Telegram (parse_mode=HTML)
- NO markdown: no **, no ## , no ```, no tables
- Start directly with 📊 <b>Обработка за {day}</b>
- Allowed tags: <b>, <i>, <code>, <s>, <u>
- If entries already processed, return status report in same HTML format"""

        try:
            # Pass TODOIST_API_TOKEN to openclaw subprocess for MCP
            env = os.environ.copy()
            if self.todoist_api_key:
                env["TODOIST_API_TOKEN"] = self.todoist_api_key

            result = subprocess.run(
                [
                    "openclaw",
                    "agent", "--agent", "dbrain-processor", "--session-id", "dbrain-isolated",
                    
                    "-m", prompt,],
                cwd=self.vault_path.parent,
                capture_output=True,
                text=True,
                timeout=DEFAULT_TIMEOUT,
                check=False,
                env=env,
            )

            if result.returncode != 0:
                logger.error("openclaw processing failed: %s", result.stderr)
                return {
                    "error": result.stderr or "openclaw processing failed",
                    "processed_entries": 0,
                }

            # Return human-readable output
            output = result.stdout.strip()
            return {
                "report": output,
                "processed_entries": 1,  # успешно обработано
            }

        except subprocess.TimeoutExpired:
            logger.error("openclaw processing timed out")
            return {
                "error": "Processing timed out",
                "processed_entries": 0,
            }
        except FileNotFoundError:
            logger.error("openclaw CLI not found")
            return {
                "error": "openclaw CLI not installed",
                "processed_entries": 0,
            }
        except Exception as e:
            logger.exception("Unexpected error during processing")
            return {
                "error": str(e),
                "processed_entries": 0,
            }

    def execute_prompt(self, user_prompt: str, user_id: int = 0) -> dict[str, Any]:
        """Execute arbitrary prompt with openclaw.

        Args:
            user_prompt: User's natural language request
            user_id: Telegram user ID for session context

        Returns:
            Execution report as dict
        """
        today = date.today()

        # Load context
        todoist_ref = self._load_todoist_reference()
        session_context = self._get_session_context(user_id)

        prompt = f"""Ты - персональный ассистент d-brain.

CONTEXT:
- Текущая дата: {today}
- Vault path: {self.vault_path}

{session_context}=== TODOIST REFERENCE ===
{todoist_ref}
=== END REFERENCE ===

ПЕРВЫМ ДЕЛОМ: вызови mcp__todoist__user-info чтобы убедиться что MCP работает.

CRITICAL MCP RULE:
- ТЫ ИМЕЕШЬ ДОСТУП к mcp__todoist__* tools — ВЫЗЫВАЙ ИХ НАПРЯМУЮ
- НИКОГДА не пиши "MCP недоступен" или "добавь вручную"
- Если tool вернул ошибку — покажи ТОЧНУЮ ошибку в отчёте

USER REQUEST:
{user_prompt}

CRITICAL OUTPUT FORMAT:
- Return ONLY raw HTML for Telegram (parse_mode=HTML)
- NO markdown: no **, no ##, no ```, no tables, no -
- Start with emoji and <b>header</b>
- Allowed tags: <b>, <i>, <code>, <s>, <u>
- Be concise - Telegram has 4096 char limit

EXECUTION:
1. Analyze the request
2. Call MCP tools directly (mcp__todoist__*, read/write files)
3. Return HTML status report with results"""

        try:
            env = os.environ.copy()
            if self.todoist_api_key:
                env["TODOIST_API_KEY"] = self.todoist_api_key

            result = subprocess.run(
                [
                    "openclaw",
                    "agent", "--agent", "dbrain-processor", "--session-id", "dbrain-isolated",
                    
                    "-m", prompt,],
                cwd=self.vault_path.parent,
                capture_output=True,
                text=True,
                timeout=DEFAULT_TIMEOUT,
                check=False,
                env=env,
            )

            if result.returncode != 0:
                logger.error("openclaw execution failed: %s", result.stderr)
                return {
                    "error": result.stderr or "openclaw execution failed",
                    "processed_entries": 0,
                }

            return {
                "report": result.stdout.strip(),
                "processed_entries": 1,
            }

        except subprocess.TimeoutExpired:
            logger.error("openclaw execution timed out")
            return {"error": "Execution timed out", "processed_entries": 0}
        except FileNotFoundError:
            logger.error("openclaw CLI not found")
            return {"error": "openclaw CLI not installed", "processed_entries": 0}
        except Exception as e:
            logger.exception("Unexpected error during execution")
            return {"error": str(e), "processed_entries": 0}

    def generate_weekly(self) -> dict[str, Any]:
        """Generate weekly digest with openclaw.

        Returns:
            Weekly digest report as dict
        """
        today = date.today()

        # Step 1: Run goal alignment check
        alignment_report = self._run_goal_aligner()

        prompt = f"""Сегодня {today}. Сгенерируй недельный дайджест.

ALIGNMENT REPORT:
{alignment_report}

Используй эту информацию о связи задач↔целей в дайджесте.

ПЕРВЫМ ДЕЛОМ: вызови mcp__todoist__user-info чтобы убедиться что MCP работает.

CRITICAL MCP RULE:
- ТЫ ИМЕЕШЬ ДОСТУП к mcp__todoist__* tools — ВЫЗЫВАЙ ИХ НАПРЯМУЮ
- НИКОГДА не пиши "MCP недоступен" или "добавь вручную"
- Для выполненных задач: вызови mcp__todoist__find-completed-tasks tool
- Если tool вернул ошибку — покажи ТОЧНУЮ ошибку в отчёте

WORKFLOW:
1. Собери данные за неделю (daily файлы в 80 Ежедневные/, completed tasks через MCP)
2. Проанализируй прогресс по целям (60 Цели/3-weekly.md)
3. Определи победы и вызовы
4. Сгенерируй HTML отчёт

CRITICAL OUTPUT FORMAT:
- Return ONLY raw HTML for Telegram (parse_mode=HTML)
- NO markdown: no **, no ##, no ```, no tables
- Start with 📅 <b>Недельный дайджест</b>
- Allowed tags: <b>, <i>, <code>, <s>, <u>
- Be concise - Telegram has 4096 char limit"""

        try:
            env = os.environ.copy()
            if self.todoist_api_key:
                env["TODOIST_API_KEY"] = self.todoist_api_key

            result = subprocess.run(
                [
                    "openclaw",
                    "agent", "--agent", "dbrain-processor", "--session-id", "dbrain-isolated",
                    
                    "-m", prompt,],
                cwd=self.vault_path.parent,
                capture_output=True,
                text=True,
                timeout=DEFAULT_TIMEOUT,
                check=False,
                env=env,
            )

            if result.returncode != 0:
                logger.error("Weekly digest failed: %s", result.stderr)
                return {
                    "error": result.stderr or "Weekly digest failed",
                    "processed_entries": 0,
                }

            output = result.stdout.strip()

            # Save to summaries/ and update MOC
            try:
                summary_path = self._save_weekly_summary(output, today)
                self._update_weekly_moc(summary_path)
            except Exception as e:
                logger.warning("Failed to save weekly summary: %s", e)

            return {
                "report": output,
                "processed_entries": 1,
            }

        except subprocess.TimeoutExpired:
            logger.error("Weekly digest timed out")
            return {"error": "Weekly digest timed out", "processed_entries": 0}
        except FileNotFoundError:
            logger.error("openclaw CLI not found")
            return {"error": "openclaw CLI not installed", "processed_entries": 0}
        except Exception as e:
            logger.exception("Unexpected error during weekly digest")
            return {"error": str(e), "processed_entries": 0}
