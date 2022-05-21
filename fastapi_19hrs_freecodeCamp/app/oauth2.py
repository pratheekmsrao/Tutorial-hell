from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi_19hrs_freecodeCamp.app import models
from fastapi_19hrs_freecodeCamp.app.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# screte key
# algorithm
# expiration time
from fastapi_19hrs_freecodeCamp.app.schema import TokenData

SECRET_KEY = "fc1056ce25c477a9a4ae487a6b49e666779821a4eab4f1b5caa24f87084aad10"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exceptions
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exceptions
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not authorize",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token, credentials_exceptions)
    user=db.query(models.User).filter(models.User.id==token.id).first()
    return user
