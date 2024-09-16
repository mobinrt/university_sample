from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from abc import abstractmethod

from DB.models import StudentModel, student_course_association

class EnrollmentStudentInCourse:
    
    @staticmethod
    async def is_student_enrolled_in_course(session: AsyncSession, course_id: int, student_id: int):
            student_enrollment_query = await session.execute(
            select(StudentModel.id).join(student_course_association).where(
                student_course_association.c.course_id == course_id,
                student_course_association.c.student_id == student_id
                )
            )
            return student_enrollment_query.scalar() is not None
    