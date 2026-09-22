"""
Stage 4: Enterprise ERP API Tool Integrations
Provides callable tools for the LLM Orchestrator.
"""

from datetime import datetime, timedelta

MOCK_ERP_DB = {
    "ORD-1001": {
        "order_id": "ORD-1001",
        "customer": "Alice Smith",
        "item": "Wireless Headphones",
        "delivered_days_ago": 3,
        "status": "DELIVERED"
    },
    "ORD-1002": {
        "order_id": "ORD-1002",
        "customer": "Bob Jones",
        "item": "Gaming Laptop",
        "delivered_days_ago": 12,
        "status": "DELIVERED"
    }
}

def tool_fetch_order(order_id: str) -> dict:
    """Tool: Retrieve live order record from ERP API."""
    order = MOCK_ERP_DB.get(order_id.upper())
    if order:
        return {"found": True, "data": order}
    return {"found": False, "error": f"Order {order_id} not found in ERP."}

def tool_create_replacement_ticket(order_id: str, reason: str) -> dict:
    """Tool: Creates a replacement ticket in warehouse service."""
    return {
        "ticket_id": f"TKT-REPLACE-{order_id[-4:]}",
        "order_id": order_id,
        "status": "APPROVED_LABEL_GENERATED",
        "message": f"Replacement approved for order {order_id}. Prepaid shipping label sent to customer email.",
        "reason": reason
    }
