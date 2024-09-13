from SERVICE.services_teacher import TeacherServices
from DB.models import TeacherModel, StudentModel, CourseModel
from ENUMS.object_type_str import ObjectToSTR
from id_manager import UniqueID
from SCHEMA.schema_teacher import TeacherDisplay, TeacherCreate, TeacherUpdate
from USECASE.manage_object import ObjectUseCase
from ENUMS.object_type_digit import ObjectDigits
from UTILITY.custom_error import CustomError

from fastapi import HTTPException, status

class TeacherUseCase(ObjectUseCase[TeacherServices]):
    def __init__(self, teacher_service: TeacherServices, unique_id: UniqueID):
        super().__init__(teacher_service, unique_id, ObjectToSTR.TEACHER)
    
    async def create(self, new_teacher: TeacherCreate):
        if not new_teacher.name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username should not be blank!')
        
        teacher_id = self.unique_id.insert(ObjectDigits.TEACHER.value, ObjectToSTR.TEACHER.value)
        db_teacher = await self.service.create_object(new_teacher, teacher_id)
        self.unique_id.save_to_dict(db_teacher.name, db_teacher.id, ObjectToSTR.TEACHER.value)
        return db_teacher
    
    async def update(self, update_teacher: TeacherModel, login_teacher: TeacherModel):
        current_teacher = await self.service.update_obj(update_teacher, login_teacher)
        return TeacherDisplay.model_validate(current_teacher)
    
    async def fired_students_from_course(self, course_id: int, student_id: int, current_user: TeacherModel):
        course = await self.service.get_object_by_id_filter_model(course_id, CourseModel)
        if not course:
            raise CustomError.existince_check(course_id, ObjectToSTR.COURSE, False)
        
        if course.teacher_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to remove students from this course."
            )
        
        is_enrolled = await self.service.is_student_enrolled_in_course(course_id, student_id)
        if not is_enrolled:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student is not enrolled in this course."
            )
            
        await self.service.remove_student_from_course(course_id, student_id)

        return {"message": f"Student with ID {student_id} has been removed from course {course.name}."}
        

        
