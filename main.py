from fastapi import FastAPI, Query, Body
from pydantic import BaseModel
from enum import Enum
from typing import Annotated
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

class UpdateTask(BaseModel):
  title: str | None = None
  description: str | None = None

class UpdateStatus(BaseModel):
  status: TaskStatus
  priority: TaskPriority

class MetaData(BaseModel):
  updated_by: str
  reason: str

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

@api.post("/tasks/{id}/comment")
def post_comment(id: int, comment: Annotated[str, Body()], notify: bool = False):
  for item in tasks:
    if item['id'] == id:
      item['comment'] = comment
      item['notify'] = notify
      return item

@api.put("/tasks/{id}/status")
def put_status(id: int, update: UpdateStatus):
  for item in tasks:
    if item['id'] == id:
      item['status'] = update.status
      return item
    
@api.put("/tasks/{id}/priority")
def put_priority(id: int, update: UpdateStatus):
  for item in tasks:
    if item['id'] == id:
      item['priority'] = update.priority
      return item

@api.put("/tasks/{id}/content")
def put_content(id: int, content: UpdateTask, meta: MetaData):
  for item in tasks:
    if item['id'] == id:
      if content.title:
        item['title'] = content.title
      if content.description:
        item['description'] = content.description
      item['updated_by'] = meta.updated_by
      item['reason'] = meta.reason
      return item
    
@api.delete("/tasks/{id}")
def delete_task(id: int):
  for item in tasks:
    if item['id'] == id:
      tasks.remove(item)
  return tasks

@api.get("/tasks/stats/by-status")
def get_status_stats():
  status_stats = {'todo': 0, 'in_progress': 0, 'done': 0}
  for item in tasks:
    if item['status'] == 'todo':
      status_stats['todo'] += 1
    if item['status'] == 'in_progress':
      status_stats['in_progress'] += 1
    if item['status'] == 'done':
      status_stats['done'] += 1
    
  return status_stats

@api.get("/tasks/stats/by-priority")
def get_priority_stats():
  priority_stats = {'low': 0, 'medium': 0, 'high': 0}
  for item in tasks:
    if item['priority'] == 'low':
      priority_stats['low'] += 1
    if item['priority'] == 'medium':
      priority_stats['medium'] += 1
    if item['priority'] == 'high':
      priority_stats['high'] += 1
    
  return priority_stats

@api.get("/tasks/search")
def get_search(
  text: Annotated[str, Query(min_length=3)],
  title: Annotated[str | None, Query(description="Search by title")] = None
):
  filtered = [item for item in tasks if item['title'] == title] if title else tasks
  searched = [item for item in filtered if text.lower() in item['description'].lower()]
  return searched

@api.get("/tasks/{id}")
def get_task(id: int):
  for item in tasks:
    if item['id'] == id:
      return item

@api.get("/tasks")
def get_tasks(status: TaskStatus | None = None, priority: TaskPriority | None = None, skip: int = 0, limit: int = 10):
  filtered = tasks
  if status:
    filtered = [item for item in filtered if item['status'] == status.value]
  if priority:
    filtered = [item for item in filtered if item['priority'] == priority.value]

  return filtered[skip:skip+limit]

