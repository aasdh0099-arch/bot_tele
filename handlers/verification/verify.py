"""
Verification Bot - Verify Handler.
Handles /verify and /status commands.
"""

import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from database_pg import (
    get_or_create_bot_user,
    create_verification,
    get_verification_by_telegram
)

# Conversation states
STUDENT_ID, FULLNAME = range(2)

# Owner for admin
OWNER_TELEGRAM_ID = int(os.getenv("OWNER_TELEGRAM_ID", "0"))


def is_owner(user_id: int) -> bool:
    return user_id == OWNER_TELEGRAM_ID


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    user = update.effective_user
    bot_id = context.bot_data.get('bot_id')
    
    # Register user
    bot_user = get_or_create_bot_user(
        bot_id=bot_id,
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name
    )
    context.user_data['bot_user_id'] = bot_user['id']
    
    # Check existing verification
    existing = get_verification_by_telegram(bot_id, user.id)
    
    keyboard = []
    if existing:
        status_emoji = {"pending": "⏳", "approved": "✅", "rejected": "❌"}
        status = existing.get('status', 'pending')
        emoji = status_emoji.get(status, "❓")
        
        text = (
            f"👋 Halo, {user.first_name}!\n\n"
            f"📋 Status verifikasi Anda: {emoji} *{status.upper()}*\n\n"
            "Gunakan /status untuk detail lebih lanjut."
        )
        
        if status == "rejected":
            keyboard.append([InlineKeyboardButton("🔄 Verifikasi Ulang", callback_data="start_verify")])
    else:
        text = (
            f"👋 Selamat datang, {user.first_name}!\n\n"
            "🎓 *Bot Verifikasi Mahasiswa*\n\n"
            "Gunakan bot ini untuk memverifikasi status mahasiswa Anda.\n\n"
            "Klik tombol di bawah atau gunakan /verify untuk memulai."
        )
        keyboard.append([InlineKeyboardButton("✅ Mulai Verifikasi", callback_data="start_verify")])
    
    if is_owner(user.id):
        keyboard.append([InlineKeyboardButton("🔧 Admin - Pending", callback_data="admin_pending")])
    
    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard) if keyboard else None
    )


async def verify_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start verification process."""
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        message = query.message
        edit = True
    else:
        message = update.message
        edit = False
    
    user = update.effective_user
    bot_id = context.bot_data.get('bot_id')
    
    # Check existing pending/approved
    existing = get_verification_by_telegram(bot_id, user.id)
    if existing and existing['status'] in ['pending', 'approved']:
        text = (
            f"⚠️ Anda sudah memiliki verifikasi dengan status: *{existing['status'].upper()}*\n\n"
            "Gunakan /status untuk melihat detail."
        )
        if edit:
            await message.edit_text(text, parse_mode="Markdown")
        else:
            await message.reply_text(text, parse_mode="Markdown")
        return ConversationHandler.END
    
    text = (
        "🎓 *Verifikasi Mahasiswa*\n\n"
        "Silakan masukkan NIM (Nomor Induk Mahasiswa) Anda:"
    )
    
    keyboard = [[InlineKeyboardButton("❌ Batal", callback_data="verify_cancel")]]
    
    if edit:
        await message.edit_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    
    return STUDENT_ID


async def verify_student_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive student ID."""
    student_id = update.message.text.strip()
    
    # Basic validation
    if len(student_id) < 5:
        await update.message.reply_text("❌ NIM terlalu pendek. Silakan masukkan NIM yang valid:")
        return STUDENT_ID
    
    context.user_data['verify_student_id'] = student_id
    
    keyboard = [[InlineKeyboardButton("❌ Batal", callback_data="verify_cancel")]]
    
    await update.message.reply_text(
        "📝 Masukkan nama lengkap Anda (sesuai kartu mahasiswa):",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    return FULLNAME


async def verify_fullname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive full name and submit verification."""
    user = update.effective_user
    bot_id = context.bot_data.get('bot_id')
    
    student_id = context.user_data.get('verify_student_id')
    full_name = update.message.text.strip()
    
    # Create verification
    verification = create_verification(bot_id, user.id, student_id, full_name)
    
    await update.message.reply_text(
        "✅ *Verifikasi Terkirim!*\n\n"
        f"📋 NIM: `{student_id}`\n"
        f"👤 Nama: {full_name}\n\n"
        "⏳ Status: *PENDING*\n\n"
        "Mohon tunggu persetujuan dari admin. "
        "Gunakan /status untuk mengecek status verifikasi.",
        parse_mode="Markdown"
    )
    
    # Notify owner
    try:
        from telegram import Bot
        bot = context.bot
        await bot.send_message(
            chat_id=OWNER_TELEGRAM_ID,
            text=(
                "🔔 *Verifikasi Baru!*\n\n"
                f"👤 User: {user.first_name} (@{user.username or 'N/A'})\n"
                f"📋 NIM: `{student_id}`\n"
                f"👤 Nama: {full_name}\n\n"
                "Gunakan /start di bot untuk review."
            ),
            parse_mode="Markdown"
        )
    except:
        pass
    
    # Clear user data
    context.user_data.pop('verify_student_id', None)
    
    return ConversationHandler.END


async def verify_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel verification."""
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text("❌ Verifikasi dibatalkan.")
    else:
        await update.message.reply_text("❌ Verifikasi dibatalkan.")
    
    return ConversationHandler.END


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check verification status."""
    user = update.effective_user
    bot_id = context.bot_data.get('bot_id')
    
    verification = get_verification_by_telegram(bot_id, user.id)
    
    if not verification:
        await update.message.reply_text(
            "📋 Anda belum memiliki verifikasi.\n\n"
            "Gunakan /verify untuk memulai proses verifikasi.",
            parse_mode="Markdown"
        )
        return
    
    status_emoji = {"pending": "⏳", "approved": "✅", "rejected": "❌"}
    status = verification.get('status', 'pending')
    emoji = status_emoji.get(status, "❓")
    
    text = (
        f"📋 *Status Verifikasi*\n\n"
        f"📋 NIM: `{verification['student_id']}`\n"
        f"👤 Nama: {verification['full_name']}\n"
        f"📊 Status: {emoji} *{status.upper()}*\n"
    )
    
    if status == "approved" and verification.get('verified_at'):
        text += f"✅ Diverifikasi: {verification['verified_at'].strftime('%d/%m/%Y %H:%M')}"
    elif status == "rejected":
        text += "\n💡 Anda dapat mengajukan verifikasi ulang dengan /verify"
    
    await update.message.reply_text(text, parse_mode="Markdown")
