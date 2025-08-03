"""
Snow Village - Main Application
Login screen with user registration and authentication
"""

import streamlit as st
import os
import base64
import time
import sys
sys.path.append(os.path.dirname(__file__))
from database_manager import DatabaseManager

def handle_submit(intent: str):
    """
    Handle button clicks for registration and login
    """
    name = st.session_state.get("user_name_input", "")
    if name and name.strip():
        db = DatabaseManager()
        name = name.strip()
        
        if intent == 'play':  # New user registration
            if db.check_user_exists(name):
                # Existing user
                st.session_state.popup_message = f"User already registered. {name} can continue playing!"
                st.session_state.popup_type = "existing_user"
            else:
                # New user
                success, message = db.register_user(name)
                if success:
                    st.session_state.popup_message = f"Registration complete! Welcome to SnowVillage, {name}!"
                    st.session_state.popup_type = "new_user"
                    st.session_state.result = {
                        "name": name,
                        "intent": "new_user"
                    }
                else:
                    st.session_state.error_message = message
        
        elif intent == 'login':  # Existing user login
            success, message = db.login_user(name)
            if success:
                st.session_state.result = {
                    "name": name,
                    "intent": "existing_user"
                }
            else:
                st.session_state.error_message = "User not found. Please register first."
        
        # Clear error messages if not login intent
        if 'error_message' in st.session_state and intent != 'login':
            if 'error_message' in st.session_state:
                del st.session_state.error_message
    else:
        # Validation failed
        st.session_state.error_message = "Please enter an account identifier"

def launch_screen():
    """
    Build and display the login screen UI
    """
    if 'result' in st.session_state and st.session_state.result:
        result = st.session_state.result
        del st.session_state.result
        return result

    # --- Image and style setup ---
    def get_base64_img(path):
        if os.path.exists(path):
            with open(path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        return ""

    base_dir = os.path.dirname(__file__)
    logo_path = os.path.join(base_dir, "frontend", "public", "SnowVillageLogo.png")
    bg_path = os.path.join(base_dir, "frontend", "public", "bg-villag-go.png")
    
    logo_base64 = get_base64_img(logo_path)
    bg_base64 = get_base64_img(bg_path)

    # Snowflake blue gradient background
    bg_style = f"background: linear-gradient(135deg, #1a237e, #283593, #3949ab, #42a5f5);" if not bg_base64 else f"background: url(data:image/png;base64,{bg_base64}) no-repeat center center fixed; background-size: cover;"
    
    st.markdown(f"""
    <style>
        .stApp {{ {bg_style} }}
        .card {{
            background: rgba(30, 30, 30, 0.9);
            border: 1px solid rgba(79, 195, 247, 0.3);
            border-radius: 16px;
            padding: 2.5rem;
            text-align: center;
            max-width: 450px;
            margin: 1rem auto;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        }}
        .stButton button {{
            border-radius: 12px !important;
            height: 50px;
            font-weight: 600;
            margin: 0.5rem 0;
        }}
        .stButton button[data-baseweb="button"][kind="primary"] {{
            background: #1976d2 !important;
            border-color: #1976d2 !important;
        }}
        .stTextInput input {{
            border-radius: 12px !important;
            padding: 1rem !important;
            height: 50px;
            border: 2px solid #424242 !important;
            background: rgba(50, 50, 50, 0.8) !important;
            color: white !important;
        }}
        .stTextInput input::placeholder {{
            color: #9e9e9e !important;
        }}
    </style>
    """, unsafe_allow_html=True)

    # --- UI Layout ---
    _left_gap, center_col, _right_gap = st.columns([1, 2, 1])
    with center_col:
        # --- Card section ---
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Snowflake logo or icon
        if logo_base64:
            st.image(f"data:image/png;base64,{logo_base64}", width=60)
        else:
            st.markdown("<div style='font-size: 40px; color: #4FC3F7;'>❄️</div>", unsafe_allow_html=True)

        # Text content
        card_content_html = """
        <h1 style="color: #4FC3F7; font-size: 2.2rem; font-weight: 700; margin-bottom: 0.5rem;">Snowflake Intelligence</h1>
        <p style="color: #E0E0E0; font-size: 1.1rem; margin-bottom: 1.5rem;">Talk to your data, unlock real business insights</p>
        <div style="color: #B0BEC5; font-size: 0.9rem; margin-bottom: 1.5rem;">Enter your account identifier or account URL</div>
        """
        st.markdown(card_content_html, unsafe_allow_html=True)

        st.text_input(
            "Account Identifier",
            placeholder="Account Identifier",
            key="user_name_input",
            label_visibility="collapsed"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)

        # --- Button section ---
        if 'error_message' in st.session_state and st.session_state.error_message:
            st.error(st.session_state.error_message, icon="⚠️")
            del st.session_state.error_message

        # Popup messages
        if 'popup_message' in st.session_state and st.session_state.popup_message:
            if st.session_state.popup_type == "new_user":
                st.success(st.session_state.popup_message, icon="🎉")
            elif st.session_state.popup_type == "existing_user":
                st.info(st.session_state.popup_message, icon="ℹ️")
            # Clear popup after display
            del st.session_state.popup_message
            del st.session_state.popup_type
        
        st.button("Let's Play!", use_container_width=True, on_click=handle_submit, args=('play',), type="primary")
        st.button("Existing Users Click Here", use_container_width=True, on_click=handle_submit, args=('login',))
        
        # Account identifier location info
        st.markdown(
            '<div style="color: #94a3b8; font-size: 0.8rem; margin-top: 1rem;">Account identifier location</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div style="color: #4FC3F7; font-size: 0.8rem;">https://&lt;account_identifier&gt;.snowflakecomputing.com</div>',
            unsafe_allow_html=True
        )
    
    return None

def main():
    """
    Main function to run the Snow Village application
    """
    # ==================================================================
    # --- Main application block ---
    # ==================================================================
    st.set_page_config(
        page_title="Welcome to Snow Village",
        page_icon="❄️",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    st.markdown("<style>[data-testid='stSidebar'] { display: none; }</style>", unsafe_allow_html=True)

    if "user_info" not in st.session_state:
        st.session_state.user_info = None

    login_result = launch_screen()

    if login_result:
        st.session_state.user_info = login_result
        if login_result['intent'] == 'new_user':
            st.balloons()
            st.success(f"🎉 Welcome {st.session_state.user_info['name']}!")
            st.info("Moving to problem list page...")
            time.sleep(2)
            st.switch_page("pages/problem_list.py")
        elif login_result['intent'] == 'existing_user':
            st.balloons()
            st.success(f"🎉 Welcome back {st.session_state.user_info['name']}!")
            st.info("Moving to problem list page...")
            time.sleep(2)
            st.switch_page("pages/problem_list.py")

if __name__ == "__main__":
    main()