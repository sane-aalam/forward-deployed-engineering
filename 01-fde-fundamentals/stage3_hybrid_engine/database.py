"""
Stage 3: Enterprise Order Database Layer
In-memory database simulating enterprise ERP / Order records.
"""

from datetime import datetime, timedelta

# Mock Database Records
ORDERS_DB = {
    "ORD-1001": {
        "order_id": "ORD-1001",
        "customer_name": "Alice Smith",
        "product": "Wireless Headphones",
        "delivery_date": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"), # 3 days ago
        "status": "DELIVERED",
        "item_condition": "Damaged in Transit"
    },
    "ORD-1002": {
        "order_id": "ORD-1002",
        "customer_name": "Bob Jones",
        "product": "Gaming Laptop",
        "delivery_date": (datetime.now() - timedelta(days=12)).strftime("%Y-%m-%d"), # 12 days ago
        "status": "DELIVERED",
        "item_condition": "Changed Mind"
    },
    "ORD-1003": {
        "order_id": "ORD-1003",
        "customer_name": "Charlie Brown",
        "product": "Smart Watch",
        "delivery_date": None,
        "status": "IN_TRANSIT",
        "item_condition": "Intact"
    }
}

def get_order_details(order_id: str) -> dict:
    """Fetch order details by ID."""
    return ORDERS_DB.get(order_id.upper())
