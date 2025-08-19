#!/usr/bin/env python3
"""
Homebrew content management endpoints for The Hero Foundry backend server.

Provides tools for building custom content with balance validation, power budget analysis, and compatibility checking.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from ...core.database import get_db_session_dependency
from ...core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/", response_model=List[Dict[str, Any]])
async def list_homebrew_content(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return"),
    content_type: Optional[str] = Query(None, description="Filter by content type"),
    ruleset_id: Optional[str] = Query(None, description="Filter by ruleset ID"),
    db: AsyncSession = Depends(get_db_session_dependency)
) -> List[Dict[str, Any]]:
    """List all homebrew content with optional filtering."""
    
    try:
        # This endpoint would query the appropriate homebrew content tables
        # For now, return a placeholder response
        return {
            "message": "Homebrew content listing endpoint - implementation pending",
            "filters": {
                "skip": skip,
                "limit": limit,
                "content_type": content_type,
                "ruleset_id": ruleset_id
            }
        }
        
    except Exception as e:
        logger.error(f"Error retrieving homebrew content: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve homebrew content")


@router.post("/validate")
async def validate_homebrew_content(
    content_data: Dict[str, Any],
    db: AsyncSession = Depends(get_db_session_dependency)
) -> Dict[str, Any]:
    """Validate homebrew content against ruleset schemas and balance guidelines."""
    
    try:
        # Extract content information
        content_type = content_data.get("content_type")
        ruleset_id = content_data.get("ruleset_id")
        content = content_data.get("content", {})
        
        if not content_type:
            raise HTTPException(status_code=400, detail="Content type is required")
        
        if not ruleset_id:
            raise HTTPException(status_code=400, detail="Ruleset ID is required")
        
        # Perform validation
        validation_result = await _validate_content(content_type, content, ruleset_id, db)
        
        return {
            "content_type": content_type,
            "ruleset_id": ruleset_id,
            "is_valid": validation_result["is_valid"],
            "validation_errors": validation_result["validation_errors"],
            "warnings": validation_result["warnings"],
            "balance_score": validation_result["balance_score"],
            "power_budget_analysis": validation_result["power_budget_analysis"],
            "validation_timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error validating homebrew content: {e}")
        raise HTTPException(status_code=500, detail="Failed to validate homebrew content")


@router.post("/analyze-balance")
async def analyze_content_balance(
    content_data: Dict[str, Any],
    db: AsyncSession = Depends(get_db_session_dependency)
) -> Dict[str, Any]:
    """Analyze the balance and power budget of homebrew content."""
    
    try:
        # Extract content information
        content_type = content_data.get("content_type")
        content = content_data.get("content", {})
        
        if not content_type:
            raise HTTPException(status_code=400, detail="Content type is required")
        
        # Perform balance analysis
        balance_analysis = await _analyze_content_balance(content_type, content, db)
        
        return {
            "content_type": content_type,
            "balance_analysis": balance_analysis,
            "power_budget": balance_analysis["power_budget"],
            "balance_score": balance_analysis["balance_score"],
            "recommendations": balance_analysis["recommendations"],
            "analysis_timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing content balance: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze content balance")


@router.get("/templates/{content_type}")
async def get_content_template(
    content_type: str = Path(..., description="Type of content template to retrieve"),
    ruleset_id: Optional[str] = Query(None, description="Ruleset ID for template"),
    db: AsyncSession = Depends(get_db_session_dependency)
) -> Dict[str, Any]:
    """Get a template for creating homebrew content of a specific type."""
    
    try:
        # Get template based on content type
        template = await _get_content_template(content_type, ruleset_id, db)
        
        return {
            "content_type": content_type,
            "template": template,
            "ruleset_id": ruleset_id,
            "description": f"Template for creating {content_type} content"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving template for {content_type}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve content template")


@router.post("/export")
async def export_homebrew_content(
    content_ids: List[str],
    export_format: str = Query("json", description="Export format (json, yaml, markdown)"),
    db: AsyncSession = Depends(get_db_session_dependency)
) -> Dict[str, Any]:
    """Export homebrew content in various formats."""
    
    try:
        if not content_ids:
            raise HTTPException(status_code=400, detail="At least one content ID is required")
        
        # Validate export format
        valid_formats = ["json", "yaml", "markdown"]
        if export_format not in valid_formats:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid export format. Must be one of: {', '.join(valid_formats)}"
            )
        
        # Export content
        export_result = await _export_content(content_ids, export_format, db)
        
        return {
            "exported_content": export_result["content"],
            "export_format": export_format,
            "export_timestamp": datetime.now(timezone.utc).isoformat(),
            "file_size": export_result["file_size"],
            "download_url": export_result["download_url"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting homebrew content: {e}")
        raise HTTPException(status_code=500, detail="Failed to export homebrew content")


# Helper functions for homebrew content management

async def _validate_content(
    content_type: str,
    content: Dict[str, Any],
    ruleset_id: str,
    db: AsyncSession
) -> Dict[str, Any]:
    """Validate homebrew content against ruleset rules."""
    
    validation_errors = []
    warnings = []
    balance_score = 0.0
    
    # Basic validation
    if not content.get("name"):
        validation_errors.append("Content must have a name")
    
    if not content.get("description"):
        warnings.append("Content should have a description")
    
    # Content type specific validation
    if content_type == "race":
        balance_score = await _validate_race_balance(content)
    elif content_type == "class":
        balance_score = await _validate_class_balance(content)
    elif content_type == "spell":
        balance_score = await _validate_spell_balance(content)
    elif content_type == "item":
        balance_score = await _validate_item_balance(content)
    else:
        warnings.append(f"Unknown content type: {content_type}")
    
    # Power budget analysis
    power_budget_analysis = await _analyze_power_budget(content_type, content)
    
    return {
        "is_valid": len(validation_errors) == 0,
        "validation_errors": validation_errors,
        "warnings": warnings,
        "balance_score": balance_score,
        "power_budget_analysis": power_budget_analysis
    }


async def _analyze_content_balance(
    content_type: str,
    content: Dict[str, Any],
    db: AsyncSession
) -> Dict[str, Any]:
    """Analyze the balance of homebrew content."""
    
    balance_score = 0.0
    power_budget = {}
    recommendations = []
    
    # Analyze based on content type
    if content_type == "race":
        balance_score, power_budget, recommendations = await _analyze_race_balance(content)
    elif content_type == "class":
        balance_score, power_budget, recommendations = await _analyze_class_balance(content)
    elif content_type == "spell":
        balance_score, power_budget, recommendations = await _analyze_spell_balance(content)
    elif content_type == "item":
        balance_score, power_budget, recommendations = await _analyze_item_balance(content)
    
    return {
        "balance_score": balance_score,
        "power_budget": power_budget,
        "recommendations": recommendations
    }


async def _get_content_template(
    content_type: str,
    ruleset_id: Optional[str],
    db: AsyncSession
) -> Dict[str, Any]:
    """Get a template for creating homebrew content."""
    
    # Basic templates for different content types
    templates = {
        "race": {
            "name": "",
            "description": "",
            "ability_score_increases": {},
            "traits": [],
            "subraces": [],
            "age": "",
            "alignment": "",
            "size": "medium",
            "speed": 30,
            "languages": ["common"]
        },
        "class": {
            "name": "",
            "description": "",
            "hit_die": "d8",
            "primary_ability": "",
            "saving_throw_proficiencies": [],
            "armor_proficiencies": [],
            "weapon_proficiencies": [],
            "tool_proficiencies": [],
            "skill_proficiencies": [],
            "features": [],
            "spellcasting": False,
            "spellcasting_ability": None
        },
        "spell": {
            "name": "",
            "level": 0,
            "school": "",
            "casting_time": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "higher_levels": "",
            "classes": []
        },
        "item": {
            "name": "",
            "description": "",
            "type": "",
            "rarity": "",
            "cost": "",
            "weight": 0,
            "properties": [],
            "magical": False,
            "attunement": False
        }
    }
    
    return templates.get(content_type, {})


async def _export_content(
    content_ids: List[str],
    export_format: str,
    db: AsyncSession
) -> Dict[str, Any]:
    """Export homebrew content in the specified format."""
    
    # This would implement the actual export logic
    # For now, return a placeholder response
    
    return {
        "content": f"Exported {len(content_ids)} items in {export_format} format",
        "file_size": "0 KB",
        "download_url": "/exports/homebrew-content.json"
    }


# Balance validation functions for different content types

async def _validate_race_balance(content: Dict[str, Any]) -> float:
    """Validate race balance and return a score from 0.0 to 1.0."""
    score = 0.5  # Base score
    
    # Check ability score increases
    ability_increases = content.get("ability_score_increases", {})
    total_increase = sum(ability_increases.values())
    
    if total_increase <= 2:
        score += 0.2
    elif total_increase <= 3:
        score += 0.1
    else:
        score -= 0.2
    
    # Check traits
    traits = content.get("traits", [])
    if len(traits) <= 3:
        score += 0.1
    elif len(traits) > 5:
        score -= 0.2
    
    return max(0.0, min(1.0, score))


async def _validate_class_balance(content: Dict[str, Any]) -> float:
    """Validate class balance and return a score from 0.0 to 1.0."""
    score = 0.5  # Base score
    
    # Check hit die
    hit_die = content.get("hit_die", "d8")
    if hit_die == "d12":
        score += 0.1
    elif hit_die == "d6":
        score -= 0.1
    
    # Check proficiencies
    armor_profs = len(content.get("armor_proficiencies", []))
    weapon_profs = len(content.get("weapon_proficiencies", []))
    
    if armor_profs + weapon_profs <= 4:
        score += 0.1
    elif armor_profs + weapon_profs > 8:
        score -= 0.2
    
    return max(0.0, min(1.0, score))


async def _validate_spell_balance(content: Dict[str, Any]) -> float:
    """Validate spell balance and return a score from 0.0 to 1.0."""
    score = 0.5  # Base score
    
    # Check spell level
    level = content.get("level", 0)
    if level <= 3:
        score += 0.1
    elif level >= 7:
        score -= 0.1
    
    # Check components
    components = content.get("components", [])
    if "V" in components and "S" in components:
        score += 0.1  # Verbal + Somatic is standard
    
    return max(0.0, min(1.0, score))


async def _validate_item_balance(content: Dict[str, Any]) -> float:
    """Validate item balance and return a score from 0.0 to 1.0."""
    score = 0.5  # Base score
    
    # Check rarity
    rarity = content.get("rarity", "common")
    rarity_scores = {"common": 0.1, "uncommon": 0.0, "rare": -0.1, "very_rare": -0.2, "legendary": -0.3}
    score += rarity_scores.get(rarity, 0.0)
    
    # Check magical properties
    if content.get("magical", False):
        score -= 0.1  # Magical items are typically more powerful
    
    return max(0.0, min(1.0, score))


# Power budget analysis functions

async def _analyze_power_budget(content_type: str, content: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze the power budget of homebrew content."""
    
    if content_type == "race":
        return await _analyze_race_power_budget(content)
    elif content_type == "class":
        return await _analyze_class_power_budget(content)
    elif content_type == "spell":
        return await _analyze_spell_power_budget(content)
    elif content_type == "item":
        return await _analyze_item_power_budget(content)
    
    return {"total_power": 0, "power_breakdown": {}, "recommendations": []}


async def _analyze_race_power_budget(content: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze race power budget."""
    power_breakdown = {
        "ability_scores": 0,
        "traits": 0,
        "subraces": 0,
        "languages": 0
    }
    
    # Calculate power from ability score increases
    ability_increases = content.get("ability_score_increases", {})
    power_breakdown["ability_scores"] = sum(ability_increases.values()) * 0.5
    
    # Calculate power from traits
    traits = content.get("traits", [])
    power_breakdown["traits"] = len(traits) * 0.3
    
    # Calculate power from subraces
    subraces = content.get("subraces", [])
    power_breakdown["subraces"] = len(subraces) * 0.4
    
    total_power = sum(power_breakdown.values())
    
    recommendations = []
    if total_power > 3.0:
        recommendations.append("Consider reducing ability score increases or traits")
    elif total_power < 1.5:
        recommendations.append("Consider adding more traits or subraces")
    
    return {
        "total_power": total_power,
        "power_breakdown": power_breakdown,
        "recommendations": recommendations
    }


async def _analyze_class_power_budget(content: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze class power budget."""
    power_breakdown = {
        "hit_die": 0,
        "proficiencies": 0,
        "features": 0,
        "spellcasting": 0
    }
    
    # Calculate power from hit die
    hit_die = content.get("hit_die", "d8")
    hit_die_power = {"d6": 0.5, "d8": 1.0, "d10": 1.5, "d12": 2.0}
    power_breakdown["hit_die"] = hit_die_power.get(hit_die, 1.0)
    
    # Calculate power from proficiencies
    armor_profs = len(content.get("armor_proficiencies", []))
    weapon_profs = len(content.get("weapon_proficiencies", []))
    power_breakdown["proficiencies"] = (armor_profs + weapon_profs) * 0.2
    
    # Calculate power from features
    features = content.get("features", [])
    power_breakdown["features"] = len(features) * 0.3
    
    # Calculate power from spellcasting
    if content.get("spellcasting", False):
        power_breakdown["spellcasting"] = 1.0
    
    total_power = sum(power_breakdown.values())
    
    recommendations = []
    if total_power > 4.0:
        recommendations.append("Consider reducing proficiencies or features")
    elif total_power < 2.0:
        recommendations.append("Consider adding more features or proficiencies")
    
    return {
        "total_power": total_power,
        "power_breakdown": power_breakdown,
        "recommendations": recommendations
    }


async def _analyze_spell_power_budget(content: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze spell power budget."""
    power_breakdown = {
        "level": 0,
        "components": 0,
        "range": 0,
        "duration": 0
    }
    
    # Calculate power from spell level
    level = content.get("level", 0)
    power_breakdown["level"] = level * 0.5
    
    # Calculate power from components
    components = content.get("components", [])
    power_breakdown["components"] = len(components) * 0.1
    
    # Calculate power from range
    range_value = content.get("range", "")
    if "self" in range_value:
        power_breakdown["range"] = 0.5
    elif "touch" in range_value:
        power_breakdown["range"] = 0.3
    elif "60 feet" in range_value or "30 feet" in range_value:
        power_breakdown["range"] = 0.1
    
    # Calculate power from duration
    duration = content.get("duration", "")
    if "concentration" in duration:
        power_breakdown["duration"] = 0.2
    elif "1 hour" in duration or "8 hours" in duration:
        power_breakdown["duration"] = 0.3
    
    total_power = sum(power_breakdown.values())
    
    recommendations = []
    if total_power > level + 1.0:
        recommendations.append("Consider reducing spell power to match level")
    elif total_power < level * 0.5:
        recommendations.append("Consider increasing spell power to match level")
    
    return {
        "total_power": total_power,
        "power_breakdown": power_breakdown,
        "recommendations": recommendations
    }


async def _analyze_item_power_budget(content: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze item power budget."""
    power_breakdown = {
        "rarity": 0,
        "properties": 0,
        "magical": 0,
        "attunement": 0
    }
    
    # Calculate power from rarity
    rarity = content.get("rarity", "common")
    rarity_power = {"common": 0.5, "uncommon": 1.0, "rare": 1.5, "very_rare": 2.0, "legendary": 2.5}
    power_breakdown["rarity"] = rarity_power.get(rarity, 0.5)
    
    # Calculate power from properties
    properties = content.get("properties", [])
    power_breakdown["properties"] = len(properties) * 0.2
    
    # Calculate power from magical nature
    if content.get("magical", False):
        power_breakdown["magical"] = 0.5
    
    # Calculate power from attunement
    if content.get("attunement", False):
        power_breakdown["attunement"] = -0.3  # Attunement reduces power
    
    total_power = sum(power_breakdown.values())
    
    recommendations = []
    if total_power > rarity_power.get(rarity, 1.0) + 0.5:
        recommendations.append("Consider reducing properties to match rarity")
    elif total_power < rarity_power.get(rarity, 1.0) - 0.5:
        recommendations.append("Consider adding properties to match rarity")
    
    return {
        "total_power": total_power,
        "power_breakdown": power_breakdown,
        "recommendations": recommendations
    }
