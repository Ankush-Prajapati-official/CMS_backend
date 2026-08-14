from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import DATABASE_URL
from app.models.base import Base

#create connection with postgre
engine = create_engine(
    DATABASE_URL,
    echo=True
)

# create session 
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)