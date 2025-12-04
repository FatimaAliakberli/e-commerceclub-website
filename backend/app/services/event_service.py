from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from app.models.event import Event
from app.models.registration import Registration
from app.schemas.event import EventCreate, EventUpdate
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from typing import Optional, List

class EventService:
    """Service layer for event operations"""
    
    @staticmethod
    def create_event(db: Session, event_data: EventCreate, admin_id: int) -> Event:
        """Create a new event"""
        event = Event(
            title=event_data.title,
            description=event_data.description,
            event_date=event_data.event_date,
            event_time=event_data.event_time,
            location=event_data.location,
            capacity=event_data.capacity,
            registration_deadline=event_data.registration_deadline,
            image_url=event_data.image_url,
        )
        
        db.add(event)
        db.commit()
        db.refresh(event)
        return event
    
    @staticmethod
    def get_event(db: Session, event_id: int) -> Optional[Event]:
        """Get event by ID"""
        return db.query(Event).filter(Event.id == event_id).first()
    
    @staticmethod
    def get_events(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        include_past: bool = False,
        include_inactive: bool = False
    ) -> tuple[List[Event], int]:
        """Get list of events with pagination"""
        query = db.query(Event)
        
        # Filter conditions
        filters = []
        if not include_past:
            filters.append(Event.event_date >= datetime.utcnow())
        if not include_inactive:
            filters.append(Event.is_active == True)
        
        if filters:
            query = query.filter(and_(*filters))
        
        # Get total count
        total = query.count()
        
        # Apply pagination and sorting
        events = query.order_by(Event.event_date.asc()).offset(skip).limit(limit).all()
        
        return events, total
    
    @staticmethod
    def update_event(
        db: Session,
        event_id: int,
        event_data: EventUpdate
    ) -> Optional[Event]:
        """Update an event"""
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            return None
        
        # Update only provided fields
        update_data = event_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(event, field, value)
        
        db.commit()
        db.refresh(event)
        return event
    
    @staticmethod
    def delete_event(db: Session, event_id: int) -> bool:
        """Delete an event (soft delete by setting inactive)"""
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            return False
        
        # Check if there are active registrations
        active_registrations = db.query(Registration).filter(
            Registration.event_id == event_id,
            Registration.is_cancelled == False
        ).count()
        
        if active_registrations > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot delete event with {active_registrations} active registrations"
            )
        
        # Soft delete
        event.is_active = False
        db.commit()
        return True
    
    @staticmethod
    def get_event_participants(db: Session, event_id: int) -> List[Registration]:
        """Get all participants for an event"""
        return db.query(Registration).filter(
            Registration.event_id == event_id,
            Registration.is_cancelled == False
        ).all()
    
    @staticmethod
    def check_availability(db: Session, event_id: int) -> dict:
        """Check event availability"""
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )
        
        return {
            "capacity": event.capacity,
            "current_registrations": event.current_registrations,
            "available_spots": event.capacity - event.current_registrations,
            "is_full": event.current_registrations >= event.capacity,
            "registration_open": datetime.utcnow() < event.registration_deadline
        }