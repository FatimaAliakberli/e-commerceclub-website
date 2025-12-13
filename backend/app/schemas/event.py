from datetime import datetime
from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional


class EventBase(BaseModel):
    title: str
    description: str
    event_date: datetime      # Pydantic accepts full datetime string (YYYY-MM-DDTHH:MM)
    event_time: Optional[str] = None
    location: str
    capacity: int
    registration_deadline: datetime
    image_url: str | None = None


class EventCreate(EventBase):

    # Validate that deadline < event_date
    @field_validator("registration_deadline")
    def validate_deadline(cls, v, info):
        event_date = info.data.get("event_date")
        if event_date and v >= event_date:
            raise ValueError("registration_deadline must be before event_date")
        return v


class EventUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    event_date: datetime | None = None
    event_time: str | None = None
    location: str | None = None
    capacity: int | None = None
    registration_deadline: datetime | None = None
    image_url: str | None = None
    is_active: bool | None = None


class EventResponse(EventBase):
    id: int
    current_registrations: int
    is_active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class EventListResponse(BaseModel):
    events: list[EventResponse]

    model_config = ConfigDict(from_attributes=True)
