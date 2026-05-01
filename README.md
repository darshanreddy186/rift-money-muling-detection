# Rift-2026 Money Muling Detection
# 💰 Graph-Based Financial Crime Detection Engine  
## Money Muling Detection System – RIFT 2026 Hackathon

---

## 🚨 Problem Statement

Money muling is a major financial crime technique where illicit funds are transferred through networks of accounts to hide the original source of money.

Traditional SQL-based systems fail to detect:
- Multi-hop laundering
- Circular fund routing
- Smurfing patterns
- Layered transaction rings

This project builds a **Graph-Theory-Based Financial Crime Detection Engine** to identify suspicious mule networks using transaction graph analysis.

---

## 🧠 Core Idea

We convert financial transactions into a **directed graph**:

- **Nodes** → Bank Accounts  
- **Edges** → Transactions  
- **Edge Weight** → Transaction Amount  
- **Timestamp** → Temporal Analysis  

Using graph algorithms, we detect suspicious transaction patterns and assign risk scores.

---

## 🔎 Detection Patterns Implemented

### 1️⃣ Circular Fund Routing (Cycles)

Money flows in a loop:
A → B → C → A

- Detect cycles of length 3–5  
- All accounts in the cycle are flagged under the same `ring_id`

---

### 2️⃣ Smurfing (Fan-In / Fan-Out)

- Many small incoming transactions to one account (Aggregator)
- One account distributing funds to many accounts

---

### 3️⃣ Rapid Layering

Funds transferred across multiple accounts within a short time window:
---

### 4️⃣ High-Risk Clusters

Dense transaction subgraphs with:
- High connectivity
- Abnormal transaction frequency
- Suspicious volume concentration

---

## 🧮 Suspicion Scoring Model

Each account receives a **Suspicion Score (0–100)** based on:

| Factor | Impact |
|--------|--------|
| Cycle Participation | High |
| Smurfing Behavior | Medium |
| Rapid Layering | High |
| Volume Anomaly | Medium |
| Ring Connectivity | High |

Risk Levels:
- 🟢 Low Risk  
- 🟡 Medium Risk  
- 🔴 High Risk  

---

## 🏗️ System Architecture
Transaction CSV
↓
Graph Builder
↓
Pattern Detection Engine
↓
Risk Scoring Module
↓
Interactive Visualization UI


---

## 🖥️ Tech Stack

### Frontend
- React
- TypeScript
- TailwindCSS
- Cytoscape.js (Graph Visualization)

### Backend
- Python / Node.js
- NetworkX (Graph Analysis)
- FastAPI / Express

### Dataset
- Synthetic Financial Transactions (5K–10K records)
- CSV format

---

## 📊 Input Dataset Format

| Column Name     | Type     | Description |
|---------------|----------|------------|
| transaction_id | String   | Unique transaction ID |
| sender_id      | String   | Sender account ID |
| receiver_id    | String   | Receiver account ID |
| amount         | Float    | Transaction amount |
| timestamp      | DateTime | Format: YYYY-MM-DD HH:MM:SS |

---

## ⚡ How to Run the Project

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-repo/money-muling-engine.git
cd money-muling-engine
2️⃣ Backend Setup (Python Example)
cd backend
pip install -r requirements.txt
uvicorn api:app --reload
3️⃣ Frontend Setup
cd frontend
npm install
npm run dev
4️⃣ Open in Browser
http://localhost:5173
```bash
---
<img width="1914" height="974" alt="Screenshot 2026-02-20 010742" src="https://github.com/user-attachments/assets/d25db6cc-3bf4-4943-bf06-7e2dcecdf60d" />

<img width="1919" height="1079" alt="Screenshot 2026-04-17 165330" src="https://github.com/user-attachments/assets/9243696a-0d27-46b9-9134-ddbd292aa267" />

<img width="1919" height="1079" alt="Screenshot 2026-04-17 165330" src="https://github.com/user-attachments/assets/c65309f4-aa87-4e48-9427-8649dcd1c231" />




