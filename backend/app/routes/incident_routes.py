from fastapi import APIRouter, HTTPException
from sqlalchemy import select, case
from app.database import SessionLocal, mongo_db
from app.models.work_item import WorkItem
from app.models.rca import RCA
from datetime import datetime
from fastapi import Body

router = APIRouter(prefix="/api/incidents", tags=["Incidents"])


@router.get("")
async def get_incidents():
    async with SessionLocal() as session:
        result = await session.execute(
            select(WorkItem).order_by(
                case(
                    (WorkItem.status == "OPEN", 1),
                    (WorkItem.status == "INVESTIGATING", 2),
                    (WorkItem.status == "RESOLVED", 3),
                    (WorkItem.status == "CLOSED", 4),
                    else_=5
                ),
                case(
                    (WorkItem.severity == "P0", 1),
                    (WorkItem.severity == "P1", 2),
                    (WorkItem.severity == "P2", 3),
                    else_=4
                ),
                WorkItem.id.desc()
            )
        )

        incidents = result.scalars().all()

        return [
            {
                "id": i.id,
                "component_id": i.component_id,
                "component_type": i.component_type,
                "severity": i.severity,
                "status": i.status,
                "title": i.title,
                "start_time": i.start_time,
                "created_at": i.created_at
            }
            for i in incidents
        ]


@router.get("/{incident_id}")
async def get_incident(incident_id: int):
    async with SessionLocal() as session:
        incident = await session.get(WorkItem, incident_id)

        if not incident:
            raise HTTPException(status_code=404, detail="Incident not found")

        return {
            "id": incident.id,
            "component_id": incident.component_id,
            "component_type": incident.component_type,
            "severity": incident.severity,
            "status": incident.status,
            "title": incident.title,
            "start_time": incident.start_time,
            "created_at": incident.created_at
        }


@router.get("/{incident_id}/signals")
async def get_incident_signals(incident_id: int):
    signals = []

    cursor = mongo_db.signals.find({"work_item_id": incident_id})

    async for signal in cursor:
        signal["_id"] = str(signal["_id"])
        signals.append(signal)

    return signals


@router.post("/{incident_id}/rca")
async def submit_rca(incident_id: int, data: dict):
    async with SessionLocal() as session:
        incident = await session.get(WorkItem, incident_id)

        if not incident:
            raise HTTPException(status_code=404, detail="Incident not found")

        rca = RCA(
            work_item_id=incident_id,
            root_cause=data.get("root_cause"),
            fix_applied=data.get("fix_applied"),
            prevention=data.get("prevention"),
            end_time=datetime.utcnow()
        )

        session.add(rca)

        # MTTR calculation
        mttr_seconds = (rca.end_time - incident.start_time).total_seconds()

        await session.commit()

        return {
            "message": "RCA submitted successfully. Use status API to close incident",
            "mttr_seconds": mttr_seconds
        }
    


@router.patch("/{incident_id}/status")
async def update_status(
    incident_id: int,
    data: dict = Body(...)
):
    new_status = data.get("status")

    valid_status = ["OPEN", "INVESTIGATING", "RESOLVED", "CLOSED"]

    if new_status not in valid_status:
        raise HTTPException(status_code=400, detail="Invalid status")

    async with SessionLocal() as session:
        incident = await session.get(WorkItem, incident_id)

        if not incident:
            raise HTTPException(status_code=404, detail="Incident not found")

        # 🚫 Block CLOSED without RCA
        if new_status == "CLOSED":
            result = await session.execute(
                select(RCA).where(RCA.work_item_id == incident_id)
            )
            rca = result.scalar_one_or_none()

            if not rca:
                raise HTTPException(
                    status_code=400,
                    detail="Cannot close incident without RCA"
                )

        incident.status = new_status
        await session.commit()

        return {"message": f"Status updated to {new_status}"}