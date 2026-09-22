# Stage 2: Machine Learning Intent Classification

This module demonstrates **Level 2** support automation: training a supervised statistical ML model (TF-IDF + Naive Bayes) to classify user queries into intent categories.

## 🚀 How to Run

```bash
# 1. Train the model
python 01-fde-fundamentals/stage2_ml_classification/train_model.py

# 2. Run intent predictions
python 01-fde-fundamentals/stage2_ml_classification/predict.py
```

## 🧠 Key Takeaways & Limitations

* **Pros:** Handles variations in natural phrasing and slang (e.g. *"Delivery kab hogi?"* mapped to `order_status`).
* **Cons (Bottleneck):** Classification **identifies the topic**, but cannot perform business actions (e.g., checking actual database delivery dates, applying return window policy rules, or generating customized user responses).
