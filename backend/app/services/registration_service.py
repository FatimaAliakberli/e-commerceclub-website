from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.orm import selectinload
from app.models.event import Event
from app.models.registration import Registration
from app.models.user import User
from datetime import datetime
from fastapi import HTTPException, status
from typing import List, Optional

class RegistrationService:
    """Service layer for registration operations"""
    
    @staticmethod
    def register_for_event(
        db: Session,
        event_id: int,
        user_id: int
    ) -> Registration:
        """Register a user for an event"""
        
        # Get event
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )
        
        # Check if event is active
        if not event.is_active:  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Event is not active"
            )
        
        # Check registration deadline
        if datetime.utcnow() > event.registration_deadline:  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration deadline has passed"
            )
        
        # Check capacity
        if event.current_registrations >= event.capacity:  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Event is at full capacity"
            )
        
        # Check for duplicate registration
        existing = db.query(Registration).filter(
            and_(
                Registration.event_id == event_id,
                Registration.user_id == user_id,
                Registration.is_cancelled.is_(False)
            )
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You are already registered for this event"
            )
        
        # Create registration
        registration = Registration(
            user_id=user_id,
            event_id=event_id
        )
        
        # Update event registration count
        event.current_registrations = event.current_registrations + 1  # type: ignore
        
        db.add(registration)
        db.commit()
        db.refresh(registration)
        
        return registration
    
    @staticmethod
    def cancel_registration(
        db: Session,
        registration_id: int,
        user_id: int
    ) -> Registration:
        """Cancel a registration"""
        
        registration = db.query(Registration).filter(
            Registration.id == registration_id
        ).first()
        
        if not registration:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registration not found"
            )
        
        # Verify ownership
        if registration.user_id != user_id:  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to cancel this registration"
            )
        
        # Check if already cancelled
        if registration.is_cancelled:  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration is already cancelled"
            )
        
        # Check 24-hour rule
        event = db.query(Event).filter(Event.id == registration.event_id).first()
        hours_until_event = (
            event.event_date - datetime.utcnow()  # type: ignore
        ).total_seconds() / 3600
        
        if hours_until_event < 24:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot cancel within 24 hours of event"
            )
        
        # Cancel registration
        registration.is_cancelled = True  # type: ignore
        registration.cancelled_at = datetime.utcnow()  # type: ignore
        
        # Update event registration count
        event.current_registrations = event.current_registrations - 1  # type: ignore
        
        db.commit()
        db.refresh(registration)
        
        return registration
    
    # --- NEW METHOD FOR ADMIN VIEW ---
    @staticmethod
    def get_registrants_by_event_id(
        
        db: Session,
        event_id: int
    ) -> List[Registration]:
        """
        ADMIN FUNCTION: Get a list of all active (non-cancelled) registrations for an event,
        eagerly loading the related User object.
        """
        # Use .options(selectinload(Registration.user)) to tell SQLAlchemy
        # to fetch the related 'user' data in the same transaction.
        return db.query(Registration).options(
            selectinload(Registration.user)
        ).filter(
            and_(
                Registration.event_id == event_id,
                Registration.is_cancelled.is_(False)
            )
        ).all()
    
    @staticmethod
    def get_user_registrations(
        db: Session,
        user_id: int,
        include_cancelled: bool = False
    ) -> List[Registration]:
        """Get all registrations for a user"""
        query = db.query(Registration).filter(Registration.user_id == user_id)
        
        if not include_cancelled:
            query = query.filter(Registration.is_cancelled.is_(False))  # type: ignore
        
        return query.order_by(Registration.registered_at.desc()).all()
    
    @staticmethod
    def get_registration(
        db: Session,
        registration_id: int
    ) -> Optional[Registration]:
        """Get a specific registration"""
        return db.query(Registration).filter(Registration.id == registration_id).first()
