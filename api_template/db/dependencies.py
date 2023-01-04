from typing import AsyncGenerator

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api_template.settings import settings

engine = create_engine(str(settings.db_url), pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_db_session() -> Session:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()