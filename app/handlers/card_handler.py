"""Telegram conversation handler for card generation."""

import logging
import os
from datetime import datetime, timedelta
from pathlib import Path

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from app.config import settings
from app.models import CardData
from app.services import CardGeneratorService
from app.utils import MESSAGES, COUNTRY_KEYBOARD, PRICE_KEYBOARD, ConversationStates

logger = logging.getLogger(__name__)


class CardConversationHandler:
    """Handles the conversation flow for card generation."""

    def __init__(self):
        """Initialize the conversation handler."""
        self.card_generator = CardGeneratorService()

    def _is_authorized(self, user_id: int) -> bool:
        """Check if the user is authorized to use the bot."""
        return user_id == settings.AUTHORIZED_USER_ID

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """
        Handle the /start command - begin card generation flow.

        Args:
            update: Telegram update object
            context: Telegram context

        Returns:
            Next conversation state
        """
        if not self._is_authorized(update.effective_user.id):
            await update.message.reply_text(MESSAGES["unauthorized"])
            return ConversationHandler.END

        reply_markup = ReplyKeyboardMarkup(
            PRICE_KEYBOARD, one_time_keyboard=True, resize_keyboard=True
        )
        await update.message.reply_text(MESSAGES["select_price"], reply_markup=reply_markup)
        return ConversationStates.PRICE

    async def handle_price(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """
        Handle price selection.

        Args:
            update: Telegram update object
            context: Telegram context

        Returns:
            Next conversation state
        """
        context.user_data["price"] = update.message.text.strip()

        reply_markup = ReplyKeyboardMarkup(
            COUNTRY_KEYBOARD, one_time_keyboard=True, resize_keyboard=True
        )
        await update.message.reply_text(MESSAGES["select_country"], reply_markup=reply_markup)
        return ConversationStates.COUNTRY

    async def handle_country(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """
        Handle country selection.

        Args:
            update: Telegram update object
            context: Telegram context

        Returns:
            Next conversation state
        """
        context.user_data["country"] = update.message.text.strip()
        await update.message.reply_text(MESSAGES["enter_code"])
        return ConversationStates.CODE

    async def handle_code(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """
        Handle activation code input.

        Args:
            update: Telegram update object
            context: Telegram context

        Returns:
            Next conversation state
        """
        user_input = update.message.text.strip()
        formatted_code = CardData.format_activation_code(user_input)
        context.user_data["activation_code"] = formatted_code

        await update.message.reply_text(MESSAGES["enter_name"])
        return ConversationStates.NAME

    async def handle_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """
        Handle customer name input and generate the card.

        Args:
            update: Telegram update object
            context: Telegram context

        Returns:
            Conversation end state
        """
        if not self._is_authorized(update.effective_user.id):
            await update.message.reply_text(MESSAGES["unauthorized"])
            return ConversationHandler.END

        # Get current time with timezone offset
        now = datetime.utcnow() + timedelta(hours=settings.TIMEZONE_OFFSET_HOURS)

        # Create card data
        card_data = CardData(
            price=context.user_data["price"],
            country=context.user_data["country"],
            activation_code=context.user_data["activation_code"],
            customer_name=update.message.text.strip(),
            issue_date=now.strftime("%Y-%m-%d"),
            issue_time=now.strftime("%I:%M %p"),
        )

        # Generate output path
        output_path = settings.TEMP_DIR / f"output_{update.message.chat_id}_{now.timestamp()}.png"

        try:
            # Generate the card
            self.card_generator.generate_card(card_data.to_dict(), output_path)

            # Send the card to the user
            with open(output_path, "rb") as photo:
                await update.message.reply_photo(photo=photo)

            logger.info(f"Card generated and sent to user {update.effective_user.id}")

        except Exception as e:
            logger.error(f"Error generating card: {e}")
            await update.message.reply_text("❌ حدث خطأ أثناء إنشاء البطاقة. حاول مرة أخرى.")

        finally:
            # Clean up the generated file
            if output_path.exists():
                os.remove(output_path)

        return ConversationHandler.END

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """
        Handle /cancel command - abort the conversation.

        Args:
            update: Telegram update object
            context: Telegram context

        Returns:
            Conversation end state
        """
        await update.message.reply_text(MESSAGES["cancelled"])
        return ConversationHandler.END

    def get_handler(self) -> ConversationHandler:
        """
        Get the configured conversation handler.

        Returns:
            ConversationHandler instance
        """
        return ConversationHandler(
            entry_points=[CommandHandler("start", self.start)],
            states={
                ConversationStates.PRICE: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_price)
                ],
                ConversationStates.COUNTRY: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_country)
                ],
                ConversationStates.CODE: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_code)
                ],
                ConversationStates.NAME: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_name)
                ],
            },
            fallbacks=[CommandHandler("cancel", self.cancel)],
        )
