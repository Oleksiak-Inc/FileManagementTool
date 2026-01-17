from typing import List, Optional
from sqlalchemy.orm import Session

from app.database.models import Scenario
from app.schemas.scenario import ScenarioCreate, ScenarioUpdate


def get_scenario_by_id(db: Session, scenario_id: int) -> Optional[Scenario]:
    return db.query(Scenario).filter(Scenario.id == scenario_id).first()


def get_scenarios(db: Session, skip: int = 0, limit: int = 100) -> List[Scenario]:
    return db.query(Scenario).offset(skip).limit(limit).all()


def create_scenario(db: Session, scenario_in: ScenarioCreate) -> Scenario:
    scenario = Scenario(**scenario_in.dict())
    db.add(scenario)
    db.commit()
    db.refresh(scenario)
    return scenario


def update_scenario(db: Session, scenario_id: int, scenario_in: ScenarioUpdate) -> Optional[Scenario]:
    scenario = get_scenario_by_id(db, scenario_id)
    if not scenario:
        return None

    for field, value in scenario_in.dict(exclude_unset=True).items():
        setattr(scenario, field, value)

    db.commit()
    db.refresh(scenario)
    return scenario
