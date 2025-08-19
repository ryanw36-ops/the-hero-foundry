#!/usr/bin/env python3
"""
Character model for The Hero Foundry backend server.

Defines the Character entity with all D&D character attributes, abilities, and progression tracking.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from decimal import Decimal

from sqlalchemy import String, Integer, Text, Boolean, JSON, Numeric, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from .base import BaseModel, SoftDeleteMixin, VersionedMixin


# Association tables for many-to-many relationships
character_spells = Table(
    'character_spells',
    BaseModel.metadata,
    Column('character_id', UUID(as_uuid=False), ForeignKey('characters.id'), primary_key=True),
    Column('spell_id', UUID(as_uuid=False), ForeignKey('spells.id'), primary_key=True),
    Column('prepared', Boolean, default=False),
    Column('cast_at_level', Integer, default=1)
)

character_features = Table(
    'character_features',
    BaseModel.metadata,
    Column('character_id', UUID(as_uuid=False), ForeignKey('characters.id'), primary_key=True),
    Column('feature_id', UUID(as_uuid=False), ForeignKey('features.id'), primary_key=True),
    Column('source', String(100)),  # class, race, background, etc.
    Column('level_gained', Integer, default=1)
)

character_items = Table(
    'character_items',
    BaseModel.metadata,
    Column('character_id', UUID(as_uuid=False), ForeignKey('characters.id'), primary_key=True),
    Column('item_id', UUID(as_uuid=False), ForeignKey('items.id'), primary_key=True),
    Column('quantity', Integer, default=1),
    Column('equipped', Boolean, default=False),
    Column('location', String(100))  # backpack, equipped, etc.
)


class Character(BaseModel, SoftDeleteMixin, VersionedMixin):
    """Character model representing a D&D character."""
    
    __tablename__ = "characters"
    
    # Basic character information
    character_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    player_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Character level and experience
    level: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    experience_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    experience_to_next_level: Mapped[int] = mapped_column(Integer, default=300, nullable=False)
    
    # Core attributes
    strength: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    dexterity: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    constitution: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    intelligence: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    wisdom: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    charisma: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    
    # Ability score modifiers (calculated)
    strength_modifier: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    dexterity_modifier: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    constitution_modifier: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    intelligence_modifier: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    wisdom_modifier: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    charisma_modifier: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Character details
    race: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    subrace: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    character_class: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    subclass: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    background: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Hit points and combat
    max_hit_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    current_hit_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    temporary_hit_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    hit_dice: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    hit_dice_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Armor class and initiative
    armor_class: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    initiative_bonus: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    speed: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    
    # Proficiencies
    proficiency_bonus: Mapped[int] = mapped_column(Integer, default=2, nullable=False)
    saving_throw_proficiencies: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    skill_proficiencies: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    weapon_proficiencies: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    armor_proficiencies: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    
    # Skills (calculated from abilities + proficiencies)
    skills: Mapped[Optional[Dict[str, int]]] = mapped_column(JSON, nullable=True)
    
    # Spellcasting
    spellcasting_ability: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    spell_save_dc: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    spell_attack_bonus: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Equipment and wealth
    copper_pieces: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    silver_pieces: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    electrum_pieces: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    gold_pieces: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    platinum_pieces: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Character appearance and personality
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    height: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    weight: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    eyes: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    skin: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    hair: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Personality traits
    personality_traits: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    ideals: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    bonds: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    flaws: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    
    # Character notes and backstory
    backstory: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    allies_and_organizations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    character_appearance: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    additional_features_and_traits: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Game mechanics
    inspiration: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    exhaustion_level: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Ruleset and validation
    ruleset_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False), ForeignKey('rulesets.id'), nullable=True)
    is_valid: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    validation_errors: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    
    # Relationships
    spells = relationship("Spell", secondary=character_spells, back_populates="characters")
    features = relationship("Feature", secondary=character_features, back_populates="characters")
    items = relationship("Item", secondary=character_items, back_populates="characters")
    
    def __post_init__(self):
        """Calculate derived values after initialization."""
        self._calculate_ability_modifiers()
        self._calculate_skills()
        self._calculate_combat_values()
    
    def _calculate_ability_modifiers(self):
        """Calculate ability score modifiers."""
        self.strength_modifier = (self.strength - 10) // 2
        self.dexterity_modifier = (self.dexterity - 10) // 2
        self.constitution_modifier = (self.constitution - 10) // 2
        self.intelligence_modifier = (self.intelligence - 10) // 2
        self.wisdom_modifier = (self.wisdom - 10) // 2
        self.charisma_modifier = (self.charisma - 10) // 2
    
    def _calculate_skills(self):
        """Calculate skill modifiers based on abilities and proficiencies."""
        if not self.skill_proficiencies:
            self.skill_proficiencies = []
        
        self.skills = {
            "acrobatics": self.dexterity_modifier + (self.proficiency_bonus if "acrobatics" in self.skill_proficiencies else 0),
            "animal_handling": self.wisdom_modifier + (self.proficiency_bonus if "animal_handling" in self.skill_proficiencies else 0),
            "arcana": self.intelligence_modifier + (self.proficiency_bonus if "arcana" in self.skill_proficiencies else 0),
            "athletics": self.strength_modifier + (self.proficiency_bonus if "athletics" in self.skill_proficiencies else 0),
            "deception": self.charisma_modifier + (self.proficiency_bonus if "deception" in self.skill_proficiencies else 0),
            "history": self.intelligence_modifier + (self.proficiency_bonus if "history" in self.skill_proficiencies else 0),
            "insight": self.wisdom_modifier + (self.proficiency_bonus if "insight" in self.skill_proficiencies else 0),
            "intimidation": self.charisma_modifier + (self.proficiency_bonus if "intimidation" in self.skill_proficiencies else 0),
            "investigation": self.intelligence_modifier + (self.proficiency_bonus if "investigation" in self.skill_proficiencies else 0),
            "medicine": self.wisdom_modifier + (self.proficiency_bonus if "medicine" in self.skill_proficiencies else 0),
            "nature": self.intelligence_modifier + (self.proficiency_bonus if "nature" in self.skill_proficiencies else 0),
            "perception": self.wisdom_modifier + (self.proficiency_bonus if "perception" in self.skill_proficiencies else 0),
            "performance": self.charisma_modifier + (self.proficiency_bonus if "performance" in self.skill_proficiencies else 0),
            "persuasion": self.charisma_modifier + (self.proficiency_bonus if "persuasion" in self.skill_proficiencies else 0),
            "religion": self.intelligence_modifier + (self.proficiency_bonus if "religion" in self.skill_proficiencies else 0),
            "sleight_of_hand": self.dexterity_modifier + (self.proficiency_bonus if "sleight_of_hand" in self.skill_proficiencies else 0),
            "stealth": self.dexterity_modifier + (self.proficiency_bonus if "stealth" in self.skill_proficiencies else 0),
            "survival": self.wisdom_modifier + (self.proficiency_bonus if "survival" in self.skill_proficiencies else 0)
        }
    
    def _calculate_combat_values(self):
        """Calculate combat-related values."""
        # Base armor class calculation (simplified)
        if self.dexterity_modifier > 0:
            self.armor_class = 10 + self.dexterity_modifier
        else:
            self.armor_class = 10
        
        # Initiative bonus
        self.initiative_bonus = self.dexterity_modifier
        
        # Spell save DC and attack bonus (if spellcasting)
        if self.spellcasting_ability:
            ability_modifier = getattr(self, f"{self.spellcasting_ability.lower()}_modifier", 0)
            self.spell_save_dc = 8 + self.proficiency_bonus + ability_modifier
            self.spell_attack_bonus = self.proficiency_bonus + ability_modifier
    
    def add_experience(self, xp: int) -> bool:
        """Add experience points and check for level up."""
        self.experience_points += xp
        
        # Check if character should level up
        if self.experience_points >= self.experience_to_next_level:
            self.level_up()
            return True
        return False
    
    def level_up(self):
        """Increase character level and recalculate values."""
        self.level += 1
        
        # Update proficiency bonus
        self.proficiency_bonus = 2 + ((self.level - 1) // 4)
        
        # Recalculate derived values
        self._calculate_skills()
        self._calculate_combat_values()
        
        # Update version
        self.increment_version("minor")
    
    def get_total_wealth(self) -> Dict[str, int]:
        """Get total wealth in all currency types."""
        return {
            "copper": self.copper_pieces,
            "silver": self.silver_pieces,
            "electrum": self.electrum_pieces,
            "gold": self.gold_pieces,
            "platinum": self.platinum_pieces
        }
    
    def get_ability_modifier(self, ability: str) -> int:
        """Get modifier for a specific ability score."""
        ability_map = {
            "strength": self.strength_modifier,
            "dexterity": self.dexterity_modifier,
            "constitution": self.constitution_modifier,
            "intelligence": self.intelligence_modifier,
            "wisdom": self.wisdom_modifier,
            "charisma": self.charisma_modifier
        }
        return ability_map.get(ability.lower(), 0)
    
    def get_skill_modifier(self, skill: str) -> int:
        """Get modifier for a specific skill."""
        return self.skills.get(skill.lower(), 0) if self.skills else 0
    
    def is_proficient_in_saving_throw(self, ability: str) -> bool:
        """Check if character is proficient in a saving throw."""
        if not self.saving_throw_proficiencies:
            return False
        return ability.lower() in [prof.lower() for prof in self.saving_throw_proficiencies]
    
    def get_saving_throw_modifier(self, ability: str) -> int:
        """Get saving throw modifier for a specific ability."""
        base_modifier = self.get_ability_modifier(ability)
        if self.is_proficient_in_saving_throw(ability):
            base_modifier += self.proficiency_bonus
        return base_modifier
