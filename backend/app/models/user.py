from sqlalchemy import Column, Integer, String, Boolean, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(length=255), unique=True, index=True, nullable=False)
    full_name = Column(String(length=100), nullable=False)
    hashed_password = Column(String(length=128), nullable=False)

    # --- RESTORED & NEW FIELDS ---
    
    # 1. RESTORED: Phone Number
    phone_number = Column(String(length=20), nullable=True) # Added max length for DB
    
    # 2. RESTORED: Flag for conditional logic
    is_university_student = Column(Boolean, default=True) 
    
    # 3. NEW: University Student ID (5 digits)
    # Note: Nullable=True because it's only required if is_university_student is True
    student_id = Column(String(length=15), index=True, nullable=True) 
    
    # 4. NEW: National ID/PIN (7 alphanumeric)
    # Note: Nullable=True because it's only required if is_university_student is False
    national_id = Column(String(length=15), index=True, nullable=True) 
    
    # --- END RESTORED & NEW FIELDS ---

    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        # 1. Student ID Uniqueness: Only apply uniqueness IF is_university_student is True
        # If is_university_student=False (0), the unique constraint is effectively bypassed.
        UniqueConstraint(student_id, is_university_student, name='uq_student_id_conditional'),
        
        # 2. National ID Uniqueness: Only apply uniqueness IF is_university_student is False
        # MySQL treats (NULL, 1) and (NULL, 1) as non-unique, but (ID, 1) and (ID, 1) as unique.
        # By including the flag, we ensure that when the ID is present, the combination is unique.
        UniqueConstraint(national_id, is_university_student, name='uq_national_id_conditional'),

        # Note: If your MySQL version supports functional indexes, a better approach might exist, 
        # but this is the most common cross-dialect solution.
    )
