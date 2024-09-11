from fastapi import APIRouter, status, Depends
from typing import List

from SERVICE.services_course import CourseServices

from SCHEMA.schemas import CourseCreate, CourseDisplay
from DEPEND.depend_service import get_course_service

router = APIRouter(prefix='/course', tags=['course'])

@router.post("/create/", response_model=CourseDisplay, status_code=status.HTTP_201_CREATED)
async def create_course(course: CourseCreate, course_service: CourseServices = Depends(get_course_service)):
    return await course_service.create_object(course)

@router.get("/get/course/by/id/{course_id}", response_model=CourseDisplay, status_code=status.HTTP_200_OK)
async def get_course_by_id(course_id:int, course_service: CourseServices = Depends(get_course_service)):
    return await course_service.get_object_by_id(course_id)
    
@router.get("/get/all", response_model=List[CourseDisplay], status_code=status.HTTP_200_OK)
async def get_all_courses(course_service: CourseServices = Depends(get_course_service)):
    return await course_service.get_all_objects()
    
@router.delete('/delete/by/id/{course_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_course_by_id(course_id: int, course_service: CourseServices = Depends(get_course_service)):
    await course_service.delete_by_id(course_id)
    
@router.put('/update/course/by/id/{course_id}', response_model=CourseDisplay, status_code=status.HTTP_200_OK)
async def update_course(course: CourseCreate, course_id, course_service: CourseServices = Depends(get_course_service)):
    return await course_service.update_obj(course, course_id)
    
@router.get('/get/hash_table/id', response_model=dict, status_code=status.HTTP_200_OK)
async def get_hash_table_id(course_service: CourseServices = Depends(get_course_service)):
    return await course_service.get_hash_table_id()
