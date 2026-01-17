from typing import List, Optional
from sqlalchemy.orm import Session

from app.database.models import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


def get_project_by_id(db: Session, project_id: int) -> Optional[Project]:
    return db.query(Project).filter(Project.id == project_id).first()


def get_projects(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    client_id: Optional[int] = None,
) -> List[Project]:
    query = db.query(Project)

    if client_id is not None:
        query = query.filter(Project.client_id == client_id)

    return query.offset(skip).limit(limit).all()


def create_project(db: Session, project_in: ProjectCreate) -> Project:
    project = Project(**project_in.dict())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def update_project(
    db: Session,
    project_id: int,
    project_in: ProjectUpdate,
) -> Optional[Project]:
    project = get_project_by_id(db, project_id)
    if not project:
        return None

    for field, value in project_in.dict(exclude_unset=True).items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)
    return project
