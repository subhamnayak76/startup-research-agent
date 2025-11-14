from fastapi import APIRouter,HTTPException

from typing import List
from models.user import User
from schema.user import UserInput,UserResponse,Login,LoginResponse


router = APIRouter(prefix="/users",tags=["users"])

@router.post("/signup",response_model=UserResponse)
async def create_user(data:UserInput):
    existing_user = await User.find_one({
        "$or": [
            {
                "email": data.email
            },
            {
                "username": data.username
            }
        ]
    })

    if existing_user:
        raise HTTPException(status_code=400,detail="user with email or username is already exits")
    
    user = User(
        username = data.username,
        email=data.email,
        password_hash=User.hash_password(data.password)
    )

    await user.insert()

    return UserResponse(
        id = str(user.id),
        username = user.username,
        email = user.email

    )

@router.post("/signin",response_model=LoginResponse)
async def login_user(data:Login):
    user = await User.find_one({"email":data.email})
    if not user or not User.verfiy_password(data.password,user.password_hash):
        raise HTTPException(status_code=401,detail="invalid email or password")
    
    return LoginResponse(
        id = str(user.id),
        username = user.username,
        email =user.email,
        message="Login succesfull"
    )



@router.get("/{user_id}",response_model=UserResponse)
async def get_user(user_id:str):
    user = await User.get(user_id)
    
    if not user:
        HTTPException(status_code=404,detail="user not found")

    return UserResponse(
        id = str(user.id),
        username = user.username,
        email = user.email
    )   



