"""
Stage 3: Business Policy Engine
Evaluates enterprise business policy rules against order metadata.
"""

from datetime import datetime

MAX_REPLACEMENT_DAYS = 7  # Policy: Return/Replacement allowed within 7 days

def evaluate_replacement_policy(order_details: dict) -> dict:
    if not order_details:
        return {
            "eligible": False,
            "decision": "ORDER_NOT_FOUND",
            "reason": "Invalid or missing Order ID."
        }
        
    if order_details["status"] != "DELIVERED":
        return {
            "eligible": False,
            "decision": "ORDER_NOT_DELIVERED",
            "reason": f"Order status is '{order_details['status']}'. Item must be delivered first."
        }
        
    delivery_date = datetime.strptime(order_details["delivery_date"], "%Y-%m-%d")
    days_elapsed = (datetime.now() - delivery_date).days
    
    if days_elapsed <= MAX_REPLACEMENT_DAYS:
        return {
            "eligible": True,
            "decision": "APPROVED_REPLACEMENT",
            "days_elapsed": days_elapsed,
            "reason": f"Delivered {days_elapsed} days ago (within the {MAX_REPLACEMENT_DAYS}-day return window)."
        }
    else:
        return {
            "eligible": False,
            "decision": "REJECTED_POLICY_EXPIRED",
            "days_elapsed": days_elapsed,
            "reason": f"Delivered {days_elapsed} days ago, exceeding the maximum {MAX_REPLACEMENT_DAYS}-day policy limit."
        }
