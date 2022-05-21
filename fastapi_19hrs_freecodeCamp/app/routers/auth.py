from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from fastapi_19hrs_freecodeCamp.app.database import get_db
from fastapi_19hrs_freecodeCamp.app.oauth2 import create_access_token
from fastapi_19hrs_freecodeCamp.app.schema import UserLogin, Token
from fastapi_19hrs_freecodeCamp.app import models
from fastapi_19hrs_freecodeCamp.app.utils import verify_password

router = APIRouter(tags=["Authentication"])


@router.post('/login',response_model=Token)
def login(user_credntials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credntials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    if not verify_password(user_credntials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid pwd credentials")

    access_token = create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
