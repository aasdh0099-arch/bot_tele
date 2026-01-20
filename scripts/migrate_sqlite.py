"""
Migration Script: SQLite to PostgreSQL

Migrates existing data from SQLite (store.db) to PostgreSQL for multi-bot platform.
"""

import os
import sqlite3
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()


def get_sqlite_connection():
    """Get SQLite connection."""
    db_path = os.path.join(os.path.dirname(__file__), "..", "store.db")
    if not os.path.exists(db_path):
        print(f"❌ SQLite database not found at: {db_path}")
        return None
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def get_pg_connection():
    """Get PostgreSQL connection."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL not set")
        return None
    return psycopg2.connect(database_url)


def migrate():
    """
    Migrate data from SQLite to PostgreSQL.
    
    This script will:
    1. Create a new bot entry for your existing single bot
    2. Migrate all categories to that bot
    3. Migrate all products with their content
    4. Migrate all orders
    5. Migrate all users as bot_users
    """
    print("=" * 50)
    print("🔄 SQLite to PostgreSQL Migration")
    print("=" * 50)
    
    # Get connections
    sqlite_conn = get_sqlite_connection()
    if not sqlite_conn:
        return False
    
    pg_conn = get_pg_connection()
    if not pg_conn:
        return False
    
    pg_cursor = pg_conn.cursor()
    
    try:
        # Step 1: Get or create your user in PostgreSQL
        owner_email = input("📧 Enter your email (for dashboard login): ").strip()
        
        pg_cursor.execute("SELECT id FROM users WHERE email = %s", (owner_email,))
        user_row = pg_cursor.fetchone()
        
        if user_row:
            user_id = user_row[0]
            print(f"✅ Found existing user: {owner_email} (ID: {user_id})")
        else:
            # Create user with default password
            from werkzeug.security import generate_password_hash
            default_password = generate_password_hash("changeme123")
            pg_cursor.execute(
                "INSERT INTO users (email, password_hash, name) VALUES (%s, %s, %s) RETURNING id",
                (owner_email, default_password, "Owner")
            )
            user_id = pg_cursor.fetchone()[0]
            print(f"✅ Created new user: {owner_email} (ID: {user_id})")
            print("⚠️ Default password: changeme123 - please change this!")
        
        # Step 2: Get bot token from old .env or ask user
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not bot_token:
            bot_token = input("🤖 Enter your Telegram bot token: ").strip()
        
        bot_username = input("🏷️ Enter bot username (without @): ").strip()
        bot_name = input("📝 Enter bot display name: ").strip()
        pakasir_slug = os.getenv("PAKASIR_PROJECT_SLUG", "")
        pakasir_key = os.getenv("PAKASIR_API_KEY", "")
        
        # Check if bot already exists
        pg_cursor.execute("SELECT id FROM bots WHERE telegram_token = %s", (bot_token,))
        bot_row = pg_cursor.fetchone()
        
        if bot_row:
            bot_id = bot_row[0]
            print(f"✅ Found existing bot (ID: {bot_id})")
        else:
            pg_cursor.execute(
                """INSERT INTO bots (user_id, telegram_token, bot_username, bot_name, bot_type, pakasir_slug, pakasir_api_key)
                   VALUES (%s, %s, %s, %s, 'store', %s, %s) RETURNING id""",
                (user_id, bot_token, bot_username, bot_name, pakasir_slug, pakasir_key)
            )
            bot_id = pg_cursor.fetchone()[0]
            print(f"✅ Created bot: @{bot_username} (ID: {bot_id})")
        
        pg_conn.commit()
        
        # Step 3: Migrate categories
        print("\n📁 Migrating categories...")
        sqlite_cursor = sqlite_conn.cursor()
        sqlite_cursor.execute("SELECT * FROM categories")
        categories = sqlite_cursor.fetchall()
        
        cat_id_map = {}  # old_id -> new_id
        for cat in categories:
            pg_cursor.execute(
                """INSERT INTO categories (bot_id, name, description, is_active, sort_order)
                   VALUES (%s, %s, %s, %s, %s) RETURNING id""",
                (bot_id, cat['name'], cat['description'], bool(cat['is_active']), cat['sort_order'])
            )
            new_id = pg_cursor.fetchone()[0]
            cat_id_map[cat['id']] = new_id
        
        print(f"   ✅ Migrated {len(categories)} categories")
        pg_conn.commit()
        
        # Step 4: Migrate products
        print("\n📦 Migrating products...")
        sqlite_cursor.execute("SELECT * FROM products")
        products = sqlite_cursor.fetchall()
        
        prod_id_map = {}  # old_id -> new_id
        for prod in products:
            new_cat_id = cat_id_map.get(prod['category_id'])
            pg_cursor.execute(
                """INSERT INTO products (bot_id, category_id, name, description, price, content_type, is_active)
                   VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id""",
                (bot_id, new_cat_id, prod['name'], prod['description'], prod['price'],
                 prod['content_type'], bool(prod['is_active']))
            )
            new_prod_id = pg_cursor.fetchone()[0]
            prod_id_map[prod['id']] = new_prod_id
            
            # Add product content as stock if it exists
            if prod['content']:
                pg_cursor.execute(
                    "INSERT INTO product_stock (product_id, content) VALUES (%s, %s)",
                    (new_prod_id, prod['content'])
                )
        
        print(f"   ✅ Migrated {len(products)} products")
        pg_conn.commit()
        
        # Step 5: Migrate users as bot_users
        print("\n👥 Migrating users...")
        sqlite_cursor.execute("SELECT * FROM users")
        users = sqlite_cursor.fetchall()
        
        user_id_map = {}  # old_id -> new_bot_user_id
        for u in users:
            pg_cursor.execute(
                """INSERT INTO bot_users (bot_id, telegram_id, username, first_name)
                   VALUES (%s, %s, %s, %s) RETURNING id""",
                (bot_id, u['telegram_id'], u['username'], u['first_name'])
            )
            new_id = pg_cursor.fetchone()[0]
            user_id_map[u['id']] = new_id
        
        print(f"   ✅ Migrated {len(users)} users")
        pg_conn.commit()
        
        # Step 6: Migrate orders
        print("\n📋 Migrating orders...")
        sqlite_cursor.execute("SELECT * FROM orders")
        orders = sqlite_cursor.fetchall()
        
        for order in orders:
            new_prod_id = prod_id_map.get(order['product_id'])
            new_user_id = user_id_map.get(order['user_id'])
            
            if new_prod_id and new_user_id:
                pg_cursor.execute(
                    """INSERT INTO orders (bot_id, bot_user_id, product_id, order_id, amount, fee, total, status, payment_method, qris_string, paid_at, created_at)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (bot_id, new_user_id, new_prod_id, order['order_id'], order['amount'],
                     order['fee'], order['total'], order['status'], order['payment_method'],
                     order['qris_string'], order['paid_at'], order['created_at'])
                )
        
        print(f"   ✅ Migrated {len(orders)} orders")
        pg_conn.commit()
        
        print("\n" + "=" * 50)
        print("✅ Migration completed successfully!")
        print("=" * 50)
        print(f"\n📊 Summary:")
        print(f"   • Bot ID: {bot_id}")
        print(f"   • Categories: {len(categories)}")
        print(f"   • Products: {len(products)}")
        print(f"   • Users: {len(users)}")
        print(f"   • Orders: {len(orders)}")
        print(f"\n💡 You can now run the multi-bot platform with: python main.py")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        pg_conn.rollback()
        return False
    finally:
        sqlite_conn.close()
        pg_conn.close()


if __name__ == "__main__":
    migrate()
