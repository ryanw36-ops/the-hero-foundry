#!/usr/bin/env python3
"""
Base SQLAlchemy model for The Hero Foundry backend server.

Provides common fields, utilities, and base functionality for all database models.
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from sqlalchemy import Column, String, DateTime, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

Base = declarative_base()


class TimestampMixin:
    """Mixin to add timestamp fields to models."""
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )


class UUIDMixin:
    """Mixin to add UUID primary key to models."""
    
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False
    )


class BaseModel(Base, UUIDMixin, TimestampMixin):
    """Base model with common fields and functionality."""
    
    __abstract__ = True
    
    # Metadata fields
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Status and versioning
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    version: Mapped[str] = mapped_column(String(50), default="1.0.0", nullable=False)
    
    # Metadata and tags
    tags: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    # Audit fields
    created_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    updated_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    def __repr__(self) -> str:
        """String representation of the model."""
        return f"<{self.__class__.__name__}(id={self.id}, name='{self.name}')>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary representation."""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                result[column.name] = value.isoformat()
            else:
                result[column.name] = value
        return result
    
    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """Update model attributes from dictionary."""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)
        self.updated_at = datetime.now(timezone.utc)
    
    @classmethod
    def get_table_name(cls) -> str:
        """Get the table name for this model."""
        return cls.__tablename__
    
    @classmethod
    def get_columns(cls) -> list:
        """Get list of column names for this model."""
        return [column.name for column in cls.__table__.columns]


class SoftDeleteMixin:
    """Mixin to add soft delete functionality to models."""
    
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    deleted_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    def soft_delete(self, deleted_by: Optional[str] = None) -> None:
        """Mark the record as deleted without removing it from the database."""
        self.is_deleted = True
        self.deleted_at = datetime.now(timezone.utc)
        self.deleted_by = deleted_by
        self.updated_at = datetime.now(timezone.utc)
    
    def restore(self, restored_by: Optional[str] = None) -> None:
        """Restore a soft-deleted record."""
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        self.updated_at = datetime.now(timezone.utc)


class VersionedMixin:
    """Mixin to add versioning functionality to models."""
    
    major_version: Mapped[int] = mapped_column(default=1, nullable=False)
    minor_version: Mapped[int] = mapped_column(default=0, nullable=False)
    patch_version: Mapped[int] = mapped_column(default=0, nullable=False)
    
    @property
    def version_string(self) -> str:
        """Get the version as a string."""
        return f"{self.major_version}.{self.minor_version}.{self.patch_version}"
    
    def increment_version(self, version_type: str = "patch") -> None:
        """Increment the version number."""
        if version_type == "major":
            self.major_version += 1
            self.minor_version = 0
            self.patch_version = 0
        elif version_type == "minor":
            self.minor_version += 1
            self.patch_version = 0
        else:  # patch
            self.patch_version += 1
        
        self.updated_at = datetime.now(timezone.utc)


# Utility functions for models
def generate_uuid() -> str:
    """Generate a new UUID string."""
    return str(uuid.uuid4())


def get_current_timestamp() -> datetime:
    """Get current timestamp in UTC."""
    return datetime.now(timezone.utc)


def format_timestamp(timestamp: datetime) -> str:
    """Format timestamp as ISO string."""
    return timestamp.isoformat()


def parse_timestamp(timestamp_str: str) -> datetime:
    """Parse ISO timestamp string to datetime."""
    return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
