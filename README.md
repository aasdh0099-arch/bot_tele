# Multi-Bot Telegram Platform

Platform untuk menjalankan dan mengelola multiple Telegram bot dari satu server.

## 🤖 Bot Types

| Type            | Description                                 |
| --------------- | ------------------------------------------- |
| `store`         | Digital store dengan QRIS payment (Pakasir) |
| `verification`  | Verifikasi mahasiswa/member sederhana       |
| `points_verify` | Verifikasi dengan sistem poin (MySQL)       |
| `custom`        | Template kosong untuk bot custom            |

## 📁 Folder Structure

```
bot_tele/
├── api/                    # Flask API backend
├── web/                    # Next.js web dashboard
├── handlers/               # Bot type handlers
│   ├── store/              # Store bot
│   ├── verification/       # Simple verification
│   ├── points_verify/      # Points verification
│   └── custom/             # Custom template
├── scripts/                # Migration scripts
├── services/               # External services (Pakasir)
├── utils/                  # Shared utilities
├── webhook/                # Webhook handlers
├── bot_manager.py          # Multi-bot orchestrator
├── bot_instance.py         # Single bot wrapper
├── database_pg.py          # PostgreSQL (store/verification)
├── database_mysql.py       # MySQL (points_verify)
├── main.py                 # Entry point
└── requirements.txt        # Dependencies
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Update Database Schema

```bash
python scripts/update_schema.py
```

### 4. Add Bots via Dashboard

- Start API: `cd api && python app.py`
- Start Web: `cd web && npm run dev`
- Login and add bots with their tokens

### 5. Run Bots

```bash
python main.py
```

## ⚙️ Configuration

### .env Variables

```env
# Database (PostgreSQL - Neon)
DATABASE_URL=postgresql://...

# Owner Telegram ID (admin access)
OWNER_TELEGRAM_ID=123456789

# MySQL (for points_verify bot type)
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=password
MYSQL_DATABASE=verify
```

## 📝 License

Private use only.
