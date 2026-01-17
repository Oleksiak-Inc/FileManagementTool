from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.api.dependencies import get_current_tester
from app.database.models import Tester
from app.schemas.client import ClientCreate, ClientUpdate, ClientResponse
from app.services.client import (
    get_clients, get_client_by_id, create_client, update_client
)

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("/", response_model=List[ClientResponse])
def read_clients(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    _: Tester = Depends(get_current_tester),
):
    return get_clients(db, skip, limit)


@router.get("/{client_id}", response_model=ClientResponse)
def read_client(
    client_id: int,
    db: Session = Depends(get_db),
    _: Tester = Depends(get_current_tester),
):
    client = get_client_by_id(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_new_client(
    client: ClientCreate,
    db: Session = Depends(get_db),
    _: Tester = Depends(get_current_tester),
):
    return create_client(db, client)


@router.patch("/{client_id}", response_model=ClientResponse)
def update_existing_client(
    client_id: int,
    client: ClientUpdate,
    db: Session = Depends(get_db),
    _: Tester = Depends(get_current_tester),
):
    updated = update_client(db, client_id, client)
    if not updated:
        raise HTTPException(status_code=404, detail="Client not found")
    return updated