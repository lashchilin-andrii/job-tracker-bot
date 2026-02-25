import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.base.model import BaseAlchemyModel


class UserModel(BaseAlchemyModel):
    __tablename__ = "user"

    user_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
    )

    user_name: Mapped[str] = mapped_column(String(50), nullable=True)
    user_first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    user_last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    user_language: Mapped[str] = mapped_column(String(10), nullable=False)
