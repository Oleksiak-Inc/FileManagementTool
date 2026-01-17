# --- /home/oleksiak/FileManagementTool/FileManagementSystem/app/utils/file_management.py ---
import os
import shutil
from pathlib import Path
from typing import List, Tuple
from datetime import datetime


class FileManager:
    def __init__(self, base_path: Path):
        self.base_path = base_path
    
    def cleanup_orphaned_files(self, db_attachments: List[Tuple[str, str]]) -> List[str]:
        """Remove files that exist on disk but don't have database records."""
        orphaned_files = []
        
        # Walk through all files in upload directory
        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                file_path = Path(root) / file
                relative_path = str(file_path.relative_to(self.base_path).parent)
                
                # Check if this file exists in database
                found = False
                for db_filename, db_relative_path in db_attachments:
                    if file == db_filename and relative_path == db_relative_path:
                        found = True
                        break
                
                if not found:
                    try:
                        file_path.unlink()
                        orphaned_files.append(str(file_path))
                    except OSError as e:
                        print(f"Failed to delete orphaned file {file_path}: {e}")
        
        return orphaned_files
    
    def cleanup_empty_directories(self) -> List[str]:
        """Remove empty directories in the uploads folder."""
        empty_dirs = []
        
        for root, dirs, files in os.walk(self.base_path, topdown=False):
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                try:
                    if not any(dir_path.iterdir()):
                        dir_path.rmdir()
                        empty_dirs.append(str(dir_path))
                except OSError as e:
                    print(f"Failed to remove directory {dir_path}: {e}")
        
        return empty_dirs
    
    def get_storage_stats(self) -> dict:
        """Get statistics about file storage."""
        total_size = 0
        file_count = 0
        dir_count = 0
        
        for root, dirs, files in os.walk(self.base_path):
            dir_count += len(dirs)
            for file in files:
                file_path = Path(root) / file
                total_size += file_path.stat().st_size
                file_count += 1
        
        return {
            "total_size_bytes": total_size,
            "total_size_mb": total_size / (1024 * 1024),
            "file_count": file_count,
            "directory_count": dir_count,
            "upload_directory": str(self.base_path)
        }
    
    def backup_files(self, backup_dir: Path) -> bool:
        """Create a backup of all uploaded files."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = backup_dir / f"uploads_backup_{timestamp}"
            
            if self.base_path.exists():
                shutil.copytree(self.base_path, backup_path)
                return True
            return False
        except Exception as e:
            print(f"Backup failed: {e}")
            return False


# Create global file manager instance
from app.config import settings
file_manager = FileManager(settings.UPLOAD_PATH)