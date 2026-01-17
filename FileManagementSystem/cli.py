import click
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.services.tester import create_tester, get_testers, get_tester_by_email
from app.schemas.tester import TesterCreate
from init_db import init_db as init_db_func
from app.utils.auth import hash_password
from app.utils.file_management import FileManager
from app.config import settings

file_manager = FileManager(settings.UPLOAD_PATH)

@click.group()
def cli():
    """CLI for FileManagementSystem backend."""
    pass

# ------------------------
# DB commands
# ------------------------
@cli.command()
def initdb():
    """Initialize the database schema."""
    init_db_func()

# ------------------------
# Tester commands
# ------------------------
@cli.command()
@click.option("--first-name", prompt=True, help="First name of the tester")
@click.option("--last-name", prompt=True, help="Last name of the tester")
@click.option("--email", prompt=True, help="Email of the tester")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True, help="Password")
@click.option("--tester-type-id", default=0, help="tester type definition: 0=regular, 2=admin, 1=super")
def addtester(first_name, last_name, email, password, tester_type_id):
    """Add a new tester directly via CLI."""
    db = SessionLocal()
    try:
        # Check if tester exists
        existing_tester = get_tester_by_email(db, email)
        if existing_tester:
            click.echo(f"Error: Tester with email {email} already exists")
            return
        
        # Create tester
        tester_data = TesterCreate(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            tester_type_id=tester_type_id
        )
        
        tester = create_tester(db, tester_data)
        click.echo(f"Tester created successfully: {tester.email} (ID: {tester.id})")
        
    except Exception as e:
        click.echo(f"Error creating tester: {e}")
    finally:
        db.close()

@cli.command()
def getalltesters():
    """Get all testers."""
    db = SessionLocal()
    try:
        testers = get_testers(db)
        for tester in testers:
            click.echo(f"{tester.id}: {tester.email} - {tester.first_name} {tester.last_name}")
    except Exception as e:
        click.echo(f"Error getting testers: {e}")
    finally:
        db.close()


@cli.command()
def cleanup_files():
    """Clean up orphaned files and empty directories."""
    from app.utils.file_management import file_manager
    from app.database.session import SessionLocal
    from app.database.models import Attachment
    
    db = SessionLocal()
    try:
        # Get all attachments from database
        attachments = db.query(Attachment.filename, Attachment.relative_path).all()
        
        # Clean up orphaned files
        orphaned = file_manager.cleanup_orphaned_files(attachments)
        if orphaned:
            click.echo(f"Removed {len(orphaned)} orphaned files:")
            for file in orphaned:
                click.echo(f"  - {file}")
        else:
            click.echo("No orphaned files found.")
        
        # Clean up empty directories
        empty_dirs = file_manager.cleanup_empty_directories()
        if empty_dirs:
            click.echo(f"Removed {len(empty_dirs)} empty directories:")
            for dir_path in empty_dirs:
                click.echo(f"  - {dir_path}")
        else:
            click.echo("No empty directories found.")
            
    except Exception as e:
        click.echo(f"Error cleaning up files: {e}")
    finally:
        db.close()

@cli.command()
def storage_stats():
    """Show file storage statistics."""
    from app.utils.file_management import file_manager
    
    stats = file_manager.get_storage_stats()
    click.echo("File Storage Statistics:")
    click.echo(f"  Upload Directory: {stats['upload_directory']}")
    click.echo(f"  Total Files: {stats['file_count']}")
    click.echo(f"  Total Size: {stats['total_size_mb']:.2f} MB ({stats['total_size_bytes']} bytes)")
    click.echo(f"  Directories: {stats['directory_count']}")

@cli.command()
@click.option("--backup-dir", default="backups", help="Directory to store backups")
def backup_files(backup_dir):
    """Create a backup of uploaded files."""
    from app.utils.file_management import file_manager
    from pathlib import Path
    
    backup_path = Path(backup_dir)
    backup_path.mkdir(parents=True, exist_ok=True)
    
    success = file_manager.backup_files(backup_path)
    if success:
        click.echo(f"Backup created successfully in {backup_dir}")
    else:
        click.echo("Backup failed")



if __name__ == "__main__":
    cli()