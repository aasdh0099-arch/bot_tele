"""
Custom Bot Handlers Package.
Minimal handlers for custom bot type - just /start.
"""

from telegram.ext import CommandHandler
from telegram import Update
from telegram.ext import ContextTypes

from database_pg import get_or_create_bot_user


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start for custom bot."""
    user = update.effective_user
    bot_id = context.bot_data.get('bot_id')
    
    # Register user
    get_or_create_bot_user(
        bot_id=bot_id,
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name
    )
    
    await update.message.reply_text(
        f"👋 Halo, {user.first_name}!\n\n"
        "🤖 Bot ini dalam tahap pengembangan.\n"
        "Silakan hubungi admin untuk informasi lebih lanjut."
    )


def get_custom_handlers(bot_id: int) -> list:
    """Get handlers for custom bot type."""
    return [
        CommandHandler("start", start_command)
    ]
