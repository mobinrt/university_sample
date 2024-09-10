from fastapi import status, HTTPException

from ENUMS.object_type_str import ObjectToSTR

class CustomError:
    def existince_check(id:int, obj_to_str: ObjectToSTR, exist: bool):
        if exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"{obj_to_str.value} with id {id} already exist."
            )
        else:    
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail=f"{obj_to_str.value} with id {id} does not exist."
                )     