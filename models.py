# models.py
# Schema & Data Models Layer - holds pure data structures/schemas.

from typing import List, Dict, Optional
from dataclasses import dataclass, field

@dataclass
class AbilityDefinition:
    name: str
    description: str
    cooldown: int = 0

@dataclass
class CharacterSchema:
    name: str
    character_class: str
    race: str
    hit_points: int
    abilities: List[AbilityDefinition] = field(default_factory=list)
