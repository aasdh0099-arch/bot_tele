"""
Pakasir API Client for QRIS payment integration.
Supports per-bot configuration for multi-bot platform.
"""

import aiohttp
from typing import Optional
from dataclasses import dataclass


PAKASIR_API_BASE_URL = "https://app.pakasir.com/api"


@dataclass
class PaymentResponse:
    """Response from creating a payment."""
    project: str
    order_id: str
    amount: int
    fee: int
    total_payment: int
    payment_method: str
    payment_number: str  # QRIS string
    expired_at: str


@dataclass
class TransactionStatus:
    """Transaction status response."""
    order_id: str
    amount: int
    status: str  # 'pending', 'completed', etc.
    payment_method: str
    completed_at: Optional[str] = None


class PakasirClient:
    """Pakasir API client for payment operations."""
    
    def __init__(self, project_slug: str = None, api_key: str = None):
        """
        Initialize Pakasir client.
        
        Args:
            project_slug: Pakasir project slug (per-bot)
            api_key: Pakasir API key (per-bot)
        """
        self.base_url = PAKASIR_API_BASE_URL
        self.project = project_slug or ""
        self.api_key = api_key or ""
    
    async def create_transaction(
        self, 
        order_id: str, 
        amount: int,
        payment_method: str = "qris"
    ) -> Optional[PaymentResponse]:
        """
        Create a new payment transaction.
        
        Args:
            order_id: Unique order identifier
            amount: Payment amount in IDR (without fee)
            payment_method: Payment method (qris, bni_va, bri_va, etc.)
        
        Returns:
            PaymentResponse with QRIS string and payment details
        """
        if not self.project or not self.api_key:
            print("❌ Pakasir not configured for this bot")
            return None
        
        url = f"{self.base_url}/transactioncreate/{payment_method}"
        payload = {
            "project": self.project,
            "order_id": order_id,
            "amount": amount,
            "api_key": self.api_key
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        payment = data.get("payment", {})
                        return PaymentResponse(
                            project=payment.get("project", ""),
                            order_id=payment.get("order_id", ""),
                            amount=payment.get("amount", 0),
                            fee=payment.get("fee", 0),
                            total_payment=payment.get("total_payment", 0),
                            payment_method=payment.get("payment_method", ""),
                            payment_number=payment.get("payment_number", ""),
                            expired_at=payment.get("expired_at", "")
                        )
                    else:
                        error_text = await response.text()
                        print(f"❌ Pakasir API error: {response.status} - {error_text}")
                        return None
            except Exception as e:
                print(f"❌ Pakasir API exception: {e}")
                return None
    
    async def get_transaction_status(
        self, 
        order_id: str, 
        amount: int
    ) -> Optional[TransactionStatus]:
        """
        Get the status of a transaction.
        
        Args:
            order_id: Order identifier
            amount: Original transaction amount
        
        Returns:
            TransactionStatus with current status
        """
        if not self.project or not self.api_key:
            return None
        
        url = f"{self.base_url}/transactiondetail"
        params = {
            "project": self.project,
            "order_id": order_id,
            "amount": amount,
            "api_key": self.api_key
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        tx = data.get("transaction", {})
                        return TransactionStatus(
                            order_id=tx.get("order_id", ""),
                            amount=tx.get("amount", 0),
                            status=tx.get("status", ""),
                            payment_method=tx.get("payment_method", ""),
                            completed_at=tx.get("completed_at")
                        )
                    else:
                        return None
            except Exception as e:
                print(f"❌ Pakasir status check error: {e}")
                return None
    
    async def cancel_transaction(self, order_id: str, amount: int) -> bool:
        """
        Cancel a pending transaction.
        
        Args:
            order_id: Order identifier
            amount: Original transaction amount
        
        Returns:
            True if cancelled successfully
        """
        if not self.project or not self.api_key:
            return False
        
        url = f"{self.base_url}/transactioncancel"
        payload = {
            "project": self.project,
            "order_id": order_id,
            "amount": amount,
            "api_key": self.api_key
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload) as response:
                    return response.status == 200
            except Exception as e:
                print(f"❌ Pakasir cancel error: {e}")
                return False
    
    async def simulate_payment(self, order_id: str, amount: int) -> bool:
        """
        Simulate a payment (only works in sandbox mode).
        
        Args:
            order_id: Order identifier
            amount: Transaction amount
        
        Returns:
            True if simulation successful
        """
        if not self.project or not self.api_key:
            return False
        
        url = f"{self.base_url}/paymentsimulation"
        payload = {
            "project": self.project,
            "order_id": order_id,
            "amount": amount,
            "api_key": self.api_key
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload) as response:
                    return response.status == 200
            except Exception as e:
                print(f"❌ Pakasir simulation error: {e}")
                return False
