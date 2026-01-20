"""Points Verify Admin Commands (PostgreSQL version)"""
import os
import asyncio
import secrets
import string
from telegram import Update
from telegram.ext import ContextTypes
from database_pg import (
    get_pv_user, add_pv_balance, block_pv_user, unblock_pv_user,
    get_pv_blacklist, create_pv_card_key, get_pv_card_keys, get_all_pv_user_ids
)

OWNER_TELEGRAM_ID = int(os.getenv("OWNER_TELEGRAM_ID", "0"))


def is_admin(user_id: int) -> bool:
    return user_id == OWNER_TELEGRAM_ID


async def addbalance_command(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_id: int):
    """Handle /addbalance <user_id> <amount>"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Akses ditolak.")
        return
    
    if len(context.args) < 2:
        await update.message.reply_text("Penggunaan: /addbalance <user_id> <jumlah>")
        return
    
    try:
        target_id = int(context.args[0])
        amount = int(context.args[1])
    except ValueError:
        await update.message.reply_text("❌ Format salah.")
        return
    
    if add_pv_balance(bot_id, target_id, amount):
        user = get_pv_user(bot_id, target_id)
        await update.message.reply_text(
            f"✅ Berhasil menambah {amount} poin ke user {target_id}\n"
            f"Saldo baru: {user['balance']} poin"
        )
    else:
        await update.message.reply_text("❌ User tidak ditemukan.")


async def block_command(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_id: int):
    """Handle /block <user_id>"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Akses ditolak.")
        return
    
    if not context.args:
        await update.message.reply_text("Penggunaan: /block <user_id>")
        return
    
    try:
        target_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ User ID harus angka.")
        return
    
    if block_pv_user(bot_id, target_id):
        await update.message.reply_text(f"✅ User {target_id} diblokir.")
    else:
        await update.message.reply_text("❌ User tidak ditemukan.")


async def white_command(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_id: int):
    """Handle /white <user_id> - unblock"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Akses ditolak.")
        return
    
    if not context.args:
        await update.message.reply_text("Penggunaan: /white <user_id>")
        return
    
    try:
        target_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ User ID harus angka.")
        return
    
    if unblock_pv_user(bot_id, target_id):
        await update.message.reply_text(f"✅ User {target_id} di-unblock.")
    else:
        await update.message.reply_text("❌ User tidak ditemukan.")


async def blacklist_command(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_id: int):
    """Handle /blacklist - view blocked users"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Akses ditolak.")
        return
    
    blocked = get_pv_blacklist(bot_id)
    
    if not blocked:
        await update.message.reply_text("📋 Tidak ada user yang diblokir.")
        return
    
    text = f"📋 *Blacklist ({len(blocked)} users)*\n\n"
    for u in blocked[:20]:
        text += f"• {u['telegram_id']} - @{u.get('username', 'N/A')}\n"
    
    await update.message.reply_text(text, parse_mode="Markdown")


async def genkey_command(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_id: int):
    """Handle /genkey <balance> [max_uses] [count]"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Akses ditolak.")
        return
    
    if not context.args:
        await update.message.reply_text(
            "Penggunaan: /genkey <poin> [max_uses] [jumlah]\n"
            "Contoh: /genkey 10 5 3 (3 kode, masing-masing 10 poin, max 5x pakai)"
        )
        return
    
    try:
        balance = int(context.args[0])
        max_uses = int(context.args[1]) if len(context.args) > 1 else 1
        count = int(context.args[2]) if len(context.args) > 2 else 1
        count = min(count, 10)  # Max 10 keys at once
    except ValueError:
        await update.message.reply_text("❌ Format salah.")
        return
    
    keys = []
    for _ in range(count):
        key_code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        if create_pv_card_key(bot_id, key_code, balance, update.effective_user.id, max_uses):
            keys.append(key_code)
    
    if keys:
        text = f"✅ *{len(keys)} Kode Dibuat*\n\n"
        for key in keys:
            text += f"`{key}` ({balance} poin, {max_uses}x)\n"
        await update.message.reply_text(text, parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Gagal membuat kode.")


async def listkeys_command(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_id: int):
    """Handle /listkeys - view all keys"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Akses ditolak.")
        return
    
    keys = get_pv_card_keys(bot_id)
    
    if not keys:
        await update.message.reply_text("📋 Belum ada kode.")
        return
    
    text = f"📋 *Card Keys ({len(keys)})*\n\n"
    for k in keys[:20]:
        status = "✅" if k['current_uses'] < k['max_uses'] else "❌"
        text += f"{status} `{k['key_code']}` - {k['balance']}pts ({k['current_uses']}/{k['max_uses']})\n"
    
    await update.message.reply_text(text, parse_mode="Markdown")


async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_id: int):
    """Handle /broadcast <message>"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Akses ditolak.")
        return
    
    if not context.args:
        await update.message.reply_text("Penggunaan: /broadcast <pesan>")
        return
    
    message = " ".join(context.args)
    user_ids = get_all_pv_user_ids(bot_id)
    
    if not user_ids:
        await update.message.reply_text("Tidak ada user untuk broadcast.")
        return
    
    await update.message.reply_text(f"📢 Mengirim ke {len(user_ids)} users...")
    
    success = 0
    for uid in user_ids:
        try:
            await context.bot.send_message(chat_id=uid, text=f"📢 *Broadcast*\n\n{message}", parse_mode="Markdown")
            success += 1
            await asyncio.sleep(0.05)  # Rate limit
        except Exception:
            pass
    
    await update.message.reply_text(f"✅ Terkirim ke {success}/{len(user_ids)} users.")
