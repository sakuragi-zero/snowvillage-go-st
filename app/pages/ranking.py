"""
ランキングページ
"""
import streamlit as st
import os
import base64


# ページ設定
st.set_page_config(
    page_title="Snow Village - ランキング",
    page_icon="🏆",
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
        
        .ranking-header {{
            text-align: center;
            color: #1a237e;
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }}
        
        .ranking-container {{
            background: #ffffff;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}
        
        .rank-item {{
            display: flex;
            align-items: center;
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 8px;
            background: #f8f9fa;
        }}
        
        .rank-number {{
            font-size: 1.5rem;
            font-weight: bold;
            margin-right: 1rem;
            min-width: 3rem;
            text-align: center;
        }}
        
        .rank-1 {{ background: linear-gradient(45deg, #FFD700, #FFA500); color: white; }}
        .rank-2 {{ background: linear-gradient(45deg, #C0C0C0, #A9A9A9); color: white; }}
        .rank-3 {{ background: linear-gradient(45deg, #CD7F32, #B8860B); color: white; }}
        
        .user-info {{
            flex-grow: 1;
        }}
        
        .username {{
            font-weight: bold;
            font-size: 1.1rem;
        }}
        
        .task-count {{
            color: #666;
            font-size: 0.9rem;
        }}
        
        .completion-date {{
            color: #999;
            font-size: 0.8rem;
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
    </style>
    """, unsafe_allow_html=True)
    
    # サイドバーにユーザー情報を表示
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
        
        if st.button("ランキング", use_container_width=True, disabled=True, key="nav_ranking"):
            pass  # 現在のページ
            
        if st.button("匿名投稿", use_container_width=True, key="nav_post"):
            st.switch_page("pages/post.py")
    
    # ヘッダー
    st.markdown('''
    <h1 class="ranking-header">
        <span class="material-icons" style="font-size: 3rem; vertical-align: middle; margin-right: 0.5rem; color: #1a237e;">leaderboard</span>
        ユーザーランキング
    </h1>
    ''', unsafe_allow_html=True)
    
    # ランキング表示
    display_ranking()
    
    # 戻るボタン
    if st.button("ダッシュボードに戻る", use_container_width=True, type="primary"):
        st.switch_page("pages/dashboard.py")


def display_ranking():
    """ランキング表示"""
    from task_db import TaskService
    
    task_service = TaskService()
    ranking_data = task_service.get_user_ranking()
    
    if not ranking_data:
        st.info("まだランキングデータがありません。")
        return
    
    st.markdown('''
    <h3 style="color: #1a237e; display: flex; align-items: center; margin-bottom: 1rem;">
        <span class="material-icons" style="font-size: 1.5rem; margin-right: 0.5rem;">trending_up</span>
        タスク完了数ランキング（上位10位）
    </h3>
    ''', unsafe_allow_html=True)
    st.caption("同じタスク数の場合は、最初に到達したユーザーが上位になります")
    
    for i, rank_data in enumerate(ranking_data, 1):
        username = rank_data['username']
        completed_tasks = rank_data['completed_tasks']
        first_completion = rank_data['first_completion']
        
        # ランク別スタイル
        rank_class = ""
        rank_display = ""
        if i == 1:
            rank_class = "rank-1"
            rank_display = '<span class="material-icons" style="font-size: 1.5rem; color: #1a1a1a; text-shadow: 0 0 3px #FFD700;">workspace_premium</span>'
        elif i == 2:
            rank_class = "rank-2"
            rank_display = '<span class="material-icons" style="font-size: 1.5rem; color: #1a1a1a; text-shadow: 0 0 3px #C0C0C0;">workspace_premium</span>'
        elif i == 3:
            rank_class = "rank-3"
            rank_display = '<span class="material-icons" style="font-size: 1.5rem; color: #1a1a1a; text-shadow: 0 0 3px #CD7F32;">workspace_premium</span>'
        else:
            rank_display = f'<span style="font-weight: bold; color: #1a1a1a;">{i}位</span>'
        
        # 完了日時の表示
        completion_text = ""
        if first_completion and completed_tasks > 0:
            completion_text = f"初回完了: {first_completion.strftime('%Y年%m月%d日 %H:%M')}"
        elif completed_tasks == 0:
            completion_text = "タスク未完了"
        
        st.markdown(f"""
        <div class="rank-item {rank_class}">
            <div class="rank-number">{rank_display}</div>
            <div class="user-info">
                <div class="username">{username}</div>
                <div class="task-count">完了タスク数: {completed_tasks}個</div>
                <div class="completion-date">{completion_text}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()