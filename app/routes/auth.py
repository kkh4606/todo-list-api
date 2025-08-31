from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, models, util, oauth2, schema


router = APIRouter(tags=["AUTHENTICATION"])


@router.post("/login")
def user_login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    if user is None or not util.verify_password(
        user_credentials.password, user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials"
        )

    access_token = oauth2.create_access_token(data={"user_id": str(user.id)})

    tokenData = schema.Token(access_token=access_token, token_type="bearer")

    return tokenData
