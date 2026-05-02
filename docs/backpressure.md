# ⚡ Backpressure Handling

## Problem

In a production system, signals can arrive at very high rates (up to 10,000/sec).  
Directly writing to the database can cause:

- Database overload
- System crashes
- Data loss

## Solution

The system uses **Redis as a buffer layer**.

## Flow
Incoming Signals → Redis Queue → Worker → Database

## How it works

1. API receives signals
2. Signals are pushed to Redis (fast, in-memory)
3. Worker processes signals asynchronously
4. Database writes happen independently

## Benefits

- Prevents database overload
- Smooth handling of traffic spikes
- No data loss
- System remains responsive

## Additional Safeguards

- Rate limiting on API
- Async processing
- Queue decoupling