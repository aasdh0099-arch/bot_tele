"""
Store Bot - Admin Handler.
Handles admin operations for store management.
"""

import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from database_pg import (
    get_categories_by_bot,
    get_category_by_id,
    create_category,
    update_category,
    delete_category,
    get_products_by_bot,
    get_product_by_id,
    create_product,
    update_product,
    delete_product,
    get_orders_by_bot,
    get_bot_stats,
    add_stock_items
)
from utils.keyboard import create_back_keyboard

# Conversation states
CAT_NAME, CAT_DESC = range(2)
PROD_NAME, PROD_DESC, PROD_PRICE, PROD_CONTENT, PROD_CATEGORY = range(2, 7)

# Owner check
OWNER_TELEGRAM_ID = int(os.getenv("OWNER_TELEGRAM_ID", "0"))


def is_owner(user_id: int) -> bool:
    """Check if user is the owner."""
    return user_id == OWNER_TELEGRAM_ID


async def admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show admin panel menu."""
    query = update.callback_query
    await query.answer()
    
    if not is_owner(update.effective_user.id):
        await query.edit_message_text("⛔ Akses ditolak.")
        return
    
    keyboard = [
        [InlineKeyboardButton("📁 Kategori", callback_data="admin_categories"),
         InlineKeyboardButton("📦 Produk", callback_data="admin_products")],
        [InlineKeyboardButton("📋 Pesanan", callback_data="admin_orders"),
         InlineKeyboardButton("📊 Statistik", callback_data="admin_stats")],
        [InlineKeyboardButton("◀️ Kembali", callback_data="back_menu")]
    ]
    
    await query.edit_message_text(
        "🔧 *Panel Admin*\n\nPilih menu untuk mengelola toko:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ==================== CATEGORY MANAGEMENT ====================

async def admin_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show category management."""
    query = update.callback_query
    await query.answer()
    
    if not is_owner(update.effective_user.id):
        return
    
    bot_id = context.bot_data.get('bot_id')
    categories = get_categories_by_bot(bot_id, active_only=False)
    
    keyboard = []
    for cat in categories:
        status = "✅" if cat['is_active'] else "❌"
        keyboard.append([InlineKeyboardButton(
            f"{status} {cat['name']}", 
            callback_data=f"admin_cat_{cat['id']}"
        )])
    
    keyboard.append([InlineKeyboardButton("➕ Tambah Kategori", callback_data="admin_cat_add")])
    keyboard.append([InlineKeyboardButton("◀️ Kembali", callback_data="menu_admin")])
    
    await query.edit_message_text(
        "📁 *Manajemen Kategori*\n\nPilih kategori untuk mengelola:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def admin_category_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show category detail."""
    query = update.callback_query
    await query.answer()
    
    if not is_owner(update.effective_user.id):
        return
    
    category_id = int(query.data.split("_")[2])
    category = get_category_by_id(category_id)
    
    if not category:
        await query.edit_message_text("❌ Kategori tidak ditemukan.")
        return
    
    status = "Aktif ✅" if category['is_active'] else "Nonaktif ❌"
    text = (
        f"📁 *{category['name']}*\n\n"
        f"📝 {category.get('description') or 'Tidak ada deskripsi'}\n"
        f"📊 Status: {status}"
    )
    
    toggle_text = "❌ Nonaktifkan" if category['is_active'] else "✅ Aktifkan"
    keyboard = [
        [InlineKeyboardButton(toggle_text, callback_data=f"admin_cat_toggle_{category_id}")],
        [InlineKeyboardButton("🗑️ Hapus", callback_data=f"admin_cat_del_{category_id}")],
        [InlineKeyboardButton("◀️ Kembali", callback_data="admin_categories")]
    ]
    
    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def admin_category_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Toggle category status."""
    query = update.callback_query
    await query.answer()
    
    if not is_owner(update.effective_user.id):
        return
    
    category_id = int(query.data.split("_")[3])
    category = get_category_by_id(category_id)
    
    if category:
        new_status = not category['is_active']
        update_category(category_id, is_active=new_status)
    
    # Redirect back to detail
    query.data = f"admin_cat_{category_id}"
    await admin_category_detail(update, context)


async def admin_category_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete a category."""
    query = update.callback_query
    await query.answer("🗑️ Kategori dihapus")
    
    if not is_owner(update.effective_user.id):
        return
    
    category_id = int(query.data.split("_")[3])
    delete_category(category_id)
    
    await admin_categories(update, context)


async def admin_category_add_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start adding new category."""
    query = update.callback_query
    await query.answer()
    
    if not is_owner(update.effective_user.id):
        return ConversationHandler.END
    
    keyboard = [[InlineKeyboardButton("❌ Batal", callback_data="admin_cancel")]]
    
    await query.edit_message_text(
        "📁 *Tambah Kategori Baru*\n\nMasukkan nama kategori:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    return CAT_NAME


async def admin_category_add_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive category name."""
    context.user_data['new_cat_name'] = update.message.text
    
    keyboard = [[InlineKeyboardButton("❌ Batal", callback_data="admin_cancel")]]
    
    await update.message.reply_text(
        "📝 Masukkan deskripsi kategori (atau ketik '-' untuk skip):",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    return CAT_DESC


async def admin_category_add_desc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive category description and create."""
    bot_id = context.bot_data.get('bot_id')
    name = context.user_data.get('new_cat_name')
    desc = update.message.text if update.message.text != '-' else None
    
    create_category(bot_id, name, desc)
    
    await update.message.reply_text(
        f"✅ Kategori *{name}* berhasil ditambahkan!",
        parse_mode="Markdown",
        reply_markup=create_back_keyboard("admin_categories")
    )
    
    return ConversationHandler.END


# ==================== PRODUCT MANAGEMENT ====================

async def admin_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show product management."""
    query = update.callback_query
    await query.answer()
    
    if not is_owner(update.effective_user.id):
        return
    
    bot_id = context.bot_data.get('bot_id')
    products = get_products_by_bot(bot_id, active_only=False)
    
    keyboard = []
    for prod in products:
        status = "✅" if prod['is_active'] else "❌"
        stock = prod.get('stock', 0)
        keyboard.append([InlineKeyboardButton(
            f"{status} {prod['name']} [{stock}]",
            callback_data=f"admin_prod_{prod['id']}"
        )])
    
    keyboard.append([InlineKeyboardButton("➕ Tambah Produk", callback_data="admin_prod_add")])
    keyboard.append([InlineKeyboardButton("◀️ Kembali", callback_data="menu_admin")])
    
    await query.edit_message_text(
        "📦 *Manajemen Produk*\n\nPilih produk untuk mengelola:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def admin_product_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show product detail."""
    query = update.callback_query
    await query.answer()
    
    if not is_owner(update.effective_user.id):
        return
    
    product_id = int(query.data.split("_")[2])
    product = get_product_by_id(product_id)
    
    if not product:
        await query.edit_message_text("❌ Produk tidak ditemukan.")
        return
    
    status = "Aktif ✅" if product['is_active'] else "Nonaktif ❌"
    price_str = f"Rp {product['price']:,}".replace(",", ".")
    stock = product.get('stock', 0)
    
    text = (
        f"📦 *{product['name']}*\n\n"
        f"📝 {product.get('description') or 'Tidak ada deskripsi'}\n"
        f"💰 Harga: {price_str}\n"
        f"📊 Status: {status}\n"
        f"📦 Stok: {stock}"
    )
    
    toggle_text = "❌ Nonaktifkan" if product['is_active'] else "✅ Aktifkan"
    keyboard = [
        [InlineKeyboardButton(toggle_text, callback_data=f"admin_prod_toggle_{product_id}")],
        [InlineKeyboardButton("🗑️ Hapus", callback_data=f"admin_prod_del_{product_id}")],
        [InlineKeyboardButton("◀️ Kembali", callback_data="admin_products")]
    ]
    
    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def admin_product_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Toggle product status."""
    query = update.callback_query
    await query.answer()
    
    if not is_owner(update.effective_user.id):
        return
    
    product_id = int(query.data.split("_")[3])
    product = get_product_by_id(product_id)
    
    if product:
        new_status = not product['is_active']
        update_product(product_id, is_active=new_status)
    
    query.data = f"admin_prod_{product_id}"
    await admin_product_detail(update, context)


async def admin_product_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete a product."""
    query = update.callback_query
    await query.answer("🗑️ Produk dihapus")
    
    if not is_owner(update.effective_user.id):
        return
    
    product_id = int(query.data.split("_")[3])
    delete_product(product_id)
    
    await admin_products(update, context)


async def admin_product_add_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start adding new product."""
    query = update.callback_query
    await query.answer()
    
    if not is_owner(update.effective_user.id):
        return ConversationHandler.END
    
    bot_id = context.bot_data.get('bot_id')
    categories = get_categories_by_bot(bot_id)
    
    if not categories:
        await query.edit_message_text(
            "❌ Tidak ada kategori. Buat kategori terlebih dahulu.",
            reply_markup=create_back_keyboard("admin_products")
        )
        return ConversationHandler.END
    
    keyboard = []
    for cat in categories:
        keyboard.append([InlineKeyboardButton(
            cat['name'],
            callback_data=f"addprod_cat_{cat['id']}"
        )])
    keyboard.append([InlineKeyboardButton("❌ Batal", callback_data="admin_cancel")])
    
    await query.edit_message_text(
        "📦 *Tambah Produk Baru*\n\nPilih kategori produk:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    return PROD_CATEGORY


async def admin_product_select_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive category selection."""
    query = update.callback_query
    await query.answer()
    
    category_id = int(query.data.split("_")[2])
    context.user_data['new_prod_cat'] = category_id
    
    keyboard = [[InlineKeyboardButton("❌ Batal", callback_data="admin_cancel")]]
    
    await query.edit_message_text(
        "📝 Masukkan nama produk:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    return PROD_NAME


async def admin_product_add_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive product name."""
    context.user_data['new_prod_name'] = update.message.text
    
    keyboard = [[InlineKeyboardButton("❌ Batal", callback_data="admin_cancel")]]
    
    await update.message.reply_text(
        "📝 Masukkan deskripsi produk (atau '-' untuk skip):",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    return PROD_DESC


async def admin_product_add_desc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive product description."""
    context.user_data['new_prod_desc'] = update.message.text if update.message.text != '-' else None
    
    keyboard = [[InlineKeyboardButton("❌ Batal", callback_data="admin_cancel")]]
    
    await update.message.reply_text(
        "💰 Masukkan harga produk (angka saja, contoh: 15000):",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    return PROD_PRICE


async def admin_product_add_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive product price."""
    try:
        price = int(update.message.text.replace(".", "").replace(",", ""))
        context.user_data['new_prod_price'] = price
    except ValueError:
        await update.message.reply_text("❌ Harga tidak valid. Masukkan angka saja:")
        return PROD_PRICE
    
    keyboard = [[InlineKeyboardButton("❌ Batal", callback_data="admin_cancel")]]
    
    await update.message.reply_text(
        "📦 Masukkan stok produk (satu item per baris):\n\n"
        "Contoh:\n"
        "akun1@email.com:pass123\n"
        "akun2@email.com:pass456",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    return PROD_CONTENT


async def admin_product_add_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive product content and create."""
    bot_id = context.bot_data.get('bot_id')
    
    name = context.user_data.get('new_prod_name')
    desc = context.user_data.get('new_prod_desc')
    price = context.user_data.get('new_prod_price')
    category_id = context.user_data.get('new_prod_cat')
    stock_items = update.message.text.strip().split('\n')
    
    # Create product
    product = create_product(bot_id, category_id, name, price, desc)
    
    # Add stock items
    if stock_items and stock_items[0]:
        add_stock_items(product['id'], stock_items)
    
    await update.message.reply_text(
        f"✅ Produk *{name}* berhasil ditambahkan!\n"
        f"📦 {len(stock_items)} stok ditambahkan.",
        parse_mode="Markdown",
        reply_markup=create_back_keyboard("admin_products")
    )
    
    # Clear user data
    context.user_data.pop('new_prod_name', None)
    context.user_data.pop('new_prod_desc', None)
    context.user_data.pop('new_prod_price', None)
    context.user_data.pop('new_prod_cat', None)
    
    return ConversationHandler.END


async def admin_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel admin operation."""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "❌ Operasi dibatalkan.",
        reply_markup=create_back_keyboard("menu_admin")
    )
    
    return ConversationHandler.END


# ==================== ORDERS & STATS ====================

async def admin_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show recent orders."""
    query = update.callback_query
    await query.answer()
    
    if not is_owner(update.effective_user.id):
        return
    
    bot_id = context.bot_data.get('bot_id')
    orders = get_orders_by_bot(bot_id, limit=20)
    
    if not orders:
        await query.edit_message_text(
            "📋 *Pesanan*\n\n📭 Belum ada pesanan.",
            parse_mode="Markdown",
            reply_markup=create_back_keyboard("menu_admin")
        )
        return
    
    status_emoji = {"pending": "⏳", "paid": "✅", "cancelled": "❌", "expired": "⌛"}
    
    text = "📋 *Pesanan Terbaru*\n\n"
    for order in orders[:10]:
        emoji = status_emoji.get(order['status'], "❓")
        amount_str = f"Rp {order['amount']:,}".replace(",", ".")
        text += f"{emoji} `{order['order_id']}`\n"
        text += f"   📦 {order.get('product_name', 'N/A')} | {amount_str}\n\n"
    
    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=create_back_keyboard("menu_admin")
    )


async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show bot statistics."""
    query = update.callback_query
    await query.answer()
    
    if not is_owner(update.effective_user.id):
        return
    
    bot_id = context.bot_data.get('bot_id')
    stats = get_bot_stats(bot_id)
    
    revenue_str = f"Rp {stats['total_revenue']:,}".replace(",", ".")
    
    text = (
        "📊 *Statistik Toko*\n\n"
        f"📦 Produk: {stats['total_products']}\n"
        f"👥 User: {stats['total_users']}\n"
        f"🛒 Pesanan: {stats['total_orders']}\n"
        f"💰 Total Revenue: {revenue_str}"
    )
    
    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=create_back_keyboard("menu_admin")
    )
