from fastapi import FastAPI, Response, status, Depends
# from fastapi import Body
from typing import Optional, List
from passlib.context import CryptContext
# from random import randint
from fastapi.exceptions import HTTPException
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, SessionLocal, get_db
from .models import Post



models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', port=5433, database='fastapi', user='postgres',  password='99keroti', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connected')
#         break
#     except Exception as error:
#         print('Connecting to database failed')
#         print("Error: ", error)
#         time.sleep(2)

# my_posts = [{"title": "Title of post 1", "content": "Content of post 1", "id": "1"}, {"title": "Title of post 2", "content": "Content of post 2", "id": "2"}]

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


@app.get("/posts", response_model=List[schemas.Post])  # Get all posts
def getPost(db: Session = Depends(get_db)):
	# cursor.execute("""SELECT * FROM posts""")
	# posts = cursor.fetchall()
	# print(posts)
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)  # Create a new post
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db)):
	# cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
	# new_post = cursor.fetchone()
	# conn.commit()
    new_post = models.Post(**post.dict()) # Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model=schemas.Post) # Get a single post
def get_post(id: int, db: Session = Depends(get_db)):
# 	cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
# 	post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
		# response.status_code = status.HTTP_404_NOT_FOUND
		# return {"message": f"post with id {id} not found"}
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT) # Delete a single post
def delete_post(id: int, db: Session = Depends(get_db)):
# 	#find index of post
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    post.delete(synchronize_session=False)
    db.commit()


@app.put("/posts/{id}", response_model=schemas.Post) #update post
def update_post(id: int, updated_post: schemas.CreatePost, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)
    post_new = post.first()
    if post_new == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    post.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post.first()


@app.post("/user", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)  # Create a new post
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    hashed = pwd_context.hash(user.password)
    user.password = hashed
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users", response_model=List[schemas.CreateUser])  # Get all users
def getPost(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users