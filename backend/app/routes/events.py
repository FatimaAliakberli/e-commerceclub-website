from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.user import User
from app.schemas.event import (
    EventCreate, EventUpdate, EventResponse, EventListResponse
)
from app.schemas.registration import RegistrationResponse
from app.services.event_service import EventService
from app.utils.dependencies import get_current_user, get_current_admin
import math
from pydantic import BaseModel, field_validator, ConfigDict

router = APIRouter(tags=["Events"])

@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    event_data: EventCreate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a new event (Admin only)"""
    event = EventService.create_event(db, event_data, current_admin.id)
    return event

@router.get("/", response_model=EventListResponse)
async def list_events(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    include_past: bool = Query(False),
    include_inactive: bool = Query(False),
    db: Session = Depends(get_db)
):
    """List all events with pagination"""
    skip = (page - 1) * page_size
    
    events, total = EventService.get_events(
        db, 
        skip=skip, 
        limit=page_size,
        include_past=include_past,
        include_inactive=include_inactive
    )
    
    total_pages = math.ceil(total / page_size)
    
    return {
        "events": events,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }

@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific event by ID"""
    event = EventService.get_event(db, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return event

@router.put("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: int,
    event_data: EventUpdate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update an event (Admin only)"""
    event = EventService.update_event(db, event_id, event_data)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return event

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete an event (Admin only)"""
    success = EventService.delete_event(db, event_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return None

@router.get("/{event_id}/availability")
async def check_availability(
    event_id: int,
    db: Session = Depends(get_db)
):
    """Check event availability"""
    return EventService.check_availability(db, event_id)

@router.get("/{event_id}/participants", response_model=List[RegistrationResponse])
async def get_event_participants(
    event_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all participants for an event (Admin only)"""
    participants = EventService.get_event_participants(db, event_id)
    return participants
