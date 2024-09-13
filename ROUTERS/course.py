from fastapi import APIRouter, status, Depends
from typing import List

from USECASE.manage_course import CourseUseCase
from SCHEMA.schemas import CourseCreate, CourseDisplay, CourseUpdate
from DEPEND.depend_usecase import get_course_usecase

router = APIRouter(prefix='/course', tags=['course'])

@router.post("/create/", response_model=CourseDisplay, status_code=status.HTTP_201_CREATED)
async def create_course(course: CourseCreate, course_usecase: CourseUseCase = Depends(get_course_usecase)):
    return await course_usecase.create(course)

@router.get("/course/by/id/{course_id}", response_model=CourseDisplay, status_code=status.HTTP_200_OK)
async def get_course_by_id(course_id:int, course_usecase: CourseUseCase = Depends(get_course_usecase)):
    return await course_usecase.get_by_id(course_id)
    
@router.get("/all", response_model=List[CourseDisplay], status_code=status.HTTP_200_OK)
async def get_all_courses(course_usecase: CourseUseCase = Depends(get_course_usecase)):
    return await course_usecase.get_all()
    
@router.delete('/by/{course_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_course_by_id(course_id: int, course_usecase: CourseUseCase = Depends(get_course_usecase)):
    await course_usecase.delete_by_id(course_id)
    
@router.put('/update/course/by/{course_id}', response_model=CourseDisplay, status_code=status.HTTP_200_OK)
async def update_course(course: CourseUpdate, course_id, course_usecase: CourseUseCase = Depends(get_course_usecase)):
    return await course_usecase.update(course, course_id)
    
@router.get('/get/hash_table/id', response_model=dict, status_code=status.HTTP_200_OK)
async def get_hash_table_id(course_usecase: CourseUseCase = Depends(get_course_usecase)):
    return await course_usecase.get_hash_table_id()
