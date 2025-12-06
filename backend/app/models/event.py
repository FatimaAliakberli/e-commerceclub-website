from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, DateTime, Boolean, Integer
from sqlalchemy.sql import func
from app.database import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    # Important: annotate with Python datetime (NOT SQLAlchemy DateTime)
    event_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    registration_deadline: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    event_time: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)

    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    current_registrations: Mapped[int] = mapped_column(Integer, default=0)

    image_url: Mapped[str | None] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
