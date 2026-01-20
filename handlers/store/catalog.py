"""
Store Bot - Catalog Handler.
Handles category and product browsing.
"""

from telegram import Update
from telegram.ext import ContextTypes

from database_pg import (
    get_categories_by_bot,
    get_products_by_category,
    get_product_by_id,
    get_category_by_id
)
from utils.keyboard import (
    create_category_keyboard,
    create_product_keyboard,
    create_product_detail_keyboard,
    create_back_keyboard
)


async def show_catalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show catalog categories."""
    query = update.callback_query
    await query.answer()
    
    bot_id = context.bot_data.get('bot_id')
    categories = get_categories_by_bot(bot_id)
    
    if not categories:
        await query.edit_message_text(
            "📭 *Katalog Kosong*\n\nBelum ada kategori produk tersedia.",
            parse_mode="Markdown",
            reply_markup=create_category_keyboard([])
        )
        return
    
    text = (
        "📦 *Katalog Produk*\n\n"
        "Pilih kategori di bawah ini:"
    )
    
    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=create_category_keyboard(categories)
    )


async def show_category_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show products in a category."""
    query = update.callback_query
    await query.answer()
    
    bot_id = context.bot_data.get('bot_id')
    
    # Extract category ID from callback data
    category_id = int(query.data.split("_")[1])
    
    category = get_category_by_id(category_id)
    products = get_products_by_category(category_id, bot_id)
    
    if not category:
        await query.edit_message_text(
            "❌ Kategori tidak ditemukan.",
            reply_markup=create_back_keyboard()
        )
        return
    
    if not products:
        text = f"📁 *{category['name']}*\n\n📭 Tidak ada produk dalam kategori ini."
    else:
        text = (
            f"📁 *{category['name']}*\n"
            f"{category.get('description') or ''}\n\n"
            f"📦 *{len(products)} produk tersedia:*"
        )
    
    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=create_product_keyboard(products, category_id)
    )


async def show_product_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show product detail."""
    query = update.callback_query
    await query.answer()
    
    # Extract product ID from callback data
    product_id = int(query.data.split("_")[1])
    
    product = get_product_by_id(product_id)
    
    if not product:
        await query.edit_message_text(
            "❌ Produk tidak ditemukan.",
            parse_mode="Markdown",
            reply_markup=create_back_keyboard()
        )
        return
    
    # Format price
    price_str = f"Rp {product['price']:,}".replace(",", ".")
    
    # Stock info
    stock = product.get('stock', 0)
    if stock == -1 or stock is None:
        stock_str = "Unlimited"
    elif stock > 0:
        stock_str = f"{stock} tersedia"
    else:
        stock_str = "❌ Stok habis"
    
    text = (
        f"🛍️ *{product['name']}*\n\n"
        f"{product.get('description') or 'Tidak ada deskripsi.'}\n\n"
        f"💰 *Harga:* {price_str}\n"
        f"📦 *Stok:* {stock_str}"
    )
    
    # Check if product is available
    if stock == 0:
        await query.edit_message_text(
            text + "\n\n⚠️ *Maaf, produk ini sedang tidak tersedia.*",
            parse_mode="Markdown",
            reply_markup=create_back_keyboard(f"cat_{product['category_id']}")
        )
        return
    
    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=create_product_detail_keyboard(product_id, product['category_id'])
    )
