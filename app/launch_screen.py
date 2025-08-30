"""
Snow Village - Main Application
Login screen with user registration and authentication
"""

import streamlit as st
import os
import base64
import time
from user import UserService

@st.fragment
def handle_user_validation(name: str):
    """
    Handle user existence check with fragment for better performance
    """
    user_service = UserService()
    
    with st.spinner("ユーザー情報を確認中..."):
        success, message, user = user_service.login_user(name)
        user_exists = user is not None
    
    return user_exists

def display_messages():
    """
    Display error and popup messages
    """
    # Error messages
    if 'error_message' in st.session_state and st.session_state.error_message:
        st.error(st.session_state.error_message, icon="⚠️")
        del st.session_state.error_message

    # Popup messages
    if 'popup_message' in st.session_state and st.session_state.popup_message:
        if st.session_state.popup_type == "new_user":
            st.success(st.session_state.popup_message, icon="🎉")
        elif st.session_state.popup_type == "existing_user":
            st.info(st.session_state.popup_message)
        # Clear popup after display
        del st.session_state.popup_message
        del st.session_state.popup_type

def handle_submit(intent: str):
    """
    Handle button clicks for registration and login
    """
    name = st.session_state.get("user_name_input", "")
    if name and name.strip():
        name = name.strip()
        
        # Use fragment for user validation
        user_exists = handle_user_validation(name)
        
        user_service = UserService()
        
        if intent == 'play':  # New user registration
            if user_exists:
                # Existing user - show popup message and prompt to use login button
                st.session_state.popup_message = f"⚠️ 「{name}」は既に登録済みです。登録済みの方は下の「登録済みの方はこちら」ボタンからログインしてください。"
                st.session_state.popup_type = "existing_user"
            else:
                # New user registration
                with st.spinner("新規登録中..."):
                    success, message, user = user_service.register_user(name)
                if success and user:
                    st.session_state.popup_message = f"登録完了！{name}さん、ようこそSnowVillageへ！"
                    st.session_state.popup_type = "new_user"
                    st.session_state.result = {
                        "name": name,
                        "intent": "new_user",
                        "user": user
                    }
                else:
                    st.session_state.error_message = message
        
        elif intent == 'login':  # Existing user login
            if not user_exists:
                st.session_state.error_message = f"「{name}」は登録されていません。新規登録してください。"
            else:
                with st.spinner("ログイン中..."):
                    success, message, user = user_service.login_user(name)
                if success and user:
                    st.session_state.result = {
                        "name": name,
                        "intent": "existing_user",
                        "user": user
                    }
                else:
                    st.session_state.error_message = f"「{name}」は登録済みですが、ログインに失敗しました。管理者にお問い合わせください。"
        
        # Clear error messages if not login intent
        if 'error_message' in st.session_state and intent != 'login':
            if 'error_message' in st.session_state:
                del st.session_state.error_message
    else:
        # Validation failed
        st.session_state.error_message = "名前を入力してください"

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
    logo_path = os.path.join(base_dir, "frontend", "public", "SnowVillageLogo-white.png")
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
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        # Snowflake logo or icon (centered for mobile)
        if logo_base64:
            st.markdown(
                f'<div style="display: flex; justify-content: center; align-items: center; width: 100%; margin-bottom: 1rem;"><img src="data:image/png;base64,{logo_base64}" width="60" style="margin: 0 auto;"></div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown("<div style='font-size: 40px; color: #4FC3F7; text-align: center; display: flex; justify-content: center; width: 100%; margin-bottom: 1rem;'>❄️</div>", unsafe_allow_html=True)

        # Text content
        st.markdown("""
        <style>
        .mobile-title {
            font-size: 3rem;
        }
        @media (max-width: 768px) {
            .mobile-title {
                font-size: 2.2rem;
            }
        }
        @media (max-width: 480px) {
            .mobile-title {
                font-size: 1.8rem;
            }
        }
        </style>
        <div style="text-align: center; width: 100%;">
            <h1 class="mobile-title" style="color: #4FC3F7; font-weight: 700; margin: 0 0 0.8rem 0; padding: 0; line-height: 1; text-align: center; display: block;">SnowVillage GO</h1>
            <p style="color: #E0E0E0; font-size: 1.1rem; margin: 0 auto 1.2rem auto; padding: 0; line-height: 1.2; text-align: center; display: block; font-weight: 600;">Snowflake World Tour Tokyo</p>
            <div style="color: #94a3b8; font-size: 0.8rem; text-align: center; line-height: 1.4; margin: 0 auto 1rem auto; display: block;">
                ✓ SWTTokyoをもっと楽しもう！<br>
                ✓ コミュニティミッションにチャレンジ<br>
                ✓ 気軽に投稿できる質問フォーム
            </div>
            <div style="color: #94a3b8; font-size: 0.7rem; text-align: center; margin: 0 auto 1.5rem auto; display: block;">※登録名でユーザー識別します。他の人とかぶらなさそうな自由な名前をつかってね！</div>
        </div>
        """, unsafe_allow_html=True)

        st.text_input(
            "名前",
            placeholder="ユーザー名の入力",
            key="user_name_input",
            label_visibility="collapsed"
        )

        # Display messages using fragment
        display_messages()
        
        st.button("ユーザー登録する", use_container_width=True, on_click=handle_submit, args=('play',))
        st.button("遊びに行く！", use_container_width=True, on_click=handle_submit, args=('login',))
        
    
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
        st.session_state.authenticated_user = login_result.get('user')
        
        if login_result['intent'] == 'new_user':
            st.snow()
            st.success(f"🎉 ようこそ {st.session_state.user_info['name']} さん！")
            st.info("ダッシュボードへ移動します...")
            time.sleep(4)
            st.switch_page("pages/dashboard.py")
        elif login_result['intent'] == 'existing_user':
            st.snow()
            st.success(f"おかえりなさい {st.session_state.user_info['name']} さん！")
            st.info("ダッシュボードへ移動します...")
            time.sleep(4)
            st.switch_page("pages/dashboard.py")

if __name__ == "__main__":
    main()