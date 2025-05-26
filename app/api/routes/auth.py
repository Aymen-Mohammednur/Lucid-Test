from fastapi import APIRouter, Depends, status
from typing import Annotated

from app.schemas.user import UserCreate, UserLogin
from app.schemas.token import Token
from app.api.deps import get_auth_service
from app.services.auth import AuthService

router = APIRouter()

@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(
    payload: UserCreate,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    """Register a new user and immediately return a bearer token."""
    return auth_service.signup(payload)

@router.post("/login", response_model=Token)
async def login(
    payload: UserLogin,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    """Authenticate email + password and obtain a bearer token."""
    return auth_service.login(payload)
