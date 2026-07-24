from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.database import (
    create_db_and_tables,
    insert_sample_data,
    engine,
    Task,
)
from sqlmodel import Session, select

app = FastAPI(
    title="Task API",
    version="1.0.0",
    description="Week 2 Backend Internship CRUD API"
)
create_db_and_tables()
insert_sample_data()

def insert_sample_data():
    with Session(engine) as session:

        statement = select(Task)
        tasks = session.exec(statement).all()

        if len(tasks) == 0:
            session.add(Task(title="Learn FastAPI", done=False))
            session.add(Task(title="Do Assignment", done=False))
            session.add(Task(title="Sleep", done=True))
            session.commit()


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
    with Session(engine) as session:
        tasks = session.exec(select(Task)).all()
        return tasks


@app.get("/tasks/{id}", summary="Get Task By ID")
def get_task(id: int):
    with Session(engine) as session:
        task = session.get(Task, id)

        if task is None:
            raise HTTPException(
                status_code=404,
                detail=f"Task {id} not found"
            )

        return task


@app.post("/tasks", status_code=201, summary="Create Task")
def create_task(task: TaskCreate):

    if task.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    with Session(engine) as session:
        new_task = Task(
            title=task.title,
            done=False
        )

        session.add(new_task)
        session.commit()
        session.refresh(new_task)

        return new_task


@app.put("/tasks/{id}", summary="Update Task")
def update_task(id: int, updated_task: TaskUpdate):

    if updated_task.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    with Session(engine) as session:
        task = session.get(Task, id)

        if task is None:
            raise HTTPException(
                status_code=404,
                detail=f"Task {id} not found"
            )

        task.title = updated_task.title
        task.done = updated_task.done

        session.add(task)
        session.commit()
        session.refresh(task)

        return task


@app.delete("/tasks/{id}", status_code=204, summary="Delete Task")
def delete_task(id: int):

    with Session(engine) as session:
        task = session.get(Task, id)

        if task is None:
            raise HTTPException(
                status_code=404,
                detail=f"Task {id} not found"
            )

        session.delete(task)
        session.commit()

        return