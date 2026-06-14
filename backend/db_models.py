from datetime import datetime
from enum import Enum
from typing import List, Literal, Optional
from beanie import Document, Link
from click import Option
from pydantic import BaseModel, EmailStr, Field


class CustomerTier(str, Enum):
    standard = "standard"
    premium = "premium"
    vip = "vip"


class OrderStatus(str, Enum):
    delivered = "delivered"
    shipped = "shipped"
    cancelled = "cancelled"
    refunded = "refunded"


class ProductCategory(str, Enum):
    electronics = "electronics"
    accessories = "accessories"
    software = "software"
    final_sale = "final_sale"

refund_decision = Literal["approved", "denied", "escalate"]

class ProductItem(BaseModel):
    sku: str
    name: str
    category: ProductCategory
    price: float
    quantity: int = 1
    final_sale: bool = False
    opened: bool = False
    damaged_by_customer: bool = False
    
class RefundDecision(BaseModel):
    decision: Optional[refund_decision] = None  # approved, denied, escalate
    reason: str = ''
    refund_amount: Optional[float] = None
    requires_human_review: bool = False

class Customer(Document):
    name: str
    email: str
    tier: CustomerTier
    account_created_at: datetime
    is_flagged_for_abuse: bool = False
    notes: Optional[str] = None

    class Settings:
        name = "customers"

class Order(Document):
    order_number: str
    customer_email: EmailStr
    customer: Link[Customer]
    items: List[ProductItem]
    status: OrderStatus
    order_date: datetime
    delivery_date: Optional[datetime] = None
    purchased_during_black_november: bool = False
    payment_method: str
    refund_requested: bool = False
    refund_decision: Optional[RefundDecision]

    class Settings:
        name = "orders"