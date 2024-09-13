from fastapi import APIRouter, status, Depends
from typing import List

from USECASE.manage_student import StudentUseCase
from SCHEMA.schema_student import StudentCreate, StudentDisplay, StudentUpdate
from DEPEND.depend_service import get_auth_service
from DEPEND.depend_usecase import get_student_usecase
from AUTH.athentication import oauth2_sc
from AUTH.auth_services import AuthServices

router = APIRouter(prefix='/student', tags=['student'])


@router.post("/create/", response_model=StudentDisplay, status_code=status.HTTP_201_CREATED)
async def create_student(student: StudentCreate, student_usecase: StudentUseCase = Depends(get_student_usecase)):
    return await student_usecase.create(student)

@router.get("/student/{student_id}", response_model=StudentDisplay, status_code=status.HTTP_200_OK)
async def get_student_by_id(stu_id:int, student_usecase: StudentUseCase = Depends(get_student_usecase)):
    return await student_usecase.get_by_id(stu_id)
    
@router.get("/all", response_model=List[StudentDisplay], status_code=status.HTTP_200_OK)
async def get_all_students(student_usecase: StudentUseCase = Depends(get_student_usecase)):
    return await student_usecase.get_all()

@router.put('/update/current_student', response_model=StudentDisplay, status_code=status.HTTP_200_OK)
async def update_student(
    student: StudentUpdate,
    token: str = Depends(oauth2_sc),
    auth_service: AuthServices = Depends(get_auth_service),
    student_usecase: StudentUseCase = Depends(get_student_usecase)
    ):
    current_user = await auth_service.get_current_user(token)
    return await student_usecase.update(student, current_user)

@router.delete('/delete/{student_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_student_by_id(stu_id: int, student_usecase: StudentUseCase = Depends(get_student_usecase)):
    await student_usecase.delete_by_id(stu_id)

@router.get('/get/hash_table/id', response_model=dict, status_code=status.HTTP_200_OK)
async def get_hash_table_id(student_usecase: StudentUseCase = Depends(get_student_usecase)):
    return await student_usecase.get_hash_table_id()

@router.post("/courses/enroll/{course_id}", status_code=status.HTTP_200_OK)
async def enroll_student(
    course_id: int, 
    token: str = Depends(oauth2_sc),
    auth_service: AuthServices = Depends(get_auth_service),
    student_usecase: StudentUseCase = Depends(get_student_usecase)
):
    current_user = await auth_service.get_current_user(token)
    return await student_usecase.attend_in_course(course_id, current_user)
    