from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.models.work_item import Base


class RCA(Base):
    __tablename__ = "rca"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    work_item_id: Mapped[int] = mapped_column(Integer, ForeignKey("work_items.id"))

    root_cause: Mapped[str] = mapped_column(String(255))
    fix_applied: Mapped[str] = mapped_column(String(255))
    prevention: Mapped[str] = mapped_column(String(255))

    end_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)