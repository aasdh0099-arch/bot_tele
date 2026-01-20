"""
Verification Bot Handlers Package.
Handlers for student/member verification bot type.
"""

from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters
)

from .verify import (
    start_command,
    verify_command,
    verify_student_id,
    verify_fullname,
    verify_cancel,
    status_command,
    STUDENT_ID, FULLNAME
)
from .admin import (
    admin_pending,
    admin_approve,
    admin_reject
)


def get_all_verification_handlers(bot_id: int) -> list:
    """
    Get all handlers for a verification bot.
    
    Args:
        bot_id: Database ID of the bot
        
    Returns:
        List of handlers to register
    """
    handlers = []
    
    # Verification conversation
    verify_conv = ConversationHandler(
        entry_points=[
            CommandHandler("verify", verify_command),
            CallbackQueryHandler(verify_command, pattern="^start_verify$")
        ],
        states={
            STUDENT_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, verify_student_id)],
            FULLNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, verify_fullname)],
        },
        fallbacks=[
            CallbackQueryHandler(verify_cancel, pattern="^verify_cancel$"),
            CommandHandler("cancel", verify_cancel)
        ],
        per_message=False
    )
    handlers.append(verify_conv)
    
    # Commands
    handlers.extend([
        CommandHandler("start", start_command),
        CommandHandler("status", status_command),
    ])
    
    # Admin callbacks
    handlers.extend([
        CallbackQueryHandler(admin_pending, pattern="^admin_pending$"),
        CallbackQueryHandler(admin_approve, pattern="^approve_\\d+$"),
        CallbackQueryHandler(admin_reject, pattern="^reject_\\d+$"),
    ])
    
    return handlers
