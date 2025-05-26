from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserLogin
from app.schemas.token import Token
from app.core.security import create_access_token, verify_password
from app.models.user import User

class AuthService:
    """Business logic around registration, login, and token validation."""

    def __init__(self, session: Session):
        self.repo = UserRepository(session)

    def signup(self, payload: UserCreate) -> Token:
        """Create a new user and return an auth token."""
        if self.repo.get_by_email(payload.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
        user = self.repo.add(email=payload.email, password=payload.password)
        return Token(access_token=create_access_token(str(user.id)))

    def login(self, payload: UserLogin) -> Token:
        """Authenticate credentials and issue a fresh token."""
        user = self.repo.get_by_email(payload.email)
        if not user or not verify_password(payload.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
        return Token(access_token=create_access_token(str(user.id)))

    def validate_token(self, token: str) -> User:
        """Return the User that the token belongs to."""
        from app.core.security import decode_token
        payload = decode_token(token)
        user_id: int = int(payload["sub"])
        user = self.repo.get(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user
