from src.base.repository import SQLAlchemyRepository
from src.user_job.model import UserJobModel
from src.database import SessionLocal
from sqlalchemy import select


class UserJobRepository(SQLAlchemyRepository):
    alchemy_model: type[UserJobModel] = UserJobModel

    def read_all_by_property(
        self,
        property_name: str,
        property_value: any,
    ):
        """Read one entry of a specified model by a specified field from db."""
        with SessionLocal() as session:
            query = select(self.alchemy_model).where(
                getattr(self.alchemy_model, property_name) == property_value,
            )
            result = session.execute(query)
            return result.scalars().all()
