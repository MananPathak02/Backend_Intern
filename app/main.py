from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Task API",
    version="1.0.0",
    description="Week 2 Backend Internship CRUD API"
)

tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "done": False
    },
    {
        "id": 2,
        "title": "Do Assignment",
        "done": False
    },
    {
        "id": 3,
        "title": "Sleep",
        "done": True
    }
]


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str
    done: bool


@app.get("/", summary="API Information")
def home():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": [
            "/tasks"
        ]
    }


@app.get("/health", summary="Health Check")
def health():
    return {
        "status": "ok"
    }


@app.get("/tasks", summary="Get All Tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{id}", summary="Get Task By ID")
def get_task(id: int):

    for task in tasks:
        if task["id"] == id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )


@app.post("/tasks", status_code=201, summary="Create Task")
def create_task(task: TaskCreate):

    if task.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "done": False
    }

    tasks.append(new_task)

    return new_task


@app.put("/tasks/{id}", summary="Update Task")
def update_task(id: int, updated_task: TaskUpdate):

    if updated_task.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    for task in tasks:
        if task["id"] == id:
            task["title"] = updated_task.title
            task["done"] = updated_task.done
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )


@app.delete("/tasks/{id}", status_code=204, summary="Delete Task")
def delete_task(id: int):

    for index, task in enumerate(tasks):
        if task["id"] == id:
            tasks.pop(index)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )