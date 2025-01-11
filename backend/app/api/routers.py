from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db.session import SessionLocal
from app.schemas.user import UserCreate
from app.schemas.task import TaskResponse, TaskCreate
from app.api import crud
from app.auth import utils, auth
from app.models.user import User

user_router = APIRouter(prefix="/user", tags=["User"])
task_router = APIRouter(prefix="/task", tags=["Task"])


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# User Registration Endpoint
@user_router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )
    created_user = crud.create_user(db, user)
    return {"message": "User registered successfully", "user": {"username": created_user.username}}


# User Login Endpoint
@user_router.post("/login", status_code=status.HTTP_200_OK)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password"
        )
    token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer", "username": user.username }


# Create Task Endpoint
@task_router.post("/create", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db), user: User = Depends(auth.get_current_user)):
    created_task = crud.create_task(db, task, user.id)
    return created_task


# Get All Tasks Endpoint
@task_router.get("/", response_model=list[TaskResponse], status_code=status.HTTP_200_OK)
def get_all_tasks(db: Session = Depends(get_db), user: User = Depends(auth.get_current_user)):
    tasks = crud.get_tasks(db, user.id)
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No tasks found for the user"
        )
    return tasks


# Get Task by ID Endpoint
@task_router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def get_task_by_id(task_id: int, db: Session = Depends(get_db), user: User = Depends(auth.get_current_user)):
    task = crud.get_task(db, task_id, user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found or not accessible"
        )
    return task


# Update Task Endpoint
@task_router.put("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def update_task(
    task_id: int, task: TaskCreate, db: Session = Depends(get_db), user: User = Depends(auth.get_current_user)
):
    updated_task = crud.update_task(db, task, task_id, user.id)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found or not accessible"
        )
    return updated_task


# Delete Task Endpoint
@task_router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int, db: Session = Depends(get_db), user: User = Depends(auth.get_current_user)):
    if not crud.delete_task(db, task_id, user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found or not accessible"
        )
    return {"message": "Task deleted successfully"}

