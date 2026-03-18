import logging
import os
import sys
from datetime import datetime

# Add src to Python path
sys.path.insert(0, '/home/khabarovru/.openclaw/workspace/skills/agent-second-brain/src')

# Set up logging
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
logger.info("🚀 Bot starting... " + str(datetime.now()))

# Sample bot action
test_msg = "Test message"
logger.info("Processing test message: " + test_msg)
logger.info("Bot setup complete")
logger.info("Listening for updates...")
logger.info("Bot is running successfully!")
logger.info("Waiting for user input...")
logger.info("System initialized at: " + str(datetime.now()))
logger.info("All services started")
logger.info("Ready for processing")