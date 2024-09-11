from abc import ABC, abstractmethod
from typing import TypeVar, List

T = TypeVar('T')

class BaseService(ABC):
    @abstractmethod
    async def create_object(self, new_object: T) -> T:
        pass

    @abstractmethod
    async def get_object_by_id(self, object_id: int) -> T:
        pass

    @abstractmethod
    async def get_all_objects(self) -> List[T]:
        pass

    @abstractmethod
    async def update_obj(self, update_object: T, current_object: T) -> T:
        pass

    @abstractmethod
    async def delete_by_id(self, object_id: int) -> None:
        pass
