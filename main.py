from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
import datetime

api = FastAPI()

class TaskStatus(str, Enum):
  todo = "todo"
  in_progress = "in_progress"
  done = "done"

class TaskPriority(str, Enum):
  low = "low"
  medium = "medium"
  high = "high"

class TaskCreate(BaseModel):
  title: str
  description: str
  priority: TaskPriority
  status: TaskStatus = TaskStatus.todo

class Task(BaseModel):
  id: int
  title: str
  description: str
  priority: TaskPriority
  status: TaskStatus
  created_at: str

tasks = [
  {
    "id": 1,
    "title": "Coding",
    "description": "Learn FastAPI for 1h",
    "priority": "medium",
    "status": "todo",
    "created_at": "2025-12-17 17:28:43.335223"
  },
  {
    "id": 2,
    "title": "Coding",
    "description": "Learn Python for 2h",
    "priority": "medium",
    "status": "todo",
    "created_at": "2025-12-17 17:28:54.185812"
  },
  {
    "id": 3,
    "title": "Gym",
    "description": "Push training for 1h",
    "priority": "medium",
    "status": "todo",
    "created_at": "2025-12-17 17:29:39.160028"
  },
  {
    "id": 4,
    "title": "Gym",
    "description": "Pull training for 1h",
    "priority": "medium",
    "status": "todo",
    "created_at": "2025-12-17 17:29:44.716334"
  },
  {
    "id": 5,
    "title": "Food",
    "description": "Prepare breakfast for tommorow",
    "priority": "high",
    "status": "todo",
    "created_at": "2025-12-17 17:30:01.692241"
  },
  {
    "id": 6,
    "title": "Read",
    "description": "Read a book for 15 minutes",
    "priority": "low",
    "status": "todo",
    "created_at": "2025-12-17 17:30:22.390974"
  },
  {
    "id": 7,
    "title": "Meditate",
    "description": "Meditate for 10 minutes",
    "priority": "low",
    "status": "todo",
    "created_at": "2025-12-17 17:30:39.803484"
  }
]

@api.post("/tasks/create")
def tasks_post(task: TaskCreate):
  task_id = max(item['id'] for item in tasks) + 1 if tasks else 1

  new_task = {
    'id': task_id,
    'title': task.title,
    'description': task.description,
    'priority': task.priority,
    'status': task.status,
    'created_at': str(datetime.datetime.now())
  }

  tasks.append(new_task)
  return new_task

@api.get("/tasks")
def get_tasks(status: TaskStatus | None = None, priority: TaskPriority | None = None, skip: int = 0, limit: int = 10):
  filtered = tasks
  if status:
    filtered = [item for item in filtered if item['status'] == status]
  if priority:
    filtered = [item for item in filtered if item['priority'] == priority]

  result = [] 
  for i, item in enumerate(filtered):
    if skip <= i and i < skip + limit:
      result.append(item)

  return result