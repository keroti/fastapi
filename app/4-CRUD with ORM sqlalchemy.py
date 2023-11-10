from fastapi import FastAPI, Response, status, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, SessionLocal, get_db
from .models import Post


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def find_post(id):
	for post in my_posts:
		if int(post["id"]) == int(id):
			return post
	return None

def find_index_post(id):
	for i, j   in enumerate(my_posts):
		if j["id"] == id:
			return i



@app.get("/")
def root():
	return {"message": "Hello Keroti! How are you?"}


@app.get("/posts")  # Get all posts
def getPost(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED)  # Create a new post
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict()) # Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}") # Get a single post
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT) # Delete a single post
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    post.delete(synchronize_session=False)
    db.commit()


@app.put("/posts/{id}") #update post
def update_post(id: int, updated_post: schemas.CreatePost, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    post_new = post.first()
    if post_new == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    post.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post.first()

# @app.get("/posts/latest") # Get the latest post
# def get_latest_post():
# 	post = my_posts[len(my_posts) - 1]
# 	return {"latest_post": post}