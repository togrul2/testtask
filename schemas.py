"""
Defines the Pydantic models (schemas) for request and response validation.
Ensures extensive type validation for all endpoints.
"""

from pydantic import BaseModel, EmailStr, constr


class UserBase(BaseModel):
    """Base class for User schema."""
    email: EmailStr


class UserCreate(UserBase):
    """User creation schema used for registration."""
    password: constr(min_length=6)


class UserLogin(UserBase):
    """User login schema used for authentication."""
    password: str


class Token(BaseModel):
    """Token schema used for JWT token response."""
    token: str


class PostCreate(BaseModel):
    """Post schema used for creation."""
    # Validator to verify that text is not blank and does not exceed 1MB.
    text: constr(min_length=1, max_length=1024 * 1024)


class PostResponse(BaseModel):
    """Post schema used for response."""

    postID: int
    text: str

    class Config:
        from_attributes = True
