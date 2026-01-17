from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..extensions import db

class TestCase(db.Model):
    __tablename__ = "test_case"

    id = Column(Integer, primary_key=True)
    scenario_id = Column(Integer, ForeignKey("scenario.id"), nullable=False)
    status_set_id = Column(Integer, ForeignKey("status_set.id"), nullable=False)

    versions = relationship("TestCaseVersion", back_populates="test_case")
