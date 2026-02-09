#!/usr/bin/env python3
"""
FGGSTORE Card Generator Bot
Main entry point for the Telegram bot application.
"""

import logging
import sys

from telegram.ext import ApplicationBuilder

from app import __version__
from app.config import settings
from app.handlers import CardConversationHandler


def setup_logging() -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        format=settings.LOG_FORMAT,
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def main() -> None:
    """Main function to run the bot."""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        # Validate configuration
        settings.validate()
        settings.setup_directories()

        logger.info(f"Starting FGGSTORE Card Generator Bot v{__version__}")
        logger.info(f"Authorized User ID: {settings.AUTHORIZED_USER_ID}")

        # Build the application
        application = ApplicationBuilder().token(settings.BOT_TOKEN).build()

        # Create and add conversation handler
        conversation_handler = CardConversationHandler()
        application.add_handler(conversation_handler.get_handler())

        # Start the bot
        logger.info("Bot is running and polling for updates...")
        application.run_polling(allowed_updates=["message"])

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        logger.error(f"Required file not found: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
