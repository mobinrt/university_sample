from fastapi import APIRouter, status, Depends
from typing import List

from SCHEMA.schemas import ClassCreate, ClassDisplay
from SERVICE.services_class import ClassroomServices
from DEPEND.depend_service import get_classroom_service

router = APIRouter(prefix='/classroom', tags=['classroom'])

@router.post("/create/", response_model=ClassDisplay, status_code=status.HTTP_201_CREATED)
async def create_classroom(classroom: ClassCreate, classroom_service: ClassroomServices = Depends(get_classroom_service)):
    return await classroom_service.create_object(classroom)

@router.get("/get/classroom/by/id/{classroom_id}", response_model=ClassDisplay, status_code=status.HTTP_200_OK)
async def get_classroom_by_id(stu_id:int, classroom_service: ClassroomServices = Depends(get_classroom_service)):
    return await classroom_service.get_object_by_id(stu_id)
    
@router.get("/get/all", response_model=List[ClassDisplay], status_code=status.HTTP_200_OK)
async def get_all_classrooms(classroom_service: ClassroomServices = Depends(get_classroom_service)):
    return await classroom_service.get_all_objects()
 
@router.put('/update/classroom/by/id/{classroom_id}', response_model=ClassDisplay, status_code=status.HTTP_200_OK)
async def update_classroom(classroom: ClassCreate, classroom_id, classroom_service: ClassroomServices = Depends(get_classroom_service)):
    old_classroom = await classroom_service.get_object_by_id(classroom_id)
    return await classroom_service.update_obj(classroom, old_classroom)
    
@router.delete('/delete/by/id/{classroom_id}', status_code=status.HTTP_200_OK)
async def delete_classroom_by_id(stu_id: int, classroom_service: ClassroomServices = Depends(get_classroom_service)):
    return await classroom_service.delete_by_id(stu_id)
