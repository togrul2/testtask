"""Routes for user authentication and post management."""
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

import models
import schemas
import repository
import auth
from database import get_db

router = APIRouter()


@router.post("/signup", response_model=schemas.Token, summary="User Signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Creates a new user using email and password.
    Returns a JWT token upon successful signup.
    """
    db_user = repository.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = repository.create_user(db, user)
    token = auth.create_access_token({"user_id": new_user.id})
    return schemas.Token(token=token)


@router.post("/login", response_model=schemas.Token, summary="User Login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Authenticates the user using email and password.
    Returns a JWT token upon successful login.
    """
    db_user = repository.authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = auth.create_access_token({"user_id": db_user.id})
    return schemas.Token(token=token)


@router.post("/addpost", response_model=schemas.PostResponse, summary="Add a Post")
async def add_post(
        post: schemas.PostCreate,
        current_user: models.User = Depends(auth.get_current_user),
        db: Session = Depends(get_db),
):
    """
    Accepts text (payload limited to 1MB) and a valid JWT token.
    Saves the post in the database and returns the postID.
    """
    # Validate payload size in bytes (limit: 1 MB)
    if len(post.text.encode("utf-8")) > 1 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Payload exceeds 1MB limit")
    created_post = repository.create_post(db, user_id=current_user.id, text=post.text)
    # Invalidate the cache for the user's posts
    repository.invalidate_cache(current_user.id)
    return schemas.PostResponse(postID=created_post.id, text=created_post.text)


@router.get("/getposts", response_model=list[schemas.PostResponse], summary="Get User Posts")
def get_posts(
        current_user: models.User = Depends(auth.get_current_user),
        db: Session = Depends(get_db),
):
    """
    Requires a valid JWT token.
    Returns all posts of the authenticated user.
    Implements in-memory caching (5 minutes) to reduce DB calls.
    """
    posts = repository.get_posts_for_user(db, current_user.id)
    return [schemas.PostResponse(postID=post.id, text=post.text) for post in posts]


@router.delete("/deletepost", summary="Delete a Post")
def delete_post(
        post_id: int,
        current_user: models.User = Depends(auth.get_current_user),
        db: Session = Depends(get_db),
):
    """
    Accepts a postID and a valid JWT token.
    Deletes the specified post if it belongs to the authenticated user.
    """
    deleted = repository.delete_post(db, user_id=current_user.id, post_id=post_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Post not found or not authorized")

    # Invalidate the cache for the user's posts
    repository.invalidate_cache(current_user.id)
