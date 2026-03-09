from src.user.schema import User
from src.user.model import UserModel
from src.user.repository import UserRepository


def create_user(user: User) -> UserModel | None:
    """Create a user in db from User model if not exists."""

    if UserRepository().read_by_property("user_id", user.user_id):
        return

    return UserRepository().create_one(
        UserModel(
            user_id=user.user_id,
            user_name=user.user_name,
            user_first_name=user.user_first_name,
            user_last_name=user.user_last_name,
            user_language=user.user_language,
        )
    )


def get_user_by_id(user_id: str) -> UserModel | None:
    """Get user entry from db by id or None."""
    return UserRepository().read_by_property("user_id", user_id)
