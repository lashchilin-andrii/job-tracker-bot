import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.base.model import BaseAlchemyModel


class UserJobModel(BaseAlchemyModel):
    __tablename__ = "user_job"

    user_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
    )

    job_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
    )

    user_job_status: Mapped[str] = mapped_column(String(50), nullable=False)
