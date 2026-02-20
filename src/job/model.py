import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.base.model import BaseAlchemyModel


class JobModel(BaseAlchemyModel):
    __tablename__ = "job"

    job_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
    )

    job_name: Mapped[str] = mapped_column(String(100), nullable=False)
    job_location: Mapped[str] = mapped_column(String(50), nullable=True)
    job_salary: Mapped[str] = mapped_column(String(50), nullable=True)
    job_source: Mapped[str] = mapped_column(String(50), nullable=True)
    job_type: Mapped[str] = mapped_column(String(50), nullable=True)
    job_link: Mapped[str] = mapped_column(String(250), nullable=True)
    job_company: Mapped[str] = mapped_column(String(100), nullable=True)
    job_updated: Mapped[str] = mapped_column(String(50), nullable=True)
