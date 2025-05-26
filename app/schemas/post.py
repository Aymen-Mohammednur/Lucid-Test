from datetime import datetime

from pydantic import BaseModel, Field, PositiveInt, validator

_ONE_MB = 1_048_576  # bytes

class PostCreate(BaseModel):
    """Payload to create a post."""
    text: str = Field(..., max_length=_ONE_MB, description="Post body ≤ 1 MB")

    @validator("text")
    def ensure_byte_size(cls, v: str):
        """Validate UTF8 byte length does not exceed 1MB."""
        if len(v.encode("utf-8")) > _ONE_MB:
            raise ValueError("Post body exceeds 1 MB")
        return v

class PostOut(BaseModel):
    """Representation of a post."""
    id: PositiveInt
    text: str
    created_at: datetime

    class Config:
        from_attributes = True
