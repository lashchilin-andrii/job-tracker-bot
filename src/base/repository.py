from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import select

from src.database import SessionLocal
from src.base.model import BaseAlchemyModel


class AbstractRepository(ABC):
    @abstractmethod
    def create_one(self):
        raise NotImplementedError

    @abstractmethod
    def read_one_by_property(self):
        raise NotImplementedError

    @abstractmethod
    def read_all(self):
        raise NotImplementedError

    @abstractmethod
    def delete_one(self):
        raise NotImplementedError

    @abstractmethod
    def delete_one_by_property(self):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    alchemy_model: type[BaseAlchemyModel]

    def create_one(
        self,
        alchemy_object: BaseAlchemyModel,
    ):
        """Create one entry of a specified model in db."""
        with SessionLocal() as session:
            session.add(alchemy_object)
            session.commit()
            session.refresh(alchemy_object)
            return alchemy_object

    def read_one_by_property(
        self,
        property_name: str,
        property_value: Any,
    ):
        """Read one entry of a specified model by a specified field from db."""
        with SessionLocal() as session:
            query = select(self.alchemy_model).where(
                getattr(self.alchemy_model, property_name) == property_value,
            )
            result = session.execute(query)
            return result.scalars().first()

    def read_all(self):
        """Read all entries of a specified model from db."""
        with SessionLocal() as session:
            stmt = select(self.alchemy_model)
            result = session.execute(stmt)
            return result.scalars().all()

    def delete_one(
        self,
        alchemy_object_to_delete: BaseAlchemyModel,
    ):
        """Delete one entry of a given specified model."""
        with SessionLocal() as session:
            session.delete(alchemy_object_to_delete)
            session.commit()
            return alchemy_object_to_delete

    def delete_one_by_property(
        self,
        property_name: str,
        property_value: Any,
    ):
        """Delete one entry of a specified model by a specified field from db."""
        with SessionLocal() as session:
            entry = self.read_one_by_property(
                property_name=property_name,
                property_value=property_value,
            )
            if entry is None:
                return None
            session.delete(entry)
            session.commit()
            return entry
