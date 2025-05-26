from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import hash_password

class UserRepository:
    """DB operations related to ser records."""

    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str) -> User | None:
        """Return a user with email or None if not found."""
        return self.session.scalar(select(User).where(User.email == email))

    def get(self, user_id: int) -> User | None:
        """Return a user by ID or None if not found."""
        return self.session.get(User, user_id)

    def add(self, email: str, password: str) -> User:
        """Add a new user with email and password."""
        db_user = User(email=email, hashed_password=hash_password(password))
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user
