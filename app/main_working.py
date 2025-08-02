"""SnowVillage GO メインアプリケーション - 動作版"""

import streamlit as st
import sys
import os
import base64

# プロジェクトルートをパスに追加
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'snowvillage_ui'))

from app.database.db_manager import get_db
from app.auth.auth_manager import AuthManager
from app.auth.session_manager import SessionManager
from app.pages.learning_page import LearningPage
from app.pages.challenge_page import ChallengePage


def main():
    """メインアプリケーション"""
    
    # ページ設定
    st.set_page_config(
        page_title="SnowVillage GO - Snowflake World Tour Tokyo 2025",
        page_icon="❄️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # サイドバーを非表示
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
    
    # データベース初期化
    db = get_db()
    auth_manager = AuthManager(db)
    session_manager = SessionManager(db)
    
    # ページ状態の初期化
    if 'page' not in st.session_state:
        st.session_state.page = "landing"
    
    # ページルーティング
    page = st.session_state.page
    
    if page == "landing":
        render_landing_page(auth_manager, session_manager)
    elif page == "learning":
        learning_page = LearningPage(db)
        learning_page.render()
    elif page == "challenge":
        challenge_page = ChallengePage(db)
        challenge_page.render()
    else:
        st.error("不明なページです。")
        st.session_state.page = "landing"
        st.rerun()


def render_landing_page(auth_manager: AuthManager, session_manager: SessionManager):
    """ランディングページをレンダリング"""
    
    # 既にログインしている場合は学習ページにリダイレクト
    if session_manager.is_logged_in():
        st.session_state.page = "learning"
        st.rerun()
    
    # 画像をbase64エンコード
    logo_base64 = ""
    bg_base64 = ""
    
    # ロゴ画像
    logo_path = os.path.join(os.path.dirname(__file__), "..", "snowvillage_ui", "frontend", "public", "SnowVillageLogo.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as img_file:
            logo_base64 = base64.b64encode(img_file.read()).decode()
    
    # 背景画像
    bg_path = os.path.join(os.path.dirname(__file__), "..", "snowvillage_ui", "frontend", "public", "bg-villag-go.png")
    if os.path.exists(bg_path):
        with open(bg_path, "rb") as img_file:
            bg_base64 = base64.b64encode(img_file.read()).decode()
    
    # 背景CSS
    if bg_base64:
        bg_style = f"background: url(data:image/png;base64,{bg_base64}) no-repeat center center fixed; background-size: cover;"
    else:
        bg_style = "background: linear-gradient(135deg, #1e2a78, #3730a3, #4338ca);"
    
    # 統合されたコンポーネント
    component_html = f"""
    <div style="
        {bg_style}
        min-height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    ">
        <div style="
            background: rgba(30, 41, 59, 0.9);
            border: 1px solid rgba(148, 163, 184, 0.3);
            border-radius: 16px;
            padding: 3rem 2.5rem;
            text-align: center;
            max-width: 450px;
            width: 100%;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        ">
            <!-- ロゴ -->
            <div style="margin-bottom: 1.5rem;">
                {"<img src='data:image/png;base64," + logo_base64 + "' style='width: 80px; height: 80px; margin: 0 auto; display: block;' alt='SnowVillage Logo'>" if logo_base64 else "<div style='width: 80px; height: 80px; margin: 0 auto; background: #60a5fa; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; color: white;'>❄️</div>"}
            </div>
            
            <!-- タイトル -->
            <h1 style="
                color: white;
                font-size: 3rem;
                font-weight: 700;
                margin-bottom: 0.5rem;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            ">SnowVillage GO</h1>
            
            <!-- サブタイトル -->
            <p style="
                color: #cbd5e1;
                font-size: 1.2rem;
                margin-bottom: 2rem;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            ">Snowflake World Tour Tokyo 2025</p>
            
            <!-- 機能リスト -->
            <div style="
                color: #94a3b8;
                font-size: 1rem;
                margin-bottom: 2rem;
            ">
                <div style="margin: 0.5rem 0;">✓ Snowflakeを知る</div>
                <div style="margin: 0.5rem 0;">✓ クエストとチャレンジ</div>
                <div style="margin: 0.5rem 0;">✓ ランキングと景品</div>
            </div>
            
            <!-- 入力フィールド -->
            <input 
                type="text" 
                id="userName"
                placeholder="名前を入力してください"
                style="
                    background: white;
                    border: 2px solid #e2e8f0;
                    border-radius: 12px;
                    padding: 1rem;
                    font-size: 1.1rem;
                    margin-bottom: 1rem;
                    width: 100%;
                    box-sizing: border-box;
                    color: #1f2937;
                "
            />
            
            <!-- 遊びに行くボタン -->
            <button 
                onclick="submitForm('play')"
                style="
                    background: white;
                    color: #3730a3;
                    border: none;
                    border-radius: 12px;
                    padding: 1rem 2rem;
                    font-size: 1.1rem;
                    font-weight: 600;
                    width: 100%;
                    height: 60px;
                    margin-bottom: 1rem;
                    cursor: pointer;
                    transition: all 0.3s ease;
                "
                onmouseover="this.style.background='#f8fafc'; this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 25px rgba(0, 0, 0, 0.15)'"
                onmouseout="this.style.background='white'; this.style.transform='translateY(0)'; this.style.boxShadow='none'"
            >遊びに行く！</button>
            
            <!-- 登録済みボタン -->
            <button 
                onclick="submitForm('login')"
                style="
                    background: transparent;
                    color: white;
                    border: 2px solid rgba(255, 255, 255, 0.3);
                    border-radius: 12px;
                    padding: 1rem 2rem;
                    font-size: 1.1rem;
                    font-weight: 600;
                    width: 100%;
                    height: 60px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                "
                onmouseover="this.style.background='rgba(255, 255, 255, 0.1)'; this.style.borderColor='rgba(255, 255, 255, 0.5)'"
                onmouseout="this.style.background='transparent'; this.style.borderColor='rgba(255, 255, 255, 0.3)'"
            >登録済みの方はこちら</button>
        </div>
    </div>
    
    <script>
        function submitForm(intent) {{
            const userName = document.getElementById('userName').value;
            if (!userName.trim()) {{
                alert('名前を入力してください');
                return;
            }}
            window.parent.postMessage({{
                type: 'submit',
                name: userName.trim(),
                intent: intent
            }}, '*');
        }}
    </script>
    """
    
    # コンポーネント表示
    result = st.components.v1.html(component_html, height=700, scrolling=False)
    
    # JavaScriptからの応答処理
    if result and result.get('type') == 'submit':
        name = result.get('name', '').strip()
        intent = result.get('intent', '')
        
        if name and intent in ['play', 'login']:
            # ユーザー認証または作成
            user = auth_manager.authenticate_or_create_user(name)
            
            if user:
                # セッション作成
                session_manager.login_user(user)
                
                # 成功メッセージ
                if intent == 'play':
                    st.success(f"🎉 ようこそ {user.name} さん！SnowVillage GOの世界へ！")
                else:
                    st.success(f"🎉 おかえりなさい {user.name} さん！")
                
                # 学習ページへリダイレクト
                st.session_state.page = "learning"
                st.rerun()
            else:
                st.error("ユーザーの作成または認証に失敗しました。")


if __name__ == "__main__":
    main()