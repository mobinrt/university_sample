from DB.models import TeacherModel, CourseModel
from id_manager import UniqueID
from ENUMS.object_type_str import ObjectToSTR
from ENUMS.object_type_digit import ObjectDigits
from SCHEMA.schema_teacher import TeacherDisplay
from SERVICE.services_object import ObjectServices
from UTILITY.custom_error import CustomError
from DB.models import student_course_association
import hash

from sqlalchemy import delete  
from sqlalchemy.future import select
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


class TeacherServices(ObjectServices):
    def __init__(self, session: AsyncSession, unique_id: UniqueID):
        super().__init__(session, unique_id, TeacherModel, ObjectToSTR.TEACHER)
        
    async def create_object(self, new_teacher: TeacherModel):
        if not new_teacher.name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username should not be blank!')

        teacher_id = self.unique_id.insert(ObjectDigits.TEACHER.value, ObjectToSTR.TEACHER.value)
        hash_password = hash.get_password_hash(new_teacher.password)
        db_teacher = self.model(id=teacher_id, name=new_teacher.name, password=hash_password)

        self.session.add(db_teacher)
        await self.session.commit()
        await self.session.refresh(db_teacher)
        self.unique_id.save_to_dict(db_teacher.name, db_teacher.id, ObjectToSTR.TEACHER.value)
        return db_teacher

    async def update_obj(self, update_teacher: TeacherModel, login_teacher: TeacherModel):
        current_teacher = await super().update_obj(update_teacher, login_teacher)
        return TeacherDisplay.model_validate(current_teacher)
    
    async def fired_students_from_course(self, course_id: int, student_id: int, current_user: TeacherModel):
        course_query = await self.session.execute(
            select(CourseModel).where(CourseModel.id == course_id)
        )
        course = course_query.scalars().first()
        
        if not course:
            CustomError.existince_check(course_id, ObjectToSTR.COURSE, 0)
        
        if course.teacher_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to remove students from this course."
            )
            
        student_enrollment_query = await self.session.execute(
            select(student_course_association.c.student_id).where(
                student_course_association.c.course_id == course_id,
                student_course_association.c.student_id == student_id
            )
        )
        is_enrolled = student_enrollment_query.scalar() is not None

        if not is_enrolled:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student is not enrolled in this course."
            )
            
        await self.session.execute(
            delete(student_course_association).where(
                student_course_association.c.course_id == course_id,
                student_course_association.c.student_id == student_id
            )
        )
        await self.session.commit()

        return {"message": f"Student with ID {student_id} has been removed from course {course.name}."}
