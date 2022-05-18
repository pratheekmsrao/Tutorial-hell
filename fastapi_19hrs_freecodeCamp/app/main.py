import random
from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from starlette.responses import Response

print("hi")

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "title of post 2", "content": "content of post 2", "id": 2},
]


def find_post(post_id: int):
    for post in posts:
        if post["id"] == post_id:
            return post
    return "not found"


def delete_post_l(post_id: int):
    for i, post in enumerate(posts):
        if post["id"] == post_id:
            posts.pop(i)
            return "post deleted"
    return "not found"


# def update_post(post: Post):
#     p = find_post(post.id)
#     p.update(post.dict())


@app.get("/", status_code=status.HTTP_200_OK)
def home():
    if random.randint(10, 20) % 2 == 0:
        raise HTTPException(status_code=500, detail="even number")
    return {"message": "Hello World!!!!", "status": 200}


@app.get("/posts")
def get_posts():
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    print(post)
    print(post.dict())
    post_dict = post.dict()
    post_dict["id"] = random.randrange(0, 100001010100101)
    posts.append(post_dict)
    return {"data": post}


@app.put("/posts/{id}", status_code=status.HTTP_201_CREATED)
def update_post(id: int, post: Post):
    post_d = post.dict()
    print(post)
    for i, p in enumerate(posts):
        if p["id"] == id:
            post_d["id"] = id
            posts[i] = post_d
    return {"data": find_post(id)}


@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_post(id: int):
    return {"data": find_post(int(id))}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    p = delete_post_l(id)
    # return {"data": find_post(id)}
    return Response(status_code=status.HTTP_204_NO_CONTENT)
