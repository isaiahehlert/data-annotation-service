from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from .db import Base, engine, get_db
from . import models, schemas

app = FastAPI(title="Data Annotation Management Service")
Base.metadata.create_all(bind=engine)

VALID_STATUSES = {"pending", "in_progress", "done"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/projects", response_model=schemas.ProjectOut, status_code=201)
def create_project(payload: schemas.ProjectCreate, db: Session = Depends(get_db)):
    project = models.Project(name=payload.name, description=payload.description)
    db.add(project)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Project name must be unique")
    db.refresh(project)
    return project

@app.get("/projects", response_model=list[schemas.ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()

@app.get("/projects/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)):
    p = db.query(models.Project).filter_by(id=project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    total = db.query(func.count(models.Task.id)).filter_by(project_id=project_id).scalar()
    done = db.query(func.count(models.Task.id)).filter_by(project_id=project_id, status="done").scalar()
    return {
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "created_at": p.created_at,
        "total_tasks": total,
        "annotated_tasks": done
    }

@app.post("/projects/{project_id}/tasks", status_code=201)
def create_tasks(project_id: int, payload: dict, db: Session = Depends(get_db)):
    if not db.query(models.Project).filter_by(id=project_id).first():
        raise HTTPException(status_code=404, detail="Project not found")
    tasks = payload.get("tasks")
    if not tasks:
        raise HTTPException(status_code=400, detail="Invalid tasks")
    ids = []
    for t in tasks:
        task = models.Task(project_id=project_id, input_data=t["input_data"], status="pending")
        db.add(task)
        db.commit()
        db.refresh(task)
        ids.append(task.id)
    return ids

@app.get("/projects/{project_id}/tasks")
def list_tasks(project_id: int, status: str | None = Query(default=None), db: Session = Depends(get_db)):
    if not db.query(models.Project).filter_by(id=project_id).first():
        raise HTTPException(status_code=404, detail="Project not found")
    q = db.query(models.Task).filter_by(project_id=project_id)
    if status:
        if status not in VALID_STATUSES:
            raise HTTPException(status_code=400, detail="Invalid status")
        q = q.filter_by(status=status)
    return q.all()

@app.post("/tasks/{task_id}/annotations", status_code=201)
def create_annotation(task_id: int, payload: dict, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter_by(id=task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    a = models.Annotation(
        task_id=task_id,
        annotator=payload["annotator"],
        annotation_data=payload["annotation_data"]
    )
    task.status = "done"
    db.add(a)
    db.commit()
    db.refresh(a)
    return a

@app.get("/tasks/{task_id}/annotations")
def list_annotations(task_id: int, db: Session = Depends(get_db)):
    if not db.query(models.Task).filter_by(id=task_id).first():
        raise HTTPException(status_code=404, detail="Task not found")
    return db.query(models.Annotation).filter_by(task_id=task_id).all()

@app.get("/projects/{project_id}/stats")
def project_stats(project_id: int, db: Session = Depends(get_db)):
    if not db.query(models.Project).filter_by(id=project_id).first():
        raise HTTPException(status_code=404, detail="Project not found")
    total = db.query(func.count(models.Task.id)).filter_by(project_id=project_id).scalar()
    done = db.query(func.count(models.Task.id)).filter_by(project_id=project_id, status="done").scalar()
    rows = db.query(models.Annotation.annotator, func.count(models.Annotation.id)).join(models.Task).filter(models.Task.project_id==project_id).group_by(models.Annotation.annotator).all()
    by_annotator = {r[0]: r[1] for r in rows}
    return {
        "total_tasks": total,
        "annotated_tasks": done,
        "by_annotator": by_annotator
    }
