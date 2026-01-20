"""
Broadcast routes.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import aiohttp
import asyncio

from database import (
    get_bot_by_id, create_broadcast, get_broadcasts_by_bot,
    get_bot_users_for_broadcast
)

broadcast_bp = Blueprint('broadcast', __name__, url_prefix='/api')


async def send_telegram_message(bot_token: str, chat_id: int, text: str) -> bool:
    """Send a message via Telegram Bot API."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                return response.status == 200
    except Exception:
        return False


async def broadcast_messages(bot_token: str, user_ids: list[int], message: str) -> int:
    """Broadcast message to multiple users. Returns success count."""
    success_count = 0
    for user_id in user_ids:
        if await send_telegram_message(bot_token, user_id, message):
            success_count += 1
        await asyncio.sleep(0.05)  # Rate limiting
    return success_count


@broadcast_bp.route('/bots/<int:bot_id>/broadcast', methods=['GET'])
@jwt_required()
def list_broadcasts(bot_id: int):
    """List broadcast history for a bot."""
    user_id = int(get_jwt_identity())
    
    # Verify bot ownership
    bot = get_bot_by_id(bot_id, user_id)
    if not bot:
        return jsonify({'error': 'Bot tidak ditemukan'}), 404
    
    broadcasts = get_broadcasts_by_bot(bot_id)
    
    return jsonify({
        'broadcasts': [{
            'id': b['id'],
            'message': b['message'][:100] + '...' if len(b['message']) > 100 else b['message'],
            'recipients_count': b['recipients_count'],
            'status': b['status'],
            'created_at': b['created_at'].isoformat() if b['created_at'] else None,
        } for b in broadcasts]
    })


@broadcast_bp.route('/bots/<int:bot_id>/broadcast', methods=['POST'])
@jwt_required()
def send_broadcast(bot_id: int):
    """Send a broadcast message to all bot users."""
    user_id = int(get_jwt_identity())
    
    # Verify bot ownership
    bot = get_bot_by_id(bot_id, user_id)
    if not bot:
        return jsonify({'error': 'Bot tidak ditemukan'}), 404
    
    data = request.get_json()
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify({'error': 'Pesan wajib diisi'}), 400
    
    if len(message) > 4096:
        return jsonify({'error': 'Pesan maksimal 4096 karakter'}), 400
    
    # Get all users for this bot
    users = get_bot_users_for_broadcast(bot_id)
    
    if not users:
        return jsonify({'error': 'Tidak ada user untuk broadcast'}), 400
    
    # Create broadcast record
    broadcast = create_broadcast(bot_id, message)
    
    # Send messages
    user_ids = [u['telegram_id'] for u in users]
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    success_count = loop.run_until_complete(
        broadcast_messages(bot['telegram_token'], user_ids, message)
    )
    loop.close()
    
    return jsonify({
        'message': f'Broadcast berhasil dikirim ke {success_count}/{len(users)} user',
        'broadcast': {
            'id': broadcast['id'],
            'recipients_count': success_count,
            'total_users': len(users),
        }
    })
