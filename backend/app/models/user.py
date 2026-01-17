from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..extensions import db

class User(db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    user_group_id = Column(Integer, ForeignKey("user_group.id"))
    user_type_id = Column(Integer, ForeignKey("user_type.id"), nullable=False)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login_at = Column(DateTime)

    user_type = relationship("UserType")
    user_group = relationship("UserGroup", foreign_keys=[user_group_id])
