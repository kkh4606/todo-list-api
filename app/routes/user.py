from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import database, models, schema, util


router = APIRouter(prefix="/users", tags=["USER"])


@router.get("/")
def get_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()

    return users


@router.get("/{id}")
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id : {id} not found",
        )

    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.CreateUser, db: Session = Depends(database.get_db)):

    hashed_password = util.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.put("/{id}")
def update_user():
    pass


@router.delete("/{id}")
def delete_user():
    pass
