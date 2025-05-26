from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.auth import AuthService
from app.services.post import PostService
from app.models.user import User

oauth2_scheme = HTTPBearer()

def get_auth_service(db: Annotated[Session, Depends(get_db)]) -> AuthService:
    """Dependency function that provides an instance of AuthService using a database session."""
    return AuthService(db)

def get_post_service(db: Annotated[Session, Depends(get_db)]) -> PostService:
    """Dependency function that provides an instance of PostService using a database session."""
    return PostService(db)

def get_current_user(
    token: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> User:
    """Dependency function that validates the token and returns the current user."""
    return auth_service.validate_token(token.credentials)
