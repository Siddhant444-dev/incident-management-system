# 🧠 Design Decisions

## 1. Why Redis?

- High-speed in-memory storage
- Supports queue (streams)
- Ideal for buffering high-throughput data

## 2. Why MongoDB?

- Flexible schema
- Stores raw signals (audit log)
- Easy to query JSON data

## 3. Why PostgreSQL?

- Strong consistency
- Transactional support
- Ideal for incident lifecycle and RCA

## 4. Why Async Processing?

- Handles high concurrency
- Improves system throughput
- Avoids blocking operations

## 5. Why Debouncing?

- Prevents alert storms
- Groups similar signals into one incident
- Reduces noise

## 6. Why Separate Databases?

- MongoDB → high-volume logs
- PostgreSQL → structured data

## 7. Lifecycle Enforcement

OPEN → INVESTIGATING → RESOLVED → CLOSED

- Prevents invalid transitions
- Ensures RCA before closure

## 8. Trade-offs

- Added complexity (multiple systems)
- Requires coordination between services
- Slight delay due to async processing