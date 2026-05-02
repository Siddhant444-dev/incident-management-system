# 🏗️ System Architecture

## Overview

The Incident Management System (IMS) is designed as a distributed, asynchronous system to handle high-throughput signal ingestion and incident management.

## Architecture Diagram
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
│ │
▼ ▼
MongoDB PostgreSQL
(Signals) (Incidents + RCA)


## Components

### 1. API Layer (FastAPI)
- Handles incoming signals
- Applies rate limiting
- Pushes signals to Redis queue

### 2. Redis (Queue Layer)
- Acts as buffer between ingestion and processing
- Prevents overload during spikes
- Stores signals temporarily

### 3. Worker (Async Processor)
- Consumes signals from Redis
- Applies debouncing logic
- Writes to databases

### 4. MongoDB (Data Lake)
- Stores raw signals (audit log)
- Enables debugging and traceability

### 5. PostgreSQL (Source of Truth)
- Stores incidents (Work Items)
- Stores RCA records
- Maintains strong consistency

### 6. Frontend (React)
- Displays incidents
- Shows signal details
- Allows RCA submission
- Handles lifecycle transitions