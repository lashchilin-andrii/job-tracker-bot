import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.database import BaseAlchemyModel


class VacancyModel(BaseAlchemyModel):
    __tablename__ = "vacancy"

    vacancy_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    vacancy_name: Mapped[str] = mapped_column(String(50), nullable=True)
