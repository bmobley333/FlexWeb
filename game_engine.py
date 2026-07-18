# game_engine.py
# Core Game Logic Layer - pure rules, calculations, and mechanics.
# Contains no UI code or direct data access calls.

import random
import re

class GameEngine:
    @staticmethod
    def roll_dice(sides: int) -> int:
        """Rolls a single dice with the specified number of sides."""
        if sides < 1:
            sides = 4
        return random.randint(1, sides)

    @staticmethod
    def parse_die_sides(die_str: str) -> int:
        """Parses a die string (e.g. 'd8', 'Might💪 d8') to get the number of sides."""
        if not die_str:
            return 4  # default to d4
        
        # Match digits after 'd' or 'd(digits)'
        match = re.search(r'd(\d+)', die_str.lower())
        if match:
            sides = int(match.group(1))
            # Enforce bounds [4, 12]
            if sides < 4:
                return 4
            if sides > 12:
                return 12
            return sides
        return 4

    @staticmethod
    def roll_ability_check(
        skilled: bool,
        attribute_die_str: str,
        bonus: int,
        advantage: bool = False,
        disadvantage: bool = False
    ) -> dict:
        """
        Executes a cinematic Ability Check / Roll according to FlexMoxie rules:
        #d20 + d(Atr) + Bonus
        """
        # Determine number and selection of d20s based on skill and adv/dis
        if advantage and disadvantage:
            # Cancel out
            advantage = False
            disadvantage = False

        d20_count = 1
        keep_mode = "highest" # "highest", "lowest", "single"

        if skilled:
            if advantage:
                d20_count = 3
                keep_mode = "highest"
            elif disadvantage:
                d20_count = 1
                keep_mode = "single"
            else:
                d20_count = 2
                keep_mode = "highest"
        else:
            if advantage:
                d20_count = 2
                keep_mode = "highest"
            elif disadvantage:
                d20_count = 2
                keep_mode = "lowest"
            else:
                d20_count = 1
                keep_mode = "single"

        # Roll the d20s
        d20_rolls = [random.randint(1, 20) for _ in range(d20_count)]
        
        if keep_mode == "highest":
            kept_d20 = max(d20_rolls)
        elif keep_mode == "lowest":
            kept_d20 = min(d20_rolls)
        else:
            kept_d20 = d20_rolls[0]

        # Roll the Attribute Die
        sides = GameEngine.parse_die_sides(attribute_die_str)
        atr_roll = random.randint(1, sides)

        # Calculate total
        total = kept_d20 + atr_roll + bonus

        # Count Tremendous (natural 20) and Critical (natural 1) on ANY of the rolled d20s
        tremendous_count = d20_rolls.count(20)
        critical_count = d20_rolls.count(1)

        # Format narrative result
        narrative = "Normal Success/Failure"
        if tremendous_count > 0:
            if tremendous_count == 3:
                narrative = "🌟🌟🌟 Triple Tremendous!"
            elif tremendous_count == 2:
                narrative = "🌟🌟 Double Tremendous!"
            else:
                narrative = "🌟 Tremendous!"
        elif critical_count > 0:
            if critical_count == 3:
                narrative = "💀💀💀 Triple Critical!"
            elif critical_count == 2:
                narrative = "💀💀 Double Critical!"
            else:
                narrative = "💀 Critical!"

        return {
            "rolls": d20_rolls,
            "kept_d20": kept_d20,
            "atr_die": f"d{sides}",
            "atr_roll": atr_roll,
            "bonus": bonus,
            "total": total,
            "tremendous_count": tremendous_count,
            "critical_count": critical_count,
            "narrative": narrative
        }

    @staticmethod
    def calculate_encumbrance(inventory: list) -> float:
        """Calculates total weight of character inventory."""
        total_weight = 0.0
        for item in inventory:
            if not isinstance(item, dict):
                continue
            
            # Extract values handle case-insensitively
            qty = 0
            weight = 0.0
            
            for k, v in item.items():
                k_lower = k.lower()
                if "qty" in k_lower or "quantity" in k_lower:
                    try:
                        qty = int(v)
                    except (ValueError, TypeError):
                        qty = 0
                elif "weight" in k_lower or "wt" in k_lower:
                    try:
                        weight = float(v)
                    except (ValueError, TypeError):
                        weight = 0.0
            
            total_weight += qty * weight
            
        return round(total_weight, 2)

