# 🧪 Yield Prediction - Simulated Backend Module

This Flask-based backend simulates data storage and retrieval for crop yield predictions using a local JSON file — acting as a dummy database until full DB integration (e.g., PostgreSQL) is done.

---

## 🚀 Features

- ✅ **POST /fake-yield** – Submit user inputs + predicted yield
- ✅ **GET /fake-yield** – View all stored prediction records
- ✅ **PUT /fake-yield/<id>** – Update an existing record by ID
- ✅ **DELETE /fake-yield/<id>** – Delete a prediction record

---

## 📦 Data Stored (Example)

```json
{
  "id": "1234-uuid",
  "rainfall": 220,
  "temperature": 29,
  "ph": 6.7,
  "predicted_yield": 3.9,
  "timestamp": "2025-07-30 21:45:00"
}
