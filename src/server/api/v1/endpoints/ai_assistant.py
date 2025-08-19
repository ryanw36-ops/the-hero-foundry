#!/usr/bin/env python3
"""
AI Assistant endpoints for The Hero Foundry backend server.

Provides context-aware AI assistance, rule explanations, and character optimization advice.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import json

from fastapi import APIRouter, Depends, HTTPException, Query, Path, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from ...core.database import get_db_session_dependency
from ...core.config import get_settings
from ...core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)
settings = get_settings()


@router.post("/chat")
async def ai_chat(
    message: Dict[str, Any],
    db: AsyncSession = Depends(get_db_session_dependency)
) -> Dict[str, Any]:
    """Send a message to the AI assistant and get a response."""
    
    try:
        # Extract message data
        user_message = message.get("message", "")
        context = message.get("context", {})
        character_id = context.get("character_id")
        current_step = context.get("current_step")
        ruleset_id = context.get("ruleset_id")
        
        if not user_message:
            raise HTTPException(status_code=400, detail="Message content is required")
        
        # Get AI response
        ai_response = await _get_ai_response(user_message, context, db)
        
        # Log the interaction
        logger.info(f"AI chat interaction: {user_message[:100]}...")
        
        return {
            "response": ai_response["response"],
            "suggestions": ai_response["suggestions"],
            "rule_explanations": ai_response["rule_explanations"],
            "context_used": context,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in AI chat: {e}")
        raise HTTPException(status_code=500, detail="Failed to process AI chat request")


@router.post("/explain-rule")
async def explain_rule(
    rule_request: Dict[str, Any],
    db: AsyncSession = Depends(get_db_session_dependency)
) -> Dict[str, Any]:
    """Get AI explanation of a specific rule or mechanic."""
    
    try:
        # Extract rule information
        rule_name = rule_request.get("rule_name", "")
        rule_context = rule_request.get("context", {})
        character_level = rule_context.get("character_level", 1)
        character_class = rule_context.get("character_class", "")
        
        if not rule_name:
            raise HTTPException(status_code=400, detail="Rule name is required")
        
        # Get rule explanation
        explanation = await _explain_rule(rule_name, rule_context, db)
        
        return {
            "rule_name": rule_name,
            "explanation": explanation["explanation"],
            "examples": explanation["examples"],
            "related_rules": explanation["related_rules"],
            "tips": explanation["tips"],
            "context": rule_context,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error explaining rule {rule_request.get('rule_name', 'unknown')}: {e}")
        raise HTTPException(status_code=500, detail="Failed to explain rule")


@router.post("/optimize-character")
async def optimize_character(
    optimization_request: Dict[str, Any],
    db: AsyncSession = Depends(get_db_session_dependency)
) -> Dict[str, Any]:
    """Get AI suggestions for character optimization."""
    
    try:
        # Extract optimization parameters
        character_data = optimization_request.get("character_data", {})
        optimization_goals = optimization_request.get("goals", [])
        constraints = optimization_request.get("constraints", {})
        
        if not character_data:
            raise HTTPException(status_code=400, detail="Character data is required")
        
        # Get optimization suggestions
        optimization = await _optimize_character(character_data, optimization_goals, constraints, db)
        
        return {
            "character_name": character_data.get("character_name", "Unknown"),
            "optimization_goals": optimization_goals,
            "suggestions": optimization["suggestions"],
            "build_recommendations": optimization["build_recommendations"],
            "feat_suggestions": optimization["feat_suggestions"],
            "spell_recommendations": optimization["spell_recommendations"],
            "priority_order": optimization["priority_order"],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error optimizing character: {e}")
        raise HTTPException(status_code=500, detail="Failed to optimize character")


@router.post("/validate-build")
async def validate_character_build(
    build_data: Dict[str, Any],
    db: AsyncSession = Depends(get_db_session_dependency)
) -> Dict[str, Any]:
    """Validate a character build and provide feedback."""
    
    try:
        # Extract build information
        character_build = build_data.get("character_build", {})
        ruleset_id = build_data.get("ruleset_id")
        
        if not character_build:
            raise HTTPException(status_code=400, detail="Character build data is required")
        
        # Validate the build
        validation = await _validate_character_build(character_build, ruleset_id, db)
        
        return {
            "is_valid": validation["is_valid"],
            "validation_errors": validation["validation_errors"],
            "warnings": validation["warnings"],
            "suggestions": validation["suggestions"],
            "balance_score": validation["balance_score"],
            "power_analysis": validation["power_analysis"],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error validating character build: {e}")
        raise HTTPException(status_code=500, detail="Failed to validate character build")


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: str,
    db: AsyncSession = Depends(get_db_session_dependency)
):
    """WebSocket endpoint for real-time AI chat."""
    
    await websocket.accept()
    logger.info(f"WebSocket connection established for client {client_id}")
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Process message
            response = await _get_ai_response(
                message_data.get("message", ""),
                message_data.get("context", {}),
                db
            )
            
            # Send response back to client
            await websocket.send_text(json.dumps({
                "type": "ai_response",
                "response": response["response"],
                "suggestions": response["suggestions"],
                "timestamp": datetime.now(timezone.utc).isoformat()
            }))
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket connection closed for client {client_id}")
    except Exception as e:
        logger.error(f"Error in WebSocket connection for client {client_id}: {e}")
        try:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": "An error occurred while processing your request"
            }))
        except:
            pass


# Helper functions for AI assistant functionality

async def _get_ai_response(
    user_message: str,
    context: Dict[str, Any],
    db: AsyncSession
) -> Dict[str, Any]:
    """Get AI response based on user message and context."""
    
    # This would integrate with OpenAI or another AI service
    # For now, return a placeholder response
    
    # Analyze message intent
    intent = _analyze_message_intent(user_message)
    
    # Generate contextual response
    if intent == "character_creation":
        response = _generate_character_creation_response(user_message, context)
    elif intent == "rule_question":
        response = _generate_rule_explanation_response(user_message, context)
    elif intent == "optimization":
        response = _generate_optimization_response(user_message, context)
    else:
        response = _generate_general_response(user_message, context)
    
    return {
        "response": response["response"],
        "suggestions": response["suggestions"],
        "rule_explanations": response.get("rule_explanations", [])
    }


async def _explain_rule(
    rule_name: str,
    context: Dict[str, Any],
    db: AsyncSession
) -> Dict[str, Any]:
    """Explain a specific rule or mechanic."""
    
    # This would query the ruleset database and provide AI-enhanced explanations
    # For now, return placeholder content
    
    rule_explanations = {
        "ability_scores": {
            "explanation": "Ability scores represent your character's basic attributes: Strength, Dexterity, Constitution, Intelligence, Wisdom, and Charisma. Each score ranges from 1 to 20, with 10-11 being average.",
            "examples": ["A Strength of 16 means your character is quite strong", "A Dexterity of 8 means your character is somewhat clumsy"],
            "related_rules": ["ability modifiers", "saving throws", "skill checks"],
            "tips": ["Focus on ability scores that benefit your class", "Consider racial bonuses when planning ability scores"]
        },
        "spellcasting": {
            "explanation": "Spellcasting allows characters to cast magical spells. Different classes gain spellcasting in different ways, and spells have various components, ranges, and durations.",
            "examples": ["Wizards learn spells from spellbooks", "Clerics pray for their spells each day"],
            "related_rules": ["spell slots", "spell components", "concentration"],
            "tips": ["Always have backup spells prepared", "Consider spell components when adventuring"]
        }
    }
    
    explanation = rule_explanations.get(rule_name.lower(), {
        "explanation": f"Rule explanation for {rule_name} is not yet implemented.",
        "examples": [],
        "related_rules": [],
        "tips": []
    })
    
    return explanation


async def _optimize_character(
    character_data: Dict[str, Any],
    goals: List[str],
    constraints: Dict[str, Any],
    db: AsyncSession
) -> Dict[str, Any]:
    """Provide character optimization suggestions."""
    
    # This would analyze the character and provide AI-powered optimization advice
    # For now, return placeholder suggestions
    
    suggestions = []
    build_recommendations = []
    feat_suggestions = []
    spell_recommendations = []
    priority_order = []
    
    # Analyze character class
    character_class = character_data.get("character_class", "")
    if character_class:
        if "fighter" in character_class.lower():
            suggestions.append("Consider taking the Great Weapon Master feat for high damage output")
            build_recommendations.append("Focus on Strength and Constitution for melee combat")
        elif "wizard" in character_class.lower():
            suggestions.append("Maximize Intelligence for spell effectiveness")
            build_recommendations.append("Take feats like War Caster for concentration advantage")
    
    # Analyze ability scores
    ability_scores = character_data.get("ability_scores", {})
    if ability_scores:
        highest_score = max(ability_scores.values())
        highest_ability = max(ability_scores, key=ability_scores.get)
        suggestions.append(f"Your highest ability is {highest_ability} ({highest_score}) - build around this strength")
    
    return {
        "suggestions": suggestions,
        "build_recommendations": build_recommendations,
        "feat_suggestions": feat_suggestions,
        "spell_recommendations": spell_recommendations,
        "priority_order": priority_order
    }


async def _validate_character_build(
    character_build: Dict[str, Any],
    ruleset_id: Optional[str],
    db: AsyncSession
) -> Dict[str, Any]:
    """Validate a character build and provide feedback."""
    
    # This would perform comprehensive validation against ruleset rules
    # For now, return basic validation
    
    validation_errors = []
    warnings = []
    suggestions = []
    
    # Basic validation
    if not character_build.get("character_name"):
        validation_errors.append("Character must have a name")
    
    if character_build.get("level", 0) < 1:
        validation_errors.append("Character level must be at least 1")
    
    # Ability score validation
    ability_scores = character_build.get("ability_scores", {})
    for ability, score in ability_scores.items():
        if score < 1 or score > 20:
            validation_errors.append(f"{ability.title()} score must be between 1 and 20")
        elif score > 18:
            warnings.append(f"{ability.title()} score of {score} is unusually high")
    
    # Calculate balance score
    balance_score = _calculate_build_balance_score(character_build)
    
    # Generate suggestions
    if balance_score < 0.5:
        suggestions.append("Consider redistributing ability scores for better balance")
    
    return {
        "is_valid": len(validation_errors) == 0,
        "validation_errors": validation_errors,
        "warnings": warnings,
        "suggestions": suggestions,
        "balance_score": balance_score,
        "power_analysis": _analyze_build_power(character_build)
    }


def _analyze_message_intent(message: str) -> str:
    """Analyze the intent of a user message."""
    
    message_lower = message.lower()
    
    if any(word in message_lower for word in ["create", "make", "build", "new character"]):
        return "character_creation"
    elif any(word in message_lower for word in ["rule", "how", "what", "explain", "mean"]):
        return "rule_question"
    elif any(word in message_lower for word in ["optimize", "best", "improve", "better"]):
        return "optimization"
    else:
        return "general"


def _generate_character_creation_response(message: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Generate response for character creation questions."""
    
    current_step = context.get("current_step", "unknown")
    
    responses = {
        "race_selection": {
            "response": "Great question about race selection! Consider your character's backstory and the mechanical benefits. Each race offers unique abilities that can complement your class choice.",
            "suggestions": [
                "Look at ability score bonuses that match your class",
                "Consider racial traits that enhance your playstyle",
                "Think about the story implications of your choice"
            ]
        },
        "class_selection": {
            "response": "Class selection is a crucial decision! Think about how you want to play and contribute to the party. Each class has different roles and playstyles.",
            "suggestions": [
                "Consider party composition and roles",
                "Think about your preferred playstyle (melee, ranged, support, etc.)",
                "Look at class features and how they scale with levels"
            ]
        },
        "ability_scores": {
            "response": "Ability scores form the foundation of your character! Focus on the abilities that matter most for your class, but don't neglect others completely.",
            "suggestions": [
                "Prioritize your class's primary ability score",
                "Consider secondary abilities that support your build",
                "Don't let any score fall below 8 unless you have a specific reason"
            ]
        }
    }
    
    return responses.get(current_step, {
        "response": "I'd be happy to help with character creation! What specific aspect would you like guidance on?",
        "suggestions": [
            "Start with your character concept and backstory",
            "Choose a class that fits your desired playstyle",
            "Consider how your race and class work together"
        ]
    })


def _generate_rule_explanation_response(message: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Generate response for rule explanation questions."""
    
    return {
        "response": "I'd be happy to explain that rule! Rules in D&D can be complex, but understanding them helps make better decisions for your character.",
        "suggestions": [
            "Check the Player's Handbook for the official rule text",
            "Look for examples in the rulebook",
            "Consider how the rule interacts with other game mechanics"
        ],
        "rule_explanations": [
            "Rules often have exceptions and special cases",
            "Context matters - the same rule might work differently in different situations"
        ]
    }


def _generate_optimization_response(message: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Generate response for optimization questions."""
    
    return {
        "response": "Character optimization is about making choices that support your goals! The key is finding the right balance between effectiveness and fun.",
        "suggestions": [
            "Define what 'optimal' means for your character concept",
            "Consider both mechanical effectiveness and roleplay potential",
            "Don't sacrifice fun for a few extra points of damage"
        ]
    }


def _generate_general_response(message: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Generate general response for other types of questions."""
    
    return {
        "response": "I'm here to help with your D&D character creation and gameplay questions! Feel free to ask about specific rules, character builds, or game mechanics.",
        "suggestions": [
            "Be specific about what you want to know",
            "Provide context about your character and situation",
            "Ask follow-up questions if you need clarification"
        ]
    }


def _calculate_build_balance_score(character_build: Dict[str, Any]) -> float:
    """Calculate a balance score for a character build (0.0 to 1.0)."""
    
    score = 0.5  # Base score
    
    # Analyze ability score distribution
    ability_scores = character_build.get("ability_scores", {})
    if ability_scores:
        scores = list(ability_scores.values())
        score_variance = max(scores) - min(scores)
        
        if score_variance <= 6:
            score += 0.2  # Balanced scores
        elif score_variance >= 12:
            score -= 0.2  # Very uneven scores
    
    # Consider class-ability synergy
    character_class = character_build.get("character_class", "")
    primary_ability = character_build.get("primary_ability", "")
    
    if character_class and primary_ability:
        class_ability_map = {
            "fighter": "strength",
            "wizard": "intelligence",
            "rogue": "dexterity",
            "cleric": "wisdom",
            "bard": "charisma"
        }
        
        if class_ability_map.get(character_class.lower()) == primary_ability.lower():
            score += 0.1  # Good class-ability synergy
    
    return max(0.0, min(1.0, score))


def _analyze_build_power(character_build: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze the power level of a character build."""
    
    power_analysis = {
        "combat_power": 0.5,
        "utility_power": 0.5,
        "survivability": 0.5,
        "overall_power": 0.5
    }
    
    # This would implement more sophisticated power analysis
    # For now, return basic analysis
    
    return power_analysis
