from src.base.repository import SQLAlchemyRepository
from src.user.model import UserModel


class UserRepository(SQLAlchemyRepository):
    alchemy_model: type[UserModel] = UserModel
