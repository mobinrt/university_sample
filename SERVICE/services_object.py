from typing import Type, TypeVar, List, Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from abc import abstractmethod

from UTILITY.utility_course import CourseUtils 
from UTILITY.custom_error import CustomError
from id_manager import UniqueID
from ENUMS.object_type_str import ObjectToSTR 
import hash

T = TypeVar('T')  

class ObjectServices:
    def __init__(self, session: AsyncSession, unique_id: UniqueID, model: Type[T], object_to_str: ObjectToSTR) -> None:
        self.session = session
        self.unique_id = unique_id
        self.model = model
        self.object_to_str = object_to_str
    
    @abstractmethod
    async def create_object(self, new_object: T) -> T:
        pass
    
    
    async def get_object_by_id(self, object_id: int) -> T:
        result = await self.session.execute(select(self.model).filter(self.model.id == object_id))
        object = result.scalars().first()
        if object is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{self.model.__name__} not found')
        
        return object


    async def get_all_objects(self) -> List[T]:
        result = await self.session.execute(select(self.model))
        objects = result.scalars().all()
        return objects
    
    
    async def update_obj(self, update_obj, current_obj):
        for var, value in vars(update_obj).items():
            if var == 'password':
                value = hash.get_password_hash(value)  
            setattr(current_obj, var, value) if value else None
        
        self.session.add(current_obj)    
        await self.session.commit()
        await self.session.refresh(current_obj)
        return current_obj
        
            
    async def delete_by_id(self, object_id: int):
        del_object = await self.get_object_by_id(object_id)
        if not del_object:
            CustomError.existince_check(object_id, self.object_to_str.value, False)

        if self.object_to_str.value != 'classroom':
            self.unique_id.delete(object_id, self.object_to_str.value)
            self.unique_id.save_to_file('unique_id_state.json')

        if self.object_to_str.value in ['classroom', 'teacher']:
            await CourseUtils.delete_courses_by_object_id(self.session, object_id, self.object_to_str.value, self.unique_id)

        await self.session.delete(del_object)
        await self.session.commit()
        
    async def get_hash_table_id(self) -> dict:
        return self.unique_id.get_table(self.object_to_str.value)

