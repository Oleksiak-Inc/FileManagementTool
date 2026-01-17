# --- /home/oleksiak/FileManagementTool/FileManagementSystem/app/services/attachment.py ---
import os
import shutil
import uuid
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_

from app.database.models import Attachment, Tester, Resolution
from app.schemas.attachment import AttachmentCreate, AttachmentUpdate
from app.config import settings


def get_attachment_by_id(db: Session, attachment_id: int) -> Optional[Attachment]:
    """Get a single attachment by ID with relationships."""
    return db.query(Attachment).filter(Attachment.id == attachment_id).first()


def get_attachments(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    filename: Optional[str] = None,
    uploaded_by: Optional[int] = None,
    resolution_id: Optional[int] = None,
    parent_attachment_id: Optional[int] = None,
    presentmon_file: Optional[bool] = None,
) -> List[Attachment]:
    """Get multiple attachments with optional filtering."""
    query = db.query(Attachment)

    if filename:
        query = query.filter(Attachment.filename.ilike(f"%{filename}%"))
    if uploaded_by is not None:
        query = query.filter(Attachment.uploaded_by == uploaded_by)
    if resolution_id is not None:
        query = query.filter(Attachment.resolution_id == resolution_id)
    if parent_attachment_id is not None:
        if parent_attachment_id == 0:  # Special case for root attachments
            query = query.filter(Attachment.parent_attachment_id.is_(None))
        else:
            query = query.filter(Attachment.parent_attachment_id == parent_attachment_id)
    if presentmon_file is not None:
        query = query.filter(Attachment.presentmon_file == presentmon_file)

    return query.order_by(Attachment.uploaded_at.desc()).offset(skip).limit(limit).all()


def create_attachment(db: Session, attachment_in: AttachmentCreate) -> Attachment:
    """Create a new attachment record."""
    # Check if uploader exists
    uploader = db.query(Tester).filter(Tester.id == attachment_in.uploaded_by).first()
    if not uploader:
        raise ValueError(f"Tester with ID {attachment_in.uploaded_by} does not exist")
    
    # Check if resolution exists if provided
    if attachment_in.resolution_id:
        resolution = db.query(Resolution).filter(Resolution.id == attachment_in.resolution_id).first()
        if not resolution:
            raise ValueError(f"Resolution with ID {attachment_in.resolution_id} does not exist")
    
    # Check if parent attachment exists if provided
    if attachment_in.parent_attachment_id:
        parent = db.query(Attachment).filter(Attachment.id == attachment_in.parent_attachment_id).first()
        if not parent:
            raise ValueError(f"Parent attachment with ID {attachment_in.parent_attachment_id} does not exist")
    
    attachment = Attachment(**attachment_in.dict())
    db.add(attachment)
    
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        if "foreign key constraint" in str(e).lower():
            if "uploaded_by" in str(e):
                raise ValueError(f"Invalid uploaded_by: {attachment_in.uploaded_by}")
            elif "resolution_id" in str(e):
                raise ValueError(f"Invalid resolution_id: {attachment_in.resolution_id}")
            elif "parent_attachment_id" in str(e):
                raise ValueError(f"Invalid parent_attachment_id: {attachment_in.parent_attachment_id}")
        else:
            raise ValueError(f"Database error: {e}")
    
    db.refresh(attachment)
    return attachment


def update_attachment(
    db: Session,
    attachment_id: int,
    attachment_in: AttachmentUpdate,
) -> Optional[Attachment]:
    """Update an existing attachment."""
    attachment = get_attachment_by_id(db, attachment_id)
    if not attachment:
        return None

    update_data = attachment_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(attachment, field, value)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        if "foreign key constraint" in str(e).lower():
            raise ValueError(f"Invalid foreign key reference in update data")
        else:
            raise ValueError(f"Database error: {e}")
    
    db.refresh(attachment)
    return attachment


def get_attachments_by_uploader(db: Session, uploader_id: int) -> List[Attachment]:
    """Get all attachments uploaded by a specific tester."""
    return db.query(Attachment).filter(Attachment.uploaded_by == uploader_id).all()


def get_attachment_tree(db: Session, parent_id: Optional[int] = None) -> List[Dict[str, Any]]:
    """Get attachments as a tree structure."""
    query = db.query(Attachment).filter(Attachment.parent_attachment_id == parent_id)
    attachments = query.all()
    
    result = []
    for attachment in attachments:
        attachment_dict = {
            "id": attachment.id,
            "filename": attachment.filename,
            "uploaded_by": attachment.uploaded_by,
            "uploaded_at": attachment.uploaded_at,
            "children": get_attachment_tree(db, attachment.id)
        }
        result.append(attachment_dict)
    
    return result


def get_root_attachments(db: Session) -> List[Attachment]:
    """Get all root attachments (without parent)."""
    return db.query(Attachment).filter(Attachment.parent_attachment_id.is_(None)).all()


def create_attachment_version(
    db: Session,
    original_attachment_id: int,
    new_filename: str,
    new_relative_path: str,
    uploaded_by: int
) -> Attachment:
    """Create a new version of an existing attachment."""
    original = get_attachment_by_id(db, original_attachment_id)
    if not original:
        raise ValueError(f"Original attachment with ID {original_attachment_id} does not exist")
    
    # Create new attachment as child of the original
    new_attachment_data = AttachmentCreate(
        parent_attachment_id=original_attachment_id,
        resolution_id=original.resolution_id,
        filename=new_filename,
        relative_path=new_relative_path,
        presentmon_file=original.presentmon_file,
        presentmon_version=original.presentmon_version,
        settings=original.settings,
        uploaded_by=uploaded_by
    )
    
    return create_attachment(db, new_attachment_data)