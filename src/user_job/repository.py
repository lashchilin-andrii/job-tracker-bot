from src.base.repository import SQLAlchemyRepository
from src.user_job.model import UserJobModel


class UserJobRepository(SQLAlchemyRepository):
    alchemy_model: type[UserJobModel] = UserJobModel
