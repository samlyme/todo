from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Task(BaseModel):
    id: int
    name: str
    description: str


# lol
db: dict[int, Task] = {}


@app.get('/')
async def home():
    return {'message': 'welcome'}


@app.post('/tasks')
async def create_task(task: Task) -> Task:
    if task.id in db:
        raise HTTPException(status_code=400, detail="task already exists")
    db[task.id] = task
    return task


@app.get('/tasks/{task_id}')
async def read_task(task_id: int) -> Task:
    if task_id not in db:
        raise HTTPException(status_code=404, detail="task not found")

    return db[task_id]


@app.put('/tasks/{task_id}')
async def update_task(task_id: int, task: Task) -> Task:
    if task.id != task_id:
        raise HTTPException(status_code=400, detail="bad req")

    if task_id not in db:
        raise HTTPException(status_code=404, detail="task not found")

    db[task.id].name = task.name
    db[task.id].description = task.description

    return db[task.id]


@app.delete('/tasks/{task_id}')
async def delete_task(task_id: int):
    ret = db.pop(task_id, None)
    if not ret:
        raise HTTPException(status_code=404, detail="task not found")
    return ret
