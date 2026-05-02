import json
from app.database import redis_client, mongo_db, SessionLocal
from app.models.work_item import WorkItem


async def process_signals():
    last_id = "0-0"

    while True:
        response = await redis_client.xread(
            {"signal_stream": last_id},
            count=10,
            block=5000
        )

        if not response:
            continue

        for stream, messages in response:
            for msg_id, data in messages:
                signal = json.loads(data["data"])

                component_id = signal.get("component_id")
                if not component_id:
                   print("Skipped invalid signal:", signal)
                   continue
                component_type = signal.get("component_type", "UNKNOWN")
                severity = signal.get("severity", "P3")
                message = signal.get("message", "Incident detected")

                debounce_key = f"debounce:{component_id}"
                existing_work_item_id = await redis_client.get(debounce_key)

                if existing_work_item_id:
                    work_item_id = int(existing_work_item_id)
                    print(f"Debounced signal linked to incident {work_item_id}")
                else:
                    async with SessionLocal() as session:
                        work_item = WorkItem(
                            component_id=component_id,
                            component_type=component_type,
                            severity=severity,
                            status="OPEN",
                            title=f"{severity} incident on {component_id}: {message}"
                        )

                        session.add(work_item)
                        await session.commit()
                        await session.refresh(work_item)

                        work_item_id = work_item.id

                    await redis_client.setex(debounce_key, 10, str(work_item_id))
                    print(f"New incident created: {work_item_id}")

                signal["work_item_id"] = work_item_id
                await mongo_db.signals.insert_one(signal)

                last_id = msg_id