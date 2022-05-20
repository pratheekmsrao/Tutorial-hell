from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session

from fastapi_19hrs_freecodeCamp.app import models
from fastapi_19hrs_freecodeCamp.app.database import get_db
from fastapi_19hrs_freecodeCamp.app.schema import UserCreate, UserOut
from fastapi_19hrs_freecodeCamp.app.utils import get_password_hash

router = APIRouter(
    prefix='/users',tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_pwd = get_password_hash(user.password)

    user.password = hashed_pwd
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return user
