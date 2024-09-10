from DB.models import ClassModel, CourseModel
from SERVICE.services_object import ObjectServices
from ENUMS.object_type_str import ObjectToSTR
from id_manager import UniqueID
from UTILITY.custom_error import CustomError
from SCHEMA.schemas import ClassDisplay, ClassCreate

from sqlalchemy.future import select
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

class ClassroomServices(ObjectServices):
    
    def __init__(self, session: AsyncSession, unique_id: UniqueID):
        super().__init__(session, unique_id, ClassModel, ObjectToSTR.CLASSROOM)
    
    async def classroom_query(self, new_classroom_id: int):
        classroom = await self.session.execute(
            select(ClassModel).where(ClassModel.id == new_classroom_id)
        )
        classroom = classroom.scalars().first()
        
        if classroom:
            CustomError.existince_check(classroom.id, ObjectToSTR.CLASSROOM, 1)
                           
    async def create_object(self, new_classroom: ClassModel):
        if not new_classroom.id or new_classroom.id <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Class number is not valid!')
        
        self.classroom_query(new_classroom.id) 
               
        db_classroom = ClassModel(id=new_classroom.id)
        self.session.add(db_classroom)
        await self.session.commit()
        await self.session.refresh(db_classroom)
        return db_classroom
               
    async def update_obj(self, updated_class: ClassCreate, old_classroom: ClassModel):
        self.classroom_query(updated_class.id)
        self.update_class_id(old_classroom.id, updated_class.id)    
        classroom = await super().update_obj(updated_class, old_classroom)
        return ClassDisplay.model_validate(classroom)
               
    async def get_hash_table_id(slef):
        raise NotImplementedError("This method is not applicable for ClassroomServices")
    
    async def update_class_id(self, old_id: int, new_id: int):
        result = await self.session.execute(
            "UPDATE courses SET class_id = :new_id WHERE class_id = :old_id",
            {'new_id': new_id, 'old_id': old_id}
        )
        if result.rowcount == 0:
            raise ValueError("No courses were updated, check if old_id exists.")