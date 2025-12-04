from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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
    
    class Config:
        from_attributes = True

class RegistrationWithDetails(RegistrationResponse):
    """Full registration with user and event details"""
    user_name: str
    user_email: str
    event: 'EventResponse'
    
    class Config:
        from_attributes = True