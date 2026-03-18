"""Organize command handler."""

import asyncio
import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from d_brain.bot.formatters import format_organize_report
from d_brain.config import get_settings
from d_brain.services.processor import ClaudeProcessor

router = Router(name="organize")
logger = logging.getLogger(__name__)


@router.message(Command("organize"))
async def cmd_organize(message: Message) -> None:
    """Handle /organize command - organize vault with note-organizer."""
    user_id = message.from_user.id if message.from_user else "unknown"
    logger.info("Organize command triggered by user %s", user_id)

    status_msg = await message.answer("📁 Организую vault... сканирую заметки...")

    settings = get_settings()
    processor = ClaudeProcessor(settings.vault_path, settings.todoist_api_key)

    async def run_with_progress() -> dict:
        task = asyncio.create_task(
            asyncio.to_thread(processor.organize_vault)
        )

        elapsed = 0
        while not task.done():
            await asyncio.sleep(30)
            elapsed += 30
            if not task.done():
                try:
                    await status_msg.edit_text(
                        f"📁 Организую vault... ({elapsed // 60}m {elapsed % 60}s)"
                    )
                except Exception:
                    pass

        return await task

    report = await run_with_progress()

    formatted = format_organize_report(report)
    try:
        await status_msg.edit_text(formatted)
    except Exception:
        await status_msg.edit_text(formatted, parse_mode=None)