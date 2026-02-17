import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.model import BaseAlchemyModel


class VacancyModel(BaseAlchemyModel):
    __tablename__ = "vacancy"

    vacancy_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
    )

    vacancy_name: Mapped[str] = mapped_column(String(50), nullable=True)
