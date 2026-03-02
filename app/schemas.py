from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: Optional[str]
    created_at: datetime


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    project_id: int
    input_data: Dict[str, Any]
    status: str
    created_at: datetime


class AnnotationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    task_id: int
    annotator: str
    annotation_data: Dict[str, Any]
    created_at: datetime


class ProjectStats(BaseModel):
    total_tasks: int
    annotated_tasks: int
    by_annotator: Dict[str, int]
