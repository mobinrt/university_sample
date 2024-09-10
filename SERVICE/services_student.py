from DB.models import StudentModel, CourseModel, student_course_association
from id_manager import UniqueID
from SERVICE.services_object import ObjectServices
from ENUMS.object_type_str import ObjectToSTR
from ENUMS.object_type_digit import ObjectDigits
from SCHEMA.schema_student import StudentDisplay
from UTILITY.custom_error import CustomError
import hash

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class StudentServices(ObjectServices):
    def __init__(self, session: AsyncSession, unique_id: UniqueID):
        super().__init__(session, unique_id, StudentModel, ObjectToSTR.STUDENT)
        
    async def create_object(self, new_student: StudentModel):
            if not new_student.name:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username should not be blank!')
            
            stu_id = self.unique_id.insert(ObjectDigits.STUDENT.value, ObjectToSTR.STUDENT.value)
            hash_password = hash.get_password_hash(new_student.password)
            db_student = self.model(id=stu_id, name=new_student.name, password=hash_password, major=new_student.major)
            '''
            Model Validation 
            or
            Service Layer Validation
            '''
            self.session.add(db_student)
            await self.session.commit()
            await self.session.refresh(db_student)
            self.unique_id.save_to_dict(db_student.name, db_student.id, ObjectToSTR.STUDENT.value)
            return db_student
    
    async def update_obj(self, update_stu: StudentModel, login_stu: StudentModel):
        current_stu = await super().update_obj(update_stu, login_stu)
        return StudentDisplay.model_validate(current_stu)
            
    async def attend_in_course(self, course_id: int, current_user: StudentModel):
        course_query = await self.session.execute(select(CourseModel).where(CourseModel.id == course_id))
        course = course_query.scalars().first()
        if not course:
            CustomError.existince_check(course_id, ObjectToSTR.COURSE, 0)

        student_enrollment_query = await self.session.execute(
        select(StudentModel.id).join(student_course_association).where(
            student_course_association.c.course_id == course_id,
            student_course_association.c.student_id == current_user.id
            )
        )
        is_enrolled = student_enrollment_query.scalar() is not None

        if is_enrolled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"You are already enrolled in course {course.name}."
            )

        await self.session.execute(
        student_course_association.insert().values(
            student_id=current_user.id,
            course_id=course_id
            )
        )
        await self.session.commit()
        await self.session.refresh(course)
        
        return {"message": f"You are enrolled in course {course.name}."}
    
