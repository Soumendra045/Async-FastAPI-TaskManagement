from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column, Mapped
# pyrefly: ignore [missing-import]
from src.database.database import Base
from sqlalchemy import String, TIMESTAMP, ForeignKey, func, Text, Enum
from datetime import datetime
from typing import List

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False,index=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    create_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now())
    update_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now(), onupdate=func.now())
    role: Mapped[str] = mapped_column(Enum('user', 'admin'),default='user')

    projects: Mapped[List['Project']] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    
class Project(Base):
    __tablename__ = 'projects'
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False,index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Enum('pending', 'in_progress', 'completed'), nullable=False, default='pending')
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now(), onupdate=func.now())

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"),nullable=False)
    owner: Mapped["User"] = relationship(
        back_populates="projects",
        lazy="selectin"
    )

    comments: Mapped[List['Comment']] = relationship(
        back_populates="project",
        cascade="all, delete-orphan"
    )


class Comment(Base):
    __tablename__ = 'comments'
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now(), onupdate=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"),nullable=False)
    project: Mapped["Project"] = relationship(
        back_populates="comments",
        lazy="selectin"
    )