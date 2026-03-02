from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, func, Enum
from sqlalchemy.orm import relationship
from .db import Base
import enum

class TaskStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    input_data = Column(JSON, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.pending)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    project = relationship("Project", back_populates="tasks")
    annotations = relationship("Annotation", back_populates="task", cascade="all, delete-orphan")

class Annotation(Base):
    __tablename__ = "annotations"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    annotator = Column(String, nullable=False)
    annotation_data = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    task = relationship("Task", back_populates="annotations")
