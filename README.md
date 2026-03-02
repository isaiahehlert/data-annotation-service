# Data Annotation Management Service

A production-style REST API for managing data annotation workflows.

Built with FastAPI, SQLAlchemy, and SQLite.  
Fully containerized with Docker.  
Tested with PyTest and integrated with GitHub Actions CI.

Repository:  
https://github.com/isaiahehlert/data-annotation-service

---

## Overview

This service allows teams to:

- Create annotation projects
- Load and manage annotation tasks
- Submit annotations
- Track task completion
- Aggregate statistics by annotator

The system models a realistic annotation lifecycle and demonstrates:

- Relational database modeling
- REST API design
- Input validation and error handling
- Aggregation queries
- Containerized deployment
- CI-based test execution

---

## Tech Stack

- Python 3.11
- FastAPI
- SQLAlchemy ORM
- SQLite
- Docker
- PyTest
- GitHub Actions

---

## Architecture

Project → Task → Annotation

- A Project contains multiple Tasks.
- A Task can receive multiple Annotations.
- When an Annotation is submitted, the Task status transitions to "done".
- Project statistics are computed using SQL aggregation queries.

---

## API Endpoints

### Projects

POST /projects  
Create a new project (unique name required)

GET /projects  
List all projects

GET /projects/{project_id}  
Retrieve project details and task counts

---

### Tasks

POST /projects/{project_id}/tasks  
Create multiple tasks under a project

GET /projects/{project_id}/tasks  
List tasks (optional status filter)

---

### Annotations

POST /tasks/{task_id}/annotations  
Submit annotation and mark task as complete

GET /tasks/{task_id}/annotations  
List all annotations for a task

---

### Statistics

GET /projects/{project_id}/stats  

Returns:

- total_tasks
- annotated_tasks
- by_annotator (aggregation)

---

## Running Locally

```
bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Swagger UI:
http://localhost:8000/docs

⸻

Running with Docker
```
docker build -t annotation-service .
docker run -p 8000:8000 annotation-service
```
Access:
http://localhost:8000/docs

⸻

Example Usage

Create a project:
```
curl -X POST http://localhost:8000/projects \
-H "Content-Type: application/json" \
-d '{"name":"demo","description":"test"}'
```
Create tasks:
```
curl -X POST http://localhost:8000/projects/1/tasks \
-H "Content-Type: application/json" \
-d '{"tasks":[{"input_data":{"text":"hello"}}]}'
```
Submit annotation:
```
curl -X POST http://localhost:8000/tasks/1/annotations \
-H "Content-Type: application/json" \
-d '{"annotator":"alice","annotation_data":{"label":"positive"}}'
```
Get project statistics:
```
curl http://localhost:8000/projects/1/stats
```

⸻

Testing

Run test suite:
```
pytest -q
```
Tests cover:
	•	Happy path workflows
	•	Duplicate project validation
	•	Non-existent resource handling
	•	Task lifecycle transitions

⸻

CI

GitHub Actions workflow automatically runs tests on push.

⸻

Design Notes
	•	Enforces unique project names (returns HTTP 400 on conflict)
	•	Returns 404 for non-existent resources
	•	Uses SQL aggregation for statistics
	•	Follows RESTful conventions with appropriate status codes
	•	Designed for clarity, correctness, and maintainability
