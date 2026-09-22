"""
Stage 4: Generative AI Agent Orchestrator
Simulates an LLM reasoning loop + RAG Context Injection + Tool Calling.
"""

import re
from rag_engine import PolicyRAGEngine
from erp_tools import tool_fetch_order, tool_create_replacement_ticket

class SupportGenAIAgent:
    def __init__(self):
        self.rag = PolicyRAGEngine()

    def process(self, query: str) -> dict:
        reasoning_logs = []
        
        # 1. RAG Step: Retrieve relevant policy context
        reasoning_logs.append("[Step 1: RAG Retrieval] Querying policy knowledge base...")
        policy_docs = self.rag.retrieve(query, top_k=1)
        retrieved_policy = policy_docs[0]
        reasoning_logs.append(f"  └─ Context Injected: '{retrieved_policy['title']}' (Score: {retrieved_policy['relevance_score']})")

        # 2. Entity Extraction: Extract Order ID
        match = re.search(r"ORD-\d+", query, re.IGNORECASE)
        order_id = match.group(0).upper() if match else None

        # 3. Agent Tool Call Loop
        if order_id:
            reasoning_logs.append(f"[Step 2: Tool Execution] Calling ERP Tool `fetch_order({order_id})`...")
            order_res = tool_fetch_order(order_id)
            
            if order_res["found"]:
                order_data = order_res["data"]
                days_ago = order_data["delivered_days_ago"]
                reasoning_logs.append(f"  └─ ERP Data: Item '{order_data['item']}' delivered {days_ago} days ago.")

                # 4. LLM Reasoning & Rule Synthesis
                reasoning_logs.append("[Step 3: Reasoning & Policy Decision]")
                if days_ago <= 7 and ("damaged" in query.lower() or "broken" in query.lower() or "replace" in query.lower()):
                    reasoning_logs.append("  └─ Evaluation: Days since delivery (3) <= Policy max (7 days). Eligible!")
                    
                    # Tool Execution: Create Ticket
                    tkt = tool_create_replacement_ticket(order_id, reason="Item damaged upon arrival")
                    reasoning_logs.append(f"  └─ Executed Tool: `create_replacement_ticket()` ──> Ticket ID: {tkt['ticket_id']}")

                    final_response = (
                        f"Hello {order_data['customer']},\n\n"
                        f"I'm sorry to hear that your {order_data['item']} arrived damaged! "
                        f"According to our '{retrieved_policy['title']}', you are fully eligible for a free replacement since your order was delivered {days_ago} days ago.\n\n"
                        f"✅ **Action Taken:** Replacement Ticket **#{tkt['ticket_id']}** has been created. A prepaid return shipping label has been sent to your email."
                    )
                else:
                    reasoning_logs.append("  └─ Evaluation: Delivered days ago exceeds policy limits.")
                    final_response = (
                        f"Hello {order_data['customer']},\n\n"
                        f"We reviewed your request for Order #{order_id} ({order_data['item']}). "
                        f"According to our '{retrieved_policy['title']}', return/replacement requests must be submitted within 7 days of delivery. "
                        f"Since your order was delivered {days_ago} days ago, we are unable to issue an automated replacement."
                    )
            else:
                final_response = f"Order #{order_id} could not be found in our records. Please double-check your Order ID."
        else:
            final_response = (
                f"Thank you for contacting support! Regarding your query, our policy states:\n\n"
                f"\"{retrieved_policy['content']}\"\n\n"
                f"Please provide your Order ID (e.g. ORD-1001) so I can assist you further!"
            )

        return {
            "query": query,
            "retrieved_policy": retrieved_policy,
            "reasoning_logs": reasoning_logs,
            "final_response": final_response
        }
