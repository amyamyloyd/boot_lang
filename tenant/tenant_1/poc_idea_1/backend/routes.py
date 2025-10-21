from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user

router = APIRouter()

@router.get("/tasks")
async def get_tasks(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get all tasks for the current user
    """
    from .models import TaskModel
    tasks = db.query(TaskModel).filter(
        TaskModel.user_id == current_user.id
    ).all()
    return {"tasks": tasks}

@router.post("/tasks")
async def create_task(
    task_data: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Create a new task for the current user
    """
    from .models import TaskModel
    new_task = TaskModel(user_id=current_user.id, **task_data)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"task": new_task}

@router.put("/tasks/{task_id}")
async def update_task(
    task_id: int,
    task_data: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Update an existing task
    """
    from .models import TaskModel
    task = db.query(TaskModel).filter(
        TaskModel.id == task_id,
        TaskModel.user_id == current_user.id
    ).first()
    
    if not task:
        return {"error": "Task not found"}
    
    for key, value in task_data.items():
        setattr(task, key, value)
    
    db.commit()
    db.refresh(task)
    return {"task": task}

@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Delete a task
    """
    from .models import TaskModel
    task = db.query(TaskModel).filter(
        TaskModel.id == task_id,
        TaskModel.user_id == current_user.id
    ).first()
    
    if not task:
        return {"error": "Task not found"}
    
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}
