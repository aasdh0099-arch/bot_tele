# API Backend

Backend API untuk BotStore platform menggunakan Flask.

## Setup

1. Install dependencies:

```bash
cd api
pip install -r requirements.txt
```

2. Setup environment variables di `.env`:

```
DATABASE_URL=postgresql://...@...neon.tech/...
JWT_SECRET_KEY=your-secret-key-here
```

3. Run server:

```bash
python app.py
```

## Endpoints

### Auth

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Bots

- `GET /api/bots` - List user's bots
- `POST /api/bots` - Create new bot
- `GET /api/bots/:id` - Get bot details
- `PUT /api/bots/:id` - Update bot
- `DELETE /api/bots/:id` - Delete bot

### Products

- `GET /api/bots/:botId/products` - List products
- `POST /api/bots/:botId/products` - Create product
- `PUT /api/products/:id` - Update product
- `DELETE /api/products/:id` - Delete product

### Transactions

- `GET /api/bots/:botId/transactions` - List transactions

### Broadcast

- `POST /api/bots/:botId/broadcast` - Send broadcast
