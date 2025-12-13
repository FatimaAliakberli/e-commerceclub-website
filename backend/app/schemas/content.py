# schemas/content.py
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

# --- Base Schema (Shared Configuration) ---
class BaseSchema(BaseModel):
    # This configuration makes Pydantic models compatible with SQLAlchemy ORM
    model_config = ConfigDict(from_attributes=True)

# ====================================================================
# 1. ANNOUNCEMENT SCHEMAS
# ====================================================================

# Schema for creating a new announcement (Admin sends this data)
class AnnouncementCreate(BaseModel):
    title: str = Field(..., max_length=255)
    content: str
    is_published: bool = Field(True, description="Whether the announcement should be immediately visible.")

# Schema for updating an existing announcement (Admin sends this data)
class AnnouncementUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = None
    is_published: Optional[bool] = None

# Schema for responding with announcement data (API sends this back)
class AnnouncementResponse(BaseSchema):
    id: int
    title: str
    content: str
    author_id: int
    is_published: bool
    created_at: datetime
    updated_at: Optional[datetime] = None


# ====================================================================
# 2. PAGE CONTENT SCHEMAS
# ====================================================================

# Schema for updating page content (Admin sends this data)
class PageContentUpdate(BaseModel):
    content: str = Field(..., description="The full HTML or text content for the page block.")

# Schema for responding with page content data (API sends this back)
class PageContentResponse(BaseSchema):
    id: int
    page_name: str
    content: str
    updated_by: int
    updated_at: Optional[datetime] = None