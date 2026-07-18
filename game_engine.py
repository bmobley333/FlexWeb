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

    @staticmethod
    def parse_skill_name_and_count(skill_str: str) -> tuple:
        """Parses a skill string like '2_Melee 💪' or 'Melee 💪' into (base_name, count)."""
        skill_str = skill_str.strip()
        if not skill_str:
            return "", 0
        match = re.match(r'^(\d+)_(.+)$', skill_str)
        if match:
            return match.group(2).strip(), int(match.group(1))
        return skill_str, 1

    @staticmethod
    def format_skill_string(base_name: str, count: int) -> str:
        """Formats base_name and count into 'count_base_name' or 'base_name' if count <= 1."""
        if count > 1:
            return f"{count}_{base_name}"
        return base_name

    @staticmethod
    def update_skills_list(current_skills: list, remove_skills: list, add_skills: list) -> list:
        """
        Updates the character's skill list by removing a list of skills and adding another list.
        Cleanly handles count increments (e.g., '2_Melee 💪') just like the Apps Script.
        """
        # Parse current skills into a dict: base_name -> count
        skills_dict = {}
        for s in current_skills:
            base, count = GameEngine.parse_skill_name_and_count(s)
            if base:
                skills_dict[base] = skills_dict.get(base, 0) + count

        # Process removals
        for s in remove_skills:
            base, count_to_remove = GameEngine.parse_skill_name_and_count(s)
            if base in skills_dict:
                skills_dict[base] -= count_to_remove
                if skills_dict[base] <= 0:
                    del skills_dict[base]

        # Process additions
        for s in add_skills:
            base, count_to_add = GameEngine.parse_skill_name_and_count(s)
            if base:
                skills_dict[base] = skills_dict.get(base, 0) + count_to_add

        # Re-serialize to list of formatted strings
        updated_skills = []
        for base, count in skills_dict.items():
            updated_skills.append(GameEngine.format_skill_string(base, count))
        return sorted(updated_skills)

    @staticmethod
    def update_power_or_item_slot(slot: dict, selected_name: str, db_items: list) -> dict:
        """
        Looks up selected_name in db_items list (from Supabase) and populates 
        usage, action, name, and effect in the slot dict. Clears the slot if empty.
        """
        # Clear slot first
        updated_slot = {
            "select": slot.get("select", False),
            "usage": "",
            "action": "",
            "name": "",
            "effect": ""
        }
        if selected_name:
            # Check by dropdown first, then by name
            match = next((item for item in db_items if item.get("dropdown") == selected_name), None)
            if not match:
                match = next((item for item in db_items if item.get("name") == selected_name), None)
            
            if match:
                updated_slot["name"] = match.get("name") or ""
                updated_slot["usage"] = match.get("usage") or ""
                updated_slot["action"] = match.get("action") or ""
                updated_slot["effect"] = match.get("effect") or ""
        return updated_slot

