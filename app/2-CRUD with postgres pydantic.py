from fastapi import FastAPI, Response, status
from fastapi import Body
from pydantic import BaseModel
from typing import Optional
from random import randint
from fastapi.exceptions import HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
	title: str
	content: str
	published: bool = True
	rating: Optional[int] = None
while True:
    try:
        conn = psycopg2.connect(host='localhost', port=5433, database='fastapi', user='postgres',  password='99keroti', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connected')
        break
    except Exception as error:
        print('Connecting to database failed')
        print("Error: ", error)
        time.sleep(2)

my_posts = [{"title": "Title of post 1", "content": "Content of post 1", "id": "1"}, {"title": "Title of post 2", "content": "Content of post 2", "id": "2"}]

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
def getPost():
	cursor.execute("""SELECT * FROM posts""")
	posts = cursor.fetchall()
	print(posts)
	return {"message": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)  # Create a new post
def create_posts(post: Post):
	cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
	new_post = cursor.fetchone()
	conn.commit()
	return {"data": new_post}


@app.get("/posts/{id}") # Get a single post
def get_post(id: int, response: Response):
	cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
	post = cursor.fetchone()
	if not post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
		# response.status_code = status.HTTP_404_NOT_FOUND
		# return {"message": f"post with id {id} not found"}
	return {"post_details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT) # Delete a single post
def delete_post(id):
	#find index of post
	cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
	deleted_post = cursor.fetchone()
	conn.commit()
	if deleted_post == None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
	return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}") #update post
def update_post(id, post: Post):
	cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, id,))
	updated_post = cursor.fetchone()
	conn.commit()
	if updated_post == None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
	return {'data': updated_post}


@app.get("/posts/latest") # Get the latest post
def get_latest_post():
	post = my_posts[len(my_posts) - 1]
	return {"latest_post": post}
