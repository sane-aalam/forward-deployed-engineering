"""
Stage 2: ML Model Inference / Prediction Script
"""

import os
import pickle

def predict_intent(query: str):
    model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
    
    if not os.path.exists(model_path):
        from train_model import train
        train()
        
    with open(model_path, "rb") as f:
        model = pickle.load(f)
        
    predicted_label = model.predict([query])[0]
    probabilities = model.predict_proba([query])[0]
    confidence = max(probabilities)
    
    return {
        "query": query,
        "predicted_intent": predicted_label,
        "confidence": round(float(confidence), 4)
    }

if __name__ == "__main__":
    print("=" * 60)
    print("STAGE 2: MACHINE LEARNING INTENT CLASSIFIER DEMO")
    print("=" * 60)
    
    test_queries = [
        "Where is my package right now?",
        "Delivery kab hogi bhai?",
        "My phone screen is completely smashed in delivery",
        "Process my money back for the cancelled product",
        "Stop shipment for order #991"
    ]
    
    for q in test_queries:
        res = predict_intent(q)
        print(f"\nQuery: \"{res['query']}\"")
        print(f"  -> Predicted Intent : {res['predicted_intent']}")
        print(f"  -> Confidence Score: {res['confidence'] * 100:.2f}%")
        
    print("\n" + "=" * 60)
