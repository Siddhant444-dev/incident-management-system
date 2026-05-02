from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as redis

from app.config import settings

# PostgreSQL
engine = create_async_engine(settings.postgres_url, echo=True)
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# MongoDB
mongo_client = AsyncIOMotorClient(settings.mongo_url)
mongo_db = mongo_client["ims_db"]

# Redis
redis_client = redis.from_url(settings.redis_url, decode_responses=True)

async def init_db():
    from app.models.work_item import Base

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)