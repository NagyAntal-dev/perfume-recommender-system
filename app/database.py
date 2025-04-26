# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "postgresql://user:pass@192.168.0.108:5432/oltp_db"

engine = create_engine(DATABASE_URL, echo=True)  # echo for SQL logging :contentReference[oaicite:5]{index=5}
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
