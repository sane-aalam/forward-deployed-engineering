"""
Stage 2: ML Model Trainer
Trains a TF-IDF Vectorizer + Naive Bayes Classifier on customer support dataset.
"""

import json
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

def train():
    dataset_path = os.path.join(os.path.dirname(__file__), "dataset.json")
    model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
    
    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    texts = [item["text"] for item in data]
    labels = [item["label"] for item in data]
    
    # Build ML pipeline: TF-IDF + Naive Bayes
    pipeline = make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), MultinomialNB())
    pipeline.fit(texts, labels)
    
    # Save trained model pipeline
    with open(model_path, "wb") as f:
        pickle.dump(pipeline, f)
        
    print(f"✅ Successfully trained ML Intent Classifier on {len(texts)} samples.")
    print(f"💾 Model saved to: {model_path}")

if __name__ == "__main__":
    train()
