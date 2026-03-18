"""Main bot entry point."""

import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from d_brain.bot.handlers import commands, voice, buttons, process, weekly, text, photo, forward, do
from d_brain.config import Settings

LOG_FILE = os.path.expanduser("~/d-brain.log")
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


async def run_bot(settings: Settings) -> None:
    """Run the Telegram bot."""
    logger.info("🚀 Bot starting...")
    
    # Initialize bot
    bot = Bot(
        token=settings.telegram_bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # Initialize dispatcher
    dp = Dispatcher()
    
    # Register routers (order matters - specific before general)
    dp.include_router(commands.router)
    dp.include_router(buttons.router)
    dp.include_router(process.router)
    dp.include_router(weekly.router)
    dp.include_router(do.router)
    dp.include_router(voice.router)
    dp.include_router(photo.router)
    dp.include_router(forward.router)
    dp.include_router(text.router)  # text last - catches everything else
    
    logger.info("Bot handlers registered")
    logger.info(f"Allowed users: {settings.allowed_user_ids or 'all'}")
    logger.info(f"Vault path: {settings.vault_path}")
    
    # Start polling
    try:
        logger.info("Starting polling...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot crashed: {e}", exc_info=True)
    finally:
        await bot.session.close()
        logger.info("Bot stopped")
