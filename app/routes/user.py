from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from .. import database, models, schema, util, oauth2


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


@router.post(
    "/create", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut
)
def create_user(user: schema.CreateUser, db: Session = Depends(database.get_db)):

    hashed_password = util.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = oauth2.create_access_token(data={"user_id": new_user.id})
    return {
        "id": new_user.id,
        "email": new_user.email,
        "created_at": new_user.created_at,
        "token": {"access_token": access_token, "token_type": "bearer"},
    }


@router.put("/{id}")
def update_user():
    pass


@router.delete("/{id}")
def delete_user(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    user_query = db.query(models.User).filter(models.User.id == id)
    user_exist = user_query.first()

    if user_exist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id : {id} not found",
        )

    # if user_exist.id != current_user.id:  # type:ignore
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN, detail="request action not allowed"
    #     )

    user_query.delete(synchronize_session=False)
    db.commit()
    db.refresh(user_exist)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
