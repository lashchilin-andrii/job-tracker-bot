from src.database import SessionLocal
from src.user_job.model import UserJobModel
from src.base.repository import SQLAlchemyRepository


class UserJobRepository(SQLAlchemyRepository):
    alchemy_model: type[UserJobModel] = UserJobModel

    def update_one(self, alchemy_object: UserJobModel):
        with SessionLocal() as session:
            db_obj = session.get(
                self.alchemy_model,
                {"user_id": alchemy_object.user_id, "job_id": alchemy_object.job_id},
            )
            if not db_obj:
                return None

            for key, value in alchemy_object.__dict__.items():
                if key.startswith("_"):
                    continue
                setattr(db_obj, key, value)

            session.commit()
            session.refresh(db_obj)
            return db_obj
