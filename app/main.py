# """
# Snow Village - メインアプリケーション
# ログイン画面を表示し、成功後に他のページへ遷移します。
# """
# import streamlit as st
# import os
# import base64
# import time
# from app.database.db_manager import get_db
# from app.auth.auth_manager import AuthManager
# from app.auth.session_manager import SessionManager

# # --- ページ設定 (スクリプトの最初に一度だけ実行) ---
# st.set_page_config(
#     page_title="Snow Village GO",
#     page_icon="❄️",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # --- カスタムCSS (メニューとフッターを非表示) ---
# st.markdown("""
# <style>
# [data-testid="stSidebar"] { display: none; }
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# </style>
# """, unsafe_allow_html=True)


# def launch_screen_component():
#     """
#     ログイン/登録用のカスタムHTMLコンポーネントを表示し、
#     ユーザー操作の結果（ボタンクリック情報）を返します。
#     """
#     # 画像をbase64エンコード
#     logo_base64 = ""
#     logo_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "public", "SnowVillageLogo.png")
#     if os.path.exists(logo_path):
#         with open(logo_path, "rb") as img_file:
#             logo_base64 = base64.b64encode(img_file.read()).decode()
    
#     logo_html = f"""
#     <div style="margin-bottom: 1.5rem;">
#         <img src="data:image/png;base64,{logo_base64}" style="width: 80px; height: 80px; margin: 0 auto; display: block;" alt="Logo">
#     </div>
#     """ if logo_base64 else ""

#     # --- HTML, CSS, JavaScriptを定義 ---
#     component_html = f"""
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <style>
#         .card {{
#             background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(148, 163, 184, 0.3);
#             border-radius: 16px; padding: 3rem 2.5rem; text-align: center; max-width: 450px;
#             width: 100%; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3); margin: 0 auto;
#         }}
#         h1 {{ color: white; font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; }}
#         p {{ color: #cbd5e1; font-size: 1.1rem; margin-bottom: 2rem; }}
#         .features {{ color: #94a3b8; font-size: 1rem; margin-bottom: 2rem; }}
#         input[type="text"] {{
#             background: white; border: 2px solid #e2e8f0; border-radius: 12px; padding: 1rem;
#             font-size: 1.1rem; margin-bottom: 1rem; width: 100%; box-sizing: border-box;
#         }}
#         button {{
#             border-radius: 12px; padding: 1rem; font-size: 1.1rem; font-weight: 600;
#             width: 100%; height: 60px; margin-bottom: 1rem; cursor: pointer; transition: all 0.3s ease;
#         }}
#         .primary-btn {{ background: white; color: #3730a3; border: none; }}
#         .secondary-btn {{ background: transparent; color: white; border: 2px solid rgba(255, 255, 255, 0.3); }}
#     </style>
#     <div class="card">
#         {logo_html}
#         <h1>SnowVillage GO</h1>
#         <p>Snowflake World Tour Tokyo 2025</p>
#         <div class="features">
#             <div style="margin: 0.5rem 0;">✓ Snowflakeを知る</div>
#             <div style="margin: 0.5rem 0;">✓ クエストとチャレンジ</div>
#             <div style="margin: 0.5rem 0;">✓ ランキングと景品</div>
#         </div>
#         <input type="text" id="userName" placeholder="名前を入力してください">
#         <button onclick="submitForm('play')" class="primary-btn">遊びに行く！</button>
#         <button onclick="submitForm('login')" class="secondary-btn">登録済みの方はこちら</button>
#     </div>
#     <script>
#         function submitForm(intent) {{
#             const userName = document.getElementById('userName').value;
#             if (!userName.trim()) {{
#                 // Streamlitにエラーメッセージ表示を依頼
#                 window.parent.postMessage({{type: 'error', message: '名前を入力してください'}}, '*');
#                 return;
#             }}
#             // Streamlitにsubmitイベントを送信
#             window.parent.postMessage({{type: 'submit', name: userName.trim(), intent: intent}}, '*');
#         }}
#     </script>
#     """
    
#     # --- コンポーネントを表示し、返り値を受け取る ---
#     # この`st.components.v1.html`は、JavaScriptの`postMessage`で送られた値を返す
#     component_value = st.components.v1.html(component_html, height=700)
#     return component_value


# # ==================================================================
# # --- アプリケーションのメイン実行ブロック ---
# # ==================================================================

# # データベースと認証マネージャーを初期化
# db_manager = get_db()
# auth_manager = AuthManager(db_manager)
# session_manager = SessionManager(db_manager)

# # ログイン状態をセッションで管理
# if 'logged_in' not in st.session_state:
#     st.session_state.logged_in = False

# # --- ページ遷移のロジック ---
# # ログインしていない場合、ログイン画面を表示
# if not st.session_state.logged_in:
    
#     # カスタムコンポーネントを表示し、ユーザー操作の結果を受け取る
#     result = launch_screen_component()

#     # コンポーネントから結果が返ってきた場合（ボタンが押された場合）
#     if result:
#         # エラーメッセージが送られてきた場合
#         if result.get("type") == "error":
#             st.error(result.get("message", "エラーが発生しました。"))
        
#         # submitイベントが送られてきた場合
#         elif result.get("type") == "submit":
#             user_name = result.get("name")
            
#             # ユーザー認証・作成
#             user = auth_manager.authenticate_or_create_user(user_name)

#             if user:
#                 # ログイン成功
#                 session_manager.login_user(user) # Streamlitのセッションにユーザー情報を保存
#                 st.session_state.logged_in = True
#                 st.rerun() # ページを再読み込みして学習ページに遷移
#             else:
#                 st.error("ユーザーの作成または認証に失敗しました。")

# # ログインしている場合、学習ページへ
# else:
#     # ウェルカムメッセージを表示（初回のみ）
#     if 'welcome_message_shown' not in st.session_state:
#         st.balloons()
#         st.success(f"🎉 ようこそ {st.session_state.user_name} さん！")
#         time.sleep(2)
#         st.session_state.welcome_message_shown = True

#     # 学習ページに遷移
#     st.switch_page("pages/learning_page.py")

"""
Snow Village - メインアプリケーション
ログイン画面を表示し、成功後に他のページへ遷移します。
"""
import streamlit as st
import os
import base64
import time
# --- ここから修正 ---
# 'app' を付けずに、同じディレクトリ内のモジュールを直接インポート
from app.database.db_manager import get_db
from app.auth.auth_manager import AuthManager
from app.auth.session_manager import SessionManager
# --- ここまで修正 ---

# --- ページ設定 (スクリプトの最初に一度だけ実行) ---
st.set_page_config(
    page_title="Snow Village GO",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- カスタムCSS (メニューとフッターを非表示) ---
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


def launch_screen_component():
    """
    ログイン/登録用のカスタムHTMLコンポーネントを表示し、
    ユーザー操作の結果（ボタンクリック情報）を返します。
    """
    # 画像をbase64エンコード
    logo_base64 = ""
    # --- パスを修正 ---
    logo_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "public", "SnowVillageLogo.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as img_file:
            logo_base64 = base64.b64encode(img_file.read()).decode()

    logo_html = f"""
    <div style="margin-bottom: 1.5rem;">
        <img src="data:image/png;base64,{logo_base64}" style="width: 80px; height: 80px; margin: 0 auto; display: block;" alt="Logo">
    </div>
    """ if logo_base64 else ""

    # --- HTML, CSS, JavaScriptを定義 ---
    component_html = f"""
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        .card {{
            background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(148, 163, 184, 0.3);
            border-radius: 16px; padding: 3rem 2.5rem; text-align: center; max-width: 450px;
            width: 100%; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3); margin: 0 auto;
        }}
        h1 {{ color: white; font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; }}
        p {{ color: #cbd5e1; font-size: 1.1rem; margin-bottom: 2rem; }}
        .features {{ color: #94a3b8; font-size: 1rem; margin-bottom: 2rem; }}
        input[type="text"] {{
            background: white; border: 2px solid #e2e8f0; border-radius: 12px; padding: 1rem;
            font-size: 1.1rem; margin-bottom: 1rem; width: 100%; box-sizing: border-box;
        }}
        button {{
            border-radius: 12px; padding: 1rem; font-size: 1.1rem; font-weight: 600;
            width: 100%; height: 60px; margin-bottom: 1rem; cursor: pointer; transition: all 0.3s ease;
        }}
        .primary-btn {{ background: white; color: #3730a3; border: none; }}
        .secondary-btn {{ background: transparent; color: white; border: 2px solid rgba(255, 255, 255, 0.3); }}
    </style>
    <div class="card">
        {logo_html}
        <h1>SnowVillage GO</h1>
        <p>Snowflake World Tour Tokyo 2025</p>
        <div class="features">
            <div style="margin: 0.5rem 0;">✓ Snowflakeを知る</div>
            <div style="margin: 0.5rem 0;">✓ クエストとチャレンジ</div>
            <div style="margin: 0.5rem 0;">✓ ランキングと景品</div>
        </div>
        <input type="text" id="userName" placeholder="名前を入力してください">
        <button onclick="submitForm('play')" class="primary-btn">遊びに行く！</button>
        <button onclick="submitForm('login')" class="secondary-btn">登録済みの方はこちら</button>
    </div>
    <script>
        function submitForm(intent) {{
            const userName = document.getElementById('userName').value;
            if (!userName.trim()) {{
                window.parent.postMessage({{type: 'error', message: '名前を入力してください'}}, '*');
                return;
            }}
            window.parent.postMessage({{type: 'submit', name: userName.trim(), intent: intent}}, '*');
        }}
    </script>
    """
    
    component_value = st.components.v1.html(component_html, height=700, scrolling=False)
    return component_value


# ==================================================================
# --- アプリケーションのメイン実行ブロック ---
# ==================================================================

# データベースと認証マネージャーを初期化
db_manager = get_db()
auth_manager = AuthManager(db_manager)
session_manager = SessionManager(db_manager)

# ログイン状態をセッションで管理
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# ログインしていない場合、ログイン画面を表示
if not st.session_state.logged_in:
    result = launch_screen_component()

    if result:
        if result.get("type") == "error":
            st.error(result.get("message", "エラーが発生しました。"))
        
        elif result.get("type") == "submit":
            user_name = result.get("name")
            user = auth_manager.authenticate_or_create_user(user_name)

            if user:
                session_manager.login_user(user)
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("ユーザーの作成または認証に失敗しました。")

# ログインしている場合、学習ページへ
else:
    if 'welcome_message_shown' not in st.session_state:
        st.balloons()
        st.success(f"🎉 ようこそ {st.session_state.user_name} さん！")
        st.session_state.welcome_message_shown = True
        time.sleep(2)

    st.switch_page("pages/learning_page.py")