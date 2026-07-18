# app.py
# Streamlit UI Layer - purely visual dashboard.
# Captures player inputs, calls game_engine for logic, and displays states.

import streamlit as st
import pandas as pd
import importlib
import repositories
importlib.reload(repositories)
from repositories import GameRepository
import game_engine
importlib.reload(game_engine)
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
    
    # Render logo at top of left sidebar
    st.sidebar.image("logo.png")
    
    # Spacing CSS Injection (Locked to Compact Layout)
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
        /* Inline label styling for dense form layouts (2-column & 1-column) */
        div.stElementContainer:has(.inline-inputs) ~ div div[data-testid="stHorizontalBlock"]:not(:has(> div[data-testid="stColumn"]:nth-child(3))) div[data-testid="stTextInput"],
        div.stElementContainer:has(.inline-inputs) ~ div div[data-testid="stHorizontalBlock"]:not(:has(> div[data-testid="stColumn"]:nth-child(3))) div[data-testid="stNumberInput"],
        div.stElementContainer:has(.inline-inputs) ~ div div[data-testid="stHorizontalBlock"]:not(:has(> div[data-testid="stColumn"]:nth-child(3))) div[data-testid="stSelectbox"],
        div.stElementContainer:has(.inline-inputs) ~ div.stElementContainer > div[data-testid="stTextInput"] {
            display: flex !important;
            flex-direction: row !important;
            align-items: center !important;
            gap: 12px !important;
        }
        div.stElementContainer:has(.inline-inputs) ~ div div[data-testid="stHorizontalBlock"]:not(:has(> div[data-testid="stColumn"]:nth-child(3))) div[data-testid="stTextInput"] label,
        div.stElementContainer:has(.inline-inputs) ~ div div[data-testid="stHorizontalBlock"]:not(:has(> div[data-testid="stColumn"]:nth-child(3))) div[data-testid="stNumberInput"] label,
        div.stElementContainer:has(.inline-inputs) ~ div div[data-testid="stHorizontalBlock"]:not(:has(> div[data-testid="stColumn"]:nth-child(3))) div[data-testid="stSelectbox"] label,
        div.stElementContainer:has(.inline-inputs) ~ div.stElementContainer > div[data-testid="stTextInput"] label {
            min-width: 120px !important;
            margin-bottom: 0 !important;
            text-align: right !important;
            font-weight: 600 !important;
        }
        div.stElementContainer:has(.inline-inputs) ~ div div[data-testid="stHorizontalBlock"]:not(:has(> div[data-testid="stColumn"]:nth-child(3))) div[data-testid="stTextInput"] div[data-testid="stWidgetLabel"],
        div.stElementContainer:has(.inline-inputs) ~ div div[data-testid="stHorizontalBlock"]:not(:has(> div[data-testid="stColumn"]:nth-child(3))) div[data-testid="stNumberInput"] div[data-testid="stWidgetLabel"],
        div.stElementContainer:has(.inline-inputs) ~ div div[data-testid="stHorizontalBlock"]:not(:has(> div[data-testid="stColumn"]:nth-child(3))) div[data-testid="stSelectbox"] div[data-testid="stWidgetLabel"],
        div.stElementContainer:has(.inline-inputs) ~ div.stElementContainer > div[data-testid="stTextInput"] div[data-testid="stWidgetLabel"] {
            margin-bottom: 0 !important;
        }
        div.stElementContainer:has(.inline-inputs) ~ div div[data-testid="stHorizontalBlock"]:not(:has(> div[data-testid="stColumn"]:nth-child(3))) div[data-testid="stTextInput"] > div,
        div.stElementContainer:has(.inline-inputs) ~ div div[data-testid="stHorizontalBlock"]:not(:has(> div[data-testid="stColumn"]:nth-child(3))) div[data-testid="stNumberInput"] > div,
        div.stElementContainer:has(.inline-inputs) ~ div div[data-testid="stHorizontalBlock"]:not(:has(> div[data-testid="stColumn"]:nth-child(3))) div[data-testid="stSelectbox"] > div,
        div.stElementContainer:has(.inline-inputs) ~ div.stElementContainer > div[data-testid="stTextInput"] > div {
            flex-grow: 1 !important;
            min-width: 0 !important;
            width: 100% !important;
        }
        div.stElementContainer:has(.inline-inputs) ~ div div[data-testid="stHorizontalBlock"]:not(:has(> div[data-testid="stColumn"]:nth-child(3))) div[data-testid="stTextInput"] div[data-testid="stTextInputRootElement"],
        div.stElementContainer:has(.inline-inputs) ~ div div[data-testid="stHorizontalBlock"]:not(:has(> div[data-testid="stColumn"]:nth-child(3))) div[data-testid="stNumberInput"] div[data-testid="stNumberInputContainer"],
        div.stElementContainer:has(.inline-inputs) ~ div div[data-testid="stHorizontalBlock"]:not(:has(> div[data-testid="stColumn"]:nth-child(3))) div[data-testid="stSelectbox"] div[data-rac=""] {
            width: 100% !important;
            min-width: 0 !important;
        }

        /* Compact inline label styling for 3-column rows (Movement Rate & Vitality) */
        div.stElementContainer:has(.inline-inputs) ~ div div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(3)) div[data-testid="stTextInput"],
        div.stElementContainer:has(.inline-inputs) ~ div div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(3)) div[data-testid="stNumberInput"] {
            display: flex !important;
            flex-direction: row !important;
            align-items: center !important;
            gap: 6px !important;
        }
        div.stElementContainer:has(.inline-inputs) ~ div div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(3)) div[data-testid="stTextInput"] label,
        div.stElementContainer:has(.inline-inputs) ~ div div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(3)) div[data-testid="stNumberInput"] label {
            min-width: 65px !important;
            margin-bottom: 0 !important;
            text-align: right !important;
            font-weight: 600 !important;
            font-size: 0.85rem !important;
            white-space: nowrap !important;
        }
        div.stElementContainer:has(.inline-inputs) ~ div div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(3)) div[data-testid="stTextInput"] div[data-testid="stWidgetLabel"],
        div.stElementContainer:has(.inline-inputs) ~ div div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(3)) div[data-testid="stNumberInput"] div[data-testid="stWidgetLabel"] {
            margin-bottom: 0 !important;
        }
        div.stElementContainer:has(.inline-inputs) ~ div div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(3)) div[data-testid="stTextInput"] > div,
        div.stElementContainer:has(.inline-inputs) ~ div div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(3)) div[data-testid="stNumberInput"] > div {
            flex-grow: 1 !important;
            min-width: 0 !important;
            width: 100% !important;
        }
        div.stElementContainer:has(.inline-inputs) ~ div div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(3)) div[data-testid="stTextInput"] div[data-testid="stTextInputRootElement"],
        div.stElementContainer:has(.inline-inputs) ~ div div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(3)) div[data-testid="stNumberInput"] div[data-testid="stNumberInputContainer"] {
            width: 100% !important;
            min-width: 0 !important;
        }
        
        /* Inline label styling for stTextArea inside stElementContainer siblings */
        div.stElementContainer:has(.inline-inputs) ~ div.stElementContainer > div[data-testid="stTextArea"] {
            display: flex !important;
            flex-direction: row !important;
            align-items: flex-start !important;
            gap: 12px !important;
        }
        div.stElementContainer:has(.inline-inputs) ~ div.stElementContainer > div[data-testid="stTextArea"] label {
            min-width: 120px !important;
            margin-top: 8px !important;
            margin-bottom: 0 !important;
            text-align: right !important;
            font-weight: 600 !important;
        }
        div.stElementContainer:has(.inline-inputs) ~ div.stElementContainer > div[data-testid="stTextArea"] div[data-testid="stWidgetLabel"] {
            margin-bottom: 0 !important;
        }
        div.stElementContainer:has(.inline-inputs) ~ div.stElementContainer > div[data-testid="stTextArea"] > div {
            flex-grow: 1 !important;
            min-width: 0 !important;
            width: 100% !important;
        }
        
        /* Sticky top tabs area */
        div[data-testid="stTabs"] [role="tablist"] {
            position: sticky !important;
            top: 0 !important;
            z-index: 999 !important;
            background-color: var(--background-color) !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
            padding-top: 10px !important;
            padding-bottom: 10px !important;
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
        # Load tooltips
        LEVEL_NOTE = (
            "⭐ Step 1 — Level⭐ and AP🧩\n"
            "At the end of each large encounter at GM’s discretion, every player receives 1 Level⭐ and 1 Advancement Point (AP🧩). "
            "Thus, a character’s Level⭐ ALWAYS matches the total AP🧩 that character has ever received.\n\n"
            "🎲 Step 2 — Vit💖 Roll And Atr🧩 Die\n"
            "All of step 2 below is AP🧩 free and costs no AP🧩.\n\n"
            "Level   Vit Max Roll                                    Atr Die\n"
            "1-3             10+1d(Moxie🫀)+(AP🧩*2)               d4, d4, d4, d6, d8\n"
            "4-8             10+2d(Moxie🫀)+(AP🧩*2)               d4, d4, d6, d6, d8\n"
            "9-15          10+3d(Moxie🫀)+(AP🧩*2)               d4, d6, d6, d6, d8\n"
            "16-24        10+4d(Moxie🫀)+(AP🧩*2)               d4, d6, d6, d8, d8\n"
            "25-35        10+5d(Moxie🫀)+(AP🧩*2)               d4, d6, d6, d8, d8\n"
            "36-48        10+6d(Moxie🫀)+(AP🧩*2)               d4, d6, d6, d8, d10\n"
            "49-63        10+7d(Moxie🫀)+(AP🧩*2)               d4, d6, d8, d8, d10\n"
            "64-80        10+8d(Moxie🫀)+(AP🧩*2)               d6, d6, d8, d8, d10\n"
            "81-99        10+9d(Moxie🫀)+(AP🧩*2)               d6, d6, d8, d10, d10\n"
            "100-120    10+10d(Moxie🫀)+(AP🧩*2)             d6, d8, d8, d10, d10\n"
            "121-143    10+11d(Moxie🫀)+(AP🧩*2)             d6, d8, d8, d10, d12\n"
            "144-168    10+12d(Moxie🫀)+(AP🧩*2)             d6, d8, d10, d10, d12\n"
            "169-195    10+13d(Moxie🫀)+(AP🧩*2)             d8, d8, d10, d10, d12\n"
            "196-224    10+14d(Moxie🫀)+(AP🧩*2)             d8, d8, d10, d12, d12\n"
            "225+          10+15d(Moxie🫀)+(AP🧩*2)             d8, d10, d10, d12, d12"
        )
        MONEY_NOTE = "1 Gold = 100 Silver"
        ATR_DIE_NOTE = (
            "🎲 Step 2 — Atr🧩 Die Progression\n"
            "On the indicated Levels⭐ your Atr🧩 die will change:\n\n"
            "Level   Atr Die\n"
            "1-3             d4, d4, d4, d6, d8\n"
            "4-8             d4, d4, d6, d6, d8\n"
            "9-15           d4, d6, d6, d6, d8\n"
            "16-24         d4, d6, d6, d8, d8\n"
            "25-35         d4, d6, d6, d8, d8\n"
            "36-48         d4, d6, d6, d8, d10\n"
            "49-63         d4, d6, d8, d8, d10\n"
            "64-80         d6, d6, d8, d8, d10\n"
            "81-99         d6, d6, d8, d10, d10\n"
            "100-120     d6, d8, d8, d10, d10\n"
            "121-143     d6, d8, d8, d10, d12\n"
            "144-168     d6, d8, d10, d10, d12\n"
            "169-195     d8, d8, d10, d10, d12\n"
            "196-224     d8, d8, d10, d12, d12\n"
            "225+           d8, d10, d10, d12, d12"
        )
        VIT_NOTE = (
            "💖 Vit Max Roll Progression\n"
            "On each Level⭐, roll for new maximum Vit💖 (luck/keep the better roll).\n\n"
            "Level   Vit Max Roll\n"
            "1-3             10+1d(Moxie🫀)+(AP🧩*2)\n"
            "4-8             10+2d(Moxie🫀)+(AP🧩*2)\n"
            "9-15          10+3d(Moxie🫀)+(AP🧩*2)\n"
            "16-24        10+4d(Moxie🫀)+(AP🧩*2)\n"
            "25-35        10+5d(Moxie🫀)+(AP🧩*2)\n"
            "36-48        10+6d(Moxie🫀)+(AP🧩*2)\n"
            "49-63        10+7d(Moxie🫀)+(AP🧩*2)\n"
            "64-80        10+8d(Moxie🫀)+(AP🧩*2)\n"
            "81-99        10+9d(Moxie🫀)+(AP🧩*2)\n"
            "100-120    10+10d(Moxie🫀)+(AP🧩*2)\n"
            "121-143    10+11d(Moxie🫀)+(AP🧩*2)\n"
            "144-168    10+12d(Moxie🫀)+(AP🧩*2)\n"
            "169-195    10+13d(Moxie🫀)+(AP🧩*2)\n"
            "196-224    10+14d(Moxie🫀)+(AP🧩*2)\n"
            "225+          10+15d(Moxie🫀)+(AP🧩*2)"
        )
        WNDS_NOTE = (
            "💀 Wounds & Death Checks\n"
            "Death Checks = Moxie🫀 roll vs Dif = 5 + (Wnd🩸 – Vit💖).\n"
            "Example: Vit💖 20 with 23 Wnd🩸 ➡ Dif = 8.\n\n"
            "🩸 Bleeding:\n"
            "After each Death Check, Wnd🩸 always increases by 1 unless you receive wound care or healing."
        )

        sheet_data = char_state.get("sheet_data") or repo.get_default_sheet_data()
        traits = sheet_data.get("traits") or {}
        money = sheet_data.get("money") or {}
        weapons = sheet_data.get("weapons") or []
        armor_shield = sheet_data.get("armor_shield") or {}
        powers_slots = sheet_data.get("powers") or []
        magic_items_slots = sheet_data.get("magic_items") or []
        notes = sheet_data.get("notes") or ""
        vitals = sheet_data.get("vitals") or {}

        # Self-healing pad arrays
        while len(weapons) < 5:
            weapons.append({"sk": False, "m_h_s": "M", "name": "", "atk": "", "dmg": "", "max_block": ""})
        while len(powers_slots) < 10:
            powers_slots.append({"select": False, "usage": "", "action": "", "name": "", "effect": ""})
        while len(magic_items_slots) < 5:
            magic_items_slots.append({"select": False, "usage": "", "action": "", "name": "", "effect": ""})



        # Row 1: Traits & Vitals Block
        col_t1, col_t2 = st.columns([1, 1])
        with col_t1:
            st.markdown("#### 👤 General Traits & Description")
            st.markdown('<div class="inline-inputs">', unsafe_allow_html=True)
            col_sub1, col_sub2 = st.columns(2)
            with col_sub1:
                new_class = st.text_input("Class", value=char_state.get("class") or "")
                new_appearance = st.text_input("Appearance", value=traits.get("appearance") or "")
                new_pos_trait = st.text_input("Positive Trait", value=traits.get("positive_trait") or "")
            with col_sub2:
                new_race = st.text_input("Race", value=char_state.get("race") or "")
                new_hgt_wgt_age = st.text_input("Hgt / Wgt / Age", value=traits.get("hgt_wgt_age") or "")
                new_neg_trait = st.text_input("Negative Trait", value=traits.get("negative_trait") or "")
            new_flair = st.text_input("Flair", value=traits.get("flair") or "")
            new_goal = st.text_input("Adventuring Goal", value=traits.get("adventuring_goal") or "")
            new_notes = st.text_area("Gear", value=notes, height=80)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_t2:
            st.markdown("#### 💖 Health, Money & Movement")
            st.markdown('<div class="inline-inputs">', unsafe_allow_html=True)
            col_sub3, col_sub4 = st.columns(2)
            with col_sub3:
                new_level = st.number_input("Level 🎲", min_value=1, max_value=200, value=int(vitals.get("level", 1)), help=LEVEL_NOTE)
                new_gold = st.number_input("Gold 🪙", min_value=0, value=int(money.get("gold", 0)), help=MONEY_NOTE)
            with col_sub4:
                skillset_names = ["Custom / None"] + [s["name"] for s in skillsets]
                prev_skillset = sheet_data.get("active_skillset") or "Custom / None"
                if prev_skillset not in skillset_names:
                    prev_skillset = "Custom / None"
                selected_set = st.selectbox("Predefined Skillset Package 🎓", skillset_names, index=skillset_names.index(prev_skillset))
                new_silver = st.number_input("Silver 🥈", min_value=0, value=int(money.get("silver", 0)), help=MONEY_NOTE)
            st.markdown('</div>', unsafe_allow_html=True)

            st.write("**Movement Rate (MR)**")
            new_mr_base = vitals.get("mr_base", 0)  # Preserved in database save pipeline, removed from UI
            col_mr1, col_mr2 = st.columns(2)
            with col_mr1:
                new_mr_armored = st.text_input("Armored", value=vitals.get("mr_armored") or "")
            with col_mr2:
                new_mr_shield = st.text_input("Shield", value=vitals.get("mr_shield") or "")

            st.write("**Vitality Points (HP) & Wounds**")
            col_v1, col_v2, col_v3 = st.columns(3)
            with col_v1:
                new_max_hp = st.number_input("Max 💖", min_value=1, max_value=200, value=int(char_state.get("hp", 10)), help=VIT_NOTE)
            with col_v2:
                new_current_hp = st.number_input("Current 💖", min_value=0, max_value=200, value=int(vitals.get("current_hp", 10)))
            with col_v3:
                new_wounds = st.number_input("Wounds 🩸", min_value=0, value=int(vitals.get("wounds", 0)), help=WNDS_NOTE)

        # Triggers skillset update
        if selected_set != prev_skillset:
            old_set_skills = []
            if prev_skillset != "Custom / None":
                old_set_data = next((s for s in skillsets if s["name"] == prev_skillset), None)
                if old_set_data:
                    old_set_skills = old_set_data.get("skills", [])
            new_set_skills = []
            if selected_set != "Custom / None":
                new_set_data = next((s for s in skillsets if s["name"] == selected_set), None)
                if new_set_data:
                    new_set_skills = new_set_data.get("skills", [])
            
            updated_skills = GameEngine.update_skills_list(char_state.get("skills", []), old_set_skills, new_set_skills)
            char_state["skills"] = updated_skills
            sheet_data["active_skillset"] = selected_set
            sheet_data["weapons"] = weapons
            sheet_data["powers"] = powers_slots
            sheet_data["magic_items"] = magic_items_slots
            sheet_data["traits"] = {
                "positive_trait": new_pos_trait,
                "negative_trait": new_neg_trait,
                "flair": new_flair,
                "adventuring_goal": new_goal,
                "appearance": new_appearance,
                "hgt_wgt_age": new_hgt_wgt_age
            }
            sheet_data["money"] = {"gold": int(new_gold), "silver": int(new_silver)}
            sheet_data["armor_shield"] = armor_shield
            sheet_data["notes"] = notes
            sheet_data["vitals"] = {
                "level": int(new_level),
                "max_hp": int(new_max_hp),
                "current_hp": int(new_current_hp),
                "wounds": int(new_wounds),
                "mr_base": int(new_mr_base),
                "mr_armored": new_mr_armored,
                "mr_shield": new_mr_shield
            }
            
            repo.save_character(player_name, {
                "skills": updated_skills,
                "sheet_data": sheet_data
            })
            st.toast(f"🎓 Applied skillset package: {selected_set}")
            st.rerun()

        st.markdown("---")
        st.markdown("### 🎲 Attributes & Proficiencies")
        
        # Header Row
        col_hdr1, col_hdr2, col_hdr3, col_hdr4 = st.columns([1.0, 0.6, 2.2, 4.0], vertical_alignment="center")
        with col_hdr1:
            st.markdown("**✅ Atr**")
        with col_hdr2:
            st.markdown("**Die 🎲**")
        with col_hdr3:
            st.markdown("**Notes**")
        with col_hdr4:
            st.markdown("**🎓 Skilled at**")
            
        ratings = ["d4", "d6", "d8", "d10", "d12"]
        
        # Might Row
        col_m1, col_m2, col_m3, col_m4 = st.columns([1.0, 0.6, 2.2, 4.0], vertical_alignment="center")
        with col_m1:
            st.markdown("**Might 💪**")
        with col_m2:
            new_might = st.selectbox("Might Rating", ratings, index=ratings.index(char_state.get("might", "d4")), key="sb_might", label_visibility="collapsed", help=ATR_DIE_NOTE)
        with col_m3:
            st.markdown('<div style="font-size: 0.85rem; line-height: 1.25; color: rgba(255,255,255,0.75);">melee weapons, Block Def, armor 🛡️, shields 🛡️, physical strength</div>', unsafe_allow_html=True)
        with col_m4:
            st.markdown('<div style="background-color: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 4px; padding: 6px 12px; min-height: 42px; max-height: 70px; overflow-y: auto; width: 100%;"></div>', unsafe_allow_html=True)
            
        # Motion Row
        col_mo1, col_mo2, col_mo3, col_mo4 = st.columns([1.0, 0.6, 2.2, 4.0], vertical_alignment="center")
        with col_mo1:
            st.markdown("**Motion 🏃**")
        with col_mo2:
            new_motion = st.selectbox("Motion Rating", ratings, index=ratings.index(char_state.get("motion", "d4")), key="sb_motion", label_visibility="collapsed", help=ATR_DIE_NOTE)
        with col_mo3:
            st.markdown('<div style="font-size: 0.85rem; line-height: 1.25; color: rgba(255,255,255,0.75);">Nish 🚩, dodge, hurled weapons, athletics, dexterity, balance</div>', unsafe_allow_html=True)
        with col_mo4:
            st.markdown('<div style="background-color: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 4px; padding: 6px 12px; min-height: 42px; max-height: 70px; overflow-y: auto; width: 100%;"></div>', unsafe_allow_html=True)
            
        # Mind Row
        col_mi1, col_mi2, col_mi3, col_mi4 = st.columns([1.0, 0.6, 2.2, 4.0], vertical_alignment="center")
        with col_mi1:
            st.markdown("**Mind 👁️**")
        with col_mi2:
            new_mind = st.selectbox("Mind Rating", ratings, index=ratings.index(char_state.get("mind", "d4")), key="sb_mind", label_visibility="collapsed", help=ATR_DIE_NOTE)
        with col_mi3:
            st.markdown('<div style="font-size: 0.85rem; line-height: 1.25; color: rgba(255,255,255,0.75);">shot weapons, intelligence, personality, awareness, wit, charm, persuade</div>', unsafe_allow_html=True)
        with col_mi4:
            st.markdown('<div style="background-color: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 4px; padding: 6px 12px; min-height: 42px; max-height: 70px; overflow-y: auto; width: 100%;"></div>', unsafe_allow_html=True)
            
        # Magic Row
        col_ma1, col_ma2, col_ma3, col_ma4 = st.columns([1.0, 0.6, 2.2, 4.0], vertical_alignment="center")
        with col_ma1:
            st.markdown("**Magic ✨**")
        with col_ma2:
            new_magic = st.selectbox("Magic Rating", ratings, index=ratings.index(char_state.get("magic", "d4")), key="sb_magic", label_visibility="collapsed", help=ATR_DIE_NOTE)
        with col_ma3:
            st.markdown('<div style="font-size: 0.85rem; line-height: 1.25; color: rgba(255,255,255,0.75);">Saves/Resistances, arcane power</div>', unsafe_allow_html=True)
        with col_ma4:
            st.markdown('<div style="background-color: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 4px; padding: 6px 12px; min-height: 42px; max-height: 70px; overflow-y: auto; width: 100%;"></div>', unsafe_allow_html=True)
            
        # Moxie Row
        col_mx1, col_mx2, col_mx3, col_mx4 = st.columns([1.0, 0.6, 2.2, 4.0], vertical_alignment="center")
        with col_mx1:
            st.markdown("**Moxie 🫀**")
        with col_mx2:
            new_moxie = st.selectbox("Moxie Rating", ratings, index=ratings.index(char_state.get("moxie", "d4")), key="sb_moxie", label_visibility="collapsed", help=ATR_DIE_NOTE)
        with col_mx3:
            st.markdown('<div style="font-size: 0.85rem; line-height: 1.25; color: rgba(255,255,255,0.75);">Resist Saves, Death Checks, Stamina, Body</div>', unsafe_allow_html=True)
        with col_mx4:
            st.markdown('<div style="background-color: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 4px; padding: 6px 12px; min-height: 42px; max-height: 70px; overflow-y: auto; width: 100%;"></div>', unsafe_allow_html=True)
            
        new_skills = char_state.get("skills", [])

        st.markdown("---")
        # Middle Layout: Weapons Grid (Left) & Armor Card (Right)
        col_mid1, col_mid2 = st.columns([7, 5])
        
        with col_mid1:
            st.markdown("#### ⚔️ Weapons Grid")
            col_w_h1, col_w_h2, col_w_h3, col_w_h4, col_w_h5, col_w_h6 = st.columns([0.8, 1.2, 3.2, 1.8, 1.8, 1.8])
            with col_w_h1:
                st.write("**Sk**")
            with col_w_h2:
                st.write("**M/H/S**")
            with col_w_h3:
                st.write("**Weapon Name**")
            with col_w_h4:
                st.write("**Atk**")
            with col_w_h5:
                st.write("**Dmg**")
            with col_w_h6:
                st.write("**Max Blk**")
                
            updated_weapons = []
            for i, w in enumerate(weapons):
                col_w1, col_w2, col_w3, col_w4, col_w5, col_w6 = st.columns([0.8, 1.2, 3.2, 1.8, 1.8, 1.8])
                with col_w1:
                    w_sk = st.checkbox("Sk", value=w.get("sk", False), key=f"w_sk_{i}", label_visibility="collapsed")
                with col_w2:
                    w_mhs = st.selectbox("M/H/S", ["M", "H", "S"], index=["M", "H", "S"].index(w.get("m_h_s", "M")), key=f"w_mhs_{i}", label_visibility="collapsed")
                with col_w3:
                    w_name = st.text_input("Name", value=w.get("name", ""), key=f"w_name_{i}", label_visibility="collapsed")
                with col_w4:
                    w_atk = st.text_input("Atk", value=w.get("atk", ""), key=f"w_atk_{i}", label_visibility="collapsed")
                with col_w5:
                    w_dmg = st.text_input("Dmg", value=w.get("dmg", ""), key=f"w_dmg_{i}", label_visibility="collapsed")
                with col_w6:
                    w_max_block = st.text_input("Max Block", value=w.get("max_block", ""), key=f"w_max_block_{i}", label_visibility="collapsed")
                    
                updated_weapons.append({
                    "sk": w_sk,
                    "m_h_s": w_mhs,
                    "name": w_name,
                    "atk": w_atk,
                    "dmg": w_dmg,
                    "max_block": w_max_block
                })

        with col_mid2:
            st.markdown("#### 🛡️ Armor, Shield & Ratings")
            col_arm1, col_arm2 = st.columns(2)
            with col_arm1:
                arm_name = st.text_input("Armor Name", value=armor_shield.get("armor_name", ""))
                arm_def = st.text_input("Def Rating", value=armor_shield.get("armor_def", ""))
                arm_ar = st.text_input("AR Value", value=armor_shield.get("armor_ar", ""))
                dodge_act = st.text_input("Dodge Active", value=armor_shield.get("dodge_active", ""))
            with col_arm2:
                sh_name = st.text_input("Shield Name", value=armor_shield.get("shield_name", ""))
                sh_max_block = st.text_input("Shield Max Block", value=armor_shield.get("shield_max_block", ""))
                st.write("") # layout spacers
                st.write("")
                block_act = st.text_input("Block Active", value=armor_shield.get("block_active", ""))
                
            new_armor_shield = {
                "armor_name": arm_name,
                "armor_def": arm_def,
                "armor_ar": arm_ar,
                "shield_name": sh_name,
                "shield_max_block": sh_max_block,
                "block_active": block_act,
                "dodge_active": dodge_act
            }

        st.markdown("---")
        # Bottom Layout: Powers (Left) & Magic Items (Right)
        col_bot1, col_bot2 = st.columns([1, 1])
        
        with col_bot1:
            st.markdown("#### ⚡ Powers & Special Abilities")
            col_p_h1, col_p_h2, col_p_h3, col_p_h4, col_p_h5 = st.columns([0.8, 3, 1.2, 1.5, 3.5])
            with col_p_h1:
                st.write("**Sel**")
            with col_p_h2:
                st.write("**Power Preset Selection**")
            with col_p_h3:
                st.write("**Act**")
            with col_p_h4:
                st.write("**Usage**")
            with col_p_h5:
                st.write("**Effect Description**")
                
            updated_powers_slots = []
            power_names = ["Custom / None"] + [p["name"] for p in powers]
            
            for i, slot in enumerate(powers_slots):
                col_p1, col_p2, col_p3, col_p4, col_p5 = st.columns([0.8, 3, 1.2, 1.5, 3.5])
                with col_p1:
                    p_sel = st.checkbox("Sel", value=slot.get("select", False), key=f"p_sel_{i}", label_visibility="collapsed")
                with col_p2:
                    current_name = slot.get("name") or "Custom / None"
                    preset_options = [current_name] + power_names if current_name not in power_names else power_names
                    p_name_sel = st.selectbox("Preset", preset_options, index=preset_options.index(current_name), key=f"p_name_sel_{i}", label_visibility="collapsed")
                
                # Preset changed trigger
                if p_name_sel != current_name:
                    new_slot = GameEngine.update_power_or_item_slot(slot, p_name_sel if p_name_sel != "Custom / None" else "", powers)
                    powers_slots[i] = new_slot
                    sheet_data["powers"] = powers_slots
                    sheet_data["weapons"] = updated_weapons
                    sheet_data["magic_items"] = magic_items_slots
                    sheet_data["traits"] = {
                        "positive_trait": new_pos_trait,
                        "negative_trait": new_neg_trait,
                        "flair": new_flair,
                        "adventuring_goal": new_goal,
                        "appearance": new_appearance,
                        "hgt_wgt_age": new_hgt_wgt_age
                    }
                    sheet_data["money"] = {"gold": int(new_gold), "silver": int(new_silver)}
                    sheet_data["armor_shield"] = new_armor_shield
                    sheet_data["notes"] = new_notes
                    sheet_data["vitals"] = {
                        "level": int(new_level),
                        "max_hp": int(new_max_hp),
                        "current_hp": int(new_current_hp),
                        "wounds": int(new_wounds),
                        "mr_base": int(new_mr_base),
                        "mr_armored": new_mr_armored,
                        "mr_shield": new_mr_shield
                    }
                    repo.save_character(player_name, {
                        "hp": int(new_max_hp),
                        "might": new_might,
                        "motion": new_motion,
                        "mind": new_mind,
                        "magic": new_magic,
                        "moxie": new_moxie,
                        "skills": new_skills,
                        "sheet_data": sheet_data
                    })
                    st.toast(f"⚡ Loaded power: {p_name_sel}")
                    st.rerun()
                    
                with col_p3:
                    p_act = st.text_input("Act", value=slot.get("action", ""), key=f"p_act_{i}", label_visibility="collapsed")
                with col_p4:
                    p_use = st.text_input("Usage", value=slot.get("usage", ""), key=f"p_use_{i}", label_visibility="collapsed")
                with col_p5:
                    p_eff = st.text_input("Effect", value=slot.get("effect", ""), key=f"p_eff_{i}", label_visibility="collapsed")
                    
                updated_powers_slots.append({
                    "select": p_sel,
                    "name": p_name_sel if p_name_sel != "Custom / None" else slot.get("name", ""),
                    "action": p_act,
                    "usage": p_use,
                    "effect": p_eff
                })

        with col_bot2:
            st.markdown("#### 🍺 Magic Items & Special Gear")
            col_m_h1, col_m_h2, col_m_h3, col_m_h4, col_m_h5 = st.columns([0.8, 3, 1.2, 1.5, 3.5])
            with col_m_h1:
                st.write("**Sel**")
            with col_m_h2:
                st.write("**Item Preset Selection**")
            with col_m_h3:
                st.write("**Act**")
            with col_m_h4:
                st.write("**Usage**")
            with col_m_h5:
                st.write("**Effect Description**")
                
            updated_items_slots = []
            item_names = ["Custom / None"] + [m["name"] for m in magic_items]
            
            for i, slot in enumerate(magic_items_slots):
                col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns([0.8, 3, 1.2, 1.5, 3.5])
                with col_m1:
                    m_sel = st.checkbox("Sel", value=slot.get("select", False), key=f"m_sel_{i}", label_visibility="collapsed")
                with col_m2:
                    current_name = slot.get("name") or "Custom / None"
                    preset_options = [current_name] + item_names if current_name not in item_names else item_names
                    m_name_sel = st.selectbox("Preset", preset_options, index=preset_options.index(current_name), key=f"m_name_sel_{i}", label_visibility="collapsed")
                
                # Preset changed trigger
                if m_name_sel != current_name:
                    new_slot = GameEngine.update_power_or_item_slot(slot, m_name_sel if m_name_sel != "Custom / None" else "", magic_items)
                    magic_items_slots[i] = new_slot
                    sheet_data["magic_items"] = magic_items_slots
                    sheet_data["weapons"] = updated_weapons
                    sheet_data["powers"] = updated_powers_slots
                    sheet_data["traits"] = {
                        "positive_trait": new_pos_trait,
                        "negative_trait": new_neg_trait,
                        "flair": new_flair,
                        "adventuring_goal": new_goal,
                        "appearance": new_appearance,
                        "hgt_wgt_age": new_hgt_wgt_age
                    }
                    sheet_data["money"] = {"gold": int(new_gold), "silver": int(new_silver)}
                    sheet_data["armor_shield"] = new_armor_shield
                    sheet_data["notes"] = new_notes
                    sheet_data["vitals"] = {
                        "level": int(new_level),
                        "max_hp": int(new_max_hp),
                        "current_hp": int(new_current_hp),
                        "wounds": int(new_wounds),
                        "mr_base": int(new_mr_base),
                        "mr_armored": new_mr_armored,
                        "mr_shield": new_mr_shield
                    }
                    repo.save_character(player_name, {
                        "hp": int(new_max_hp),
                        "might": new_might,
                        "motion": new_motion,
                        "mind": new_mind,
                        "magic": new_magic,
                        "moxie": new_moxie,
                        "skills": new_skills,
                        "sheet_data": sheet_data
                    })
                    st.toast(f"🍺 Loaded item: {m_name_sel}")
                    st.rerun()
                    
                with col_m3:
                    m_act = st.text_input("Act", value=slot.get("action", ""), key=f"m_act_{i}", label_visibility="collapsed")
                with col_m4:
                    m_use = st.text_input("Usage", value=slot.get("usage", ""), key=f"m_use_{i}", label_visibility="collapsed")
                with col_m5:
                    m_eff = st.text_input("Effect", value=slot.get("effect", ""), key=f"m_eff_{i}", label_visibility="collapsed")
                    
                updated_items_slots.append({
                    "select": m_sel,
                    "name": m_name_sel if m_name_sel != "Custom / None" else slot.get("name", ""),
                    "action": m_act,
                    "usage": m_use,
                    "effect": m_eff
                })

        # Save updates if changes made on other fields
        compiled_sheet_data = {
            "traits": {
                "positive_trait": new_pos_trait,
                "negative_trait": new_neg_trait,
                "flair": new_flair,
                "adventuring_goal": new_goal,
                "appearance": new_appearance,
                "hgt_wgt_age": new_hgt_wgt_age
            },
            "money": {
                "gold": int(new_gold),
                "silver": int(new_silver)
            },
            "weapons": updated_weapons,
            "armor_shield": new_armor_shield,
            "powers": updated_powers_slots,
            "magic_items": updated_items_slots,
            "notes": new_notes,
            "vitals": {
                "level": int(new_level),
                "max_hp": int(new_max_hp),
                "current_hp": int(new_current_hp),
                "wounds": int(new_wounds),
                "mr_base": int(new_mr_base),
                "mr_armored": new_mr_armored,
                "mr_shield": new_mr_shield
            },
            "active_skillset": selected_set
        }

        updated_db_data = {
            "class": new_class.strip() or None,
            "race": new_race.strip() or None,
            "hp": int(new_max_hp),
            "might": new_might,
            "motion": new_motion,
            "mind": new_mind,
            "magic": new_magic,
            "moxie": new_moxie,
            "skills": new_skills,
            "sheet_data": compiled_sheet_data
        }

        # Check for diff before committing save
        has_changes = False
        for key, val in updated_db_data.items():
            if char_state.get(key) != val:
                has_changes = True
                break

        if has_changes:
            if repo.save_character(player_name, updated_db_data):
                st.toast("⚡ Changes saved automatically!")
                st.rerun()
            else:
                st.error("⚠️ Failed to auto-save character data.")

    # --- TAB 2: ACTION & ROLL CONSOLE ---
    with tab_rolls:
        
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
    # --- TAB 3: INVENTORY GRID EDITOR ---
    with tab_inv:
        
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
    # --- TAB 4: ADVENTURE & ACTION LOGS ---
    with tab_rules:
        
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
    # --- TAB 5: CODEX SEARCH ---
    with tab_codex:
        
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
    # --- TAB 6: PLAYER DIRECTORY & SHARING ---
    with tab_sharing:
        
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


if __name__ == "__main__":
    main()

