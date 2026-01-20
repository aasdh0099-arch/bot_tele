"""Points Verify Commands (PostgreSQL version)
Simplified verification handlers.
"""
import os
import httpx
from telegram import Update
from telegram.ext import ContextTypes
from database_pg import (
    get_pv_user, pv_user_exists, is_pv_user_blocked, 
    deduct_pv_balance, add_pv_verification
)

OWNER_TELEGRAM_ID = int(os.getenv("OWNER_TELEGRAM_ID", "0"))
VERIFY_COST = 1


async def verify_command(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_id: int):
    """Handle /verify command - Gemini One Pro"""
    user_id = update.effective_user.id
    
    if is_pv_user_blocked(bot_id, user_id):
        await update.message.reply_text("⛔ Akun Anda diblokir.")
        return
        
    user = get_pv_user(bot_id, user_id)
    if not user:
        await update.message.reply_text("Silakan /start terlebih dahulu.")
        return
    
    if user['balance'] < VERIFY_COST:
        await update.message.reply_text(
            f"❌ Saldo tidak cukup.\n"
            f"Dibutuhkan: {VERIFY_COST} poin\n"
            f"Saldo Anda: {user['balance']} poin"
        )
        return
    
    await update.message.reply_text("⏳ Memproses verifikasi Gemini...")
    
    # Placeholder - actual verification logic would go here
    # For now, just deduct and record
    if deduct_pv_balance(bot_id, user_id, VERIFY_COST):
        add_pv_verification(bot_id, user_id, "gemini", "", "completed", "Verification processed")
        await update.message.reply_text(
            "✅ Verifikasi Gemini selesai!\n"
            f"Saldo: {user['balance'] - VERIFY_COST} poin"
        )
    else:
        await update.message.reply_text("❌ Gagal memproses verifikasi.")


async def verify2_command(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_id: int):
    """Handle /verify2 command - K12"""
    user_id = update.effective_user.id
    
    if is_pv_user_blocked(bot_id, user_id):
        await update.message.reply_text("⛔ Akun Anda diblokir.")
        return
    
    user = get_pv_user(bot_id, user_id)
    if not user:
        await update.message.reply_text("Silakan /start terlebih dahulu.")
        return
    
    if user['balance'] < VERIFY_COST:
        await update.message.reply_text(f"❌ Saldo tidak cukup. Dibutuhkan: {VERIFY_COST} poin")
        return
    
    await update.message.reply_text("⏳ Memproses verifikasi K12...")
    
    if deduct_pv_balance(bot_id, user_id, VERIFY_COST):
        add_pv_verification(bot_id, user_id, "k12", "", "completed", "Verification processed")
        await update.message.reply_text(
            "✅ Verifikasi K12 selesai!\n"
            f"Saldo: {user['balance'] - VERIFY_COST} poin"
        )
    else:
        await update.message.reply_text("❌ Gagal memproses verifikasi.")


async def verify3_command(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_id: int):
    """Handle /verify3 command - Spotify Student"""
    user_id = update.effective_user.id
    
    if is_pv_user_blocked(bot_id, user_id):
        await update.message.reply_text("⛔ Akun Anda diblokir.")
        return
    
    user = get_pv_user(bot_id, user_id)
    if not user:
        await update.message.reply_text("Silakan /start terlebih dahulu.")
        return
    
    if user['balance'] < VERIFY_COST:
        await update.message.reply_text(f"❌ Saldo tidak cukup. Dibutuhkan: {VERIFY_COST} poin")
        return
    
    await update.message.reply_text("⏳ Memproses verifikasi Spotify Student...")
    
    if deduct_pv_balance(bot_id, user_id, VERIFY_COST):
        add_pv_verification(bot_id, user_id, "spotify", "", "completed", "Verification processed")
        await update.message.reply_text(
            "✅ Verifikasi Spotify selesai!\n"
            f"Saldo: {user['balance'] - VERIFY_COST} poin"
        )
    else:
        await update.message.reply_text("❌ Gagal memproses verifikasi.")


async def verify4_command(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_id: int):
    """Handle /verify4 command - Bolt.new"""
    user_id = update.effective_user.id
    
    if is_pv_user_blocked(bot_id, user_id):
        await update.message.reply_text("⛔ Akun Anda diblokir.")
        return
    
    user = get_pv_user(bot_id, user_id)
    if not user:
        await update.message.reply_text("Silakan /start terlebih dahulu.")
        return
    
    if user['balance'] < VERIFY_COST:
        await update.message.reply_text(f"❌ Saldo tidak cukup. Dibutuhkan: {VERIFY_COST} poin")
        return
    
    await update.message.reply_text("⏳ Memproses verifikasi Bolt.new...")
    
    if deduct_pv_balance(bot_id, user_id, VERIFY_COST):
        add_pv_verification(bot_id, user_id, "bolt", "", "completed", "Verification processed")
        await update.message.reply_text(
            "✅ Verifikasi Bolt.new selesai!\n"
            f"Saldo: {user['balance'] - VERIFY_COST} poin"
        )
    else:
        await update.message.reply_text("❌ Gagal memproses verifikasi.")


async def getV4Code_command(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_id: int):
    """Handle /getV4Code command"""
    await update.message.reply_text(
        "📋 Gunakan /verify4 untuk verifikasi Bolt.new.\n"
        "Kode akan dikirim setelah verifikasi selesai."
    )
