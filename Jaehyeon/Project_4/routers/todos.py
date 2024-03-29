import sys
sys.path.append("..")

from starlette import status
from starlette.responses import RedirectResponse

from typing import Optional
from fastapi import Depends, HTTPException, APIRouter, Request, Form
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from .auth import get_current_user, get_user_exception

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}}
)

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
async def read_all_by_user(request: Request, db: Session=Depends(get_db)):
    todos = db.query(models.Todos).filter(models.Todos.onwer_id==1).all()

    return templates.TemplateResponse("home.html", {"request": request, "todos": todos})


@router.get("/add-todo", response_class=HTMLResponse)
async def add_new_todo(request: Request):
    return templates.TemplateResponse("add-todo.html", {"request": request})

@router.post("/add-todo", response_class=HTMLResponse)
async def create_todo(
    request: Request, title: str=Form(...), description: str=Form(...),
    priority: int=Form(...), db: Session = Depends(get_db)
):
    todo_model = models.Todos({
        "title": title,
        "description": description,
        "priority": priority,
        "complete": False,
        "owner_id": 1
    })

    db.add(todo_model)
    db.commit()

    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)



@router.get("/edit-todo/{todo.id}", response_class=HTMLResponse)
async def edit_todo(request: Request):
    return templates.TemplateResponse("edit-todo.html")

@router.get("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo(request: Request, todo_id: int, db: Session=Depends(get_db)):
    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    return templates.TemplateResponse("edit-todo.html", {"request": request})

@router.post("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo_commit(
    request: Request, todo_id: int, title: str=Form(),
    description: str=Form(), priority: int=Form(), db: Session=Depends(get_db)
):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    todo_model = models.Todos({
        "title": title,
        "description": description,
        "priority": priority,
        "complete": False,
        "owner_id": 1
    })

    db.add(todo_model)
    db.commit()

    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)



@router.get("/delete/{todo_id}")
async def delete_todo(request: Request, todo_id: int, db: Session=Depends(get_db)):
    todo_model = db.query(models.Todos) \
              .filter(models.Todos.id == todo_id) \
              .filter(models.Todos.owner_id == 1) \
              .first()
    
    if todo_model == None:
        return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)
    
    db.query(models.Todos).filter(models.Todos.id == todo_id)
    db.commit()
    
    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)