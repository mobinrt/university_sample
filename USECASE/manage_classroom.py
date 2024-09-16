from SERVICE.services_classroom import ClassroomServices
from DB.models import ClassModel, CourseModel
from ENUMS.object_type_str import ObjectToSTR
from id_manager import UniqueID
from SCHEMA.schemas import ClassCreate, ClassDisplay
from USECASE.manage_object import ObjectUseCase
from ENUMS.object_type_digit import ObjectDigits
from UTILITY.custom_error import CustomError

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

class ClassroomUseCase(ObjectUseCase[ClassroomServices]):
    def __init__(self, classroom_service: ClassroomServices, unique_id: UniqueID):
        super().__init__(classroom_service, unique_id, ObjectToSTR.CLASSROOM)
    
    async def create(self, new_classroom: ClassCreate):
        if not new_classroom.id or new_classroom.id <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Class number is not valid!')
        
        if await self.service.get_object_by_id():
            CustomError.existince_check(new_classroom.id, ObjectToSTR.CLASSROOM, True)
        
        await self.service.create_object(new_classroom)
        
    async def update(self, updated_class: ClassCreate, old_classroom: ClassModel):
        exist_classroom = await self.service.get_object_by_id(updated_class.id)
        if exist_classroom:
            CustomError.existince_check(exist_classroom.id, ObjectToSTR.CLASSROOM, True)
        
        await self.service.update_class_id(old_classroom.id, updated_class.id)
        classroom = await self.service.update_obj(updated_class, old_classroom)
        return ClassDisplay.model_validate(classroom)
    