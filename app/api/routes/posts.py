from fastapi import APIRouter, Depends, Response, status
from typing import Annotated

from app.schemas.post import PostCreate, PostOut
from app.api.deps import get_post_service, get_current_user
from app.services.post import PostService
from app.models.user import User

router = APIRouter()

@router.post("/posts", response_model=PostOut, status_code=status.HTTP_201_CREATED)
async def add_post(
    payload: PostCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    post_service: Annotated[PostService, Depends(get_post_service)],
):
    """Add a post (max 1MB) on behalf of the authenticated user."""
    return post_service.add_post(current_user, payload)

@router.get("/posts", response_model=list[PostOut])
async def get_posts(
    current_user: Annotated[User, Depends(get_current_user)],
    post_service: Annotated[PostService, Depends(get_post_service)],
):
    """Return all posts for the authenticated user."""
    return post_service.get_posts(current_user)

@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    post_service: Annotated[PostService, Depends(get_post_service)],
):
    """Delete a post by ID on behalf of the authenticated user."""
    post_service.delete_post(current_user, post_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
