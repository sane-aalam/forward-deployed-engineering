"""
Stage 1: Rule-Based Customer Support AI System
Uses string normalization, keyword matching, and nested if-elif-else rules.
"""

def handle_support_ticket(query: str) -> dict:
    query_clean = query.lower().strip()
    
    # Order Status Rule
    if "where is my order" in query_clean or "track my package" in query_clean or "order status" in query_clean:
        return {
            "status": "SUCCESS",
            "stage": "Stage 1 (Rule-Based)",
            "intent": "order_status",
            "response": "Please log into your dashboard and navigate to 'My Orders' to track your shipment."
        }
    
    # Damaged Item & Replacement Rule (Hardcoded 3 days rule)
    elif "damaged" in query_clean and ("replace" in query_clean or "replacement" in query_clean) and "3 days" in query_clean:
        return {
            "status": "SUCCESS",
            "stage": "Stage 1 (Rule-Based)",
            "intent": "damaged_item_replacement",
            "response": "Eligible for replacement under 3-day policy. Please upload a photo of the damaged item."
        }
    
    # Refund Query Rule
    elif "refund" in query_clean or "money back" in query_clean:
        return {
            "status": "SUCCESS",
            "stage": "Stage 1 (Rule-Based)",
            "intent": "refund_request",
            "response": "Refunds are processed within 5 to 7 business days to your original payment method."
        }
    
    # Default Fallback (Unmatched Rule)
    else:
        return {
            "status": "FAILED_UNMATCHED",
            "stage": "Stage 1 (Rule-Based)",
            "intent": "unknown",
            "response": "Escalating ticket to a human support agent because no matching rule was found."
        }


if __name__ == "__main__":
    print("=" * 60)
    print("STAGE 1: RULE-BASED CUSTOMER SUPPORT SYSTEM DEMO")
    print("=" * 60)
    
    test_queries = [
        "Where is my order status?",
        "I received a damaged item and want to replace it, delivered 3 days ago",
        "My parcel hasn't arrived yet! Delivery kab hogi?",  # Will fail rule match
        "Can I get my money back for order #1002?",
        "Can I exchange an item delivered 5 days ago?"       # Will fail rule match
    ]
    
    for idx, q in enumerate(test_queries, 1):
        print(f"\n[Test Query {idx}]: \"{q}\"")
        result = handle_support_ticket(q)
        print(f"  -> Match Status     : {result['status']}")
        print(f"  -> Extracted Intent : {result['intent']}")
        print(f"  -> Response         : {result['response']}")
    print("\n" + "=" * 60)
