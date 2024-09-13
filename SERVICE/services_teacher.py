from DB.models import TeacherModel
from SERVICE.services_object import ObjectServices
from DB.models import student_course_association
import hash

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

class TeacherServices(ObjectServices):
    def __init__(self, session: AsyncSession):
        super().__init__(session, TeacherModel)
        
    async def create_object(self, new_teacher: TeacherModel, teacher_id: int):
        hash_password = hash.get_password_hash(new_teacher.password)
        db_teacher = self.model(id=teacher_id, name=new_teacher.name, password=hash_password)

        self.session.add(db_teacher)
        await self.session.commit()
        await self.session.refresh(db_teacher)
        return db_teacher

    async def remove_student_from_course(self, course_id: int, student_id: int):
        await self.session.execute(
            delete(student_course_association).where(
                student_course_association.c.course_id == course_id,
                student_course_association.c.student_id == student_id
            )
        )
        await self.session.commit()