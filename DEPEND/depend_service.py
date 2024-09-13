from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from DB.database import db
from id_manager import get_unique_id_instance
from SERVICE.services_student import StudentServices
from SERVICE.services_teacher import TeacherServices
from SERVICE.services_classroom import ClassroomServices
from SERVICE.services_course import CourseServices
from AUTH.auth_services import AuthServices

async def get_service(service_class, session: AsyncSession = Depends(db.get_session)):
    unique_id_instance = await get_unique_id_instance()
    return service_class(session, unique_id_instance)

async def get_student_service(session: AsyncSession = Depends(db.get_session)):     #one instanse
    return await get_service(StudentServices, session)

async def get_teacher_service(session: AsyncSession = Depends(db.get_session)):
    return await get_service(TeacherServices, session)

async def get_classroom_service(session: AsyncSession = Depends(db.get_session)):
    return await get_service(ClassroomServices, session)

async def get_course_service(session: AsyncSession = Depends(db.get_session)):
    return await get_service(CourseServices, session)

async def get_auth_service(session: AsyncSession = Depends(db.get_session)) -> AuthServices:
    return AuthServices(session=session)