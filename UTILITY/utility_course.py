from typing import Optional, List, Dict
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends 

from id_manager import UniqueID
from ENUMS.object_type_str import ObjectToSTR
from DB.models import CourseModel
from id_manager import get_unique_id_instance
       
class CourseUtils:
    
    @staticmethod
    async def get_courses_by_filter(session: AsyncSession, class_id: Optional[int] = None, teacher_id: Optional[int] = None) -> List[CourseModel]:
        query = select(CourseModel)

        if class_id:
            query = query.where(CourseModel.class_id == class_id)
        if teacher_id:
            query = query.where(CourseModel.teacher_id == teacher_id)

        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def delete_courses_by_object_id(session: AsyncSession, object_id: int, object_type: str, unique_id: UniqueID = Depends(get_unique_id_instance)) -> Dict[str, str]:

        courses = await CourseUtils.get_courses_by_filter(
            session,
            class_id=object_id if object_type == 'classroom' else None,
            teacher_id=object_id if object_type == 'teacher' else None
        )

        if not courses:
            print("Successfully deleted")
            return {"detail": "Successfully deleted"}
          
        for course in courses:
            unique_id.delete(course.id, ObjectToSTR.COURSE.value)
            unique_id.save_to_file('unique_id_state.json')

        return {"detail": f"All courses associated with {object_type} id {object_id} have been deleted."}
