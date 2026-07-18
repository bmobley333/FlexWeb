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
    # Initialize repository
    repo = GameRepository()
    
    # --- 1. Dyslexia-Friendly Spacing / View Mode Settings ---
    if "view_mode" not in st.session_state:
        st.session_state.view_mode = False # False = Compact, True = Expanded
        
    st.sidebar.header("⚙️ Interface Settings")
    
    col_left, col_toggle, col_right = st.sidebar.columns([3, 2, 3])
    
    with col_toggle:
        # Streamlit toggle switch
        view_mode = st.toggle("view_toggle", value=st.session_state.view_mode, label_visibility="collapsed")
        st.session_state.view_mode = view_mode
        
    with col_left:
        opacity = "1.0" if not view_mode else "0.4"
        st.markdown(f"<div style='text-align: right; font-weight: bold; color: #f8fafc; opacity: {opacity}; transition: opacity 0.3s;'>Compact</div>", unsafe_allow_html=True)
        
    with col_right:
        opacity = "1.0" if view_mode else "0.4"
        st.markdown(f"<div style='text-align: left; font-weight: bold; color: #f8fafc; opacity: {opacity}; transition: opacity 0.3s;'>Expanded</div>", unsafe_allow_html=True)

    # Dynamic Spacing CSS Injection
    if not view_mode:
        st.markdown("""
            <style>
            div[data-testid="stVerticalBlock"] > div {
                padding-top: 0.1rem !important;
                padding-bottom: 0.1rem !important;
            }
            .block-container {
                padding-top: 2rem !important;
                padding-bottom: 2rem !important;
            }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            div[data-testid="stVerticalBlock"] > div {
                padding-top: 0.8rem !important;
                padding-bottom: 0.8rem !important;
            }
            .block-container {
                padding-top: 4rem !important;
                padding-bottom: 4rem !important;
            }
            </style>
        """, unsafe_allow_html=True)

    # Premium Glassmorphic Styles
    st.markdown("""
        <style>
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #0f162a !important;
            border-right: 1px solid #1e293b;
        }
        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3, 
        section[data-testid="stSidebar"] h4, 
        section[data-testid="stSidebar"] h5, 
        section[data-testid="stSidebar"] h6,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] div[data-testid="stMetricLabel"] p,
        section[data-testid="stSidebar"] div[data-testid="stMetricValue"] div,
        section[data-testid="stSidebar"] div[data-testid="stMetricValue"] span,
        section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p {
            color: #f8fafc !important;
        }
        section[data-testid="stSidebar"] input {
            color: #0f172a !important;
            background-color: #ffffff !important;
        }
        /* Dashboard Container styling */
        .glass-panel {
            background: rgba(30, 41, 59, 0.4);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🌌 FlexWeb Playtest Console")
    st.write("Welcome to the Chromebook-compatible S-Tier rules sandbox.")

    # --- 2. Player Login / Selection ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("👤 Player Identity")
    player_name = st.sidebar.text_input("Enter Character Name:", value="Blake").strip()
    
    if not player_name:
        st.warning("Please enter a character name to begin.")
        return
        
    # Fetch active character state from Supabase
    char_state = repo.get_character(player_name)
    
    # --- 3. Sidebar Biometrics & Stats Display ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Active Biometrics")
    
    col_bio1, col_bio2 = st.sidebar.columns(2)
    with col_bio1:
        st.metric("Class", char_state.get("class") or "None")
        st.metric("Hit Points (HP)", char_state.get("hp", 10))
    with col_bio2:
        st.metric("Race", char_state.get("race") or "None")
        
    st.sidebar.markdown("**Core Attribute dice**")
    col_atr1, col_atr2 = st.sidebar.columns(2)
    with col_atr1:
        st.metric("Might 💪", char_state.get("might", "d4").upper())
        st.metric("Motion 🏃", char_state.get("motion", "d4").upper())
        st.metric("Mind 👁️", char_state.get("mind", "d4").upper())
    with col_atr2:
        st.metric("Magic ✨", char_state.get("magic", "d4").upper())
        st.metric("Moxie 🫀", char_state.get("moxie", "d4").upper())

    # Load dynamic options from Supabase
    powers = repo.get_all_powers()
    magic_items = repo.get_all_magic_items()
    skillsets = repo.get_all_skillsets()

    # Extract all possible skills for multiselect
    all_possible_skills = set()
    for s in skillsets:
        skills_list = s.get("skills", [])
        if isinstance(skills_list, list):
            all_possible_skills.update(skills_list)
        elif isinstance(skills_list, str):
            all_possible_skills.update([item.strip() for item in skills_list.split(",") if item.strip()])
    
    all_possible_skills = sorted(list(all_possible_skills))

    # --- 4. Main Dashboard Tabs ---
    tab_char, tab_rolls, tab_inv, tab_rules = st.tabs([
        "🛡️ Character Sheet", 
        "🎲 Action Console", 
        "🧰 Inventory Editor",
        "📜 Adventure Logs"
    ])
    
    # --- TAB 1: CHARACTER SHEET EDITOR ---
    with tab_char:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.subheader("Edit Character Traits & Stats")
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            new_class = st.text_input("Class:", value=char_state.get("class") or "")
            new_race = st.text_input("Race:", value=char_state.get("race") or "")
            new_hp = st.number_input("Hit Points (HP):", min_value=1, max_value=200, value=char_state.get("hp", 10))
            
        with col_c2:
            st.markdown("**Attribute Dice Ratings (d4 - d12)**")
            ratings = ["d4", "d6", "d8", "d10", "d12"]
            new_might = st.selectbox("Might 💪 Rating:", ratings, index=ratings.index(char_state.get("might", "d4")))
            new_motion = st.selectbox("Motion 🏃 Rating:", ratings, index=ratings.index(char_state.get("motion", "d4")))
            new_mind = st.selectbox("Mind 👁️ Rating:", ratings, index=ratings.index(char_state.get("mind", "d4")))
            new_magic = st.selectbox("Magic ✨ Rating:", ratings, index=ratings.index(char_state.get("magic", "d4")))
            new_moxie = st.selectbox("Moxie 🫀 Rating:", ratings, index=ratings.index(char_state.get("moxie", "d4")))
            
        st.markdown("---")
        st.subheader("Skills & Core Proficiencies")
        
        # Populate skillset selector
        skillset_names = ["Custom / None"] + [s["name"] for s in skillsets]
        selected_set = st.selectbox("Apply Predefined Skillset Package:", skillset_names)
        
        current_skills = char_state.get("skills", [])
        if selected_set != "Custom / None":
            # Auto-load skillset skills
            set_data = next((s for s in skillsets if s["name"] == selected_set), None)
            if set_data:
                # Merge skills
                set_skills = set_data.get("skills", [])
                current_skills = list(set(current_skills + set_skills))
                
        new_skills = st.multiselect(
            "Active Character Skills:",
            options=all_possible_skills + current_skills,
            default=current_skills
        )
        
        if st.button("Save Character Sheet 💾"):
            updated_data = {
                "class": new_class.strip() or None,
                "race": new_race.strip() or None,
                "hp": int(new_hp),
                "might": new_might,
                "motion": new_motion,
                "mind": new_mind,
                "magic": new_magic,
                "moxie": new_moxie,
                "skills": new_skills
            }
            if repo.save_character(player_name, updated_data):
                st.success("Character sheet synced to Supabase database!")
                st.rerun()
            else:
                st.info("Character state saved locally (offline fallback).")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # --- TAB 2: ACTION & ROLL CONSOLE ---
    with tab_rolls:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.subheader("Dice Rolling Mechanics")
        
        # Set up roll options
        col_opt1, col_opt2, col_opt3 = st.columns(3)
        with col_opt1:
            skilled = st.checkbox("🎓 Skilled check (Roll 2d20 instead of 1d20)")
        with col_opt2:
            roll_mode = st.selectbox("Roll Modifier:", ["Normal", "Advantage (Keep Highest)", "Disadvantage (Keep Lowest)"])
        with col_opt3:
            bonus = st.number_input("Roll Bonus:", min_value=-10, max_value=10, value=0)
            
        adv = (roll_mode == "Advantage (Keep Highest)")
        dis = (roll_mode == "Disadvantage (Keep Lowest)")
        
        st.markdown("---")
        st.write("Click an attribute button below to roll its designated die rating:")
        
        # Quick Roll Buttons
        col_r1, col_r2, col_r3, col_r4, col_r5 = st.columns(5)
        roll_trigger = None
        roll_attribute = None
        roll_die = None
        
        with col_r1:
            might_die = char_state.get("might", "d4")
            if st.button(f"Might ({might_die.upper()}) 💪"):
                roll_trigger = True
                roll_attribute = "Might"
                roll_die = might_die
        with col_r2:
            motion_die = char_state.get("motion", "d4")
            if st.button(f"Motion ({motion_die.upper()}) 🏃"):
                roll_trigger = True
                roll_attribute = "Motion"
                roll_die = motion_die
        with col_r3:
            mind_die = char_state.get("mind", "d4")
            if st.button(f"Mind ({mind_die.upper()}) 👁️"):
                roll_trigger = True
                roll_attribute = "Mind"
                roll_die = mind_die
        with col_r4:
            magic_die = char_state.get("magic", "d4")
            if st.button(f"Magic ({magic_die.upper()}) ✨"):
                roll_trigger = True
                roll_attribute = "Magic"
                roll_die = magic_die
        with col_r5:
            moxie_die = char_state.get("moxie", "d4")
            if st.button(f"Moxie ({moxie_die.upper()}) 🫀"):
                roll_trigger = True
                roll_attribute = "Moxie"
                roll_die = moxie_die
                
        # Raw d20 Roll
        if st.button("Raw d20 Roll 🎲"):
            roll_trigger = True
            roll_attribute = "Raw d20"
            roll_die = "d0" # 0 attribute sides, just d20 roll

        if roll_trigger:
            with st.spinner("Rolling..."):
                if roll_die == "d0":
                    # Simple d20 roll
                    d20_roll = GameEngine.roll_dice(20)
                    result_str = f"Rolled raw d20: {d20_roll} + {bonus} = {d20_roll + bonus}"
                    if d20_roll == 20:
                        result_str += " (🌟 Tremendous!)"
                    elif d20_roll == 1:
                        result_str += " (💀 Critical!)"
                else:
                    # FlexMoxie cinematic check
                    res = GameEngine.roll_ability_check(skilled, roll_die, bonus, adv, dis)
                    # Construct result text
                    mode_str = f"({roll_mode})" if roll_mode != "Normal" else ""
                    skill_str = "Skilled" if skilled else "Unskilled"
                    rolls_formatted = ", ".join(map(str, res["rolls"]))
                    
                    result_str = (
                        f"Rolled {roll_attribute} check {mode_str} ({skill_str}): "
                        f"[{rolls_formatted}] ➡ kept {res['kept_d20']}; "
                        f"rolled {res['atr_roll']} on {res['atr_die']}; "
                        f"+{res['bonus']} bonus. "
                        f"Total = {res['total']}."
                    )
                    if res["tremendous_count"] > 0:
                        result_str += f" ({res['narrative']})"
                    elif res["critical_count"] > 0:
                        result_str += f" ({res['narrative']})"

                st.info(result_str)
                
                # Append log and save
                current_logs = char_state.get("log", [])
                current_logs.append(result_str)
                repo.save_character(player_name, {"log": current_logs})
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # --- TAB 3: INVENTORY GRID EDITOR ---
    with tab_inv:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.subheader("Manage Character Inventory")
        
        # Load inventory
        raw_inventory = char_state.get("inventory", [])
        if not raw_inventory:
            raw_inventory = [{"Item Name": "", "Weight (lbs)": 0.0, "Quantity": 1}]
            
        df_inv = pd.DataFrame(raw_inventory)
        
        # Grid columns configuration
        edited_df = st.data_editor(
            df_inv,
            num_rows="dynamic",
            column_config={
                "Item Name": st.column_config.TextColumn("Item Name", width="medium"),
                "Weight (lbs)": st.column_config.NumberColumn("Weight (lbs)", min_value=0.0, max_value=200.0, format="%.2f"),
                "Quantity": st.column_config.NumberColumn("Quantity", min_value=0, max_value=100)
            },
            use_container_width=True
        )
        
        # Auto-calculate encumbrance weight
        edited_list = edited_df.to_dict("records")
        total_weight = GameEngine.calculate_encumbrance(edited_list)
        
        col_weight, col_save = st.columns([4, 1])
        with col_weight:
            st.metric("Total Weight Encumbrance (lbs)", f"{total_weight} lbs")
            
        with col_save:
            if st.button("Save Inventory 💾"):
                # Clean up empty rows
                cleaned_inv = [item for item in edited_list if item.get("Item Name")]
                if repo.save_character(player_name, {"inventory": cleaned_inv}):
                    st.success("Inventory synced to Supabase database!")
                    st.rerun()
                else:
                    st.error("Failed to save inventory.")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- TAB 4: ADVENTURE & ACTION LOGS ---
    with tab_rules:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        
        col_log_h, col_log_btn = st.columns([4, 1])
        with col_log_h:
            st.subheader("Scrolling Action Log")
        with col_log_btn:
            if st.button("Clear Log 🧹"):
                # Rollback/Confirmation done via explicit state change or rerun
                if repo.save_character(player_name, {"log": []}):
                    st.success("Adventure logs cleared!")
                    st.rerun()
                    
        logs = char_state.get("log", [])
        if not logs:
            st.info("No logs recorded yet. Roll some dice in the Action Console!")
        else:
            for log_entry in reversed(logs):
                st.text(log_entry)
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

