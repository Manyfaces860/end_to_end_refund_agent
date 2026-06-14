from datetime import datetime, timedelta, timezone
from db_models import *
from typing import cast

NOW = datetime(2026, datetime.today().month, datetime.today().day, tzinfo=timezone.utc)

CUSTOMERS = [
    {
        "name": "Riya Sharma",
        "email": "riya@example.com",
        "tier": CustomerTier.standard,
        "account_created_at": NOW - timedelta(days=300),
        "is_flagged_for_abuse": False,
        "notes": "Normal customer."
    },
    {
        "name": "James Miller",
        "email": "james@example.com",
        "tier": CustomerTier.premium,
        "account_created_at": NOW - timedelta(days=700),
        "is_flagged_for_abuse": False,
        "notes": "Premium member."
    },
    {
        "name": "Aisha Khan",
        "email": "aisha@example.com",
        "tier": CustomerTier.standard,
        "account_created_at": NOW - timedelta(days=120),
        "is_flagged_for_abuse": True,
        "notes": "Requires additional review."
    },
    {
        "name": "Leo Carter",
        "email": "leo@example.com",
        "tier": CustomerTier.vip,
        "account_created_at": NOW - timedelta(days=1500),
        "is_flagged_for_abuse": False,
        "notes": "VIP customer."
    },
    {
        "name": "Maya Chen",
        "email": "maya@example.com",
        "tier": CustomerTier.standard,
        "account_created_at": NOW - timedelta(days=40),
        "is_flagged_for_abuse": False,
        "notes": "New customer."
    },
    {
        "name": "David Brown",
        "email": "david@example.com",
        "tier": CustomerTier.standard,
        "account_created_at": NOW - timedelta(days=520),
        "is_flagged_for_abuse": False,
        "notes": None
    },
    {
        "name": "Emma Wilson",
        "email": "emma@example.com",
        "tier": CustomerTier.premium,
        "account_created_at": NOW - timedelta(days=910),
        "is_flagged_for_abuse": False,
        "notes": None
    },
    {
        "name": "Noah Taylor",
        "email": "noah@example.com",
        "tier": CustomerTier.standard,
        "account_created_at": NOW - timedelta(days=210),
        "is_flagged_for_abuse": False,
        "notes": None
    },
    {
        "name": "Sophia Martinez",
        "email": "sophia@example.com",
        "tier": CustomerTier.vip,
        "account_created_at": NOW - timedelta(days=1100),
        "is_flagged_for_abuse": False,
        "notes": None
    },
    {
        "name": "Liam Anderson",
        "email": "liam@example.com",
        "tier": CustomerTier.standard,
        "account_created_at": NOW - timedelta(days=80),
        "is_flagged_for_abuse": False,
        "notes": None
    },
    {
        "name": "Olivia Thomas",
        "email": "olivia@example.com",
        "tier": CustomerTier.standard,
        "account_created_at": NOW - timedelta(days=180),
        "is_flagged_for_abuse": False,
        "notes": None
    },
    {
        "name": "William Jackson",
        "email": "william@example.com",
        "tier": CustomerTier.premium,
        "account_created_at": NOW - timedelta(days=400),
        "is_flagged_for_abuse": False,
        "notes": None
    },
    {
        "name": "Isabella White",
        "email": "isabella@example.com",
        "tier": CustomerTier.standard,
        "account_created_at": NOW - timedelta(days=250),
        "is_flagged_for_abuse": False,
        "notes": None
    },
    {
        "name": "Benjamin Harris",
        "email": "ben@example.com",
        "tier": CustomerTier.standard,
        "account_created_at": NOW - timedelta(days=600),
        "is_flagged_for_abuse": False,
        "notes": None
    },
    {
        "name": "Charlotte Young",
        "email": "charlotte@example.com",
        "tier": CustomerTier.vip,
        "account_created_at": NOW - timedelta(days=1300),
        "is_flagged_for_abuse": False,
        "notes": None
    },
]

ORDERS = [
    # Normal refund approval
    {
        "order_number": "ORD-1001",
        "customer_email": "riya@example.com",
        "items": [
            {
                "sku": "AG-WATCH-PRO",
                "name": "AuraPulse Pro Smartwatch",
                "category": ProductCategory.electronics,
                "price": 299.00,
            }
        ],
        "status": OrderStatus.delivered,
        "order_date": NOW - timedelta(days=10),
        "delivery_date": NOW - timedelta(days=7),
        "payment_method": "card"
    },

    # Black November
    {
        "order_number": "ORD-1002",
        "customer_email": "james@example.com",
        "items": [
            {
                "sku": "AG-EARBUDS-LITE",
                "name": "AuraBuds Lite",
                "category": ProductCategory.electronics,
                "price": 89.00,
                "opened": True
            }
        ],
        "status": OrderStatus.delivered,
        "order_date": NOW - timedelta(days=42),
        "delivery_date": NOW - timedelta(days=39),
        "purchased_during_black_november": True,
        "payment_method": "card"
    },

    # Outside refund window
    {
        "order_number": "ORD-1003",
        "customer_email": "david@example.com",
        "items": [
            {
                "sku": "AG-STAND",
                "name": "AuraDesk Laptop Stand",
                "category": ProductCategory.accessories,
                "price": 59.00,
            }
        ],
        "status": OrderStatus.delivered,
        "order_date": NOW - timedelta(days=40),
        "delivery_date": NOW - timedelta(days=35),
        "payment_method": "paypal"
    },

    # Opened software
    {
        "order_number": "ORD-1004",
        "customer_email": "emma@example.com",
        "items": [
            {
                "sku": "AG-SOFTWARE",
                "name": "AuraStudio Pro License",
                "category": ProductCategory.software,
                "price": 199.00,
                "opened": True
            }
        ],
        "status": OrderStatus.delivered,
        "order_date": NOW - timedelta(days=5),
        "delivery_date": NOW - timedelta(days=5),
        "payment_method": "card"
    },

    # Flagged customer
    {
        "order_number": "ORD-1005",
        "customer_email": "aisha@example.com",
        "items": [
            {
                "sku": "AG-HEADPHONE",
                "name": "AuraSound Max",
                "category": ProductCategory.electronics,
                "price": 549.00,
            }
        ],
        "status": OrderStatus.delivered,
        "order_date": NOW - timedelta(days=12),
        "delivery_date": NOW - timedelta(days=9),
        "payment_method": "card"
    },

    # Final sale
    {
        "order_number": "ORD-1006",
        "customer_email": "leo@example.com",
        "items": [
            {
                "sku": "AG-CLEARANCE",
                "name": "Clearance Phone Case",
                "category": ProductCategory.final_sale,
                "price": 19.00,
                "final_sale": True
            }
        ],
        "status": OrderStatus.delivered,
        "order_date": NOW - timedelta(days=8),
        "delivery_date": NOW - timedelta(days=6),
        "payment_method": "card"
    },

    # High value escalation
    {
        "order_number": "ORD-1007",
        "customer_email": "sophia@example.com",
        "items": [
            {
                "sku": "AG-TABLET-X",
                "name": "AuraTab X",
                "category": ProductCategory.electronics,
                "price": 699.00,
            }
        ],
        "status": OrderStatus.delivered,
        "order_date": NOW - timedelta(days=15),
        "delivery_date": NOW - timedelta(days=12),
        "payment_method": "card"
    },

    # Not delivered yet
    {
        "order_number": "ORD-1008",
        "customer_email": "maya@example.com",
        "items": [
            {
                "sku": "AG-CHARGER",
                "name": "AuraFast Charger",
                "category": ProductCategory.accessories,
                "price": 39.00,
            }
        ],
        "status": OrderStatus.shipped,
        "order_date": NOW - timedelta(days=3),
        "payment_method": "card"
    },

    # Damaged by customer
    {
        "order_number": "ORD-1009",
        "customer_email": "liam@example.com",
        "items": [
            {
                "sku": "AG-SPEAKER",
                "name": "AuraMini Speaker",
                "category": ProductCategory.electronics,
                "price": 129.00,
                "opened": True,
                "damaged_by_customer": True
            }
        ],
        "status": OrderStatus.delivered,
        "order_date": NOW - timedelta(days=14),
        "delivery_date": NOW - timedelta(days=10),
        "payment_method": "card"
    },

    # High value bundle
    {
        "order_number": "ORD-1010",
        "customer_email": "riya@example.com",
        "items": [
            {
                "sku": "AG-BUNDLE",
                "name": "AuraHome Bundle",
                "category": ProductCategory.electronics,
                "price": 899.00,
            }
        ],
        "status": OrderStatus.delivered,
        "order_date": NOW - timedelta(days=25),
        "delivery_date": NOW - timedelta(days=22),
        "payment_method": "card"
    },

    # More normal approvals
    {
        "order_number": "ORD-1011",
        "customer_email": "olivia@example.com",
        "items": [{"sku":"AG-MOUSE","name":"Aura Mouse","category":ProductCategory.accessories,"price":49}],
        "status": OrderStatus.delivered,
        "order_date": NOW - timedelta(days=9),
        "delivery_date": NOW - timedelta(days=6),
        "payment_method": "card"
    },

    {
        "order_number": "ORD-1012",
        "customer_email": "william@example.com",
        "items": [{"sku":"AG-KEYBOARD","name":"Aura Keyboard","category":ProductCategory.accessories,"price":99}],
        "status": OrderStatus.delivered,
        "order_date": NOW - timedelta(days=5),
        "delivery_date": NOW - timedelta(days=3),
        "payment_method": "card"
    },

    {
        "order_number": "ORD-1013",
        "customer_email": "isabella@example.com",
        "items": [{"sku":"AG-WEBCAM","name":"Aura Webcam","category":ProductCategory.electronics,"price":79}],
        "status": OrderStatus.delivered,
        "order_date": NOW - timedelta(days=28),
        "delivery_date": NOW - timedelta(days=26),
        "payment_method": "card"
    },

    # Black November expired
    {
        "order_number": "ORD-1014",
        "customer_email": "ben@example.com",
        "items": [{"sku":"AG-EARBUDS-PRO","name":"AuraBuds Pro","category":ProductCategory.electronics,"price":149}],
        "status": OrderStatus.delivered,
        "order_date": NOW - timedelta(days=55),
        "delivery_date": NOW - timedelta(days=50),
        "purchased_during_black_november": True,
        "payment_method": "card"
    },

    # Refunded order
    {
        "order_number": "ORD-1015",
        "customer_email": "charlotte@example.com",
        "items": [{"sku":"AG-DOCK","name":"Aura Dock","category":ProductCategory.accessories,"price":129}],
        "status": OrderStatus.refunded,
        "order_date": NOW - timedelta(days=60),
        "delivery_date": NOW - timedelta(days=56),
        "payment_method": "card",
        "refund_requested": True,
        "refund_status": "approved"
    }
]
    
async def seed_database():

    await Customer.delete_all()
    await Order.delete_all()

    customers = [
        Customer(**data)
        for data in CUSTOMERS
    ]

    await Customer.insert_many(customers)
    
    saved_customers = await Customer.find_all().to_list()
    customer_map = {c.email: c for c in saved_customers}

    orders = [
        Order(
            order_number=data['order_number'],
            customer_email=data["customer_email"],
            customer=cast(Link[Customer], customer_map[data["customer_email"]]),
            status=data["status"],
            order_date=data["order_date"],
            delivery_date=data.get("delivery_date"),
            purchased_during_black_november=data.get(
                "purchased_during_black_november",
                False,
            ),
            items=[
                ProductItem(**item)
                for item in data["items"]
            ],
            payment_method=data["payment_method"],
            refund_decision=None
        )
        for data in ORDERS
    ]

    await Order.insert_many(orders)
    
    