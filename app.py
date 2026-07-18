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
    st.write("Welcome to the Chromebook-compatible S-Tier rules sandbox.")
    
    # Initialize repository
    repo = GameRepository()
    
    # 1. Player Login / Selection
    st.sidebar.header("👤 Player Identity")
    player_name = st.sidebar.text_input("Enter Character Name:", value="Blake").strip()
    
    if not player_name:
        st.warning("Please enter a character name to begin.")
        return
        
    # Fetch active character state
    char_state = repo.get_character(player_name)
    
    # 2. Sidebar Metrics
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Active Biometrics")
    st.sidebar.metric("Name", player_name)
    st.sidebar.metric("Class", char_state.get("class") or "None")
    st.sidebar.metric("Race", char_state.get("race") or "None")
    st.sidebar.metric("Hit Points (HP)", char_state.get("hp", 10))

    # 3. Main Dashboard Panels
    tab1, tab2, tab3 = st.tabs(["🛡️ Character Dashboard", "🎲 Action Console", "📜 Adventure Logs"])
    
    with tab1:
        st.subheader("Edit Character Sheet")
        col1, col2 = st.columns(2)
        
        with col1:
            new_class = st.text_input("Class:", value=char_state.get("class") or "")
            new_race = st.text_input("Race:", value=char_state.get("race") or "")
        
        with col2:
            new_hp = st.number_input("Hit Points (HP):", min_value=1, max_value=200, value=char_state.get("hp", 10))
            
        if st.button("Save Character Sheet 💾"):
            updated_data = {
                "class": new_class.strip() or None,
                "race": new_race.strip() or None,
                "hp": int(new_hp)
            }
            if repo.save_character(player_name, updated_data):
                st.success("Character sheet synced to Supabase database!")
                st.rerun()
            else:
                st.info("Character state saved locally (offline mode).")
                st.rerun()

    with tab2:
        st.subheader("Action & Dice Mechanics")
        sides = st.selectbox("Select Dice Type:", [4, 6, 8, 10, 12, 20, 100], index=5)
        
        if st.button(f"Roll d{sides} 🎲"):
            roll = GameEngine.roll_dice(sides)
            result_str = f"Rolled d{sides}: {roll}"
            st.success(result_str)
            
            # Append log and save
            current_logs = char_state.get("log", [])
            current_logs.append(result_str)
            repo.save_character(player_name, {"log": current_logs})
            st.rerun()

    with tab3:
        st.subheader("Scrolling Action Log")
        logs = char_state.get("log", [])
        if not logs:
            st.info("No logs recorded yet. Roll some dice in the Action Console!")
        else:
            for log_entry in reversed(logs):
                st.text(log_entry)

if __name__ == "__main__":
    main()
