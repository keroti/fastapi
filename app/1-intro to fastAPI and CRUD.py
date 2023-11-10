from fastapi import FastAPI, Response, status
from fastapi import Body
from pydantic import BaseModel
from typing import Optional
from random import randint
from fastapi.exceptions import HTTPException


app = FastAPI()

class Post(BaseModel):
	title: str
	content: str
	published: bool = True
	rating: Optional[int] = None

my_posts = [{"title": "Title of post 1", "content": "Content of post 1", "id": "1"}, {"title": "Title of post 2", "content": "Content of post 2", "id": "2"}]

def find_post(id):
	for post in my_posts:
		if int(post["id"]) == int(id):
			return post
	return None

@app.get("/")
def root():
	return {"message": "Hello Keroti! How are you?"}


@app.get("/posts")  # Get all posts
def getPost():
	return {"message": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)  # Create a new post
def create_posts(post: Post):
	post_dict = post.dict()
	post_dict["id"] = randint(0, 10000)
	my_posts.append(post_dict)
	return {"data": post_dict}
@app.get("/posts/latest") # Get the latest post
def get_latest_post():
	post = my_posts[len(my_posts) - 1]
	return {"latest_post": post}


@app.get("/posts/{id}") # Get a single post
def get_post(id: int, response: Response):
	post = find_post(int(id))
	if not post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
		# response.status_code = status.HTTP_404_NOT_FOUND
		# return {"message": f"post with id {id} not found"}
	return {"post_details": post}
def find_index_post(id):
	for i, j   in enumerate(my_posts):
		if j["id"] == id:
			return i

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT) # Delete a single post
def delete_post(id):
	#find index of post
	index = find_index_post(id)

	if index == None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

	my_posts.pop(index)
	return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}") #update post
def update_post(id, post: Post):
	index = find_index_post(id)

	if index == None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

	post_dict = post.dict()
	post_dict['id']= id
	my_posts[index]= post_dict
	return {'data': post_dict}