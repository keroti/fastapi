from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models
from .database import engine, SessionLocal, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return {"status": "success"}
