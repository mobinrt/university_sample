from typing import Type, TypeVar, List, Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from abc import abstractmethod

from SERVICE.base_service import BaseService
import hash

T = TypeVar('T')  

class ObjectServices(BaseService):
    def __init__(self, session: AsyncSession, model: Type[T]) -> None:
        self.session = session
        self.model = model
        
    @abstractmethod
    async def create_object(self, new_object: T) -> T:
        pass
    
    
    async def get_object_by_id(self, object_id: int) -> T:
        result = await self.session.execute(select(self.model).filter(self.model.id == object_id))
        object = result.scalars().first()
        return object
    
    async def get_object_by_id_for_model(self, object_id: int, model: Type[T]) -> T:
        result = await self.session.execute(select(model).filter(model.id == object_id))
        object = result.scalars().first()
        return object
        

    async def get_all_objects(self) -> List[T]:
        result = await self.session.execute(select(self.model))
        objects = result.scalars().all()
        return objects
    
    
    async def update_obj(self, update_obj: T, current_obj: T) -> T:
        for var, value in vars(update_obj).items():
            if var == 'password':
                value = hash.get_password_hash(value)  
            setattr(current_obj, var, value) if value else None
        
        self.session.add(current_obj)    
        await self.session.commit()
        await self.session.refresh(current_obj)
        return current_obj
        
            
    async def delete_by_id(self, del_object: int):
        await self.session.delete(del_object)
        await self.session.commit()
        
    
