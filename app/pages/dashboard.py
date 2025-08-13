"""
Simple Dashboard Page
"""
import streamlit as st
import os
import base64

# ページ設定
st.set_page_config(
    page_title="Snow Village - Dashboard",
    page_icon="❄️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# サイドバーを非表示
st.markdown("<style>[data-testid='stSidebar'] { display: none; }</style>", unsafe_allow_html=True)


def get_base64_img(path):
    """画像をbase64エンコード"""
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""


def main():
    """メイン関数"""
    # 認証チェック
    if 'user_info' not in st.session_state or not st.session_state.user_info:
        st.error("ログインが必要です")
        st.stop()
    
    user_info = st.session_state.user_info
    user = user_info.get('user')
    
    # 背景設定
    base_dir = os.path.dirname(os.path.dirname(__file__))
    bg_path = os.path.join(base_dir, "frontend", "public", "bg-villag-go.png")
    bg_base64 = get_base64_img(bg_path)
    
    bg_style = "background: linear-gradient(135deg, #1a237e, #283593, #3949ab, #42a5f5);"
    if bg_base64:
        bg_style = f"background: url(data:image/png;base64,{bg_base64}) no-repeat center center fixed; background-size: cover;"
    
    st.markdown(f"""
    <style>
        .stApp {{ {bg_style} }}
        .main-container {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 2rem;
            margin: 2rem auto;
            max-width: 800px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }}
        .welcome-header {{
            text-align: center;
            color: #1a237e;
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }}
        .user-info {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
        }}
        .logout-btn {{
            margin-top: 2rem;
            text-align: center;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    # メインコンテンツ
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # ヘッダー
    st.markdown('<h1 class="welcome-header">❄️ Snow Village Dashboard</h1>', unsafe_allow_html=True)
    
    # ウェルカムメッセージ
    st.markdown(f"## Hello, {user.username}! 🎉")
    
    # ユーザー情報
    st.markdown('<div class="user-info">', unsafe_allow_html=True)
    st.markdown("### ユーザー情報")
    st.markdown(f"**ユーザー名:** {user.username}")
    st.markdown(f"**登録日時:** {user.created_at.strftime('%Y年%m月%d日 %H:%M')}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # シンプルなメッセージ
    st.success("ログイン成功！Welcome to Snow Village! 🏔️")
    
    # ログアウトボタン
    st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
    if st.button("ログアウト", use_container_width=True, type="primary"):
        # セッションクリア
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()