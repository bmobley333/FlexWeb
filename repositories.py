# repositories.py
# Data Access Layer - handles reading from files (CSV for rules) and Supabase (for persistent characters).

import os
import pandas as pd
import streamlit as st
from supabase import create_client, Client

class GameRepository:
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
                "log": []
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
                        "log": char_data.get("log", [])
                    }
            except Exception:
                pass
        return st.session_state.player_character

    def save_character(self, name: str, data: dict):
        """Saves character to Supabase table (upsert). Falls back to session state."""
        # Update local session state first
        st.session_state.player_character.update(data)
        
        if self.client:
            try:
                # Upsert record in Supabase
                db_data = {
                    "name": name,
                    "class": data.get("class"),
                    "race": data.get("race"),
                    "hp": int(data.get("hp", 10)),
                    "might": data.get("might") or "d4",
                    "motion": data.get("motion") or "d4",
                    "mind": data.get("mind") or "d4",
                    "magic": data.get("magic") or "d4",
                    "moxie": data.get("moxie") or "d4",
                    "skills": data.get("skills") or [],
                    "inventory": data.get("inventory", []),
                    "log": data.get("log", [])
                }
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
