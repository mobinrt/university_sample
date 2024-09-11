from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from DEPEND.depend_service import get_student_service, get_classroom_service, get_course_service, get_teacher_service  
from USECASE.manage_student import StudentUsecase
from USECASE.manage_teacher import TeacherUsecase
from USECASE.manage_classroom import ClassroomUsecase
from USECASE.manage_course import CourseUsecase
from id_manager import get_unique_id_instance
from DB.database import db

async def get_usecase(usecase_class, service_function, session: AsyncSession = Depends(db.get_session)):
    unique_id_instance = await get_unique_id_instance()
    service = await service_function(session)
    return usecase_class(service, unique_id_instance)

async def get_student_usecase(session: AsyncSession = Depends(db.get_session)) -> StudentUsecase:
    return await get_usecase(StudentUsecase, get_student_service, session)

async def get_teacher_usecase(session: AsyncSession = Depends(db.get_session)) -> TeacherUsecase:
    return await get_usecase(TeacherUsecase, get_teacher_service, session)

async def get_classroom_usecase(session: AsyncSession = Depends(db.get_session)) -> ClassroomUsecase:
    return await get_usecase(ClassroomUsecase, get_classroom_service, session)

async def get_course_usecase(session: AsyncSession = Depends(db.get_session)) -> CourseUsecase:
    return await get_usecase(CourseUsecase, get_course_service, session)