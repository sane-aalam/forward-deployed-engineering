# Stage 1: Rule-Based Support System

This module demonstrates **Level 1** support automation using string normalization and hardcoded `if-elif-else` conditional logic.

## 🚀 How to Run

```bash
python 01-fde-fundamentals/stage1_rule_based/main.py
```

## 🧠 Key Takeaways & Limitations

* **Pros:** Fast, deterministic, simple to set up for basic keyword matching.
* **Cons (Brittle):** 
  * Fails when users rephrase queries (e.g. *"My parcel hasn't arrived"* vs *"Where is my order"*).
  * Cannot handle typos, multi-intent requests, or calculate dynamic business rules (e.g., checking actual order delivery date from database).
