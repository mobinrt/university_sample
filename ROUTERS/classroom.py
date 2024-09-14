from fastapi import APIRouter, status, Depends
from typing import List

from SCHEMA.schemas import ClassCreate, ClassDisplay
from USECASE.manage_classroom import ClassroomUseCase
from DEPEND.depend_usecase import get_classroom_usecase

router = APIRouter(prefix='/classroom', tags=['classroom'])

@router.post("/create/", response_model=ClassDisplay, status_code=status.HTTP_201_CREATED)
async def create_classroom(classroom: ClassCreate, classroom_usecase: ClassroomUseCase = Depends(get_classroom_usecase)):
    return await classroom_usecase.create(classroom)

@router.get("/classroom/by/{classroom_id}", response_model=ClassDisplay, status_code=status.HTTP_200_OK)
async def get_classroom_by_id(classroom_id:int, classroom_usecase: ClassroomUseCase = Depends(get_classroom_usecase)):
    return await classroom_usecase.get_by_id(classroom_id)
    
@router.get("/all", response_model=List[ClassDisplay], status_code=status.HTTP_200_OK)
async def get_all_classrooms(classroom_usecase: ClassroomUseCase = Depends(get_classroom_usecase)):
    return await classroom_usecase.get_all()
 
@router.put('/update/classroom/by/{classroom_id}', response_model=ClassDisplay, status_code=status.HTTP_200_OK)
async def update_classroom(classroom: ClassCreate, classroom_id, classroom_usecase: ClassroomUseCase = Depends(get_classroom_usecase)):
    old_classroom = await classroom_usecase.get_by_id(classroom_id)
    return await classroom_usecase.update(classroom, old_classroom)
    
@router.delete('/by/{classroom_id}', status_code=status.HTTP_200_OK)
async def delete_classroom_by_id(stu_id: int, classroom_usecase: ClassroomUseCase = Depends(get_classroom_usecase)):
    return await classroom_usecase.delete_by_id(stu_id)
