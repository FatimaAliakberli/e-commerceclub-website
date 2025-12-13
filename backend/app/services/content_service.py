# services/content_service.py

from sqlalchemy.orm import Session
from app.models.content import Announcement, PageContent
from app.schemas.content import AnnouncementCreate, AnnouncementUpdate, PageContentUpdate
from typing import List, Optional
from datetime import datetime

class ContentService:

    # --- ANNOUNCEMENT LOGIC (CRUD) ---

    @staticmethod
    def create_announcement(db: Session, announcement_data: AnnouncementCreate, author_id: int) -> Announcement:
        """Creates a new announcement."""
        db_announcement = Announcement(
            title=announcement_data.title,
            content=announcement_data.content,
            author_id=author_id,
            is_published=announcement_data.is_published
        )
        db.add(db_announcement)
        db.commit()
        db.refresh(db_announcement)
        return db_announcement

    @staticmethod
    def get_announcements(db: Session, include_unpublished: bool = False) -> List[Announcement]:
        """Retrieves announcements. Can include unpublished for admin view."""
        query = db.query(Announcement)
        if not include_unpublished:
            # Filter for publicly visible announcements
            query = query.filter(Announcement.is_published == True)
        
        # Order by creation date to show newest first
        return query.order_by(Announcement.created_at.desc()).all()

    @staticmethod
    def get_announcement_by_id(db: Session, announcement_id: int) -> Optional[Announcement]:
        """Retrieves a single announcement by ID."""
        return db.query(Announcement).filter(Announcement.id == announcement_id).first()

    @staticmethod
    def update_announcement(db: Session, announcement_id: int, update_data: AnnouncementUpdate) -> Optional[Announcement]:
        """Updates an existing announcement."""
        db_announcement = ContentService.get_announcement_by_id(db, announcement_id)
        
        if not db_announcement:
            return None # Not found

        # Use Pydantic's model_dump to get only the fields that were set (excluding None/unset values)
        update_data_dict = update_data.model_dump(exclude_unset=True)
        
        for key, value in update_data_dict.items():
            setattr(db_announcement, key, value)
        
        # Manually update 'updated_at' if needed, though your model handles it with onupdate=func.now()
        
        db.commit()
        db.refresh(db_announcement)
        return db_announcement

    @staticmethod
    def delete_announcement(db: Session, announcement_id: int) -> bool:
        """Deletes an announcement."""
        db_announcement = ContentService.get_announcement_by_id(db, announcement_id)
        if not db_announcement:
            return False # Not found
        
        db.delete(db_announcement)
        db.commit()
        return True

    # --- PAGECONTENT LOGIC (Read/Create/Update) ---
    
    @staticmethod
    def get_page_content(db: Session, page_name: str) -> Optional[PageContent]:
        """Retrieves content for a specific named page block."""
        return db.query(PageContent).filter(PageContent.page_name == page_name).first()

    @staticmethod
    def update_page_content(db: Session, page_name: str, update_data: PageContentUpdate, updated_by_id: int) -> PageContent:
        """
        Updates content for a specific named page block. If it doesn't exist, it creates it.
        This allows the admin to set up new content blocks on the fly.
        """
        db_content = ContentService.get_page_content(db, page_name)
        
        if db_content:
            # Update existing content
            db_content.content = update_data.content
            db_content.updated_by = updated_by_id
        else:
            # Create content if it doesn't exist (First time setup)
            db_content = PageContent(
                page_name=page_name,
                content=update_data.content,
                updated_by=updated_by_id
            )
            db.add(db_content)

        db.commit()
        db.refresh(db_content)
        return db_content