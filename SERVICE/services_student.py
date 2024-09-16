from DB.models import StudentModel, CourseModel, student_course_association
from SERVICE.services_object import ObjectServices
from SCHEMA.schema_student import StudentCreate
import hash

from sqlalchemy.ext.asyncio import AsyncSession

class StudentServices(ObjectServices):
    def __init__(self, session: AsyncSession):
        super().__init__(session, StudentModel)
        
    async def create_object(self, new_student: StudentCreate, stu_id: int):
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
            return db_student
    
    
    async def enroll_student_in_course(self, course_id: int, student_id: int):    
        
        await self.session.execute(
        student_course_association.insert().values(
            student_id=student_id,
            course_id=course_id
            )
        )
        await self.session.commit()
        
