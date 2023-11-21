from pydantic import BaseModel, Field, EmailStr, root_validator
from sqlalchemy import String, Boolean
from typing import Optional

class UserSchema(BaseModel):
    username: Optional[str] = None
    email: EmailStr
    password: str = Field(...,min_length=4)
    is_active: bool | None = True
    is_superuser: bool | None = False

    
    @root_validator(pre=True,skip_on_failure=True)
    def create_username(cls,values):
        username = values.get("username")
        email= values.get("email")
        
        if not username and email:
            values["username"] = email.split("@")[0]

        return values
        