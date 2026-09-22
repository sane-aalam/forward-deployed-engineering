"""
FastAPI Server providing API endpoints for all 4 Customer Support AI Stages
(Stage 1: Rule-Based, Stage 2: ML Intent Classifier, Stage 3: Hybrid Engine, Stage 4: GenAI/RAG Agent)
"""

import os
import sys
import re
import json
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Ensure base directory and stage directories are in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
for folder in ["stage1_rule_based", "stage2_ml_classification", "stage3_hybrid_engine", "stage4_genai_rag"]:
    p = os.path.join(BASE_DIR, folder)
    if p not in sys.path:
        sys.path.insert(0, p)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Import stage modules
from stage1_rule_based.main import handle_support_ticket
from stage2_ml_classification.predict import predict_intent
from stage3_hybrid_engine.database import get_order_details, ORDERS_DB
from stage3_hybrid_engine.policy_engine import evaluate_replacement_policy
from stage4_genai_rag.agent import SupportGenAIAgent

app = FastAPI(title="FDE Customer Support AI API", version="1.0.0")

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai_agent = SupportGenAIAgent()

class QueryRequest(BaseModel):
    query: str
    stage: str = "all"  # "all", "stage1", "stage2", "stage3", "stage4"
    order_id: Optional[str] = None

def run_stage1(user_query: str) -> dict:
    res = handle_support_ticket(user_query)
    logs = [
        "Step 1: Clean & normalize raw input text",
        "Step 2: Evaluate hardcoded IF-ELIF-ELSE keyword rules",
        f"Step 3: Outcome: Match '{res['status']}' -> Intent '{res['intent']}'"
    ]
    return {
        "stage_id": "stage1",
        "stage_name": "Stage 1: Hardcoded Rule-Based System",
        "status": res["status"],
        "intent": res["intent"],
        "confidence": 1.0 if res["status"] == "SUCCESS" else 0.0,
        "response": res["response"],
        "logs": logs
    }

def run_stage2(user_query: str) -> dict:
    ml_res = predict_intent(user_query)
    logs = [
        "Step 1: Load pre-trained TF-IDF vectorizer + LogisticRegression model (model.pkl)",
        f"Step 2: Vectorize query string: \"{user_query}\"",
        f"Step 3: Predict intent probability distribution",
        f"Result: Intent '{ml_res['predicted_intent']}' with {ml_res['confidence']*100:.2f}% confidence score"
    ]
    return {
        "stage_id": "stage2",
        "stage_name": "Stage 2: ML Intent Classifier",
        "status": "CLASSIFIED",
        "intent": ml_res["predicted_intent"],
        "confidence": ml_res["confidence"],
        "response": f"Predicted Intent: '{ml_res['predicted_intent']}' (Confidence: {ml_res['confidence']*100:.2f}%).\n\nNotice: Stage 2 performs Statistical NLP Intent Classification, but does not query ERP databases or execute actions.",
        "logs": logs
    }

def run_stage3(user_query: str, order_id: Optional[str] = None) -> dict:
    logs = []
    # 1. Extract intent using Stage 2 ML Classifier
    ml_result = predict_intent(user_query)
    intent = ml_result["predicted_intent"]
    confidence = ml_result["confidence"]
    logs.append(f"[Step 1: ML Classification] Intent: '{intent}' (Confidence: {confidence*100:.1f}%)")

    # Extract order_id from string if not explicitly passed
    if not order_id:
        match = re.search(r"ORD-\d+", user_query, re.IGNORECASE)
        if match:
            order_id = match.group(0).upper()

    if intent == "damaged_item" or "replace" in user_query.lower():
        if not order_id:
            logs.append("[Step 2: ERP Lookup] Failed - No Order ID detected in query.")
            return {
                "stage_id": "stage3",
                "stage_name": "Stage 3: Hybrid Engine (ML + DB + Policy Rules)",
                "status": "REQUIRES_INFO",
                "intent": intent,
                "confidence": confidence,
                "response": "Please provide a valid Order ID (e.g., ORD-1001) to verify replacement eligibility.",
                "logs": logs,
                "order_id": None
            }

        order_info = get_order_details(order_id)
        logs.append(f"[Step 2: ERP Lookup] Fetched Order {order_id}: {json.dumps(order_info)}")

        policy_eval = evaluate_replacement_policy(order_info)
        logs.append(f"[Step 3: Policy Engine] Decision: {policy_eval['decision']} ({policy_eval['reason']})")

        if policy_eval["eligible"]:
            resp = f"✅ SUCCESS: Replacement for {order_info['product']} (Order {order_id}) is APPROVED.\nReason: {policy_eval['reason']}"
            status = "SUCCESS"
        else:
            resp = f"❌ REJECTED: Replacement for Order {order_id} cannot be processed.\nReason: {policy_eval['reason']}"
            status = "REJECTED_POLICY"

        return {
            "stage_id": "stage3",
            "stage_name": "Stage 3: Hybrid Engine (ML + DB + Policy Rules)",
            "status": status,
            "intent": intent,
            "confidence": confidence,
            "response": resp,
            "logs": logs,
            "order_id": order_id
        }

    elif intent == "order_status":
        order_info = get_order_details(order_id) if order_id else None
        if order_info:
            logs.append(f"[Step 2: ERP Lookup] Fetched Order {order_id}: Status '{order_info['status']}'")
            resp = f"📦 ORDER STATUS: Order {order_id} ({order_info['product']}) is currently '{order_info['status']}'."
        else:
            logs.append("[Step 2: ERP Lookup] No specific Order ID found. Providing standard portal guidance.")
            resp = "📦 ORDER STATUS: Please log into your account dashboard or provide an Order ID (e.g. ORD-1003)."

        return {
            "stage_id": "stage3",
            "stage_name": "Stage 3: Hybrid Engine (ML + DB + Policy Rules)",
            "status": "SUCCESS",
            "intent": intent,
            "confidence": confidence,
            "response": resp,
            "logs": logs,
            "order_id": order_id
        }

    elif intent == "refund_request":
        logs.append("[Step 2: Business Policy] Applied automated refund policy response.")
        return {
            "stage_id": "stage3",
            "stage_name": "Stage 3: Hybrid Engine (ML + DB + Policy Rules)",
            "status": "SUCCESS",
            "intent": intent,
            "confidence": confidence,
            "response": "💳 REFUND: Refunds are issued automatically within 5-7 business days upon item arrival at warehouse.",
            "logs": logs,
            "order_id": order_id
        }

    else:
        logs.append("[Step 2: Fallback] Intent unknown to Policy Engine rules. Escalating.")
        return {
            "stage_id": "stage3",
            "stage_name": "Stage 3: Hybrid Engine (ML + DB + Policy Rules)",
            "status": "ESCALATED",
            "intent": intent,
            "confidence": confidence,
            "response": "Escalating query to human representative.",
            "logs": logs,
            "order_id": order_id
        }

def run_stage4(user_query: str) -> dict:
    agent_res = genai_agent.process(user_query)
    return {
        "stage_id": "stage4",
        "stage_name": "Stage 4: Generative AI Agent + Policy RAG + ERP Tools",
        "status": "SUCCESS",
        "intent": "rag_agent_autonomous",
        "confidence": 0.98,
        "response": agent_res["final_response"],
        "logs": agent_res["reasoning_logs"],
        "retrieved_policy": agent_res.get("retrieved_policy")
    }

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "FDE Support AI System Backend"}

@app.get("/api/erp-orders")
def get_orders():
    return ORDERS_DB

@app.get("/api/policies")
def get_policies():
    policies_file = os.path.join(BASE_DIR, "stage4_genai_rag", "policies.json")
    if os.path.exists(policies_file):
        with open(policies_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@app.post("/api/query")
def process_query(req: QueryRequest):
    query = req.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query string cannot be empty")

    order_id_match = re.search(r"ORD-\d+", query, re.IGNORECASE)
    extracted_order_id = req.order_id or (order_id_match.group(0).upper() if order_id_match else None)

    results = {}
    if req.stage == "all" or req.stage == "stage1":
        results["stage1"] = run_stage1(query)
    if req.stage == "all" or req.stage == "stage2":
        results["stage2"] = run_stage2(query)
    if req.stage == "all" or req.stage == "stage3":
        results["stage3"] = run_stage3(query, extracted_order_id)
    if req.stage == "all" or req.stage == "stage4":
        results["stage4"] = run_stage4(query)

    return {
        "query": query,
        "extracted_order_id": extracted_order_id,
        "stage_requested": req.stage,
        "results": results
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
