# app.py
# Streamlit UI Layer - purely visual dashboard.
# Captures player inputs, calls game_engine for logic, and displays states.

import streamlit as st
import pandas as pd
from repositories import GameRepository
from game_engine import GameEngine

# Configure widescreen layout
st.set_page_config(
    page_title="FlexWeb Playtest Console",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🌌 FlexWeb Playtest Console")
    st.write("Welcome to the Chromebook-compatible S-Tier rule sandbox.")
    
    # Initialize repository
    repo = GameRepository()
    
    # Sidebar
    with st.sidebar:
        st.header("Character Metrics")
        if st.session_state.player_character["class"]:
            st.metric("Class", st.session_state.player_character["class"])
            st.metric("HP", st.session_state.player_character["hp"])
        else:
            st.write("No character loaded.")
            
    # Main Tabs
    tab1, tab2 = st.tabs(["Dashboard", "Rules & Logs"])
    with tab1:
        st.subheader("Console Actions")
        if st.button("Roll Test Dice"):
            result = GameEngine.roll_dice(20)
            st.session_state.player_character["log"].append(f"Rolled d20: {result}")
            st.success(f"You rolled: {result}")
            
    with tab2:
        st.subheader("Action History Log")
        for log_entry in reversed(st.session_state.player_character["log"]):
            st.text(log_entry)

if __name__ == "__main__":
    main()
