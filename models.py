"""
Defines the SQLAlchemy models for the application.
Includes the User and Post models with relationships.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)

    posts = relationship("Post", back_populates="owner")


class Post(Base):
    __tablename__ = "posts"
    __table_args__ = (
        CheckConstraint("LENGTH(text) <= 1048576", name="text_length_constraint"),
    )

    id = Column(Integer, primary_key=True, index=True)
    text = Column(MEDIUMTEXT, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="posts")
