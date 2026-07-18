# repositories.py
# Data Access Layer - handles reading from files (CSV for rules) and Supabase (for persistent characters).

import os
import pandas as pd
import streamlit as st
from supabase import create_client, Client

class GameRepository:
    def get_default_sheet_data(self) -> dict:
        return {
            "traits": {
                "positive_trait": "",
                "negative_trait": "",
                "flair": "",
                "adventuring_goal": "",
                "appearance": "",
                "hgt_wgt_age": ""
            },
            "money": {
                "gold": 0,
                "silver": 0
            },
            "weapons": [
                {"sk": False, "m_h_s": "M", "name": "", "atk": "", "dmg": "", "max_block": ""},
                {"sk": False, "m_h_s": "M", "name": "", "atk": "", "dmg": "", "max_block": ""},
                {"sk": False, "m_h_s": "M", "name": "", "atk": "", "dmg": "", "max_block": ""},
                {"sk": False, "m_h_s": "M", "name": "", "atk": "", "dmg": "", "max_block": ""},
                {"sk": False, "m_h_s": "M", "name": "", "atk": "", "dmg": "", "max_block": ""}
            ],
            "armor_shield": {
                "armor_name": "",
                "armor_def": "",
                "armor_ar": "",
                "shield_name": "",
                "shield_max_block": "",
                "block_active": "",
                "dodge_active": ""
            },
            "powers": [
                {"select": False, "usage": "", "action": "", "name": "", "effect": ""},
                {"select": False, "usage": "", "action": "", "name": "", "effect": ""},
                {"select": False, "usage": "", "action": "", "name": "", "effect": ""},
                {"select": False, "usage": "", "action": "", "name": "", "effect": ""},
                {"select": False, "usage": "", "action": "", "name": "", "effect": ""},
                {"select": False, "usage": "", "action": "", "name": "", "effect": ""},
                {"select": False, "usage": "", "action": "", "name": "", "effect": ""},
                {"select": False, "usage": "", "action": "", "name": "", "effect": ""},
                {"select": False, "usage": "", "action": "", "name": "", "effect": ""},
                {"select": False, "usage": "", "action": "", "name": "", "effect": ""}
            ],
            "magic_items": [
                {"select": False, "usage": "", "action": "", "name": "", "effect": ""},
                {"select": False, "usage": "", "action": "", "name": "", "effect": ""},
                {"select": False, "usage": "", "action": "", "name": "", "effect": ""},
                {"select": False, "usage": "", "action": "", "name": "", "effect": ""},
                {"select": False, "usage": "", "action": "", "name": "", "effect": ""}
            ],
            "notes": "",
            "vitals": {
                "max_hp": 10,
                "current_hp": 10,
                "wounds": 0,
                "mr_base": 0,
                "mr_armored": "",
                "mr_shield": ""
            }
        }

    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.classes_df = None
        self.abilities_df = None
        self.client = None
        
        # Initialize runtime-only sandbox memory block in Streamlit Session State as fallback
        if "player_character" not in st.session_state:
            st.session_state.player_character = {
                "name": "Blake",
                "class": None,
                "race": None,
                "hp": 10,
                "might": "d4",
                "motion": "d4",
                "mind": "d4",
                "magic": "d4",
                "moxie": "d4",
                "skills": [],
                "inventory": [],
                "log": [],
                "sheet_data": self.get_default_sheet_data()
            }
        
        # Try to connect to Supabase
        try:
            if "connections" in st.secrets and "supabase" in st.secrets["connections"]:
                url = st.secrets["connections"]["supabase"]["SUPABASE_URL"]
                key = st.secrets["connections"]["supabase"]["SUPABASE_KEY"]
                if url and key:
                    self.client = create_client(url, key)
        except Exception as e:
            # Silent fallback during initial runs when tables aren't ready
            pass

        self.load_static_data()

    def load_static_data(self):
        """Loads static rule CSV files if they exist."""
        classes_path = os.path.join(self.data_dir, "classes.csv")
        if not os.path.exists(classes_path):
            classes_path = os.path.join("OldFlexMoxieRaw", "FlexMoxie - Codex.csv") # fallback to Codex CSV we downloaded
            
        if os.path.exists(classes_path):
            try:
                self.classes_df = pd.read_csv(classes_path)
            except Exception:
                pass

    def get_class_details(self, class_name):
        """Returns details for a class name from static CSV data."""
        if self.classes_df is not None:
            try:
                matches = self.classes_df[self.classes_df['name'] == class_name].to_dict('records')
                if matches:
                    return matches[0]
            except Exception:
                pass
        return None

    def get_character(self, name: str) -> dict:
        """Fetches character from Supabase table. Falls back to session state."""
        if self.client:
            try:
                response = self.client.table("characters").select("*").eq("name", name).execute()
                if response.data:
                    char_data = response.data[0]
                    # Map database fields to standard schema
                    loaded_sheet_data = char_data.get("sheet_data")
                    sheet_data = self.get_default_sheet_data()
                    if isinstance(loaded_sheet_data, dict):
                        for k, v in loaded_sheet_data.items():
                            if isinstance(v, dict) and k in sheet_data:
                                sheet_data[k].update(v)
                            else:
                                sheet_data[k] = v
                    return {
                        "name": char_data.get("name"),
                        "class": char_data.get("class"),
                        "race": char_data.get("race"),
                        "hp": char_data.get("hp"),
                        "might": char_data.get("might") or "d4",
                        "motion": char_data.get("motion") or "d4",
                        "mind": char_data.get("mind") or "d4",
                        "magic": char_data.get("magic") or "d4",
                        "moxie": char_data.get("moxie") or "d4",
                        "skills": char_data.get("skills") or [],
                        "inventory": char_data.get("inventory", []),
                        "log": char_data.get("log", []),
                        "owner_email": char_data.get("owner_email"),
                        "sheet_data": sheet_data
                    }
            except Exception:
                pass
        return st.session_state.player_character

    def save_character(self, name: str, data: dict):
        """Saves character to Supabase table (upsert). Falls back to session state."""
        # Update local session state first
        if st.session_state.player_character.get("name") == name:
            st.session_state.player_character.update(data)
        
        if self.client:
            try:
                # Upsert record in Supabase
                # Parse hp, skills and inventory safely
                try:
                    hp_val = int(data.get("hp", 10))
                except (ValueError, TypeError):
                    hp_val = 10

                skills_val = data.get("skills")
                skills_list = list(skills_val) if isinstance(skills_val, list) else []

                inv_val = data.get("inventory")
                inv_list = list(inv_val) if isinstance(inv_val, list) else []

                db_data = {
                    "name": name,
                    "class": data.get("class"),
                    "race": data.get("race"),
                    "hp": hp_val,
                    "might": data.get("might") or "d4",
                    "motion": data.get("motion") or "d4",
                    "mind": data.get("mind") or "d4",
                    "magic": data.get("magic") or "d4",
                    "moxie": data.get("moxie") or "d4",
                    "skills": skills_list,
                    "inventory": inv_list,
                    "log": data.get("log", []),
                    "sheet_data": data.get("sheet_data") or self.get_default_sheet_data()
                }
                if "owner_email" in data:
                    db_data["owner_email"] = data["owner_email"]
                elif "player_email" in st.session_state:
                    db_data["owner_email"] = st.session_state.player_email

                # Check if record exists to decide insert vs update
                exists = self.client.table("characters").select("id").eq("name", name).execute()
                if exists.data:
                    self.client.table("characters").update(db_data).eq("name", name).execute()
                else:
                    self.client.table("characters").insert(db_data).execute()
                return True
            except Exception as e:
                st.error(f"⚠️ Supabase Save failed: {e}")
        return False

    def get_all_powers(self) -> list:
        """Fetches all powers from Supabase. Falls back to empty list."""
        if self.client:
            try:
                res = self.client.table("powers").select("*").order("name").execute()
                return res.data or []
            except Exception:
                pass
        return []

    def get_all_magic_items(self) -> list:
        """Fetches all magic items from Supabase. Falls back to empty list."""
        if self.client:
            try:
                res = self.client.table("magic_items").select("*").order("name").execute()
                return res.data or []
            except Exception:
                pass
        return []

    def get_all_skillsets(self) -> list:
        """Fetches all skillsets from Supabase. Falls back to empty list."""
        if self.client:
            try:
                res = self.client.table("skillsets").select("*").order("name").execute()
                return res.data or []
            except Exception:
                pass
        return []

    def create_player(self, email: str, first_name: str, last_name: str) -> bool:
        """Inserts a new player into the players table."""
        if self.client:
            try:
                self.client.table("players").insert({
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name
                }).execute()
                return True
            except Exception as e:
                st.error(f"⚠️ Failed to create player: {e}")
        return False

    def get_player(self, email: str) -> dict:
        """Retrieves player profile by email."""
        if self.client:
            try:
                res = self.client.table("players").select("*").eq("email", email).execute()
                return res.data[0] if res.data else None
            except Exception:
                pass
        return None

    def get_characters_by_owner(self, owner_email: str) -> list:
        """Fetches all characters owned by a specific email."""
        if self.client:
            try:
                res = self.client.table("characters").select("*").eq("owner_email", owner_email).execute()
                return res.data or []
            except Exception:
                pass
        # Fallback to session state if it matches the current email and offline
        if "player_email" in st.session_state and st.session_state.player_email == owner_email:
            return [st.session_state.player_character]
        return []

    def get_other_players(self, current_email: str) -> list:
        """Retrieves all players except the current logged-in one."""
        if self.client:
            try:
                res = self.client.table("players").select("*").neq("email", current_email).execute()
                return res.data or []
            except Exception:
                pass
        return []

    def character_exists(self, name: str) -> bool:
        """Checks if a character name already exists in Supabase."""
        if self.client:
            try:
                res = self.client.table("characters").select("id").eq("name", name).execute()
                return bool(res.data)
            except Exception:
                pass
        return False

    def create_character(self, name: str, owner_email: str) -> bool:
        """Initializes a new character for an owner."""
        default_data = {
            "owner_email": owner_email,
            "class": None,
            "race": None,
            "hp": 10,
            "might": "d4",
            "motion": "d4",
            "mind": "d4",
            "magic": "d4",
            "moxie": "d4",
            "skills": [],
            "inventory": [],
            "log": ["Character created."],
            "sheet_data": self.get_default_sheet_data()
        }
        return self.save_character(name, default_data)

