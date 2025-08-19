#!/usr/bin/env python3
"""
Ruleset management endpoints for The Hero Foundry backend server.

Provides CRUD operations for the modular ruleset system, including validation and compatibility checking.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from ...core.database import get_db_session_dependency
from ...models.ruleset import Ruleset, RulesetType, RulesetStatus
from ...core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/", response_model=List[Dict[str, Any]])
async def list_rulesets(
    skip: int = Query(0, ge=0, description="Number of rulesets to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of rulesets to return"),
    ruleset_type: Optional[RulesetType] = Query(None, description="Filter by ruleset type"),
    status: Optional[RulesetStatus] = Query(None, description="Filter by status"),
    category: Optional[str] = Query(None, description="Filter by category"),
    db: AsyncSession = Depends(get_db_session_dependency)
) -> List[Dict[str, Any]]:
    """List all rulesets with optional filtering."""
    
    try:
        # Build query
        query = select(Ruleset).where(Ruleset.is_deleted == False)
        
        # Apply filters
        if ruleset_type:
            query = query.where(Ruleset.ruleset_type == ruleset_type)
        
        if status:
            query = query.where(Ruleset.status == status)
        
        if category:
            query = query.where(Ruleset.category == category)
        
        # Apply pagination
        query = query.offset(skip).limit(limit)
        
        # Execute query
        result = await db.execute(query)
        rulesets = result.scalars().all()
        
        # Convert to dictionaries
        ruleset_list = []
        for ruleset in rulesets:
            ruleset_dict = ruleset.to_dict()
            ruleset_dict["compatibility_info"] = ruleset.get_compatibility_info()
            ruleset_list.append(ruleset_dict)
        
        logger.info(f"Retrieved {len(ruleset_list)} rulesets")
        return ruleset_list
        
    except Exception as e:
        logger.error(f"Error retrieving rulesets: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve rulesets")


@router.get("/{ruleset_id}", response_model=Dict[str, Any])
async def get_ruleset(
    ruleset_id: str = Path(..., description="Ruleset ID"),
    db: AsyncSession = Depends(get_db_session_dependency)
) -> Dict[str, Any]:
    """Get a specific ruleset by ID."""
    
    try:
        # Query ruleset with relationships
        query = select(Ruleset).where(
            Ruleset.id == ruleset_id,
            Ruleset.is_deleted == False
        ).options(
            selectinload(Ruleset.dependencies),
            selectinload(Ruleset.characters),
            selectinload(Ruleset.races),
            selectinload(Ruleset.classes),
            selectinload(Ruleset.spells),
            selectinload(Ruleset.features),
            selectinload(Ruleset.items)
        )
        
        result = await db.execute(query)
        ruleset = result.scalar_one_or_none()
        
        if not ruleset:
            raise HTTPException(status_code=404, detail="Ruleset not found")
        
        # Convert to dictionary with relationships
        ruleset_dict = ruleset.to_dict()
        ruleset_dict["compatibility_info"] = ruleset.get_compatibility_info()
        ruleset_dict["dependencies"] = [dep.to_dict() for dep in ruleset.dependencies]
        ruleset_dict["content_counts"] = {
            "characters": len(ruleset.characters),
            "races": len(ruleset.races),
            "classes": len(ruleset.classes),
            "spells": len(ruleset.spells),
            "features": len(ruleset.features),
            "items": len(ruleset.items)
        }
        
        logger.info(f"Retrieved ruleset: {ruleset.name}")
        return ruleset_dict
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving ruleset {ruleset_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve ruleset")


@router.post("/", response_model=Dict[str, Any])
async def create_ruleset(
    ruleset_data: Dict[str, Any],
    db: AsyncSession = Depends(get_db_session_dependency)
) -> Dict[str, Any]:
    """Create a new ruleset."""
    
    try:
        # Validate required fields
        required_fields = ["name", "ruleset_type", "content_path"]
        for field in required_fields:
            if field not in ruleset_data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        # Validate ruleset type
        try:
            ruleset_type = RulesetType(ruleset_data["ruleset_type"])
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid ruleset type: {ruleset_data['ruleset_type']}")
        
        # Create ruleset instance
        ruleset = Ruleset(**ruleset_data)
        
        # Validate ruleset
        if not ruleset.is_valid():
            validation_errors = ruleset.get_validation_errors()
            raise HTTPException(
                status_code=400,
                detail=f"Ruleset validation failed: {', '.join(validation_errors)}"
            )
        
        # Add to database
        db.add(ruleset)
        await db.commit()
        await db.refresh(ruleset)
        
        logger.info(f"Created ruleset: {ruleset.name}")
        return ruleset.to_dict()
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating ruleset: {e}")
        raise HTTPException(status_code=500, detail="Failed to create ruleset")


@router.put("/{ruleset_id}", response_model=Dict[str, Any])
async def update_ruleset(
    ruleset_id: str = Path(..., description="Ruleset ID"),
    ruleset_data: Dict[str, Any] = None,
    db: AsyncSession = Depends(get_db_session_dependency)
) -> Dict[str, Any]:
    """Update an existing ruleset."""
    
    try:
        # Get existing ruleset
        query = select(Ruleset).where(
            Ruleset.id == ruleset_id,
            Ruleset.is_deleted == False
        )
        result = await db.execute(query)
        ruleset = result.scalar_one_or_none()
        
        if not ruleset:
            raise HTTPException(status_code=404, detail="Ruleset not found")
        
        # Update ruleset data
        if ruleset_data:
            # Remove fields that shouldn't be updated
            protected_fields = ["id", "created_at", "created_by"]
            for field in protected_fields:
                ruleset_data.pop(field, None)
            
            # Update ruleset attributes
            ruleset.update_from_dict(ruleset_data)
            
            # Validate updated ruleset
            if not ruleset.is_valid():
                validation_errors = ruleset.get_validation_errors()
                raise HTTPException(
                    status_code=400,
                    detail=f"Ruleset validation failed: {', '.join(validation_errors)}"
                )
        
        # Save changes
        await db.commit()
        await db.refresh(ruleset)
        
        logger.info(f"Updated ruleset: {ruleset.name}")
        return ruleset.to_dict()
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating ruleset {ruleset_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update ruleset")


@router.delete("/{ruleset_id}")
async def delete_ruleset(
    ruleset_id: str = Path(..., description="Ruleset ID"),
    permanent: bool = Query(False, description="Permanently delete ruleset"),
    db: AsyncSession = Depends(get_db_session_dependency)
) -> Dict[str, str]:
    """Delete a ruleset (soft delete by default)."""
    
    try:
        # Get existing ruleset
        query = select(Ruleset).where(
            Ruleset.id == ruleset_id,
            Ruleset.is_deleted == False
        )
        result = await db.execute(query)
        ruleset = result.scalar_one_or_none()
        
        if not ruleset:
            raise HTTPException(status_code=404, detail="Ruleset not found")
        
        # Check if ruleset is in use
        if ruleset.characters or ruleset.races or ruleset.classes:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete ruleset that is in use by characters or content"
            )
        
        if permanent:
            # Permanent deletion
            await db.delete(ruleset)
            message = f"Ruleset {ruleset.name} permanently deleted"
        else:
            # Soft deletion
            ruleset.soft_delete()
            message = f"Ruleset {ruleset.name} soft deleted"
        
        await db.commit()
        
        logger.info(message)
        return {"message": message}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting ruleset {ruleset_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete ruleset")


@router.post("/{ruleset_id}/activate")
async def activate_ruleset(
    ruleset_id: str = Path(..., description="Ruleset ID"),
    db: AsyncSession = Depends(get_db_session_dependency)
) -> Dict[str, Any]:
    """Activate a ruleset."""
    
    try:
        # Get existing ruleset
        query = select(Ruleset).where(
            Ruleset.id == ruleset_id,
            Ruleset.is_deleted == False
        )
        result = await db.execute(query)
        ruleset = result.scalar_one_or_none()
        
        if not ruleset:
            raise HTTPException(status_code=404, detail="Ruleset not found")
        
        # Check if ruleset can be activated
        if not ruleset.can_be_activated():
            raise HTTPException(
                status_code=400,
                detail="Ruleset cannot be activated. Check dependencies and validation."
            )
        
        # Activate ruleset
        success = ruleset.activate()
        if not success:
            raise HTTPException(
                status_code=400,
                detail="Failed to activate ruleset"
            )
        
        # Save changes
        await db.commit()
        await db.refresh(ruleset)
        
        logger.info(f"Activated ruleset: {ruleset.name}")
        return {
            "message": f"Ruleset {ruleset.name} activated successfully",
            "ruleset": ruleset.to_dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error activating ruleset {ruleset_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to activate ruleset")


@router.post("/{ruleset_id}/deactivate")
async def deactivate_ruleset(
    ruleset_id: str = Path(..., description="Ruleset ID"),
    db: AsyncSession = Depends(get_db_session_dependency)
) -> Dict[str, Any]:
    """Deactivate a ruleset."""
    
    try:
        # Get existing ruleset
        query = select(Ruleset).where(
            Ruleset.id == ruleset_id,
            Ruleset.is_deleted == False
        )
        result = await db.execute(query)
        ruleset = result.scalar_one_or_none()
        
        if not ruleset:
            raise HTTPException(status_code=404, detail="Ruleset not found")
        
        # Deactivate ruleset
        ruleset.deactivate()
        
        # Save changes
        await db.commit()
        await db.refresh(ruleset)
        
        logger.info(f"Deactivated ruleset: {ruleset.name}")
        return {
            "message": f"Ruleset {ruleset.name} deactivated successfully",
            "ruleset": ruleset.to_dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deactivating ruleset {ruleset_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to deactivate ruleset")


@router.get("/{ruleset_id}/validation")
async def validate_ruleset(
    ruleset_id: str = Path(..., description="Ruleset ID"),
    db: AsyncSession = Depends(get_db_session_dependency)
) -> Dict[str, Any]:
    """Validate a ruleset against its rules and dependencies."""
    
    try:
        # Get existing ruleset
        query = select(Ruleset).where(
            Ruleset.id == ruleset_id,
            Ruleset.is_deleted == False
        ).options(selectinload(Ruleset.dependencies))
        
        result = await db.execute(query)
        ruleset = result.scalar_one_or_none()
        
        if not ruleset:
            raise HTTPException(status_code=404, detail="Ruleset not found")
        
        # Perform validation
        validation_errors = ruleset.get_validation_errors()
        is_valid = len(validation_errors) == 0
        
        # Check compatibility with other active rulesets
        compatibility_issues = []
        active_rulesets_query = select(Ruleset).where(
            Ruleset.status == RulesetStatus.ACTIVE,
            Ruleset.is_deleted == False,
            Ruleset.id != ruleset_id
        )
        active_result = await db.execute(active_rulesets_query)
        active_rulesets = active_result.scalars().all()
        
        for active_ruleset in active_rulesets:
            if not ruleset.is_compatible_with(active_ruleset):
                compatibility_issues.append(f"Conflicts with active ruleset: {active_ruleset.name}")
        
        return {
            "ruleset_id": ruleset_id,
            "ruleset_name": ruleset.name,
            "is_valid": is_valid,
            "validation_errors": validation_errors,
            "compatibility_issues": compatibility_issues,
            "can_be_activated": ruleset.can_be_activated(),
            "validation_timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error validating ruleset {ruleset_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to validate ruleset")


@router.get("/{ruleset_id}/compatibility")
async def check_ruleset_compatibility(
    ruleset_id: str = Path(..., description="Ruleset ID"),
    target_ruleset_id: str = Query(..., description="Target ruleset ID to check compatibility with"),
    db: AsyncSession = Depends(get_db_session_dependency)
) -> Dict[str, Any]:
    """Check compatibility between two rulesets."""
    
    try:
        # Get both rulesets
        query = select(Ruleset).where(
            Ruleset.id.in_([ruleset_id, target_ruleset_id]),
            Ruleset.is_deleted == False
        )
        result = await db.execute(query)
        rulesets = result.scalars().all()
        
        if len(rulesets) != 2:
            raise HTTPException(status_code=404, detail="One or both rulesets not found")
        
        source_ruleset = next(r for r in rulesets if r.id == ruleset_id)
        target_ruleset = next(r for r in rulesets if r.id == target_ruleset_id)
        
        # Check compatibility
        is_compatible = source_ruleset.is_compatible_with(target_ruleset)
        
        return {
            "source_ruleset": {
                "id": source_ruleset.id,
                "name": source_ruleset.name,
                "type": source_ruleset.ruleset_type.value if isinstance(source_ruleset.ruleset_type, RulesetType) else source_ruleset.ruleset_type
            },
            "target_ruleset": {
                "id": target_ruleset.id,
                "name": target_ruleset.name,
                "type": target_ruleset.ruleset_type.value if isinstance(target_ruleset.ruleset_type, RulesetType) else target_ruleset.ruleset_type
            },
            "is_compatible": is_compatible,
            "compatibility_details": {
                "edition_match": source_ruleset.ruleset_type == target_ruleset.ruleset_type,
                "version_compatible": source_ruleset._versions_are_compatible(
                    source_ruleset.compatibility_version or "1.0",
                    target_ruleset.compatibility_version or "1.0"
                ) if source_ruleset.compatibility_version and target_ruleset.compatibility_version else True
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error checking compatibility between rulesets {ruleset_id} and {target_ruleset_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to check ruleset compatibility")
