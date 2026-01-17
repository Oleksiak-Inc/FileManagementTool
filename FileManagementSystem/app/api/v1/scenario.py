from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.api.dependencies import get_current_tester
from app.database.models import Tester
from app.schemas.scenario import ScenarioCreate, ScenarioUpdate, ScenarioResponse
from app.services.scenario import (
    get_scenarios, get_scenario_by_id, create_scenario, update_scenario
)

router = APIRouter(prefix="/scenarios", tags=["scenarios"])


@router.get("/", response_model=List[ScenarioResponse])
def read_scenarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    _: Tester = Depends(get_current_tester),
):
    return get_scenarios(db, skip, limit)


@router.get("/{scenario_id}", response_model=ScenarioResponse)
def read_scenario(
    scenario_id: int,
    db: Session = Depends(get_db),
    _: Tester = Depends(get_current_tester),
):
    scenario = get_scenario_by_id(db, scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return scenario


@router.post("/", response_model=ScenarioResponse, status_code=status.HTTP_201_CREATED)
def create_new_scenario(
    scenario: ScenarioCreate,
    db: Session = Depends(get_db),
    _: Tester = Depends(get_current_tester),
):
    return create_scenario(db, scenario)


@router.patch("/{scenario_id}", response_model=ScenarioResponse)
def update_existing_scenario(
    scenario_id: int,
    scenario: ScenarioUpdate,
    db: Session = Depends(get_db),
    _: Tester = Depends(get_current_tester),
):
    updated = update_scenario(db, scenario_id, scenario)
    if not updated:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return updated
