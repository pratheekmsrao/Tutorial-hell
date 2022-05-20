import random

import psycopg2
from fastapi import FastAPI, HTTPException, status, Depends
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from fastapi_19hrs_freecodeCamp.app import models
from fastapi_19hrs_freecodeCamp.app.database import engine, get_db
from fastapi_19hrs_freecodeCamp.app.routers import post, user

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

try:
    conn = psycopg2.connect(
        host="localhost",
        database="fastapi",
        user="postgres",
        password="postgres1",
        cursor_factory=RealDictCursor,
    )
    cursor = conn.cursor()
    print("db connected")

except Exception as e:
    print("db connection error", e)

# def find_post(post_id: int):
#     for post in posts:
#         if post["id"] == post_id:
#             return post
#     return "not found"


# def delete_post_l(post_id: int):
#     for i, post in enumerate(posts):
#         if post["id"] == post_id:
#             posts.pop(i)
#             return "post deleted"
#     return "not found"


# def update_post(post: Post):
#     p = find_post(post.id)
#     p.update(post.dict())

app.include_router(post.router)
app.include_router(user.router)


@app.get("/", status_code=status.HTTP_200_OK)
def home():
    if random.randint(10, 20) % 2 == 0:
        raise HTTPException(status_code=500, detail="even number")
    return {"message": "Hello World!!!!", "status": 200}


@app.get("/sql")
def sql_get(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"status": "success", "data": posts}
