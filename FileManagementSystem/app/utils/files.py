# --- /home/oleksiak/FileManagementTool/FileManagementSystem/app/utils/files.py ---
import os
import shutil
import uuid
from pathlib import Path
from typing import Tuple, Optional
from fastapi import UploadFile, HTTPException
import mimetypes


class FileStorage:
    def __init__(self, base_path: str = "uploads"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def generate_unique_filename(self, original_filename: str) -> str:
        """Generate a unique filename to avoid collisions."""
        ext = original_filename.split('.')[-1] if '.' in original_filename else ''
        unique_id = uuid.uuid4().hex
        if ext:
            return f"{unique_id}.{ext}"
        return unique_id
    
    def create_subdirectory(self, directory_name: str) -> Path:
        """Create a subdirectory for organizing files."""
        subdir = self.base_path / directory_name
        subdir.mkdir(parents=True, exist_ok=True)
        return subdir
    
    def save_file(self, file: UploadFile, subdirectory: str = "") -> Tuple[str, str, str]:
        """Save an uploaded file and return (filename, relative_path, full_path)."""
        # Generate unique filename
        unique_filename = self.generate_unique_filename(file.filename)
        
        # Determine subdirectory path
        if subdirectory:
            save_dir = self.create_subdirectory(subdirectory)
        else:
            save_dir = self.base_path
        
        # Full path for saving
        full_path = save_dir / unique_filename
        
        # Save the file
        with open(full_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Get relative path from base directory
        relative_path = str(save_dir.relative_to(self.base_path)) if subdirectory else ""
        
        return unique_filename, relative_path, str(full_path)
    
    def get_file_path(self, relative_path: str, filename: str) -> Path:
        """Get the full path to a stored file."""
        if relative_path:
            return self.base_path / relative_path / filename
        return self.base_path / filename
    
    def file_exists(self, relative_path: str, filename: str) -> bool:
        """Check if a file exists."""
        file_path = self.get_file_path(relative_path, filename)
        return file_path.exists()
    
    def delete_file(self, relative_path: str, filename: str) -> bool:
        """Delete a stored file."""
        file_path = self.get_file_path(relative_path, filename)
        if file_path.exists():
            file_path.unlink()
            
            # Try to remove empty directory
            if relative_path:
                dir_path = self.base_path / relative_path
                if dir_path.exists() and not any(dir_path.iterdir()):
                    dir_path.rmdir()
            return True
        return False
    
    def get_file_size(self, relative_path: str, filename: str) -> int:
        """Get the size of a file in bytes."""
        file_path = self.get_file_path(relative_path, filename)
        if file_path.exists():
            return file_path.stat().st_size
        return 0
    
    def get_mime_type(self, filename: str) -> str:
        """Get the MIME type of a file."""
        mime_type, _ = mimetypes.guess_type(filename)
        return mime_type or "application/octet-stream"


# Create a global file storage instance
file_storage = FileStorage()


def validate_file_upload(file: UploadFile, max_size: int = 100 * 1024 * 1024) -> None:
    """Validate an uploaded file."""
    # Check file size
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning
    
    if file_size > max_size:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size is {max_size / (1024*1024)}MB"
        )
    
    # Check file extension (optional - add more validation as needed)
    allowed_extensions = {'.txt', '.pdf', '.png', '.jpg', '.jpeg', '.gif', '.csv', '.json', '.xml'}
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
        )