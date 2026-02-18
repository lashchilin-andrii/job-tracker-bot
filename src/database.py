from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import DatabaseConfig

engine = create_engine(
    url=DatabaseConfig().DB_PATH,
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
