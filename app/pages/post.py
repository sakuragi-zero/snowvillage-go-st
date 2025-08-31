"""
匿名投稿ページ
"""
import streamlit as st
import os
import base64


# ページ設定
st.set_page_config(
    page_title="Snow Village - 匿名投稿",
    page_icon="edit",
    layout="centered",
    initial_sidebar_state="collapsed"
)



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
        st.info("ログインページにリダイレクトしています...")
        st.switch_page("main.py")
    
    user_info = st.session_state.user_info
    user = user_info.get('user')
    
    # 背景設定
    base_dir = os.path.dirname(os.path.dirname(__file__))
    bg_path = os.path.join(base_dir, "frontend", "public", "SnowVillageGO-white.png")
    bg_base64 = get_base64_img(bg_path)
    
    bg_style = "background: linear-gradient(135deg, #1a237e, #283593, #3949ab, #42a5f5);"
    if bg_base64:
        bg_style = f"background: url(data:image/png;base64,{bg_base64}) no-repeat center center fixed; background-size: cover;"
    
    st.markdown(f"""
    <!-- Material Icons CDN -->
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        /* 背景設定 */
        .stApp {{ 
            {bg_style} 
        }}
        
        /* Streamlitのデフォルト白い枠・余白を除去 */
        .main .block-container {{
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
            max-width: 100%;
        }}
        
        /* ヘッダー除去 */
        header[data-testid="stHeader"] {{
            display: none;
        }}
        
        /* メインコンテナ */
        .main-container {{
            background: rgba(255, 255, 255, 0.98);
            border-radius: 24px;
            padding: 2.5rem;
            margin: 2rem auto;
            max-width: 900px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1), 0 8px 25px rgba(0, 0, 0, 0.08);
            backdrop-filter: blur(10px);
        }}
        
        .post-header {{
            text-align: center;
            background: linear-gradient(135deg, #1a237e, #3949ab);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 2rem;
            letter-spacing: -0.5px;
            line-height: 1.2;
            text-shadow: 0 2px 4px rgba(26, 35, 126, 0.3);
        }}
        
        .form-container {{
            background: #ffffff;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}
        
        /* フォーム背景を透明に設定 */
        div[data-testid="stForm"] {{
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
            margin: 0 !important;
        }}
        
        .info-box {{
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 5px;
            color: #000000;
        }}
        
        .warning-box {{
            background: #fff3e0;
            border-left: 4px solid #ff9800;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 5px;
            color: #000000;
        }}
        
        .success-box {{
            background: #e8f5e8;
            border-left: 4px solid #4caf50;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 5px;
            color: #000000;
        }}
        
        .error-box {{
            background: #ffebee;
            border-left: 4px solid #f44336;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 5px;
            color: #000000;
        }}
        
        .back-btn {{
            margin-top: 2rem;
            text-align: center;
        }}
        
        /* ボタンスタイル調整 */
        .stButton > button {{
            background: #1a237e;
            color: white;
            border-radius: 10px;
            border: none;
            padding: 0.5rem 1rem;
        }}
        
        .stButton > button:hover {{
            background: #283593;
            color: #90ee90 !important;
            transition: color 0.3s ease;
        }}
        
        .stButton > button:disabled {{
            background: #f3f4f6 !important;
            color: #9ca3af !important;
            transform: none !important;
            box-shadow: none !important;
        }}
        
        /* 無効化されたボタンのホバーエフェクトを無効化 */
        .stButton > button:disabled:hover {{
            color: #9ca3af !important;
        }}
        
        /* フォーム送信ボタンのスタイル統一 */
        div[data-testid="stForm"] .stButton > button {{
            background: #1a237e !important;
            color: white !important;
            border-radius: 10px !important;
            border: none !important;
            padding: 0.5rem 1rem !important;
        }}
        
        div[data-testid="stForm"] .stButton > button:hover {{
            background: #283593 !important;
            color: #90ee90 !important;
            transition: color 0.3s ease !important;
        }}
        
        /* サイドバーを完全に非表示 */
        .stSidebar {{
            display: none !important;
        }}
        
        /* メインコンテナの調整（サイドバーなしのため全幅使用） */
        .main .block-container {{
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }}

        /* モバイル対応 */
        @media (max-width: 768px) {{
            /* メインコンテナの調整 */
            .main .block-container {{
                padding-bottom: 6rem !important;
            }}
        }}
        
    </style>
    """, unsafe_allow_html=True)
    
    
    # ヘッダー
    st.markdown('''
    <h1 class="post-header">
        <span class="material-icons" style="font-size: 3rem; vertical-align: middle; margin-right: 0.5rem; color: #1a237e;">help_outline</span>
        匿名質問
    </h1>
    ''', unsafe_allow_html=True)
    
    # ページ説明の追加
    st.markdown("""
    <div class="info-box">
        <strong><span class="material-icons" style="vertical-align: middle; margin-right: 0.25rem;">edit</span>このページについて</strong><br>
        このページは村民に匿名で質問を投稿できます。ぜひSnowVillageのSlackに参加して質問の回答を確認しよう！
    </div>
    """, unsafe_allow_html=True)
    
    # 投稿フォーム表示
    display_post_form(user)
    
    # 成功ダイアログの表示
    if st.session_state.get('show_success_dialog', False):
        show_success_dialog()
    
    # 下部ナビゲーションバー
    display_bottom_navigation()


@st.dialog("✅ 送信完了！")
def show_success_dialog():
    """送信成功ダイアログ"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <div style="font-size: 4rem; margin-bottom: 1.5rem;">
            💬
        </div>
        <h2 style="color: #10b981; font-weight: 700; margin-bottom: 1rem;">
            質問を送信しました！
        </h2>
        <p style="font-size: 1.2rem; line-height: 1.6; color: #10b981; font-weight: 600; margin-bottom: 1.5rem;">
            質問の回答が来ているか<br>
            SnowVillageのモヤモヤチャンネルを見に行こう！
        </p>
        <div style="background: #f0f9ff; border: 1px solid #0ea5e9; border-radius: 10px; padding: 1rem; margin: 1rem 0;">
            <p style="color: #0369a1; font-weight: 600; margin: 0;">
                💡 回答は匿名で投稿されるため、質問者の特定はできません
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ダイアログを閉じるボタン
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("確認しました", use_container_width=True, type="primary"):
            st.session_state.show_success_dialog = False
            st.balloons()  # 成功時のバルーン効果
            st.rerun()


def display_bottom_navigation():
    """下部ナビゲーションバーの表示"""
    
    # 3つのナビゲーションボタン
    col1, col2, col3 = st.columns(3)
    
    with col1:
        dashboard_button = st.button(
            "ミッションに挑戦", 
            key="bottom_nav_home", 
            use_container_width=True
        )
        if dashboard_button:
            st.switch_page("pages/dashboard.py")
    
    with col2:
        ranking_button = st.button(
            "ランキング", 
            key="bottom_nav_ranking", 
            use_container_width=True
        )
        if ranking_button:
            st.switch_page("pages/ranking.py")
    
    with col3:
        post_button = st.button(
            "匿名投稿", 
            key="bottom_nav_post", 
            disabled=True, 
            use_container_width=True
        )


def display_post_form(user):
    """投稿フォームの表示"""
    from slack_client import SlackClient
    
    # Slack設定確認
    slack_client = SlackClient()
    
    if not slack_client.is_configured():
        st.markdown("""
        <div class="error-box">
            <strong><span class="material-icons" style="vertical-align: middle; margin-right: 0.25rem;">warning</span>Slack設定エラー</strong><br>
            Slack Botの設定が正しく行われていません。<br>
            管理者にお問い合わせください。
        </div>
        """, unsafe_allow_html=True)
        return
    
    # 使い方説明
    st.markdown("""
    <div class="info-box">
        <strong><span class="material-icons" style="vertical-align: middle; margin-right: 0.25rem;">campaign</span>投稿について</strong><br>
        • あなたの投稿は完全に匿名でSlackチャンネルに送信されます<br>
        • 投稿者の名前は表示されません<br>
        • 送信時刻のみが記録されます<br>
        • 一度送信したメッセージは取り消せません
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('''
    <h3 style="background: linear-gradient(135deg, #1a237e, #3949ab); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-weight: 700; margin-bottom: 1rem;">
        投稿内容
    </h3>
    ''', unsafe_allow_html=True)
    
    # 投稿フォーム
    with st.form(key="anonymous_post_form", clear_on_submit=True):
        message = st.text_area(
            "メッセージ",
            placeholder="ここにメッセージを入力してください...\n\n例:\n- 技術的な質問\n- 実現したいデータ利活用シーン",
            height=150,
            max_chars=2000,
            help="最大2000文字まで入力できます",
            label_visibility="collapsed"
        )
        
        # 文字数カウンター
        if message:
            char_count = len(message)
            color = "red" if char_count > 2000 else "green" if char_count > 1500 else "gray"
            st.markdown(f'<p style="text-align: right; color: {color}; font-size: 0.8em;">文字数: {char_count}/2000</p>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 送信ボタン
        submitted = st.form_submit_button(
            "匿名で送信",
            use_container_width=True
        )
    
    # フォーム送信処理
    if submitted:
        handle_form_submission(message, slack_client, user)


def handle_form_submission(message: str, slack_client, user):
    """フォーム送信処理"""
    
    # バリデーション
    if not message or not message.strip():
        st.markdown("""
        <div class="warning-box">
            <strong><span class="material-icons" style="vertical-align: middle; margin-right: 0.25rem;">warning</span>入力エラー</strong><br>
            メッセージを入力してください。
        </div>
        """, unsafe_allow_html=True)
        return
    
    if len(message) > 2000:
        st.markdown("""
        <div class="warning-box">
            <strong><span class="material-icons" style="vertical-align: middle; margin-right: 0.25rem;">warning</span>文字数エラー</strong><br>
            メッセージは2000文字以内で入力してください。
        </div>
        """, unsafe_allow_html=True)
        return
    
    # 送信処理
    with st.spinner("Slackに送信中..."):
        success, result_message = slack_client.send_anonymous_message(
            message=message,
            username=user.username  # ログ用（Slackには表示されない）
        )
    
    # 結果表示
    if success:
        # ダイアログ表示フラグを設定
        st.session_state.show_success_dialog = True
        st.rerun()
            
    else:
        # エラー表示
        st.markdown(f"""
        <div class="error-box">
            <strong><span class="material-icons" style="vertical-align: middle; margin-right: 0.25rem;">error</span>送信失敗</strong><br>
            {result_message}
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()