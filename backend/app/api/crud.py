from sqlalchemy.orm import Session
from app.models.user import User
from app.models.task import Task
from app.schemas.user import UserCreate
from app.schemas.task import TaskCreate
from app.auth import utils


# User Functions
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = utils.hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Task Functions
def create_task(db: Session, task: TaskCreate, user_id: int):
    new_task = Task(title=task.title, description=task.description, completed=task.completed, owner_id=user_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def get_tasks(db: Session, user_id: int):
    return db.query(Task).filter(Task.owner_id == user_id).all()


def get_task(db: Session, task_id: int, user_id: int):
    return db.query(Task).filter(Task.id == task_id, Task.owner_id == user_id).first()


def update_task(db: Session, task: TaskCreate, task_id: int, user_id: int):
    task_to_update = get_task(db, task_id, user_id)
    if not task_to_update:
        return None
    task_to_update.title = task.title
    task_to_update.description = task.description
    task_to_update.completed = task.completed
    db.commit()
    db.refresh(task_to_update)
    return task_to_update


def delete_task(db: Session, task_id: int, user_id: int) -> bool:
    task_to_delete = get_task(db, task_id, user_id)
    if not task_to_delete:
        return False
    db.delete(task_to_delete)
    db.commit()
    return True
