"""
Points Verification Bot Handlers Package.
Bot type for student verification with points/balance system.
Uses PostgreSQL (Neon) database.
"""

import os
from functools import partial
from telegram.ext import CommandHandler

from .user_commands import (
    start_command,
    about_command,
    help_command,
    balance_command,
    checkin_command,
    invite_command,
    use_command,
)
from .verify_commands import (
    verify_command,
    verify2_command,
    verify3_command,
    verify4_command,
    getV4Code_command,
)
from .admin_commands import (
    addbalance_command,
    block_command,
    white_command,
    blacklist_command,
    genkey_command,
    listkeys_command,
    broadcast_command,
)


def get_all_points_verify_handlers(bot_id: int) -> list:
    """
    Get all handlers for a points verification bot.
    
    Args:
        bot_id: Database ID of the bot
        
    Returns:
        List of handlers to register
    """
    handlers = []
    
    # User commands - pass bot_id via partial
    handlers.extend([
        CommandHandler("start", partial(start_command, bot_id=bot_id)),
        CommandHandler("about", partial(about_command, bot_id=bot_id)),
        CommandHandler("help", partial(help_command, bot_id=bot_id)),
        CommandHandler("balance", partial(balance_command, bot_id=bot_id)),
        CommandHandler("qd", partial(checkin_command, bot_id=bot_id)),
        CommandHandler("invite", partial(invite_command, bot_id=bot_id)),
        CommandHandler("use", partial(use_command, bot_id=bot_id)),
    ])
    
    # Verification commands
    handlers.extend([
        CommandHandler("verify", partial(verify_command, bot_id=bot_id)),
        CommandHandler("verify2", partial(verify2_command, bot_id=bot_id)),
        CommandHandler("verify3", partial(verify3_command, bot_id=bot_id)),
        CommandHandler("verify4", partial(verify4_command, bot_id=bot_id)),
        CommandHandler("getV4Code", partial(getV4Code_command, bot_id=bot_id)),
    ])
    
    # Admin commands
    handlers.extend([
        CommandHandler("addbalance", partial(addbalance_command, bot_id=bot_id)),
        CommandHandler("block", partial(block_command, bot_id=bot_id)),
        CommandHandler("white", partial(white_command, bot_id=bot_id)),
        CommandHandler("blacklist", partial(blacklist_command, bot_id=bot_id)),
        CommandHandler("genkey", partial(genkey_command, bot_id=bot_id)),
        CommandHandler("listkeys", partial(listkeys_command, bot_id=bot_id)),
        CommandHandler("broadcast", partial(broadcast_command, bot_id=bot_id)),
    ])
    
    return handlers
