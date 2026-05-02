from fastapi import APIRouter, HTTPException, Request
from app.database import redis_client
from datetime import datetime
import json

router = APIRouter(prefix="/api", tags=["Signals"])

RATE_LIMIT = 100
WINDOW_SECONDS = 60

@router.post("/signals")
async def ingest_signal(signal: dict, request: Request):
    client_ip = request.client.host if request.client else "unknown"
    rate_key = f"rate_limit:{client_ip}"

    current_count = await redis_client.incr(rate_key)

    if current_count == 1:
        await redis_client.expire(rate_key, WINDOW_SECONDS)

    if current_count > RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Try again later."
        )

    signal["received_at"] = datetime.utcnow().isoformat()

    await redis_client.xadd(
        "signal_stream",
        {"data": json.dumps(signal)}
    )

    await redis_client.incr("metrics:signals_ingested")

    return {
        "status": "queued",
        "message": "Signal accepted for async processing"
    }