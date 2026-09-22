"""
Stage 4: Local RAG (Retrieval-Augmented Generation) Engine
Uses TF-IDF Vector Space and Cosine Similarity to retrieve policy context locally without API keys.
"""

import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class PolicyRAGEngine:
    def __init__(self, policies_file: str = None):
        if not policies_file:
            policies_file = os.path.join(os.path.dirname(__file__), "policies.json")
            
        with open(policies_file, "r", encoding="utf-8") as f:
            self.policies = json.load(f)
            
        self.documents = [f"{p['title']}: {p['content']}" for p in self.policies]
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.doc_vectors = self.vectorizer.fit_transform(self.documents)

    def retrieve(self, query: str, top_k: int = 1) -> list:
        """Retrieves top_k most relevant policy documents for a given query."""
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.doc_vectors)[0]
        
        # Rank documents by score
        ranked_indices = similarities.argsort()[::-1][:top_k]
        
        results = []
        for idx in ranked_indices:
            score = float(similarities[idx])
            results.append({
                "policy_id": self.policies[idx]["id"],
                "title": self.policies[idx]["title"],
                "content": self.policies[idx]["content"],
                "relevance_score": round(score, 4)
            })
            
        return results

if __name__ == "__main__":
    rag = PolicyRAGEngine()
    res = rag.retrieve("Can I replace a broken item delivered 3 days ago?")
    print("Retrieved Policy:")
    print(json.dumps(res, indent=2))
