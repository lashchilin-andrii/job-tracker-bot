from src.base.repository import SQLAlchemyRepository
from src.job.model import JobModel


class JobRepository(SQLAlchemyRepository):
    alchemy_model: type[JobModel] = JobModel
