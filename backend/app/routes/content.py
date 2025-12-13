# routes/content.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
# Assuming your schemas are defined here:
from app.schemas.content import (
    AnnouncementCreate, AnnouncementUpdate, AnnouncementResponse,
    PageContentResponse, PageContentUpdate
)
# Assuming your service layer is defined here:
from app.services.content_service import ContentService
from app.utils.dependencies import get_current_user, get_current_admin

router = APIRouter(prefix="/api/content", tags=["Content & Announcements"])

# --- PUBLIC ROUTES (Read Access) ---

@router.get("/announcements", response_model=List[AnnouncementResponse])
async def list_published_announcements(db: Session = Depends(get_db)):
    """
    Retrieve a list of all CURRENTLY PUBLISHED announcements for public display.
    """
    announcements = ContentService.get_announcements(db, include_unpublished=False)
    return announcements

@router.get("/pages/{page_name}", response_model=PageContentResponse)
async def get_page_content_by_name(page_name: str, db: Session = Depends(get_db)):
    """
    Retrieve the content block for a specific named page (e.g., 'about_us').
    """
    page_content = ContentService.get_page_content(db, page_name)
    if not page_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content for page '{page_name}' not found."
        )
    return page_content

# --- ADMIN ROUTES (Write Access) ---
# All routes below use 'get_current_admin'

@router.post("/announcements", response_model=AnnouncementResponse, status_code=status.HTTP_201_CREATED)
async def create_announcement(
    announcement_data: AnnouncementCreate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a new announcement. (Admin only)"""
    new_announcement = ContentService.create_announcement(
        db, 
        announcement_data, 
        current_admin.id
    )
    return new_announcement

@router.get("/admin/announcements", response_model=List[AnnouncementResponse])
async def list_all_announcements(
    include_unpublished: bool = Query(True), # Admin can see all, including drafts
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """List ALL announcements, including unpublished drafts. (Admin only)"""
    announcements = ContentService.get_announcements(db, include_unpublished=include_unpublished)
    return announcements

@router.put("/announcements/{announcement_id}", response_model=AnnouncementResponse)
async def update_announcement(
    announcement_id: int,
    update_data: AnnouncementUpdate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update an existing announcement's title, content, or published status. (Admin only)"""
    updated_announcement = ContentService.update_announcement(db, announcement_id, update_data)
    if not updated_announcement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Announcement not found"
        )
    return updated_announcement

@router.delete("/announcements/{announcement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_announcement(
    announcement_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete an announcement. (Admin only)"""
    if not ContentService.delete_announcement(db, announcement_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Announcement not found"
        )
    return None

@router.put("/pages/{page_name}", response_model=PageContentResponse)
async def update_page_content(
    page_name: str,
    content_data: PageContentUpdate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Create or update the content block for a specific named page. (Admin only)
    """
    updated_content = ContentService.update_page_content(
        db, 
        page_name, 
        content_data, 
        current_admin.id
    )
    return updated_content