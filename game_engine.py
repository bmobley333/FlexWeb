# game_engine.py
# Core Game Logic Layer - pure rules, calculations, and mechanics.
# Contains no UI code or direct data access calls.

import random

class GameEngine:
    @staticmethod
    def roll_dice(sides: int) -> int:
        """Rolls a single dice with the specified number of sides."""
        return random.randint(1, sides)

    @staticmethod
    def calculate_modifier(score: int) -> int:
        """Calculates attribute modifier based on core score."""
        return (score - 10) // 2
