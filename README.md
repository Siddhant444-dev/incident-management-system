🚨 Incident Management System (IMS)

📌 Overview:

This project implements a Mission-Critical Incident Management System (IMS) designed to handle high-volume signals (errors, latency spikes) from distributed systems and manage incident workflows.

The system ensures:

Reliable ingestion of high-throughput signals
Intelligent debouncing to prevent alert storms
Structured incident lifecycle management
Mandatory Root Cause Analysis (RCA)
Real-time dashboard for monitoring


🏗️ Architecture:
Frontend (React)
       │
       ▼
FastAPI Backend (API Layer)
       │
       ▼
Redis (Queue / Buffer)
       │
       ▼
Async Worker
   │         │
   ▼         ▼
MongoDB   PostgreSQL
(Signals) (Incidents + RCA)


⚙️ Tech Stack:
Backend: FastAPI (Async Python)
Frontend: React (Vite)
Queue: Redis Streams
Databases:
  - MongoDB → Raw signals (audit log)
  - PostgreSQL → Incidents & RCA (source of truth)
DevOps: Docker Compose


🚀 Features:
🔹 High-Throughput Signal Ingestion
Supports burst traffic using Redis Streams
Designed for scalability (10k signals/sec ready)
🔹 Backpressure Handling
Redis acts as a buffer layer between ingestion and persistence
Prevents system crashes during spikes
🔹 Debouncing Logic
100 signals → 1 incident (within 10 seconds)
🔹 Incident Lifecycle
OPEN → INVESTIGATING → RESOLVED → CLOSED
Strict lifecycle enforcement
Invalid transitions blocked
🔹 RCA Enforcement
❌ Cannot close incident without RCA
🔹 MTTR Calculation
MTTR = RCA submission time - first signal time
🔹 Observability
/health endpoint
Throughput logs every 5 seconds:
[METRICS] 25 signals/sec | Queue length: 10
🔹 Rate Limiting
Prevents API abuse
Protects system from overload
🔹 Frontend Dashboard
Live incident feed
Severity-based sorting
Incident details view
Raw signals (MongoDB)
RCA submission form
Status transition buttons


🔐 Non-Functional Enhancements (Bonus Points):
✔ Performance
Async processing using FastAPI
Redis queue for high throughput
Decoupled ingestion and processing
✔ Scalability
Worker-based architecture (can scale horizontally)
Queue-based buffering
✔ Reliability
No data loss (signals stored in MongoDB)
Fault-tolerant ingestion
✔ Security (Basic)
Rate limiting to prevent abuse
Controlled lifecycle transitions
Input validation on APIs


📊 API Endpoints:
Signals
POST /api/signals
Incidents
GET    /api/incidents
GET    /api/incidents/{id}
GET    /api/incidents/{id}/signals
PATCH  /api/incidents/{id}/status
POST   /api/incidents/{id}/rca
Health
GET /health


🧪 Sample Data:

Run simulation:

python sample-data/simulate_signals.py

Test debouncing:

python sample-data/burst_test.py


🛠️ Setup & Run Instructions:
1️⃣ Start services
docker compose up -d
2️⃣ Run backend
cd backend
uvicorn app.main:app --reload
3️⃣ Run frontend
cd frontend
npm install
npm run dev
4️⃣ Open application
http://localhost:5173


📦 Project Structure:
incident-management-system/
├── backend/
├── frontend/
├── docs/
├── sample-data/
├── docker-compose.yml
├── README.md


⚡ Backpressure Strategy:
Incoming Signals → Redis Queue → Worker → Databases
Benefits:
Prevents database overload
Handles traffic spikes smoothly
Ensures system stability
Decouples ingestion from processing


🧠 Design Highlights:
Polyglot persistence (MongoDB + PostgreSQL)
Async worker model
Queue-based architecture
Debouncing to reduce noise
Strict lifecycle enforcement
