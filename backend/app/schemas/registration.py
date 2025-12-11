from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, ForwardRef
from app.schemas.event import EventResponse

class RegistrationCreate(BaseModel):
    """Schema for registering for an event"""
    event_id: int

class RegistrationResponse(BaseModel):
    """Schema for registration responses"""
    id: int
    user_id: int
    event_id: int
    registered_at: datetime
    is_cancelled: bool
    cancelled_at: Optional[datetime]
    
    # Include event details
    event_title: Optional[str] = None
    event_date: Optional[datetime] = None
    event_location: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class RegistrationWithDetails(RegistrationResponse):
    """Full registration with user and event details"""
    user_name: str
    user_email: str
    event: 'EventResponse'
    
    model_config = ConfigDict(from_attributes=True)
