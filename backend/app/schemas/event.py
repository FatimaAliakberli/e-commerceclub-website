from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime


class EventBase(BaseModel):
    title: str
    description: str
    event_date: datetime
    event_time: str
    location: str
    capacity: int
    registration_deadline: datetime
    image_url: Optional[str] = None

    @validator("capacity")
    def validate_capacity(cls, v):
        if v < 1:
            raise ValueError("Capacity must be at least 1")
        if v > 1000:
            raise ValueError("Capacity cannot exceed 1000")
        return v

    @validator("registration_deadline")
    def validate_deadline(cls, v, values):
        if "event_date" in values and v >= values["event_date"]:
            raise ValueError("Registration deadline must be before event date")
        return v


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    event_date: Optional[datetime] = None
    event_time: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[int] = None
    registration_deadline: Optional[datetime] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class EventResponse(EventBase):
    id: int
    current_registrations: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class EventListResponse(BaseModel):
    events: list[EventResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
