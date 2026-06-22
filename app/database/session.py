import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/task_market")

connect_args = {}
if "postgresql" in DATABASE_URL:
    connect_args = {"options": "-c lc_messages=en_US.UTF-8"}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# function for getting session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()