# Stage 4: Generative AI & RAG Support Agent

This module demonstrates **Level 4** support automation: an LLM Agent combined with **Retrieval-Augmented Generation (RAG)** and **Enterprise Tool Execution**.

## 🚀 How to Run

```bash
python 01-fde-fundamentals/stage4_genai_rag/main.py
```

## 🧠 Key Architecture Takeaways

1. **RAG Policy Ingestion:** Context is dynamically retrieved from vector space (`policies.json`) and injected into the prompt context.
2. **LLM Tool Calling:** Agent inspects query, extracts entities (e.g., `ORD-1001`), executes ERP lookup tools (`tool_fetch_order`), and triggers real enterprise actions (`tool_create_replacement_ticket`).
3. **Conversational Synthesis:** Generates human-grade, polite responses explaining exact policy rationale and actions taken.
