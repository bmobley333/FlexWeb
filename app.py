# app.py
# Streamlit UI Layer - purely visual dashboard.
# Captures player inputs, calls game_engine for logic, and displays states.

import streamlit as st
import pandas as pd
from repositories import GameRepository
from game_engine import GameEngine

@st.dialog("⚠️ Character Creation Error")
def show_error_dialog(message):
    st.markdown(f"**{message}**")
    if st.button("OK", key="close_dialog_btn", use_container_width=True):
        if "dialog_to_show" in st.session_state:
            del st.session_state.dialog_to_show
        st.rerun()

# Configure widescreen layout
st.set_page_config(
    page_title="FlexWeb Playtest Console",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    if "dialog_to_show" in st.session_state:
        show_error_dialog(st.session_state.dialog_to_show)

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
        /* Fix sidebar button contrast issues */
        section[data-testid="stSidebar"] button {
            background-color: #1e293b !important;
            border: 1px solid #334155 !important;
            color: #f8fafc !important;
            transition: background-color 0.2s ease, border-color 0.2s ease;
        }
        section[data-testid="stSidebar"] button:hover {
            background-color: #334155 !important;
            border-color: #475569 !important;
        }
        section[data-testid="stSidebar"] button p,
        section[data-testid="stSidebar"] button span {
            color: #f8fafc !important;
        }
        /* Fix sidebar expander header contrast issues */
        section[data-testid="stSidebar"] details[data-testid="stExpander"] summary {
            color: #0f172a !important;
        }
        section[data-testid="stSidebar"] details[data-testid="stExpander"] summary p,
        section[data-testid="stSidebar"] details[data-testid="stExpander"] summary span {
            color: #0f172a !important;
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
    if "player_email" not in st.session_state:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.subheader("👤 Playtest Account Access")
        email = st.text_input("Enter your playtest email:").strip().lower()
        
        if email:
            player = repo.get_player(email)
            if player:
                st.session_state.player_email = email
                st.session_state.player_first = player["first_name"]
                st.session_state.player_last = player["last_name"]
                st.success(f"Welcome back, {player['first_name']}!")
                st.rerun()
            else:
                st.info("First-time login detected. Please create your profile:")
                first_name = st.text_input("First Name:")
                last_name = st.text_input("Last Name:")
                if st.button("Register & Log In 🚀"):
                    if first_name.strip() and last_name.strip():
                        repo.create_player(email, first_name.strip(), last_name.strip())
                        st.session_state.player_email = email
                        st.session_state.player_first = first_name.strip()
                        st.session_state.player_last = last_name.strip()
                        st.success("Profile created successfully!")
                        st.rerun()
                    else:
                        st.error("Please fill in both first and last name.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    st.sidebar.markdown(f"**Logged in as:**  \n{st.session_state.player_first} {st.session_state.player_last}  \n`({st.session_state.player_email})`")
    if st.sidebar.button("Logout 🚪"):
        del st.session_state.player_email
        if "player_first" in st.session_state:
            del st.session_state.player_first
        if "player_last" in st.session_state:
            del st.session_state.player_last
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.subheader("👤 Your Characters")
    
    my_characters = repo.get_characters_by_owner(st.session_state.player_email)
    char_names = [c["name"] for c in my_characters]
    
    if not char_names:
        st.sidebar.warning("No characters found. Create one below to begin:")
        with st.sidebar.form("create_first_char_form", clear_on_submit=True):
            new_char_name = st.text_input("New Character Name:").strip()
            submitted = st.form_submit_button("Create Character 🛠️")
            if submitted:
                if not new_char_name:
                    st.session_state.dialog_to_show = "Character name cannot be blank."
                    st.rerun()
                elif repo.character_exists(new_char_name):
                    st.sidebar.error("Character name already taken.")
                else:
                    repo.create_character(new_char_name, st.session_state.player_email)
                    st.sidebar.success(f"Character '{new_char_name}' created!")
                    st.rerun()
        return

    if "active_char_name" not in st.session_state or st.session_state.active_char_name not in char_names:
        st.session_state.active_char_name = char_names[0]
        
    selected_char_name = st.sidebar.selectbox(
        "Select Active Character:",
        char_names,
        index=char_names.index(st.session_state.active_char_name)
    )
    st.session_state.active_char_name = selected_char_name
    
    with st.sidebar.expander("➕ Make New Character"):
        new_char_name = st.text_input("New Character Name:", key="new_char_input").strip()
        if st.button("Create Character 🛠️", key="create_new_char_btn"):
            if not new_char_name:
                st.session_state.dialog_to_show = "Character name cannot be blank."
                st.rerun()
            elif repo.character_exists(new_char_name):
                st.sidebar.error("Character name already taken.")
            else:
                repo.create_character(new_char_name, st.session_state.player_email)
                st.sidebar.success(f"Character '{new_char_name}' created!")
                st.rerun()

    player_name = selected_char_name
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
    tab_char, tab_rolls, tab_inv, tab_rules, tab_codex, tab_sharing = st.tabs([
        "🛡️ Character Sheet", 
        "🎲 Action Console", 
        "🧰 Inventory Editor",
        "📜 Adventure Logs",
        "📖 Codex Search",
        "👥 Player Directory"
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
        
        # Check for changes and auto-save
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
        
        # Compare key-by-key to avoid saving identical data
        has_changes = False
        for key, val in updated_data.items():
            if char_state.get(key) != val:
                has_changes = True
                break
                
        if has_changes:
            if repo.save_character(player_name, updated_data):
                st.toast("⚡ Changes saved automatically!")
                st.rerun()
            else:
                st.error("⚠️ Failed to auto-save character data.")
                
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
        
        # Clean up empty rows
        cleaned_inv = [item for item in edited_list if item.get("Item Name")]
        
        # Compare cleaned inventory with raw inventory to see if they differ
        raw_cleaned = [item for item in raw_inventory if item.get("Item Name")]
        
        if cleaned_inv != raw_cleaned:
            if repo.save_character(player_name, {"inventory": cleaned_inv}):
                st.toast("⚡ Inventory saved automatically!")
                st.rerun()
            else:
                st.error("⚠️ Failed to auto-save inventory.")
                
        st.metric("Total Weight Encumbrance (lbs)", f"{total_weight} lbs")
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

    # --- TAB 5: CODEX SEARCH ---
    with tab_codex:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.subheader("Rules & Abilities Reference")
        
        db_choice = st.radio(
            "Select Rules Matrix to Search:",
            ["Powers ⚡", "Magic Items 🍺", "SkillSets 🎓"],
            horizontal=True
        )
        
        if db_choice == "Powers ⚡":
            if powers:
                df_powers = pd.DataFrame(powers)
                cols_to_show = ["name", "sub", "table_name", "usage", "action", "effect", "source", "dropdown"]
                cols_present = [c for c in cols_to_show if c in df_powers.columns]
                st.dataframe(df_powers[cols_present], use_container_width=True)
            else:
                st.info("No powers found in database.")
                
        elif db_choice == "Magic Items 🍺":
            if magic_items:
                df_items = pd.DataFrame(magic_items)
                cols_to_show = ["name", "sub", "table_name", "usage", "action", "effect", "source", "dropdown"]
                cols_present = [c for c in cols_to_show if c in df_items.columns]
                st.dataframe(df_items[cols_present], use_container_width=True)
            else:
                st.info("No magic items found in database.")
                
        elif db_choice == "SkillSets 🎓":
            if skillsets:
                formatted_sets = []
                for s in skillsets:
                    skills_list = s.get("skills", [])
                    skills_str = ", ".join(skills_list) if isinstance(skills_list, list) else str(skills_list)
                    
                    row_data = {
                        "Name": s.get("name"),
                        "Included Skills": skills_str,
                        "Source": s.get("source")
                    }
                    if "sub" in s:
                        row_data["Sub"] = s.get("sub")
                    if "table_name" in s:
                        row_data["Table Name"] = s.get("table_name")
                    if "dropdown" in s:
                        row_data["Dropdown"] = s.get("dropdown")
                        
                    formatted_sets.append(row_data)
                st.dataframe(pd.DataFrame(formatted_sets), use_container_width=True)
            else:
                st.info("No skillsets found in database.")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- TAB 6: PLAYER DIRECTORY & SHARING ---
    with tab_sharing:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.subheader("Explore Other Players' Characters")
        
        other_players = repo.get_other_players(st.session_state.player_email)
        if not other_players:
            st.info("No other registered players found in this playtest yet.")
        else:
            player_options = {f"{p['first_name']} {p['last_name']} ({p['email']})": p['email'] for p in other_players}
            selected_player_label = st.selectbox("Select Player:", list(player_options.keys()))
            
            if selected_player_label:
                target_email = player_options[selected_player_label]
                peer_chars = repo.get_characters_by_owner(target_email)
                
                if not peer_chars:
                    st.info("This player has not created any characters yet.")
                else:
                    peer_char_name = st.selectbox("Select Character to View/Clone:", [c["name"] for c in peer_chars])
                    # Find character data
                    peer_char_data = next((c for c in peer_chars if c["name"] == peer_char_name), None)
                    
                    if peer_char_data:
                        col_view1, col_view2 = st.columns(2)
                        with col_view1:
                            st.markdown(f"### 🛡️ {peer_char_data['name']}")
                            st.markdown(f"**Class:** {peer_char_data.get('class') or 'None'}")
                            st.markdown(f"**Race:** {peer_char_data.get('race') or 'None'}")
                            st.markdown(f"**HP:** {peer_char_data.get('hp', 10)}")
                            st.markdown("**Skills:**")
                            st.write(peer_char_data.get("skills") or [])
                        with col_view2:
                            st.markdown("### 📊 Attributes")
                            st.metric("Might 💪", (peer_char_data.get("might") or "d4").upper())
                            st.metric("Motion 🏃", (peer_char_data.get("motion") or "d4").upper())
                            st.metric("Mind 👁️", (peer_char_data.get("mind") or "d4").upper())
                            st.metric("Magic ✨", (peer_char_data.get("magic") or "d4").upper())
                            st.metric("Moxie 🫀", (peer_char_data.get("moxie") or "d4").upper())
                        
                        st.markdown("---")
                        # Inventory View (Read Only)
                        st.markdown("### 🧰 Inventory (Read Only)")
                        peer_inv = peer_char_data.get("inventory", [])
                        if peer_inv:
                            st.dataframe(pd.DataFrame(peer_inv), use_container_width=True)
                        else:
                            st.write("Inventory is empty.")
                        
                        st.markdown("---")
                        # Clone action
                        if st.button("📋 Clone Character to My Account"):
                            clone_name = f"{peer_char_name} (Copy)"
                            suffix = 1
                            while repo.character_exists(clone_name):
                                clone_name = f"{peer_char_name} (Copy {suffix})"
                                suffix += 1
                            
                            cloned_data = peer_char_data.copy()
                            cloned_data["name"] = clone_name
                            cloned_data["owner_email"] = st.session_state.player_email
                            
                            # Remove the database ID if present to avoid unique constraint clash on insert
                            if "id" in cloned_data:
                                del cloned_data["id"]
                                
                            if repo.save_character(clone_name, cloned_data):
                                st.success(f"Successfully cloned '{peer_char_name}' as '{clone_name}'!")
                                st.rerun()
                            else:
                                st.error("Failed to clone character.")
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

