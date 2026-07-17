# Creates a router to organize all user related API endpoints under the "/users" path.
# Accepts and validates user data using the UserReq model.
# Injects the application configuration using FastAPI's dependency injection (Depends).
# Returns a formatted response using the UserResponse model.

from fastapi import APIRouter,Depends
from config import appconfig,get_appconf
from models import UserReq,UserResponse

router=APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def create_user(user: UserReq,config: appconfig= Depends(get_appconf),):
    return UserResponse(message=f"{user.name} is added to {config.name} ")
