from fastapi import BackgroundTasks
from app.models.event import Event
from app.services.email import send_event_registration_confirmation

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.schemas.registration import (
    RegistrationCreate, RegistrationResponse, RegistrantListResponse
)
from app.services.registration_service import RegistrationService
from app.utils.dependencies import get_current_user, get_current_admin

router = APIRouter(tags=["Registrations"])

@router.post("/", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
async def register_for_event(
    registration_data: RegistrationCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Register current user for an event"""
    registration = RegistrationService.register_for_event(
        db,
        event_id=registration_data.event_id,
        user_id=current_user.id
    )

    event = db.query(Event).filter(Event.id == registration_data.event_id).first()
    if event:
        background_tasks.add_task(
            send_event_registration_confirmation,
            current_user.email,
            current_user.full_name,
            event.title,
            event.event_date,
            event.event_time,
            event.location
        )

    return registration


@router.get("/my-registrations", response_model=List[RegistrationResponse])
async def get_my_registrations(
    include_cancelled: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's registrations"""
    registrations = RegistrationService.get_user_registrations(
        db,
        user_id=current_user.id,
        include_cancelled=include_cancelled
    )
    return registrations

@router.delete("/{registration_id}", status_code=status.HTTP_200_OK)
async def cancel_registration(
    registration_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel a registration (24+ hours before event)"""
    registration = RegistrationService.cancel_registration(
        db,
        registration_id=registration_id,
        user_id=current_user.id
    )
    return {
        "message": "Registration cancelled successfully",
        "registration_id": registration.id
    }


@router.get("/event/{event_id}/registrants", response_model=List[RegistrantListResponse]) 
def get_registrants_for_event(
    event_id: int,
    current_admin: User = Depends(get_current_admin), # 💥 ADDED: Requires admin status
    db: Session = Depends(get_db)
):
    registrations = RegistrationService.get_registrants_by_event_id(db, event_id=event_id)
    return registrations


@router.get("/{registration_id}", response_model=RegistrationResponse)
async def get_registration(
    registration_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific registration"""
    registration = RegistrationService.get_registration(db, registration_id)
    
    if registration is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )
    
    # Verify ownership
    if registration.user_id != current_user.id: # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this registration"
        )
    
    return registration
