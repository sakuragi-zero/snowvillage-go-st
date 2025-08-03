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
                st.session_state.popup_message = f"登録済みユーザーです。{name}さん、続きをプレイできます！"
                st.session_state.popup_type = "existing_user"
            else:
                # New user
                success, message = db.register_user(name)
                if success:
                    st.session_state.popup_message = f"登録完了！{name}さん、ようこそSnowVillageへ！"
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
                st.session_state.error_message = "ユーザーが見つかりません。新規登録してください。"
        
        # Clear error messages if not login intent
        if 'error_message' in st.session_state and intent != 'login':
            if 'error_message' in st.session_state:
                del st.session_state.error_message
    else:
        # Validation failed
        st.session_state.error_message = "アカウント識別子を入力してください"

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
        .stButton button {{
            border-radius: 12px !important;
            height: 50px;
            font-weight: 600;
            margin: 0.5rem 0;
            background: white !important;
            color: black !important;
            border: 2px solid white !important;
        }}
        .stButton button:hover {{
            background: #f0f0f0 !important;
            color: black !important;
        }}
        .stTextInput input {{
            border-radius: 12px !important;
            padding: 1rem !important;
            height: 50px;
            border: 2px solid white !important;
            background: white !important;
            color: black !important;
        }}
        .stTextInput input::placeholder {{
            color: #666666 !important;
        }}
    </style>
    """, unsafe_allow_html=True)

    # --- UI Layout ---
    _left_gap, center_col, _right_gap = st.columns([1, 2, 1])
    with center_col:
        # Snowflake logo or icon (centered)
        if logo_base64:
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                st.image(f"data:image/png;base64,{logo_base64}", width=60)
        else:
            st.markdown("<div style='font-size: 40px; color: #4FC3F7; text-align: center;'>❄️</div>", unsafe_allow_html=True)

        # Text content
        st.markdown("""
        <h1 style="color: #4FC3F7; font-size: 2.2rem; font-weight: 700; margin-bottom: 0.5rem; text-align: center;">SnowVillage GO</h1>
        <p style="color: #E0E0E0; font-size: 1.1rem; margin-bottom: 1.5rem; text-align: center;">Snowflake World Tour Tokyo 2025</p>
        <div style="color: #B0BEC5; font-size: 0.9rem; margin-bottom: 1.5rem; text-align: center;">アカウント登録またはログイン</div>
        """, unsafe_allow_html=True)

        st.text_input(
            "アカウント識別子",
            placeholder="アカウント識別子",
            key="user_name_input",
            label_visibility="collapsed"
        )

        # Error messages
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
        
        st.button("遊びに行く！", use_container_width=True, on_click=handle_submit, args=('play',))
        st.button("登録済みの方はこちら", use_container_width=True, on_click=handle_submit, args=('login',))
        
    
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
            st.success(f"🎉 ようこそ {st.session_state.user_info['name']} さん！")
            st.info("問題一覧ページへ移動します...")
            time.sleep(2)
            st.switch_page("pages/problem_list.py")
        elif login_result['intent'] == 'existing_user':
            st.balloons()
            st.success(f"🎉 おかえりなさい {st.session_state.user_info['name']} さん！")
            st.info("問題一覧ページへ移動します...")
            time.sleep(2)
            st.switch_page("pages/problem_list.py")

if __name__ == "__main__":
    main()