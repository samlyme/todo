from datetime import datetime, timedelta
from enum import Enum
from re import M
from typing import Any, Dict
from typing_extensions import Annotated, Doc
import uuid
from uuid import UUID
from fastapi import FastAPI, HTTPException
from pydantic import UUID4, BaseModel
from faker import Faker

app = FastAPI()


class TaskPublic(BaseModel):
    name: str
    description: str | None = None
    due_date: datetime | None = None


class Task(BaseModel):
    # Style choice, just duplicate all the fields for readability.
    id: UUID
    user_id: UUID
    name: str
    description: str | None = None
    due_date: datetime | None = None
    created_at: datetime | None = None


fake = Faker()

# Generate 5 random Task objects
tasks = [
    Task(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        name=fake.sentence(nb_words=3),
        description=fake.text(),
        due_date=datetime.utcnow() + timedelta(days=fake.random_int(min=1, max=30)),
        created_at=datetime.utcnow()
    )
    for _ in range(5)
]


@app.get("/tasks/")
async def get_tasks() -> list[Task]:
    return tasks


@app.get("/tasks/{id}", responses={404: {}})
async def get_task(id: UUID4) -> TaskPublic:
    for task in tasks:
        if task.id == id:
            return TaskPublic(**task.model_dump())

    raise HTTPException(status_code=404, detail="Task not found")
