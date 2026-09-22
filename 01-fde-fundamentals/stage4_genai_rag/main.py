"""
Stage 4: Generative AI & RAG Support Agent Demo
Runs complex queries through RAG Policy Retrieval, LLM Tool Calling, and Response Synthesis.
"""

from agent import SupportGenAIAgent

if __name__ == "__main__":
    print("=" * 75)
    print("STAGE 4: GENERATIVE AI & RAG AGENT SYSTEM DEMO")
    print("=" * 75)
    
    agent = SupportGenAIAgent()
    
    test_queries = [
        "I received a broken wireless headphone for ORD-1001 3 days ago. Can I replace it?",
        "Can I get a replacement for gaming laptop ORD-1002 delivered 12 days ago?",
        "What is your standard policy for processing refunds?"
    ]
    
    for idx, query in enumerate(test_queries, 1):
        print(f"\n[QUERY {idx}]: \"{query}\"\n")
        res = agent.process(query)
        
        for log in res["reasoning_logs"]:
            print(f"  {log}")
            
        print("\n  [SYNTHESIZED AGENT RESPONSE]:")
        print("  " + "\n  ".join(res["final_response"].split("\n")))
        print("\n" + "-" * 75)
        
    print("=" * 75)
