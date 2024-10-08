from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from DEPEND.depend_service import get_student_service, get_classroom_service, get_course_service, get_teacher_service  
from USECASE.manage_student import StudentUseCase
from USECASE.manage_teacher import TeacherUseCase
from USECASE.manage_classroom import ClassroomUseCase
from USECASE.manage_course import CourseUseCase
from id_manager import get_unique_id_instance
from DB.database import db

async def get_usecase(usecase_class, service_function, session: AsyncSession = Depends(db.get_session)):
    unique_id_instance = await get_unique_id_instance()
    service = await service_function(session)
    return usecase_class(service, unique_id_instance)

async def get_student_usecase(session: AsyncSession = Depends(db.get_session)) -> StudentUseCase:
    return await get_usecase(StudentUseCase, get_student_service, session)

async def get_teacher_usecase(session: AsyncSession = Depends(db.get_session)) -> TeacherUseCase:
    return await get_usecase(TeacherUseCase, get_teacher_service, session)

async def get_classroom_usecase(session: AsyncSession = Depends(db.get_session)) -> ClassroomUseCase:
    return await get_usecase(ClassroomUseCase, get_classroom_service, session)

async def get_course_usecase(session: AsyncSession = Depends(db.get_session)) -> CourseUseCase:
    return await get_usecase(CourseUseCase, get_course_service, session)