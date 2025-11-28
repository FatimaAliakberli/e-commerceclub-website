from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base

class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, nullable=False)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class PageContent(Base):
    __tablename__ = "page_content"

    id = Column(Integer, primary_key=True, index=True)
    page_name = Column(String, unique=True, nullable=False)
    content = Column(Text, nullable=False)
    updated_by = Column(Integer, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())