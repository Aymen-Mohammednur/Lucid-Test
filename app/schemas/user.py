from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, PositiveInt

class _UserBase(BaseModel):
    email: EmailStr

class UserCreate(_UserBase):
    """Payload used to register a new user."""
    password: str = Field(min_length=8, max_length=128)

class UserLogin(UserCreate):
    """Login uses the same fields as signup."""
    pass

class UserOut(_UserBase):
    """Representation of a user."""
    id: PositiveInt
    created_at: datetime

    class Config:
        from_attributes = True
