from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
from urllib.parse import quote

# Assuming your password contains special characters like '@'
encoded_password = quote(settings.database_password, safe='')
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{encoded_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}" # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

print(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()