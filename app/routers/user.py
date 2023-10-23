from fastapi import FastAPI, Response, status, Depends, APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import models, schemas, utils
from ..database import engine, SessionLocal, get_db

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)  # Create a new post
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    #hash password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    #create new user
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=List[schemas.CreateUser])  # Get all users
def getPost(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get("/{id}", response_model=schemas.UserOut) # Get a single user
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found")

    return user
