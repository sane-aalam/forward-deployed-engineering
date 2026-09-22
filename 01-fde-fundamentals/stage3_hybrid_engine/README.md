# Stage 3: Hybrid Engine (ML Intent + Database + Business Policy Rules)

This module demonstrates **Level 3** support automation: taking ML intent predictions and combining them with structured Database lookups (ERP) and hard business policy rules (e.g. 7-day return policy matrix).

## 🚀 How to Run

```bash
python 01-fde-fundamentals/stage3_hybrid_engine/main.py
```

## 🧠 Key Takeaways

* **Bridge to Business Impact:** Unlike pure ML classification, the Hybrid Engine actively queries live database records and enforces company policies.
* **Result:** Generates concrete actions (`APPROVED_REPLACEMENT` vs `REJECTED_POLICY_EXPIRED`).
