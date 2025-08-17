"""
匿名投稿ページ
"""
import streamlit as st
import os
import base64


# ページ設定
st.set_page_config(
    page_title="Snow Village - 匿名投稿",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="expanded"
)

# サイドバーのスタイル設定
st.markdown("""
<style>
    .sidebar-content {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


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
    bg_path = os.path.join(base_dir, "frontend", "public", "dashboard.png")
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
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 2rem;
            margin: 2rem auto;
            max-width: 800px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }}
        
        .post-header {{
            text-align: center;
            color: #1a237e;
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }}
        
        .form-container {{
            background: #ffffff;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}
        
        .info-box {{
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 5px;
        }}
        
        .warning-box {{
            background: #fff3e0;
            border-left: 4px solid #ff9800;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 5px;
        }}
        
        .success-box {{
            background: #e8f5e8;
            border-left: 4px solid #4caf50;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 5px;
        }}
        
        .error-box {{
            background: #ffebee;
            border-left: 4px solid #f44336;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 5px;
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
        
        /* 無効化されたボタンのホバーエフェクトを無効化 */
        .stButton > button:disabled:hover {{
            color: #9ca3af !important;
        }}
        
        .stButton > button:disabled {{
            background: #ccc;
            color: #666;
        }}
        
        /* 送信ボタン専用スタイル */
        .send-button {{
            background: #4caf50 !important;
        }}
        
        .send-button:hover {{
            background: #45a049 !important;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    # サイドバーにナビゲーション
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 1rem;">
            <span class="material-icons" style="font-size: 2rem; color: #ffffff;">account_circle</span>
            <h3 style="margin: 0.5rem 0; color: #ffffff; font-weight: 600;">こんにちは{user.username}さん</h3>
            <div style="color: #ffffff; font-size: 0.875rem; margin-top: 0.5rem; font-weight: 500;">
                <span class="material-icons" style="font-size: 1rem; vertical-align: middle; margin-right: 0.5rem;">schedule</span>
                {user.created_at.strftime('%Y年%m月%d日 %H:%M')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<h4 style="margin: 0 0 1rem 0; color: #ffffff; font-weight: 600;"><span class="material-icons" style="vertical-align: middle; margin-right: 0.5rem;">menu</span>メニュー</h4>', unsafe_allow_html=True)
        
        if st.button("ダッシュボード", use_container_width=True, key="nav_dashboard"):
            st.switch_page("pages/dashboard.py")
        
        if st.button("ランキング", use_container_width=True, key="nav_ranking"):
            st.switch_page("pages/ranking.py")
            
        if st.button("匿名投稿", use_container_width=True, disabled=True, key="nav_post"):
            pass  # 現在のページ
    
    # メインコンテンツ
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # ヘッダー
    st.markdown('<h1 class="post-header">📝 匿名投稿</h1>', unsafe_allow_html=True)
    
    # 投稿フォーム表示
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    display_post_form(user)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 戻るボタン
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("📊 ダッシュボードに戻る", use_container_width=True, type="primary"):
        st.switch_page("pages/dashboard.py")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def display_post_form(user):
    """投稿フォームの表示"""
    from slack_client import SlackClient
    
    # Slack設定確認
    slack_client = SlackClient()
    
    if not slack_client.is_configured():
        st.markdown("""
        <div class="error-box">
            <strong>⚠️ Slack設定エラー</strong><br>
            Slack Botの設定が正しく行われていません。<br>
            管理者にお問い合わせください。
        </div>
        """, unsafe_allow_html=True)
        return
    
    # 使い方説明
    st.markdown("""
    <div class="info-box">
        <strong>📢 匿名投稿について</strong><br>
        • あなたの投稿は完全に匿名でSlackチャンネルに送信されます<br>
        • 投稿者の名前は表示されません<br>
        • 送信時刻のみが記録されます<br>
        • 一度送信したメッセージは取り消せません
    </div>
    """, unsafe_allow_html=True)
    
    # 接続状態表示
    with st.expander("🔧 Slack接続状態", expanded=False):
        if st.button("接続テスト", key="test_connection"):
            with st.spinner("接続をテスト中..."):
                success, message = slack_client.test_connection()
                if success:
                    st.success(f"✅ {message}")
                else:
                    st.error(f"❌ {message}")
    
    st.markdown("### 📝 メッセージを入力")
    
    # 投稿フォーム
    with st.form(key="anonymous_post_form", clear_on_submit=True):
        message = st.text_area(
            "投稿内容",
            placeholder="ここにメッセージを入力してください...\n\n例:\n- イベントの感想\n- 技術的な質問\n- 改善提案\n- その他のフィードバック",
            height=150,
            max_chars=2000,
            help="最大2000文字まで入力できます"
        )
        
        # 文字数カウンター
        if message:
            char_count = len(message)
            color = "red" if char_count > 2000 else "green" if char_count > 1500 else "gray"
            st.markdown(f'<p style="text-align: right; color: {color}; font-size: 0.8em;">文字数: {char_count}/2000</p>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 送信ボタン
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button(
                "🚀 匿名で送信",
                use_container_width=True,
                type="primary"
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
            <strong>⚠️ 入力エラー</strong><br>
            メッセージを入力してください。
        </div>
        """, unsafe_allow_html=True)
        return
    
    if len(message) > 2000:
        st.markdown("""
        <div class="warning-box">
            <strong>⚠️ 文字数エラー</strong><br>
            メッセージは2000文字以内で入力してください。
        </div>
        """, unsafe_allow_html=True)
        return
    
    # 送信処理
    with st.spinner("📤 Slackに送信中..."):
        success, result_message = slack_client.send_anonymous_message(
            message=message,
            username=user.username  # ログ用（Slackには表示されない）
        )
    
    # 結果表示
    if success:
        # 成功ポップアップ
        st.markdown("""
        <div class="success-box">
            <strong>🎉 送信完了！</strong><br>
            メッセージが正常に送信されました。<br>
            Slackチャンネルをご確認ください。
        </div>
        """, unsafe_allow_html=True)
        
        # 成功時のバルーン効果
        st.balloons()
        
        # セッション状態をクリア（フォームリセット用）
        if 'form_submitted' not in st.session_state:
            st.session_state.form_submitted = True
            st.rerun()
            
    else:
        # エラー表示
        st.markdown(f"""
        <div class="error-box">
            <strong>❌ 送信失敗</strong><br>
            {result_message}
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()