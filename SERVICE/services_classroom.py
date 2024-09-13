from DB.models import ClassModel, CourseModel
from SERVICE.services_object import ObjectServices

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

class ClassroomServices(ObjectServices):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ClassModel)
                           
    async def create_object(self, new_classroom: ClassModel):      
        db_classroom = ClassModel(id=new_classroom.id)
        self.session.add(db_classroom)
        await self.session.commit()
        await self.session.refresh(db_classroom)
        return db_classroom
               
    async def update_class_id(self, old_id: int, new_id: int):
        result = await self.session.execute(
            "UPDATE courses SET class_id = :new_id WHERE class_id = :old_id",
            {'new_id': new_id, 'old_id': old_id}
        )
        if result.rowcount == 0:
            raise ValueError("No courses were updated, check if old_id exists.")
    
    async def get_hash_table_id(slef):
        raise NotImplementedError("This method is not applicable for ClassroomServices")
    