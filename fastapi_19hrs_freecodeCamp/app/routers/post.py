from typing import List

from fastapi import status, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import Response

from fastapi_19hrs_freecodeCamp.app import models
from fastapi_19hrs_freecodeCamp.app.database import get_db
from fastapi_19hrs_freecodeCamp.app.oauth2 import get_current_user
from fastapi_19hrs_freecodeCamp.app.schema import PostUpdate, PostCreate, Post, UserOut

router = APIRouter(
    prefix='/posts', tags=["Posts"]
)


@router.get("/", response_model=List[Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""select * from posts""")
    # postsdb = cursor.fetchall()
    postsdb = db.query(models.Post).all()
    return postsdb


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: UserOut = Depends(get_current_user)):
    # print(post)
    # print(post.dict())
    # post_dict = post.dict()
    # post_dict["id"] = random.randrange(0, 100001010100101)
    # posts.append(post_dict)

    # new_post = models.Post(
    #     title=post.title, content=post.content, published=post.published
    # )
    # print(current_user.id, current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=Post)
def update_post(id: int, updated_post: PostUpdate, db: Session = Depends(get_db),
                current_user: UserOut = Depends(get_current_user)):
    # post_d = post.dict()
    # print(post)
    # for i, p in enumerate(posts):
    #     if p["id"] == id:
    #         post_d["id"] = id
    #         posts[i] = post_d
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to update")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: UserOut = Depends(get_current_user)):
    # p = delete_post_l(id)
    # return {"data": find_post(id)}
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to delete")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
