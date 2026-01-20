"""
Bot Manager Module.
Orchestrates multiple bot instances from the database.
"""

import asyncio
import logging
import signal
import sys
from typing import Dict, Optional

from database_pg import get_active_bots, get_bot_by_id
from bot_instance import BotInstance

logger = logging.getLogger(__name__)


class BotManager:
    """Manages multiple Telegram bot instances."""
    
    def __init__(self):
        self.bots: Dict[int, BotInstance] = {}
        self._running = False
        self._shutdown_event = asyncio.Event()
    
    def load_bots(self) -> int:
        """
        Load all active bots from database.
        
        Returns:
            Number of bots loaded
        """
        active_bots = get_active_bots()
        
        for bot_config in active_bots:
            try:
                instance = BotInstance(bot_config)
                self.bots[bot_config['id']] = instance
                logger.info(f"Loaded bot: {instance}")
            except Exception as e:
                logger.error(f"Failed to load bot {bot_config.get('id')}: {e}")
        
        return len(self.bots)
    
    def add_bot(self, bot_id: int) -> Optional[BotInstance]:
        """
        Add and start a single bot by ID.
        
        Args:
            bot_id: Database ID of the bot
            
        Returns:
            BotInstance if successful, None otherwise
        """
        if bot_id in self.bots:
            logger.warning(f"Bot {bot_id} already running")
            return self.bots[bot_id]
        
        bot_config = get_bot_by_id(bot_id)
        if not bot_config:
            logger.error(f"Bot {bot_id} not found in database")
            return None
        
        try:
            instance = BotInstance(bot_config)
            self.bots[bot_id] = instance
            return instance
        except Exception as e:
            logger.error(f"Failed to create bot {bot_id}: {e}")
            return None
    
    async def start_bot(self, bot_id: int) -> bool:
        """Start a specific bot."""
        if bot_id not in self.bots:
            instance = self.add_bot(bot_id)
            if not instance:
                return False
        
        try:
            await self.bots[bot_id].start()
            return True
        except Exception as e:
            logger.error(f"Failed to start bot {bot_id}: {e}")
            return False
    
    async def stop_bot(self, bot_id: int) -> bool:
        """Stop a specific bot."""
        if bot_id not in self.bots:
            logger.warning(f"Bot {bot_id} not found")
            return False
        
        try:
            await self.bots[bot_id].stop()
            del self.bots[bot_id]
            return True
        except Exception as e:
            logger.error(f"Failed to stop bot {bot_id}: {e}")
            return False
    
    async def restart_bot(self, bot_id: int) -> bool:
        """Restart a specific bot."""
        await self.stop_bot(bot_id)
        return await self.start_bot(bot_id)
    
    async def start_all(self):
        """Start all loaded bots concurrently."""
        if not self.bots:
            logger.warning("No bots to start")
            return
        
        tasks = [bot.start() for bot in self.bots.values()]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for bot_id, result in zip(self.bots.keys(), results):
            if isinstance(result, Exception):
                logger.error(f"Bot {bot_id} failed to start: {result}")
    
    async def stop_all(self):
        """Stop all running bots."""
        tasks = [bot.stop() for bot in self.bots.values()]
        await asyncio.gather(*tasks, return_exceptions=True)
        self.bots.clear()
    
    async def run(self):
        """
        Main run loop - starts all bots and waits for shutdown signal.
        """
        self._running = True
        
        # Setup signal handlers
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, lambda: asyncio.create_task(self._shutdown()))
            except NotImplementedError:
                # Windows doesn't support add_signal_handler
                pass
        
        print("=" * 50)
        print("🤖 Multi-Bot Platform")
        print("=" * 50)
        
        # Load bots
        count = self.load_bots()
        print(f"\n📦 Loaded {count} bot(s) from database")
        
        if count == 0:
            print("⚠️ No active bots found. Add bots via the web dashboard.")
            return
        
        # Start all bots
        print("\n🚀 Starting all bots...")
        await self.start_all()
        
        print("\n" + "=" * 50)
        print("All bots running! Press Ctrl+C to stop.")
        print("=" * 50)
        
        # Wait for shutdown
        try:
            await self._shutdown_event.wait()
        except asyncio.CancelledError:
            pass
        
        print("\n🛑 Shutting down...")
        await self.stop_all()
        print("👋 All bots stopped. Goodbye!")
    
    async def _shutdown(self):
        """Trigger shutdown."""
        self._running = False
        self._shutdown_event.set()
    
    def get_status(self) -> dict:
        """Get status of all bots."""
        return {
            "running": self._running,
            "bot_count": len(self.bots),
            "bots": [
                {
                    "id": b.bot_id,
                    "username": b.bot_username,
                    "name": b.bot_name,
                    "type": b.bot_type
                }
                for b in self.bots.values()
            ]
        }
