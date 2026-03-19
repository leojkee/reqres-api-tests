from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from infrastructure.db.base import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):

    def __init__(self, session: Session, model: type[T]):
        self.session = session
        self.model = model

    def create(self, entity: T) -> T:
        self.session.add(entity)
        self.session.flush()
        self.session.refresh(entity)
        return entity

    def get_by_id(self, entity_id: int) -> T | None:
        return self.session.get(self.model, entity_id)

    def get_all(self) -> list[T]:
        return list(self.session.query(self.model).all())

    def delete(self, entity: T) -> None:
        self.session.delete(entity)
        self.session.flush()
