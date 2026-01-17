from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..extensions import db

class TestCaseVersion(db.Model):
    __tablename__ = "test_case_version"

    id = Column(Integer, primary_key=True)
    test_case_id = Column(Integer, ForeignKey("test_case.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("user.id"), nullable=False)

    version = Column(Integer, nullable=False)
    release_ready = Column(Boolean, default=False)
    name = Column(String)
    description = Column(Text)
    steps = Column(Text)
    expected_result = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    test_case = relationship("TestCase", back_populates="versions")
