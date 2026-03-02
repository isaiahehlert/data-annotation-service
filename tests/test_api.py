from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_project_happy():
    r = client.post("/projects", json={"name": "p1", "description": "d"})
    assert r.status_code == 201

def test_project_duplicate():
    client.post("/projects", json={"name": "dup", "description": "d"})
    r = client.post("/projects", json={"name": "dup", "description": "d"})
    assert r.status_code == 400

def test_tasks_and_annotation_flow():
    p = client.post("/projects", json={"name": "flow", "description": "x"}).json()
    pid = p["id"]

    r = client.post(f"/projects/{pid}/tasks", json={"tasks":[{"input_data":{"x":1}}]})
    assert r.status_code == 201

    task_id = r.json()[0]

    r = client.post(f"/tasks/{task_id}/annotations", json={"annotator":"a","annotation_data":{"label":1}})
    assert r.status_code == 201

    stats = client.get(f"/projects/{pid}/stats").json()
    assert stats["total_tasks"] == 1
    assert stats["annotated_tasks"] == 1

def test_invalid_project():
    r = client.get("/projects/99999")
    assert r.status_code == 404
