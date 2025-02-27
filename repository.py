"""
Contains the business logic and database calls (using SQLAlchemy) for user and post operations.
Also implements in-memory caching for user posts.
"""
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy.orm import Session
import time

import models
import schemas


password_hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")


# In-memory cache: key = user_id, value = (timestamp, posts)
posts_cache = {}
CACHE_EXPIRY_SECONDS = 5 * 60  # 5 minutes


def get_user_by_email(db: Session, email: EmailStr) -> models.User | None:
    """Retrieve a user from the database by email."""
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> models.User | None:
    """Retrieve a user from the database by ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a new user."""
    hashed_password = password_hasher.hash(user.password)
    db_user = models.User(email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: EmailStr, password: str) -> models.User:
    """
    Authenticate a user by verifying the email and password.
    """

    user = get_user_by_email(db, email)

    if not user:
        return None

    if not password_hasher.verify(password, user.password):
        return None

    return user


def create_post(db: Session, user_id: int, text: str) -> models.Post:
    """Create a new post for the specified user."""
    db_post = models.Post(text=text, user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_posts_for_user(db: Session, user_id: int) -> list[models.Post]:
    """Retrieve all posts for a user, using in-memory caching to reduce DB calls."""
    current_time = time.time()

    # Check if the user's posts are in cache and not expired
    if user_id in posts_cache:
        cache_time, posts = posts_cache[user_id]
        if current_time - cache_time >= CACHE_EXPIRY_SECONDS:
            invalidate_cache(user_id)
        else:
            return posts

    # If not cached or expired, fetch from the database
    posts = db.query(models.Post).filter(models.Post.user_id == user_id).all()
    posts_cache[user_id] = (current_time, posts)
    return posts


def delete_post(db: Session, user_id: int, post_id: int) -> bool:
    """Delete a post if it belongs to the given user. Returns True if deleted, False otherwise."""
    post = (
        db
        .query(models.Post)
        .filter(models.Post.id == post_id, models.Post.user_id == user_id)
        .first()
    )

    if not post:
        return False

    db.delete(post)
    db.commit()

    return True


def invalidate_cache(user_id: int) -> None:
    """
    Invalidate the posts cache for a user.
    """
    if user_id in posts_cache:
        del posts_cache[user_id]
