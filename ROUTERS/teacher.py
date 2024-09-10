from fastapi import APIRouter, status, Depends
from typing import List

from SERVICE.services_teacher import TeacherServices
from SCHEMA.schema_teacher import TeacherDisplay, TeacherCreate, TeacherUpdate
from dependencies import get_teacher_service, get_auth_service
from AUTH.athentication import oauth2_sc
from AUTH.auth_services import AuthServices

router = APIRouter(prefix='/teacher', tags=['teacher'])

@router.post("/create/", response_model=TeacherDisplay, status_code=status.HTTP_201_CREATED)
async def create_teacher(teacher: TeacherCreate, teacher_service: TeacherServices = Depends(get_teacher_service)):
    return await teacher_service.create_object(teacher)

@router.get("/get/teacher/by/id/{teacher_id}", response_model=TeacherDisplay, status_code=status.HTTP_200_OK)
async def get_teacher_by_id(stu_id:int, teacher_service: TeacherServices = Depends(get_teacher_service)):
    return await teacher_service.get_object_by_id(stu_id)
    
@router.get("/get/all", response_model=List[TeacherDisplay], status_code=status.HTTP_200_OK)
async def get_all_teachers(teacher_service: TeacherServices = Depends(get_teacher_service)):
    return await teacher_service.get_all_objects()

@router.put('/update/me', status_code=status.HTTP_200_OK)
async def update_teacher(
    teacher: TeacherUpdate,
    token: str = Depends(oauth2_sc),
    auth_service: AuthServices = Depends(get_auth_service),
    teacher_service: TeacherServices = Depends(get_teacher_service)
    ):
    current_user = await auth_service.get_current_user(token)
    return await teacher_service.update_obj(teacher, current_user)

@router.delete('/delete/by/id/{teacher_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_teacher_by_id(stu_id: int, teacher_service: TeacherServices = Depends(get_teacher_service)):
    await teacher_service.delete_by_id(stu_id)

@router.get('/get/hash_table/id', response_model=dict, status_code=status.HTTP_200_OK)
async def get_hash_table_id(teacher_service: TeacherServices = Depends(get_teacher_service)):
    return await teacher_service.get_hash_table_id()

@router.delete("/delete/students/by/{student_id}/from/courses/{course_id}", status_code=status.HTTP_200_OK)
async def remove_student_from_course(
    student_id: int,
    course_id: int,
    token: str = Depends(oauth2_sc), 
    auth_service: AuthServices = Depends(get_auth_service),
    teacher_service: TeacherServices = Depends(get_teacher_service)
):
    current_user = await auth_service.get_current_user(token)
    response = await teacher_service.fired_students_from_course(course_id, student_id, current_user)
    return response
    