from contextlib import asynccontextmanager
import asyncio

from fastapi import FastAPI
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, init_db
from app.routes.incident_routes import router as incident_router
from app.routes.signal_routes import router as signal_router
from app.workers.signal_worker import process_signals
from app.workers.metrics_worker import print_throughput_metrics


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    asyncio.create_task(process_signals())
    asyncio.create_task(print_throughput_metrics())

    yield

    print("IMS Backend shutting down...")


app = FastAPI(
    title="IMS Backend",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(signal_router)
app.include_router(incident_router)


@app.get("/")
def root():
    return {"message": "IMS Running"}


@app.get("/health")
async def health():
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "UP"}
    except Exception as e:
        return {"status": "DOWN", "error": str(e)}