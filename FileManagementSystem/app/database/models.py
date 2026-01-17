from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, Text,
    DateTime, JSON, UniqueConstraint, Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

# -------------------------
# SIMPLE TABLES (unchanged)
# -------------------------

class Resolution(Base):
    __tablename__ = "resolution"

    id = Column(Integer, primary_key=True)
    h = Column(Integer, nullable=False)
    w = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("h", "w", name="resolution_hw_unique"),
    )


class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class TesterType(Base):
    __tablename__ = "tester_type"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)


# -------------------------
# CORE ENTITIES
# -------------------------

class Tester(Base):
    __tablename__ = "tester"

    id = Column(Integer, primary_key=True)
    tester_group_id = Column(Integer, ForeignKey("tester_group.id"), nullable=True)
    tester_type_id = Column(Integer, ForeignKey("tester_type.id"), nullable=False)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login_at = Column(DateTime(timezone=True))

    # ---- relationships ----
    tester_type = relationship("TesterType")

    tester_group = relationship(
        "TesterGroup",
        foreign_keys=[tester_group_id],
        back_populates="members"
    )

    groups_created = relationship(
        "TesterGroup",
        foreign_keys="TesterGroup.created_by_id",
        back_populates="created_by"
    )

    groups_owned = relationship(
        "TesterGroup",
        foreign_keys="TesterGroup.owner_id",
        back_populates="owner"
    )


class TesterGroup(Base):
    __tablename__ = "tester_group"

    id = Column(Integer, primary_key=True)

    created_by_id = Column(Integer, ForeignKey("tester.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("tester.id"), nullable=False)

    name = Column(String, unique=True)

    # ---- relationships ----
    created_by = relationship(
        "Tester",
        foreign_keys=[created_by_id],
        back_populates="groups_created"
    )

    owner = relationship(
        "Tester",
        foreign_keys=[owner_id],
        back_populates="groups_owned"
    )

    members = relationship(
        "Tester",
        foreign_keys="Tester.tester_group_id",
        back_populates="tester_group"
    )


# -------------------------
# REMAINING TABLES (unchanged)
# -------------------------

class StatusSet(Base):
    __tablename__ = "status_set"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True)
    status_set_id = Column(Integer, ForeignKey("status_set.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)

    status_set = relationship("StatusSet")


class Scenario(Base):
    __tablename__ = "scenario"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class TestSuite(Base):
    __tablename__ = "test_suite"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)

    client = relationship("Client")


class Device(Base):
    __tablename__ = "device"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)

    name_external = Column(String)
    name_internal = Column(String)
    cpu = Column(String)
    gpu = Column(String)
    ram = Column(String)

    project = relationship("Project")


# Update the TestCase model to include relationship with TestCaseVersion
class TestCase(Base):
    __tablename__ = "test_case"

    id = Column(Integer, primary_key=True)
    scenario_id = Column(Integer, ForeignKey("scenario.id"), nullable=False)
    status_set_id = Column(Integer, ForeignKey("status_set.id"), nullable=False)

    scenario = relationship("Scenario")
    status_set = relationship("StatusSet")
    versions = relationship("TestCaseVersion", back_populates="test_case", cascade="all, delete-orphan")
    suitcases = relationship("Suitcase", back_populates="test_case")


class TestCaseVersion(Base):
    __tablename__ = "test_case_version"

    id = Column(Integer, primary_key=True)
    test_case_id = Column(Integer, ForeignKey("test_case.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("tester.id"), nullable=False)

    release_ready = Column(Boolean, default=False)
    version = Column(Integer, nullable=False)
    name = Column(String)
    description = Column(Text)
    steps = Column(Text)
    expected_result = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    test_case = relationship("TestCase", back_populates="versions")
    creator = relationship("Tester", foreign_keys=[created_by])
    executions = relationship("Execution", back_populates="test_case_version")

    __table_args__ = (
        UniqueConstraint("test_case_id", "version", name="test_case_version_unique"),
    )

# -------------------------
# ASSOCIATION TABLES
# -------------------------

class Suitcase(Base):
    __tablename__ = "suitcase"

    id = Column(Integer, primary_key=True)
    test_case_id = Column(Integer, ForeignKey("test_case.id"), nullable=False)
    test_suite_id = Column(Integer, ForeignKey("test_suite.id"), nullable=False)

    test_case = relationship("TestCase")
    test_suite = relationship("TestSuite")


# -------------------------
# RUNS
# -------------------------

class Run(Base):
    __tablename__ = "run"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    started_at = Column(DateTime(timezone=True))
    done_at = Column(DateTime(timezone=True))

    test_suite_metadata = Column(Text)

    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)

    project = relationship("Project")
    executions = relationship("Execution", back_populates="run")


# -------------------------
# ATTACHMENTS
# -------------------------

class Attachment(Base):
    __tablename__ = "attachment"

    id = Column(Integer, primary_key=True)

    parent_attachment_id = Column(Integer, ForeignKey("attachment.id"))
    uploaded_by = Column(Integer, ForeignKey("tester.id"), nullable=False)
    resolution_id = Column(Integer, ForeignKey("resolution.id"))

    filename = Column(String)
    relative_path = Column(String)

    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    presentmon_file = Column(Boolean)
    presentmon_version = Column(String)

    settings = Column(JSON)

    parent = relationship(
        "Attachment",
        remote_side=[id],
        backref="children"
    )

    uploader = relationship("Tester")
    resolution = relationship("Resolution")

    executions = relationship("Execution", back_populates="attachment")
    #uploads = relationship("Attachment", foreign_keys="Attachment.uploaded_by", back_populates="uploader")

    __table_args__ = (
        Index("attachment_parent_idx", "parent_attachment_id"),
        Index("attachment_uploaded_by_idx", "uploaded_by"),
        Index("attachment_filename_idx", "filename"),
        Index("attachment_uploaded_at_idx", "uploaded_at"),
    )


# -------------------------
# EXECUTIONS
# -------------------------

class Execution(Base):
    __tablename__ = "execution"

    id = Column(Integer, primary_key=True)

    device_id = Column(Integer, ForeignKey("device.id"), nullable=False)
    run_id = Column(Integer, ForeignKey("run.id"), nullable=False)
    test_case_version_id = Column(Integer, ForeignKey("test_case_version.id"), nullable=False)

    executed_by = Column(Integer, ForeignKey("tester.id"), nullable=False)
    status_id = Column(Integer, ForeignKey("status.id"), nullable=False)

    attachment_id = Column(Integer, ForeignKey("attachment.id"))

    actual_result = Column(Text)
    executed_at = Column(DateTime(timezone=True))

    execution_order = Column(Integer, nullable=False)

    device = relationship("Device")
    run = relationship("Run", back_populates="executions")
    test_case_version = relationship("TestCaseVersion")
    executor = relationship("Tester")
    status = relationship("Status")
    attachment = relationship("Attachment")

    __table_args__ = (
        UniqueConstraint(
            "run_id",
            "test_case_version_id",
            name="execution_run_version_unique"
        ),
    )
