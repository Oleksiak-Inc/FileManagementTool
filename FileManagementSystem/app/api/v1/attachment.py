# --- /home/oleksiak/FileManagementTool/FileManagementSystem/app/api/v1/attachment.py ---
import os
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.api.dependencies import get_current_tester
from app.database.models import Tester as TesterModel
from app.schemas.attachment import (
    AttachmentCreate,
    AttachmentUpdate,
    AttachmentResponse,
    AttachmentWithRelationsResponse,
    FileUploadResponse
)
from app.services.attachment import (
    get_attachments,
    get_attachment_by_id,
    create_attachment,
    update_attachment,
    get_attachments_by_uploader,
    get_attachment_tree,
    get_root_attachments,
    create_attachment_version
)
from app.utils.files import file_storage, validate_file_upload
from app.config import settings

router = APIRouter(prefix="/attachments", tags=["attachments"])


@router.get("/", response_model=List[AttachmentResponse])
def read_attachments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    filename: Optional[str] = None,
    uploaded_by: Optional[int] = None,
    resolution_id: Optional[int] = None,
    parent_attachment_id: Optional[int] = None,
    presentmon_file: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get all attachments with optional filtering."""
    return get_attachments(
        db=db,
        skip=skip,
        limit=limit,
        filename=filename,
        uploaded_by=uploaded_by,
        resolution_id=resolution_id,
        parent_attachment_id=parent_attachment_id,
        presentmon_file=presentmon_file,
    )


@router.get("/{attachment_id}", response_model=AttachmentWithRelationsResponse)
def read_attachment(
    attachment_id: int,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get a specific attachment by ID."""
    attachment = get_attachment_by_id(db, attachment_id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    return attachment


@router.get("/{attachment_id}/download")
def download_attachment(
    attachment_id: int,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Download an attachment file."""
    attachment = get_attachment_by_id(db, attachment_id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    
    file_path = file_storage.get_file_path(attachment.relative_path, attachment.filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on server")
    
    return FileResponse(
        path=file_path,
        filename=attachment.filename,
        media_type='application/octet-stream'
    )


@router.get("/{attachment_id}/preview")
def preview_attachment(
    attachment_id: int,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Preview an attachment (if it's an image or text file)."""
    attachment = get_attachment_by_id(db, attachment_id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    
    file_path = file_storage.get_file_path(attachment.relative_path, attachment.filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on server")
    
    mime_type = file_storage.get_mime_type(attachment.filename)
    
    if mime_type.startswith('image/'):
        return FileResponse(
            path=file_path,
            filename=attachment.filename,
            media_type=mime_type
        )
    elif mime_type.startswith('text/'):
        with open(file_path, 'r') as f:
            content = f.read()
        return {"content": content, "filename": attachment.filename, "mime_type": mime_type}
    else:
        raise HTTPException(status_code=400, detail="File type not previewable")


@router.post("/upload", response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    resolution_id: Optional[int] = Form(None),
    parent_attachment_id: Optional[int] = Form(None),
    presentmon_file: bool = Form(False),
    presentmon_version: Optional[str] = Form(None),
    subdirectory: str = Form(""),
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Upload a new file and create an attachment record."""
    try:
        # Validate the file
        validate_file_upload(file)
        
        # Save the file to disk
        filename, relative_path, full_path = file_storage.save_file(file, subdirectory)
        
        # Create attachment record
        attachment_data = AttachmentCreate(
            parent_attachment_id=parent_attachment_id,
            resolution_id=resolution_id,
            filename=filename,
            relative_path=relative_path,
            presentmon_file=presentmon_file,
            presentmon_version=presentmon_version,
            uploaded_by=current_tester.id
        )
        
        attachment = create_attachment(db, attachment_data)
        
        # Construct file URL
        file_url = f"/api/v1/attachments/{attachment.id}/download"
        
        return FileUploadResponse(
            message="File uploaded successfully",
            attachment_id=attachment.id,
            filename=filename,
            file_path=full_path,
            file_url=file_url
        )
        
    except Exception as e:
        # Clean up file if there was an error
        if 'full_path' in locals():
            try:
                os.remove(full_path)
            except:
                pass
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{attachment_id}/version", response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED)
async def create_version(
    attachment_id: int,
    file: UploadFile = File(...),
    subdirectory: str = Form(""),
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Create a new version of an existing attachment."""
    try:
        # Validate the file
        validate_file_upload(file)
        
        # Save the file to disk
        filename, relative_path, full_path = file_storage.save_file(file, subdirectory)
        
        # Create new attachment version
        new_attachment = create_attachment_version(
            db,
            attachment_id,
            filename,
            relative_path,
            current_tester.id
        )
        
        # Construct file URL
        file_url = f"/api/v1/attachments/{new_attachment.id}/download"
        
        return FileUploadResponse(
            message="New version created successfully",
            attachment_id=new_attachment.id,
            filename=filename,
            file_path=full_path,
            file_url=file_url
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Clean up file if there was an error
        if 'full_path' in locals():
            try:
                os.remove(full_path)
            except:
                pass
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/uploader/{uploader_id}", response_model=List[AttachmentResponse])
def read_attachments_by_uploader(
    uploader_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get all attachments uploaded by a specific tester."""
    attachments = get_attachments_by_uploader(db, uploader_id)
    return attachments[skip:skip + limit]


@router.get("/tree/structure", response_model=List[dict])
def read_attachment_tree(
    parent_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get attachments in a tree structure."""
    return get_attachment_tree(db, parent_id)


@router.get("/tree/roots", response_model=List[AttachmentResponse])
def read_root_attachments(
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get all root attachments (without parent)."""
    return get_root_attachments(db)


@router.patch("/{attachment_id}", response_model=AttachmentResponse)
def update_existing_attachment(
    attachment_id: int,
    attachment_data: AttachmentUpdate,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Update an existing attachment's metadata."""
    attachment = get_attachment_by_id(db, attachment_id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    
    # Check permissions - only uploader or admin can update
    if attachment.uploaded_by != current_tester.id and current_tester.tester_type_id not in [1, 2]:
        raise HTTPException(status_code=403, detail="Not authorized to update this attachment")
    
    try:
        updated = update_attachment(db, attachment_id, attachment_data)
        if not updated:
            raise HTTPException(status_code=404, detail="Attachment not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))