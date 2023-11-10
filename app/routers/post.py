from fastapi import FastAPI, Response, status, Depends, APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import models, schemas
from ..database import engine, SessionLocal, get_db
from .. import oauth2


router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

# @router.get("/", response_model=List[schemas.Post])
@router.get("/")  # Get all posts
def getPosts(db: Session = Depends(get_db), limit: int = 15, skip: int =0, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("No_of_votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    formatted_results = []
    for post, vote_count in results:
        formatted_results.append({
            "Post": {
                "title": post.title,
                "content": post.content,
                "published": post.published,
                "id": post.id,
                "created_at": post.created_at,
                "owner_id": post.user_id,
                "owner": {
                    "id": post.owner.id,
                    "email": post.owner.email,
                    "created_at": post.owner.created_at
                }
        
            },
            "no_of_votes": vote_count 
        }
        )

    return formatted_results

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)  # Create a new post
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(user_id = current_user.id, **post.dict()) # Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.Post) # Get a single post
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT) # Delete a single post
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
 	#find index of post

    post = db.query(models.Post).filter(models.Post.id == id)
    post_new = post.first()
    if post_new == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    if post_new.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post.delete(synchronize_session=False)
    db.commit()


@router.put("/{id}", response_model=schemas.Post) #update post
def update_post(id: int, updated_post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    post_new = post.first()
    if post_new == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    if post_new.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post.first()