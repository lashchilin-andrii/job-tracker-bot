import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.model import BaseAlchemyModel


class JobModel(BaseAlchemyModel):
    __tablename__ = "job"

    job_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
    )

    job_name: Mapped[str] = mapped_column(String(50), nullable=True)
