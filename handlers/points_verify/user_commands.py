"""Points Verify User Commands (PostgreSQL version)"""
import os
from telegram import Update
from telegram.ext import ContextTypes
from database_pg import (
    get_or_create_pv_user, get_pv_user, pv_user_exists, is_pv_user_blocked,
    pv_checkin, can_pv_checkin, use_pv_card_key
)

OWNER_TELEGRAM_ID = int(os.getenv("OWNER_TELEGRAM_ID", "0"))


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_id: int):
    """Handle /start command"""
    user = update.effective_user
    
    # Check for invite
    invited_by = None
    if context.args:
        try:
            invited_by = int(context.args[0])
            if not pv_user_exists(bot_id, invited_by):
                invited_by = None
        except:
            invited_by = None
    
    # Get or create user
    pv_user = get_or_create_pv_user(
        bot_id=bot_id,
        telegram_id=user.id,
        username=user.username,
        full_name=user.full_name,
        invited_by=invited_by
    )
    
    if invited_by:
        text = (
            f"🎉 Selamat datang, {user.first_name}!\n\n"
            "Anda terdaftar melalui link undangan.\n"
            f"💰 Bonus: +1 poin\n\n"
            "Gunakan /help untuk melihat perintah."
        )
    else:
        text = (
            f"👋 Selamat datang, {user.first_name}!\n\n"
            "🤖 Bot Verifikasi Student\n\n"
            f"💰 Saldo Anda: {pv_user['balance']} poin\n\n"
            "Gunakan /help untuk melihat perintah yang tersedia."
        )
    
    await update.message.reply_text(text)


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_id: int):
    """Handle /about command"""
    await update.message.reply_text(
        "🤖 *Bot Verifikasi Student*\n\n"
        "Bot ini digunakan untuk verifikasi status pelajar/mahasiswa.\n\n"
        "💰 Setiap verifikasi membutuhkan 1 poin.\n"
        "📅 Dapatkan poin gratis dengan check-in harian.\n"
        "🎁 Undang teman untuk bonus poin.",
        parse_mode="Markdown"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_id: int):
    """Handle /help command"""
    user_id = update.effective_user.id
    is_admin = user_id == OWNER_TELEGRAM_ID
    
    text = (
        "📖 *Perintah Tersedia*\n\n"
        "👤 *User*\n"
        "/start - Mulai bot\n"
        "/balance - Cek saldo poin\n"
        "/qd - Check-in harian (+1 poin)\n"
        "/invite - Link undangan\n"
        "/use <kode> - Tukar kode redeem\n\n"
        "✅ *Verifikasi*\n"
        "/verify - Verifikasi Gemini\n"
        "/verify2 - Verifikasi K12\n"
        "/verify3 - Verifikasi Spotify\n"
        "/verify4 - Verifikasi Bolt.new\n"
    )
    
    if is_admin:
        text += (
            "\n🔧 *Admin*\n"
            "/addbalance <id> <jumlah>\n"
            "/block <id> - Blokir user\n"
            "/white <id> - Unblock user\n"
            "/blacklist - Daftar blokir\n"
            "/genkey <jumlah> [max_uses]\n"
            "/listkeys - Daftar kode\n"
            "/broadcast <pesan>\n"
        )
    
    await update.message.reply_text(text, parse_mode="Markdown")


async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_id: int):
    """Handle /balance command"""
    user_id = update.effective_user.id
    
    if is_pv_user_blocked(bot_id, user_id):
        await update.message.reply_text("⛔ Akun Anda diblokir.")
        return
    
    user = get_pv_user(bot_id, user_id)
    if not user:
        await update.message.reply_text("Silakan /start terlebih dahulu.")
        return
    
    await update.message.reply_text(
        f"💰 *Saldo Poin*\n\n"
        f"Poin Anda: *{user['balance']}* poin",
        parse_mode="Markdown"
    )


async def checkin_command(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_id: int):
    """Handle /qd check-in command"""
    user_id = update.effective_user.id
    
    if is_pv_user_blocked(bot_id, user_id):
        await update.message.reply_text("⛔ Akun Anda diblokir.")
        return
    
    if not pv_user_exists(bot_id, user_id):
        await update.message.reply_text("Silakan /start terlebih dahulu.")
        return
    
    if not can_pv_checkin(bot_id, user_id):
        await update.message.reply_text("❌ Anda sudah check-in hari ini. Kembali besok!")
        return
    
    if pv_checkin(bot_id, user_id):
        user = get_pv_user(bot_id, user_id)
        await update.message.reply_text(
            f"✅ Check-in berhasil!\n"
            f"Poin: +1\n"
            f"Saldo: {user['balance']} poin"
        )
    else:
        await update.message.reply_text("❌ Check-in gagal, coba lagi nanti.")


async def invite_command(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_id: int):
    """Handle /invite command"""
    user_id = update.effective_user.id
    
    if is_pv_user_blocked(bot_id, user_id):
        await update.message.reply_text("⛔ Akun Anda diblokir.")
        return
    
    if not pv_user_exists(bot_id, user_id):
        await update.message.reply_text("Silakan /start terlebih dahulu.")
        return
    
    bot_username = context.bot.username
    invite_link = f"https://t.me/{bot_username}?start={user_id}"
    
    await update.message.reply_text(
        f"🎁 *Link Undangan Anda*\n\n"
        f"`{invite_link}`\n\n"
        "Setiap teman yang bergabung = +2 poin untuk Anda!",
        parse_mode="Markdown"
    )


async def use_command(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_id: int):
    """Handle /use command - redeem code"""
    user_id = update.effective_user.id
    
    if is_pv_user_blocked(bot_id, user_id):
        await update.message.reply_text("⛔ Akun Anda diblokir.")
        return
    
    if not pv_user_exists(bot_id, user_id):
        await update.message.reply_text("Silakan /start terlebih dahulu.")
        return
    
    if not context.args:
        await update.message.reply_text("Penggunaan: /use <kode>")
        return
    
    key_code = context.args[0].strip()
    result = use_pv_card_key(bot_id, key_code, user_id)
    
    if result is None:
        await update.message.reply_text("❌ Kode tidak ditemukan.")
    elif result == -1:
        await update.message.reply_text("❌ Kode sudah habis digunakan.")
    elif result == -2:
        await update.message.reply_text("❌ Kode sudah expired.")
    elif result == -3:
        await update.message.reply_text("❌ Anda sudah menggunakan kode ini.")
    else:
        user = get_pv_user(bot_id, user_id)
        await update.message.reply_text(
            f"✅ Berhasil!\n"
            f"Poin: +{result}\n"
            f"Saldo: {user['balance']} poin"
        )
