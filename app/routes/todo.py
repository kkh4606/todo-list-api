from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import database, models, schema, oauth2
from typing import List


router = APIRouter(prefix="/todos", tags=["TODO"])


@router.get("/", response_model=List[schema.TodoOut])
def get_todos(
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    todos = db.query(models.Todo).filter(models.Todo.owner_id == current_user.id).all()

    return todos


@router.post("/create")
def create_todo(
    todo: schema.CreateTodo,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    new_todo = models.Todo(**todo.model_dump(), owner_id=current_user.id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo


@router.get("/{id}")
def get_todo(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    todo = db.query(models.Todo).filter(models.Todo.id == id).first()
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"todo with id : {id} not found",
        )

    return todo


@router.put("/{id}")
def update_todo(
    update_todo: schema.UpdateTodo,
    id: int,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    todo_query = db.query(models.Todo).filter(models.Todo.id == id)
    todo = todo_query.first()

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"todo with id : {id} not found",
        )

    if current_user.id != todo.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post",
        )

    todo_query.update(update_todo.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(todo)
    return todo


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    todo_query = db.query(models.Todo).filter(models.Todo.id == id)
    todo = todo_query.first()

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"todo with id : {id} not found",
        )

    if current_user.id != todo.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post",
        )

    todo_query.delete()
    db.commit()

    return
