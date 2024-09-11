from SERVICE.services_object import ObjectServices
from SCHEMA.schema_student import StudentCreate, StudentUpdate, StudentDisplay
from UTILITY.singelton_meta import SingletonMeta
from UTILITY.custom_error import CustomError
from UTILITY.utility_course import CourseUtils
from id_manager import UniqueID
from ENUMS.object_type_str import ObjectToSTR 

from abc import abstractmethod
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypeVar, List, Generic

T = TypeVar('T')
TService = TypeVar('TService', bound=ObjectServices)

class ObjectUseCase(Generic[TService]):
    def __init__(self, service: TService, unique_id: UniqueID, object_to_str: ObjectToSTR):
        self.service = service
        self.unique_id = unique_id
        self.object_to_str = object_to_str
    
    @abstractmethod
    async def create(self, new_object: T) -> T:
        pass
    
    async def get_by_id(self, object_id: int) -> T:
        selected_obj = await self.service.get_object_by_id(object_id)
        if selected_obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{self.model.__name__} not found')
        return selected_obj
        
    async def get_all(self) -> List[T]:
        return await self.service.get_all_objects()
    
    async def update(self, update_obj: T, current_obj: T) -> T:
        return await self.service.update_obj(update_obj, current_obj)
    
    async def delete(self, object_id: int):
        del_object = await self.service.get_object_by_id(object_id)
        if not del_object:
            CustomError.existince_check(object_id, self.object_to_str.value, False)
            
        if self.object_to_str.value != 'classroom':
            self.unique_id.delete(object_id, self.object_to_str.value)
            self.unique_id.save_to_file('unique_id_state.json')

        if self.object_to_str.value in ['classroom', 'teacher']:
            await CourseUtils.delete_courses_by_object_id(self.session, object_id, self.object_to_str.value, self.unique_id)
    
        await self.service.delete_by_id(del_object)
        
        
    async def get_hash_table_id(self) -> dict:
        return self.unique_id.get_table(self.object_to_str.value)

        