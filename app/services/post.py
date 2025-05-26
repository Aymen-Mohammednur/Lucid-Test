from typing import List

from cachetools import TTLCache
from sqlalchemy.orm import Session

from app.repositories.post import PostRepository
from app.models.user import User
from app.schemas.post import PostCreate, PostOut

class PostService:
    """Business logic related to Post creation, retrieval and deletion."""

    # 5‑minute (300s) per‑user cache for GetPosts
    _post_cache: TTLCache[int, List[PostOut]] = TTLCache(maxsize=1024, ttl=300)

    def __init__(self, session: Session):
        self.repo = PostRepository(session)

    def add_post(self, user: User, payload: PostCreate) -> PostOut:
        """Create a post, invalidate the users cached timeline, return it."""
        post = self.repo.add(author_id=user.id, text=payload.text)
        self._post_cache.pop(user.id, None)  # invalidate
        return PostOut.model_validate(post)

    def get_posts(self, user: User) -> List[PostOut]:
         """Return cached posts or fetch from DB and cache them."""
        if user.id in self._post_cache:
            return self._post_cache[user.id]
        posts = self.repo.get_by_author(author_id=user.id)
        serialized = [PostOut.model_validate(p) for p in posts]
        self._post_cache[user.id] = serialized
        return serialized

    def delete_post(self, user: User, post_id: int) -> None:
        self.repo.delete(post_id=post_id, author_id=user.id)
        """Delete a post and invalidate cache."""
        self._post_cache.pop(user.id, None)
