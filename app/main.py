from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models import Task

app = FastAPI()

class TaskList(BaseModel):
    id: int
    name: str
    deadline: date


@app.get("/tasks/")
async def tasks_list(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task))
    tasks = result.scalars().all()
    # tasks = [{"id": u.id,"name":u.name} for u in result.scalars().all()]
    return print(tasks)


@app.post("/tasks/")
async def create_task(task: TaskList, db: AsyncSession = Depends(get_db)):
    task=TaskList(name=task.name, deadline=task.deadline)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return print(f"{task} добавлена")



@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await db.get(TaskList, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    await db.delete(task)
    await db.commit()
    return{"status": "deleted"}

