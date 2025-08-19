#!/usr/bin/env python3
"""
Character management endpoints for The Hero Foundry backend server.

Provides CRUD operations for D&D characters, including creation, updates, validation, and progression tracking.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from ...core.database import get_db_session_dependency
from ...models.character import Character
from ...models.ruleset import Ruleset
from ...core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/", response_model=List[Dict[str, Any]])
async def list_characters(
    skip: int = Query(0, ge=0, description="Number of characters to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of characters to return"),
    ruleset_id: Optional[str] = Query(None, description="Filter by ruleset ID"),
    level_min: Optional[int] = Query(None, ge=1, description="Minimum character level"),
    level_max: Optional[int] = Query(None, ge=1, description="Maximum character level"),
    db: AsyncSession = Depends(get_db_session_dependency)
) -> List[Dict[str, Any]]:
    """List all characters with optional filtering."""
    
    try:
        # Build query
        query = select(Character).where(Character.is_deleted == False)
        
        # Apply filters
        if ruleset_id:
            query = query.where(Character.ruleset_id == ruleset_id)
        
        if level_min is not None:
            query = query.where(Character.level >= level_min)
        
        if level_max is not None:
            query = query.where(Character.level <= level_max)
        
        # Apply pagination
        query = query.offset(skip).limit(limit)
        
        # Execute query
        result = await db.execute(query)
        characters = result.scalars().all()
        
        # Convert to dictionaries
        character_list = []
        for char in characters:
            char_dict = char.to_dict()
            char_dict["ruleset_name"] = char.ruleset.name if char.ruleset else None
            character_list.append(char_dict)
        
        logger.info(f"Retrieved {len(character_list)} characters")
        return character_list
        
    except Exception as e:
        logger.error(f"Error retrieving characters: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve characters")


@router.get("/{character_id}", response_model=Dict[str, Any])
async def get_character(
    character_id: str = Path(..., description="Character ID"),
    db: AsyncSession = Depends(get_db_session_dependency)
) -> Dict[str, Any]:
    """Get a specific character by ID."""
    
    try:
        # Query character with relationships
        query = select(Character).where(
            Character.id == character_id,
            Character.is_deleted == False
        ).options(
            selectinload(Character.ruleset),
            selectinload(Character.spells),
            selectinload(Character.features),
            selectinload(Character.items)
        )
        
        result = await db.execute(query)
        character = result.scalar_one_or_none()
        
        if not character:
            raise HTTPException(status_code=404, detail="Character not found")
        
        # Convert to dictionary with relationships
        char_dict = character.to_dict()
        char_dict["ruleset"] = character.ruleset.to_dict() if character.ruleset else None
        char_dict["spells"] = [spell.to_dict() for spell in character.spells]
        char_dict["features"] = [feature.to_dict() for feature in character.features]
        char_dict["items"] = [item.to_dict() for item in character.items]
        
        logger.info(f"Retrieved character: {character.character_name}")
        return char_dict
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving character {character_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve character")


@router.post("/", response_model=Dict[str, Any])
async def create_character(
    character_data: Dict[str, Any],
    db: AsyncSession = Depends(get_db_session_dependency)
) -> Dict[str, Any]:
    """Create a new character."""
    
    try:
        # Validate required fields
        required_fields = ["character_name", "ruleset_id"]
        for field in required_fields:
            if field not in character_data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        # Check if ruleset exists and is active
        ruleset_query = select(Ruleset).where(
            Ruleset.id == character_data["ruleset_id"],
            Ruleset.is_deleted == False
        )
        ruleset_result = await db.execute(ruleset_query)
        ruleset = ruleset_result.scalar_one_or_none()
        
        if not ruleset:
            raise HTTPException(status_code=400, detail="Invalid ruleset ID")
        
        if not ruleset.is_active():
            raise HTTPException(status_code=400, detail="Ruleset is not active")
        
        # Create character instance
        character = Character(**character_data)
        
        # Validate character
        if not character.is_valid:
            validation_errors = character.validation_errors or []
            raise HTTPException(
                status_code=400,
                detail=f"Character validation failed: {', '.join(validation_errors)}"
            )
        
        # Add to database
        db.add(character)
        await db.commit()
        await db.refresh(character)
        
        logger.info(f"Created character: {character.character_name}")
        return character.to_dict()
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating character: {e}")
        raise HTTPException(status_code=500, detail="Failed to create character")


@router.put("/{character_id}", response_model=Dict[str, Any])
async def update_character(
    character_id: str = Path(..., description="Character ID"),
    character_data: Dict[str, Any] = None,
    db: AsyncSession = Depends(get_db_session_dependency)
) -> Dict[str, Any]:
    """Update an existing character."""
    
    try:
        # Get existing character
        query = select(Character).where(
            Character.id == character_id,
            Character.is_deleted == False
        )
        result = await db.execute(query)
        character = result.scalar_one_or_none()
        
        if not character:
            raise HTTPException(status_code=404, detail="Character not found")
        
        # Update character data
        if character_data:
            # Remove fields that shouldn't be updated
            protected_fields = ["id", "created_at", "created_by"]
            for field in protected_fields:
                character_data.pop(field, None)
            
            # Update character attributes
            character.update_from_dict(character_data)
            
            # Validate updated character
            if not character.is_valid:
                validation_errors = character.validation_errors or []
                raise HTTPException(
                    status_code=400,
                    detail=f"Character validation failed: {', '.join(validation_errors)}"
                )
        
        # Save changes
        await db.commit()
        await db.refresh(character)
        
        logger.info(f"Updated character: {character.character_name}")
        return character.to_dict()
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating character {character_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update character")


@router.delete("/{character_id}")
async def delete_character(
    character_id: str = Path(..., description="Character ID"),
    permanent: bool = Query(False, description="Permanently delete character"),
    db: AsyncSession = Depends(get_db_session_dependency)
) -> Dict[str, str]:
    """Delete a character (soft delete by default)."""
    
    try:
        # Get existing character
        query = select(Character).where(
            Character.id == character_id,
            Character.is_deleted == False
        )
        result = await db.execute(query)
        character = result.scalar_one_or_none()
        
        if not character:
            raise HTTPException(status_code=404, detail="Character not found")
        
        if permanent:
            # Permanent deletion
            await db.delete(character)
            message = f"Character {character.character_name} permanently deleted"
        else:
            # Soft deletion
            character.soft_delete()
            message = f"Character {character.character_name} soft deleted"
        
        await db.commit()
        
        logger.info(message)
        return {"message": message}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting character {character_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete character")


@router.post("/{character_id}/level-up")
async def level_up_character(
    character_id: str = Path(..., description="Character ID"),
    db: AsyncSession = Depends(get_db_session_dependency)
) -> Dict[str, Any]:
    """Level up a character manually."""
    
    try:
        # Get existing character
        query = select(Character).where(
            Character.id == character_id,
            Character.is_deleted == False
        )
        result = await db.execute(query)
        character = result.scalar_one_or_none()
        
        if not character:
            raise HTTPException(status_code=404, detail="Character not found")
        
        # Level up character
        character.level_up()
        
        # Save changes
        await db.commit()
        await db.refresh(character)
        
        logger.info(f"Character {character.character_name} leveled up to {character.level}")
        return {
            "message": f"Character leveled up to {character.level}",
            "character": character.to_dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error leveling up character {character_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to level up character")


@router.post("/{character_id}/add-experience")
async def add_experience(
    character_id: str = Path(..., description="Character ID"),
    experience_points: int = Query(..., ge=1, description="Experience points to add"),
    db: AsyncSession = Depends(get_db_session_dependency)
) -> Dict[str, Any]:
    """Add experience points to a character."""
    
    try:
        # Get existing character
        query = select(Character).where(
            Character.id == character_id,
            Character.is_deleted == False
        )
        result = await db.execute(query)
        character = result.scalar_one_or_none()
        
        if not character:
            raise HTTPException(status_code=404, detail="Character not found")
        
        # Add experience
        leveled_up = character.add_experience(experience_points)
        
        # Save changes
        await db.commit()
        await db.refresh(character)
        
        message = f"Added {experience_points} XP to character"
        if leveled_up:
            message += f" - Character leveled up to {character.level}!"
        
        logger.info(f"Added {experience_points} XP to character {character.character_name}")
        return {
            "message": message,
            "character": character.to_dict(),
            "leveled_up": leveled_up
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding experience to character {character_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to add experience")


@router.get("/{character_id}/validation")
async def validate_character(
    character_id: str = Path(..., description="Character ID"),
    db: AsyncSession = Depends(get_db_session_dependency)
) -> Dict[str, Any]:
    """Validate a character against its ruleset rules."""
    
    try:
        # Get existing character with ruleset
        query = select(Character).where(
            Character.id == character_id,
            Character.is_deleted == False
        ).options(selectinload(Character.ruleset))
        
        result = await db.execute(query)
        character = result.scalar_one_or_none()
        
        if not character:
            raise HTTPException(status_code=404, detail="Character not found")
        
        # Perform validation
        validation_errors = []
        warnings = []
        
        # Basic validation
        if character.level < 1:
            validation_errors.append("Character level must be at least 1")
        
        if character.experience_points < 0:
            validation_errors.append("Experience points cannot be negative")
        
        # Ability score validation
        for ability in ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]:
            score = getattr(character, ability)
            if score < 1 or score > 30:
                validation_errors.append(f"{ability.title()} score must be between 1 and 30")
            elif score > 20:
                warnings.append(f"{ability.title()} score is above 20 (unusual)")
        
        # Hit point validation
        if character.current_hit_points > character.max_hit_points:
            validation_errors.append("Current hit points cannot exceed maximum hit points")
        
        if character.temporary_hit_points < 0:
            validation_errors.append("Temporary hit points cannot be negative")
        
        # Ruleset-specific validation
        if character.ruleset:
            # Add ruleset-specific validation here
            pass
        
        # Update character validation status
        character.is_valid = len(validation_errors) == 0
        character.validation_errors = validation_errors
        
        # Save validation status
        await db.commit()
        
        return {
            "character_id": character_id,
            "character_name": character.character_name,
            "is_valid": character.is_valid,
            "validation_errors": validation_errors,
            "warnings": warnings,
            "validation_timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error validating character {character_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to validate character")
