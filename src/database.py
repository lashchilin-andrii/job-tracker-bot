from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from src.config import DatabaseConfig

engine = create_engine(
    url=DatabaseConfig().sqlite_dsn(),
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class BaseAlchemyModel(DeclarativeBase):
    _columns_values = ""
    _columns_to_show = 2

    def __repr__(self) -> str:
        """Return string representation of a model with limited columns."""
        for i, column in enumerate(self.__table__.c):
            if i < self._columns_to_show:
                self._columns_values += f"{column.key}={getattr(self, column.key)} "
            else:
                continue
        return f"{self.__tablename__}({self._columns_values.strip()})"
