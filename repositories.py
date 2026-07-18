# repositories.py
# Data Access Layer - handles reading from files (currently CSV, swappable for Supabase).

import os
import pandas as pd
import streamlit as st

# Initialize runtime-only sandbox memory block in Streamlit Session State
if "player_character" not in st.session_state:
    st.session_state.player_character = {
        "class": None,
        "race": None,
        "hp": 10,
        "log": []
    }

class GameRepository:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.classes_df = None
        self.abilities_df = None
        self.load_data()

    def load_data(self):
        """Loads CSV data files if they exist."""
        classes_path = os.path.join(self.data_dir, "classes.csv")
        abilities_path = os.path.join(self.data_dir, "abilities.csv")
        
        if os.path.exists(classes_path):
            self.classes_df = pd.read_csv(classes_path)
        if os.path.exists(abilities_path):
            self.abilities_df = pd.read_csv(abilities_path)

    def get_class_details(self, class_name):
        """Returns details for a class name."""
        if self.classes_df is not None:
            matches = self.classes_df[self.classes_df['name'] == class_name].to_dict('records')
            if matches:
                return matches[0]
        return None
