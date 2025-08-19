#!/usr/bin/env python3
"""
Ruleset model for The Hero Foundry backend server.

Defines the modular ruleset system that supports different D&D editions and homebrew content.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from enum import Enum

from sqlalchemy import String, Integer, Text, Boolean, JSON, ForeignKey, Table, Column, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from .base import BaseModel, SoftDeleteMixin, VersionedMixin


class RulesetType(str, Enum):
    """Types of rulesets supported by the system."""
    DND_5E = "dnd_5e"
    DND_2024 = "dnd_2024"
    DND_3_5 = "dnd_3_5"
    PATHFINDER_1E = "pathfinder_1e"
    PATHFINDER_2E = "pathfinder_2e"
    HOMEBREW = "homebrew"
    CUSTOM = "custom"


class RulesetStatus(str, Enum):
    """Status of a ruleset."""
    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


# Association table for ruleset dependencies
ruleset_dependencies = Table(
    'ruleset_dependencies',
    BaseModel.metadata,
    Column('ruleset_id', UUID(as_uuid=False), ForeignKey('rulesets.id'), primary_key=True),
    Column('dependency_id', UUID(as_uuid=False), ForeignKey('rulesets.id'), primary_key=True),
    Column('dependency_type', String(50)),  # required, optional, conflicts
    Column('version_constraint', String(100))  # semver constraint
)


class Ruleset(BaseModel, SoftDeleteMixin, VersionedMixin):
    """Ruleset model representing a complete set of game rules."""
    
    __tablename__ = "rulesets"
    
    # Basic ruleset information
    ruleset_type: Mapped[RulesetType] = mapped_column(String(50), nullable=False, index=True)
    status: Mapped[RulesetStatus] = mapped_column(String(50), default=RulesetStatus.DRAFT, nullable=False)
    
    # Version and compatibility
    edition: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # e.g., "5th Edition", "2024 Core"
    compatibility_version: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # e.g., "5.1", "5.2"
    
    # Content and structure
    content_path: Mapped[str] = mapped_column(String(500), nullable=False)  # Path to ruleset content files
    schema_version: Mapped[str] = mapped_column(String(50), default="1.0.0", nullable=False)
    
    # Ruleset features and capabilities
    features: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)  # List of feature names
    supported_content_types: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)  # races, classes, spells, etc.
    
    # Validation and rules
    validation_rules: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    balance_guidelines: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    # Licensing and attribution
    license: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    license_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    attribution: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    copyright_holder: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Metadata and organization
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # core, expansion, homebrew, etc.
    tags: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    
    # Content statistics
    content_count: Mapped[Optional[Dict[str, int]]] = mapped_column(JSON, nullable=True)  # Count of each content type
    last_content_update: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Dependencies and conflicts
    dependencies = relationship(
        "Ruleset",
        secondary=ruleset_dependencies,
        primaryjoin="Ruleset.id==ruleset_dependencies.c.ruleset_id",
        secondaryjoin="Ruleset.id==ruleset_dependencies.c.dependency_id",
        backref="dependent_rulesets"
    )
    
    # Content relationships
    characters = relationship("Character", back_populates="ruleset")
    races = relationship("Race", back_populates="ruleset")
    classes = relationship("CharacterClass", back_populates="ruleset")
    spells = relationship("Spell", back_populates="ruleset")
    features = relationship("Feature", back_populates="ruleset")
    items = relationship("Item", back_populates="ruleset")
    
    def __post_init__(self):
        """Initialize ruleset after creation."""
        if not self.content_count:
            self.content_count = {}
        if not self.supported_content_types:
            self.supported_content_types = []
        if not self.features:
            self.features = []
    
    def is_compatible_with(self, other_ruleset: 'Ruleset') -> bool:
        """Check if this ruleset is compatible with another ruleset."""
        # Check for direct conflicts
        if other_ruleset in self._get_conflicting_rulesets():
            return False
        
        # Check edition compatibility
        if self.ruleset_type != other_ruleset.ruleset_type:
            return False
        
        # Check version compatibility
        if self.compatibility_version and other_ruleset.compatibility_version:
            if not self._versions_are_compatible(self.compatibility_version, other_ruleset.compatibility_version):
                return False
        
        return True
    
    def _get_conflicting_rulesets(self) -> List['Ruleset']:
        """Get list of rulesets that conflict with this one."""
        conflicts = []
        for dep in self.dependencies:
            if hasattr(dep, 'dependency_type') and dep.dependency_type == 'conflicts':
                conflicts.append(dep)
        return conflicts
    
    def _versions_are_compatible(self, version1: str, version2: str) -> bool:
        """Check if two version strings are compatible."""
        # Simple version compatibility check
        # This could be enhanced with proper semver parsing
        try:
            v1_parts = [int(x) for x in version1.split('.')]
            v2_parts = [int(x) for x in version2.split('.')]
            
            # Major version must match for compatibility
            return v1_parts[0] == v2_parts[0]
        except (ValueError, IndexError):
            return False
    
    def add_content(self, content_type: str, count: int = 1) -> None:
        """Add content count for a specific type."""
        if not self.content_count:
            self.content_count = {}
        
        current_count = self.content_count.get(content_type, 0)
        self.content_count[content_type] = current_count + count
        self.last_content_update = datetime.now(timezone.utc)
    
    def remove_content(self, content_type: str, count: int = 1) -> None:
        """Remove content count for a specific type."""
        if not self.content_count:
            return
        
        current_count = self.content_count.get(content_type, 0)
        new_count = max(0, current_count - count)
        self.content_count[content_type] = new_count
        self.last_content_update = datetime.now(timezone.utc)
    
    def get_content_count(self, content_type: str) -> int:
        """Get the count of a specific content type."""
        if not self.content_count:
            return 0
        return self.content_count.get(content_type, 0)
    
    def get_total_content_count(self) -> int:
        """Get the total count of all content."""
        if not self.content_count:
            return 0
        return sum(self.content_count.values())
    
    def supports_content_type(self, content_type: str) -> bool:
        """Check if this ruleset supports a specific content type."""
        if not self.supported_content_types:
            return False
        return content_type.lower() in [ct.lower() for ct in self.supported_content_types]
    
    def add_feature(self, feature: str) -> None:
        """Add a feature to the ruleset."""
        if not self.features:
            self.features = []
        if feature not in self.features:
            self.features.append(feature)
    
    def remove_feature(self, feature: str) -> None:
        """Remove a feature from the ruleset."""
        if self.features and feature in self.features:
            self.features.remove(feature)
    
    def has_feature(self, feature: str) -> bool:
        """Check if the ruleset has a specific feature."""
        if not self.features:
            return False
        return feature.lower() in [f.lower() for f in self.features]
    
    def is_active(self) -> bool:
        """Check if the ruleset is currently active."""
        return self.status == RulesetStatus.ACTIVE
    
    def can_be_activated(self) -> bool:
        """Check if the ruleset can be activated."""
        if self.status == RulesetStatus.DEPRECATED or self.status == RulesetStatus.ARCHIVED:
            return False
        
        # Check if all required dependencies are available
        required_deps = [dep for dep in self.dependencies if hasattr(dep, 'dependency_type') and dep.dependency_type == 'required']
        for dep in required_deps:
            if not dep.is_active():
                return False
        
        return True
    
    def activate(self) -> bool:
        """Activate the ruleset if possible."""
        if not self.can_be_activated():
            return False
        
        self.status = RulesetStatus.ACTIVE
        self.updated_at = datetime.now(timezone.utc)
        return True
    
    def deactivate(self) -> None:
        """Deactivate the ruleset."""
        self.status = RulesetStatus.DRAFT
        self.updated_at = datetime.now(timezone.utc)
    
    def deprecate(self) -> None:
        """Mark the ruleset as deprecated."""
        self.status = RulesetStatus.DEPRECATED
        self.updated_at = datetime.now(timezone.utc)
    
    def archive(self) -> None:
        """Archive the ruleset."""
        self.status = RulesetStatus.ARCHIVED
        self.updated_at = datetime.now(timezone.utc)
    
    def get_validation_errors(self) -> List[str]:
        """Get validation errors for the ruleset."""
        errors = []
        
        # Check required fields
        if not self.content_path:
            errors.append("Content path is required")
        
        if not self.ruleset_type:
            errors.append("Ruleset type is required")
        
        # Check content path exists
        import os
        if not os.path.exists(self.content_path):
            errors.append(f"Content path does not exist: {self.content_path}")
        
        # Check dependencies
        for dep in self.dependencies:
            if hasattr(dep, 'dependency_type') and dep.dependency_type == 'required':
                if not dep.is_active():
                    errors.append(f"Required dependency is not active: {dep.name}")
        
        return errors
    
    def is_valid(self) -> bool:
        """Check if the ruleset is valid."""
        return len(self.get_validation_errors()) == 0
    
    def get_compatibility_info(self) -> Dict[str, Any]:
        """Get compatibility information for the ruleset."""
        return {
            "ruleset_type": self.ruleset_type.value if isinstance(self.ruleset_type, RulesetType) else self.ruleset_type,
            "edition": self.edition,
            "compatibility_version": self.compatibility_version,
            "schema_version": self.schema_version,
            "status": self.status.value if isinstance(self.status, RulesetStatus) else self.status,
            "is_active": self.is_active(),
            "can_be_activated": self.can_be_activated(),
            "is_valid": self.is_valid(),
            "validation_errors": self.get_validation_errors(),
            "content_count": self.get_total_content_count(),
            "supported_content_types": self.supported_content_types or [],
            "features": self.features or [],
            "dependencies": [dep.name for dep in self.dependencies],
            "license": self.license,
            "attribution": self.attribution
        }
