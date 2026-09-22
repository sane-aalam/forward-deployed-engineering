"""
Stage 3: Hybrid Engine Integration
Combines ML Intent Classification + Enterprise DB + Policy Rule Engine.
"""

import os
import sys
import re

# Add parent directory to sys.path so stage2 module can be imported
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from stage2_ml_classification.predict import predict_intent
from database import get_order_details
from policy_engine import evaluate_replacement_policy

def process_ticket(user_query: str, order_id: str = None):
    # 1. Extract intent using Stage 2 ML Classifier
    ml_result = predict_intent(user_query)
    intent = ml_result["predicted_intent"]
    
    # Extract order_id from string if not explicitly passed
    if not order_id:
        match = re.search(r"ORD-\d+", user_query, re.IGNORECASE)
        if match:
            order_id = match.group(0).upper()
            
    print(f"\n[Ticket Query]: \"{user_query}\"")
    print(f"  └─ Step 1: ML Intent Classification ──> Intent: '{intent}' (Confidence: {ml_result['confidence']*100:.1f}%)")
    
    # 2. Handle intent using Database + Policy Engine
    if intent == "damaged_item" or "replace" in user_query.lower():
        if not order_id:
            return "Please provide a valid Order ID (e.g., ORD-1001) to verify replacement eligibility."
            
        order_info = get_order_details(order_id)
        print(f"  └─ Step 2: Database Lookup (ERP) ────> Fetched Order: {order_info}")
        
        policy_eval = evaluate_replacement_policy(order_info)
        print(f"  └─ Step 3: Policy Rule Engine ────────> Decision: {policy_eval['decision']}")
        
        if policy_eval["eligible"]:
            return f"✅ SUCCESS: Your replacement for {order_info['product']} (Order {order_id}) is APPROVED. Reason: {policy_eval['reason']}"
        else:
            return f"❌ REJECTED: Replacement for Order {order_id} cannot be processed. Reason: {policy_eval['reason']}"

    elif intent == "order_status":
        if order_id:
            order_info = get_order_details(order_id)
            if order_info:
                return f"📦 ORDER STATUS: Order {order_id} ({order_info['product']}) is currently '{order_info['status']}'."
        return "📦 ORDER STATUS: Please log into your account dashboard or provide an Order ID."
        
    elif intent == "refund_request":
        return "💳 REFUND: Refunds are issued automatically within 5-7 business days upon item arrival at warehouse."
        
    else:
        return "Escalating query to human representative."


if __name__ == "__main__":
    print("=" * 70)
    print("STAGE 3: HYBRID ENGINE (ML INTENT + DB + POLICY RULES) DEMO")
    print("=" * 70)
    
    test_cases = [
        ("I received a broken item for ORD-1001 3 days ago. Can I replace it?", "ORD-1001"),
        ("I want to exchange my gaming laptop for ORD-1002", "ORD-1002"),
        ("Where is my order status for ORD-1003?", "ORD-1003")
    ]
    
    for query, oid in test_cases:
        res = process_ticket(query, oid)
        print(f"  └─ FINAL ACTION RESPONSE: {res}\n")
        
    print("=" * 70)
