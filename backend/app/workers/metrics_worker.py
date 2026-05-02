import asyncio
from app.database import redis_client


async def print_throughput_metrics():
    last_count = 0

    while True:
        await asyncio.sleep(5)

        current_count = await redis_client.get("metrics:signals_ingested")
        current_count = int(current_count or 0)

        signals_in_5_sec = current_count - last_count
        signals_per_sec = signals_in_5_sec / 5

        queue_length = await redis_client.xlen("signal_stream")

        print(
            f"[METRICS] Throughput: {signals_per_sec:.2f} signals/sec | "
            f"Queue length: {queue_length}"
        )

        last_count = current_count