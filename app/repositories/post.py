from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.post import Post
from fastapi import HTTPException, status

class PostRepository:
    """Low‑level DB operations related to **Post** records."""

    def __init__(self, session: Session):
        self.session = session

    def add(self, author_id: int, text: str) -> Post:
        """Insert a new post belonging to a user(author_id)."""
        db_post = Post(text=text, author_id=author_id)
        self.session.add(db_post)
        self.session.commit()
        self.session.refresh(db_post)
        return db_post

    def get_by_author(self, author_id: int) -> List[Post]:
        """Return all posts for a user(author_id) sorted newest first."""
        stmt = select(Post).where(Post.author_id == author_id).order_by(Post.id.desc())
        return list(self.session.scalars(stmt))

    def delete(self, post_id: int, author_id: int) -> None:
         """Delete post only if it belongs to the user(author)"""
        post = self.session.get(Post, post_id)
        if not post or post.author_id != author_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        self.session.delete(post)
        self.session.commit()
