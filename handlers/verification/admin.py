"""
Verification Bot - Admin Handler.
Handles admin approval/rejection of verifications.
"""

import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database_pg import (
    get_pending_verifications,
    update_verification_status
)

OWNER_TELEGRAM_ID = int(os.getenv("OWNER_TELEGRAM_ID", "0"))


def is_owner(user_id: int) -> bool:
    return user_id == OWNER_TELEGRAM_ID


async def admin_pending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show pending verifications."""
    query = update.callback_query
    await query.answer()
    
    if not is_owner(update.effective_user.id):
        await query.edit_message_text("⛔ Akses ditolak.")
        return
    
    bot_id = context.bot_data.get('bot_id')
    pending = get_pending_verifications(bot_id)
    
    if not pending:
        await query.edit_message_text(
            "📋 *Verifikasi Pending*\n\n"
            "✅ Tidak ada verifikasi yang menunggu.",
            parse_mode="Markdown"
        )
        return
    
    text = f"📋 *Verifikasi Pending ({len(pending)})*\n\n"
    
    keyboard = []
    for v in pending[:10]:
        text += (
            f"• NIM: `{v['student_id']}`\n"
            f"  Nama: {v['full_name']}\n\n"
        )
        keyboard.append([
            InlineKeyboardButton(f"✅ {v['student_id']}", callback_data=f"approve_{v['id']}"),
            InlineKeyboardButton(f"❌ {v['student_id']}", callback_data=f"reject_{v['id']}")
        ])
    
    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def admin_approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Approve a verification."""
    query = update.callback_query
    
    if not is_owner(update.effective_user.id):
        await query.answer("⛔ Akses ditolak.")
        return
    
    verification_id = int(query.data.split("_")[1])
    update_verification_status(verification_id, "approved")
    
    await query.answer("✅ Verifikasi disetujui!")
    
    # Refresh list
    await admin_pending(update, context)


async def admin_reject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reject a verification."""
    query = update.callback_query
    
    if not is_owner(update.effective_user.id):
        await query.answer("⛔ Akses ditolak.")
        return
    
    verification_id = int(query.data.split("_")[1])
    update_verification_status(verification_id, "rejected")
    
    await query.answer("❌ Verifikasi ditolak!")
    
    # Refresh list
    await admin_pending(update, context)
