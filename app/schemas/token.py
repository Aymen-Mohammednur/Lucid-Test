from pydantic import BaseModel, Field

class Token(BaseModel):
    """Represents a bearer access token."""
    access_token: str
    token_type: str = Field(default="bearer", pattern="^bearer$")
