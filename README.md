# 🚨 Incident Management System (IMS)

## 📌 Overview

This project implements a **Mission-Critical Incident Management System (IMS)** designed to handle high-volume signals such as errors and latency spikes from distributed systems and manage incident workflows.

The system ensures:

- Reliable ingestion of high-throughput signals
- Intelligent debouncing to prevent alert storms
- Structured incident lifecycle management
- Mandatory Root Cause Analysis (RCA)
- Real-time dashboard for monitoring

---

## 🏗️ Architecture

```text
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
```

---

## ⚙️ Tech Stack

### Backend
- FastAPI
- Async Python
- SQLAlchemy

### Frontend
- React
- Vite

### Queue
- Redis Streams

### Databases
- MongoDB → Raw signals / audit log
- PostgreSQL → Incidents and RCA records

### DevOps
- Docker Compose

---

## 🚀 Features

### High-Throughput Signal Ingestion
- Supports burst traffic using Redis Streams
- Designed for scalability

### Backpressure Handling
- Redis acts as a buffer between ingestion and persistence
- Prevents system crashes during traffic spikes

### Debouncing Logic
- Multiple signals from the same component within 10 seconds create only one incident
- All raw signals are linked to the same incident

### Incident Lifecycle
```text
OPEN → INVESTIGATING → RESOLVED → CLOSED
```

- Strict lifecycle enforcement
- Status transitions are controlled through backend APIs

### RCA Enforcement
- An incident cannot be moved to `CLOSED` without RCA

### MTTR Calculation
```text
MTTR = RCA submission time - first signal time
```

### Observability
- `/health` endpoint
- Throughput logs every 5 seconds

Example:

```text
[METRICS] Throughput: 25 signals/sec | Queue length: 10
```

### Rate Limiting
- Prevents API abuse
- Protects ingestion endpoint from cascading overload

### Frontend Dashboard
- Live incident feed
- Severity-based sorting
- Incident details view
- Raw signals from MongoDB
- RCA submission form
- Status transition buttons

---

## 🔐 Non-Functional Enhancements

### Performance
- Async processing using FastAPI
- Redis queue for high-throughput ingestion
- Decoupled ingestion and persistence

### Scalability
- Worker-based architecture
- Queue-based buffering
- Workers can be scaled horizontally

### Reliability
- Raw signals are stored in MongoDB
- Structured incident data is stored in PostgreSQL
- Queue prevents data loss during traffic spikes

### Security
- Rate limiting on ingestion API
- Controlled lifecycle transitions
- Basic input validation

---

## 📊 API Endpoints

### Signals

```text
POST /api/signals
```

### Incidents

```text
GET    /api/incidents
GET    /api/incidents/{id}
GET    /api/incidents/{id}/signals
PATCH  /api/incidents/{id}/status
POST   /api/incidents/{id}/rca
```

### Health

```text
GET /health
```

---

## 🧪 Sample Data

Run signal simulation:

```bash
python sample-data/simulate_signals.py
```

Test debouncing:

```bash
python sample-data/burst_test.py
```

---

## 🛠️ Setup & Run Instructions

### 1. Start services

```bash
docker compose up -d
```

### 2. Run backend

```bash
cd backend
uvicorn app.main:app --reload
```

### 3. Run frontend

```bash
cd frontend
npm install
npm run dev
```

### 4. Open application

```text
http://localhost:5173
```

---

## 📦 Project Structure

```text
incident-management-system/
├── backend/
├── frontend/
├── docs/
├── sample-data/
├── docker-compose.yml
└── README.md
```

---

## ⚡ Backpressure Strategy

```text
Incoming Signals → Redis Queue → Worker → Databases
```

### Benefits

- Prevents database overload
- Handles traffic spikes smoothly
- Ensures system stability
- Decouples ingestion from processing

---

## 🧠 Design Highlights

- Polyglot persistence using MongoDB and PostgreSQL
- Async worker model
- Queue-based architecture
- Debouncing to reduce incident noise
- Strict lifecycle enforcement
- RCA-based closure validation

---
