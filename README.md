# Data Annotation Management Service

## Run locally
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

## Run with Docker
docker build -t annotation-service .
docker run -p 8000:8000 annotation-service

## Example Usage

Create project:
curl -X POST http://localhost:8000/projects \
-H "Content-Type: application/json" \
-d '{"name":"demo","description":"test"}'

Create tasks:
curl -X POST http://localhost:8000/projects/1/tasks \
-H "Content-Type: application/json" \
-d '{"tasks":[{"input_data":{"text":"hello"}}]}'

Annotate:
curl -X POST http://localhost:8000/tasks/1/annotations \
-H "Content-Type: application/json" \
-d '{"annotator":"alice","annotation_data":{"label":"positive"}}'

Stats:
curl http://localhost:8000/projects/1/stats
