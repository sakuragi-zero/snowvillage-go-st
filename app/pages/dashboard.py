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
        /* 基本設定 */
        * {{
            box-sizing: border-box;
        }}
        
        /* 背景設定 */
        .stApp {{ 
            {bg_style}
            font-family: 'Inter', sans-serif;
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
        
        /* ヘッダー */
        .welcome-header {{
            text-align: center;
            color: #1a1a1a;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 2rem;
            letter-spacing: -0.5px;
        }}
        
        .header-icon {{
            color: #2563eb;
            margin-right: 0.5rem;
            vertical-align: middle;
        }}
        
        /* セクション見出し */
        .section-header {{
            display: flex;
            align-items: center;
            margin: 2rem 0 1rem 0;
            color: #374151;
            font-size: 1.5rem;
            font-weight: 600;
        }}
        
        .section-icon {{
            margin-right: 0.75rem;
            color: #2563eb;
            font-size: 1.75rem;
        }}
        
        /* タスクカテゴリー */
        .task-category {{
            margin: 2rem 0;
        }}
        
        /* ミッションカード */
        .mission-card {{
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border: 1px solid #e5e7eb;
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06), 0 2px 8px rgba(0, 0, 0, 0.04);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}
        
        .mission-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12), 0 6px 16px rgba(0, 0, 0, 0.08);
            border-color: #d1d5db;
        }}
        
        .mission-card.completed {{
            background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
            border-color: #a7f3d0;
        }}
        
        .mission-card.completed::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(180deg, #10b981 0%, #059669 100%);
        }}
        
        /* カード内容 */
        .card-content {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 1rem;
        }}
        
        .mission-info {{
            flex: 1;
        }}
        
        .mission-title {{
            font-size: 1.125rem;
            font-weight: 600;
            color: #111827;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
        }}
        
        .mission-type-icon {{
            margin-right: 0.5rem;
            font-size: 1.25rem;
        }}
        
        .quiz-icon {{ color: #7c3aed; }}
        .sns-icon {{ color: #dc2626; }}
        
        .mission-description {{
            color: #6b7280;
            font-size: 0.875rem;
            line-height: 1.5;
            margin-bottom: 1rem;
        }}
        
        .mission-status {{
            display: flex;
            align-items: center;
            font-size: 0.875rem;
            font-weight: 500;
        }}
        
        .status-completed {{
            color: #059669;
        }}
        
        .status-pending {{
            color: #d97706;
        }}
        
        .status-icon {{
            margin-right: 0.25rem;
            font-size: 1rem;
        }}
        
        /* アクションボタン */
        .mission-actions {{
            flex-shrink: 0;
        }}
        
        /* Material Design ボタン */
        .md-button {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.75rem 1.5rem;
            font-size: 0.875rem;
            font-weight: 500;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            text-decoration: none;
            position: relative;
            overflow: hidden;
            min-width: 100px;
        }}
        
        .md-button:before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255, 255, 255, 0.1);
            transform: translateY(100%);
            transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .md-button:hover:before {{
            transform: translateY(0);
        }}
        
        .md-button-primary {{
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            color: white;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        }}
        
        .md-button-primary:hover {{
            transform: translateY(-1px);
            box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4);
        }}
        
        .md-button-success {{
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        }}
        
        .md-button-secondary {{
            background: #f3f4f6;
            color: #374151;
            border: 1px solid #d1d5db;
        }}
        
        .md-button-secondary:hover {{
            background: #e5e7eb;
            border-color: #9ca3af;
        }}
        
        .md-button:disabled {{
            background: #f3f4f6 !important;
            color: #9ca3af !important;
            cursor: not-allowed;
            transform: none !important;
            box-shadow: none !important;
        }}
        
        .md-button-icon {{
            margin-right: 0.5rem;
            font-size: 1rem;
        }}
        
        /* 展開エリア */
        .mission-expand {{
            margin-top: 1.5rem;
            padding-top: 1.5rem;
            border-top: 1px solid #e5e7eb;
            border-radius: 12px;
            background: #f9fafb;
            padding: 1.5rem;
        }}
        
        /* Streamlit Expander 細かい調整 */
        [data-testid="stExpander"] {{
            background: #ffffff !important;
            border: 1px solid #e5e7eb !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1) !important;
            margin: 1rem 0 !important;
        }}
        
        [data-testid="stExpander"] > div {{
            background: #ffffff !important;
        }}
        
        [data-testid="stExpander"] summary {{
            background: #ffffff !important;
            color: #111827 !important;
            font-weight: 600 !important;
            border-radius: 12px !important;
            padding: 1rem !important;
        }}
        
        [data-testid="stExpander"] > div > div {{
            background: #ffffff !important;
            padding: 2rem !important;
        }}
        
        /* Expander内のテキスト要素のみ */
        [data-testid="stExpander"] .stMarkdown {{
            background: #ffffff !important;
            color: #111827 !important;
            font-weight: 600 !important;
        }}
        
        [data-testid="stExpander"] .stMarkdown p {{
            background: #ffffff !important;
            color: #111827 !important;
            font-weight: 600 !important;
        }}
        
        [data-testid="stExpander"] .stMarkdown strong {{
            background: #ffffff !important;
            color: #000000 !important;
            font-weight: 700 !important;
        }}
        
        /* ラジオボタンコンテナのみ */
        [data-testid="stExpander"] .stRadio {{
            background: #ffffff !important;
        }}
        
        [data-testid="stExpander"] .stRadio > div {{
            background: #ffffff !important;
        }}
        
        [data-testid="stExpander"] .stRadio label {{
            color: #111827 !important;
            font-weight: 600 !important;
        }}
        
        [data-testid="stExpander"] .stRadio label span {{
            color: #111827 !important;
            font-weight: 600 !important;
        }}
        
        /* ラジオボタンの選択肢テキスト */
        [data-testid="stExpander"] .stRadio label p {{
            color: #111827 !important;
            font-weight: 600 !important;
            background: #ffffff !important;
        }}
        
        [data-testid="stExpander"] .stRadio div p {{
            color: #111827 !important;
            font-weight: 600 !important;
            background: #ffffff !important;
        }}
        
        /* ラジオボタンの選択部分は元のスタイルを維持 */
        [data-testid="stExpander"] .stRadio input[type="radio"] {{
            background: initial !important;
        }}
        
        /* カラム要素のコンテナのみ */
        [data-testid="stExpander"] .stColumns {{
            background: #ffffff !important;
        }}
        
        [data-testid="stExpander"] .stColumn {{
            background: #ffffff !important;
        }}
        
        /* ボタンは元のスタイルを維持 */
        [data-testid="stExpander"] .stButton {{
            background: transparent !important;
        }}
        
        [data-testid="stExpander"] .stButton button {{
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            color: #ffffff !important;
        }}
        
        /* ボタン内のテキストも白色を保持 */
        [data-testid="stExpander"] .stButton button p {{
            color: #ffffff !important;
            background: transparent !important;
        }}
        
        /* Streamlitアラート（success/error/info）のテキスト */
        [data-testid="stExpander"] .stAlert {{
            background: #ffffff !important;
        }}
        
        [data-testid="stExpander"] .stAlert p {{
            color: #111827 !important;
            font-weight: 600 !important;
            background: #ffffff !important;
        }}
        
        [data-testid="stExpander"] .stAlert div {{
            background: #ffffff !important;
        }}
        
        /* エラー・成功メッセージの強制スタイル */
        [data-testid="stExpander"] [data-testid="stAlert"] {{
            background: #ffffff !important;
        }}
        
        [data-testid="stExpander"] [data-testid="stAlert"] p {{
            color: #111827 !important;
            font-weight: 600 !important;
            background: #ffffff !important;
        }}
        
        /* ミッションクリアポップアップ */
        .mission-clear-popup {{
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 3rem 4rem;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            z-index: 10000;
            text-align: center;
            animation: popupAnimation 0.5s ease-out;
        }}
        
        .mission-clear-popup h1 {{
            font-size: 2.5rem;
            margin-bottom: 1rem;
            color: white;
        }}
        
        .mission-clear-popup p {{
            font-size: 1.2rem;
            margin-bottom: 1.5rem;
            color: white;
        }}
        
        .popup-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 9999;
            animation: fadeIn 0.3s ease-out;
        }}
        
        @keyframes popupAnimation {{
            0% {{
                transform: translate(-50%, -50%) scale(0.5);
                opacity: 0;
            }}
            100% {{
                transform: translate(-50%, -50%) scale(1);
                opacity: 1;
            }}
        }}
        
        @keyframes fadeIn {{
            0% {{
                opacity: 0;
            }}
            100% {{
                opacity: 1;
            }}
        }}
        
        .popup-close-btn {{
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: 2px solid white;
            border-radius: 10px;
            padding: 0.75rem 2rem;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .popup-close-btn:hover {{
            background: white;
            color: #059669;
        }}
        
        /* レスポンシブ */
        @media (max-width: 768px) {{
            .main-container {{
                margin: 1rem;
                padding: 1.5rem;
                border-radius: 16px;
            }}
            
            .card-content {{
                flex-direction: column;
                gap: 1rem;
            }}
            
            .mission-actions {{
                width: 100%;
            }}
            
            .md-button {{
                width: 100%;
            }}
        }}
        
        /* ボタンスタイル調整 */
        .stButton > button {{
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            transition: all 0.2s ease;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        }}
        
        .stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4);
        }}
        
        .stButton > button:disabled {{
            background: #f3f4f6 !important;
            color: #9ca3af !important;
            transform: none !important;
            box-shadow: none !important;
        }}
        
        /* サイドバー調整 */
        .sidebar-content {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
            backdrop-filter: blur(10px);
        }}
        
        /* サイドバーボタンのホバーエフェクト */
        .stButton > button:hover {{
            color: #90ee90 !important;
            transition: color 0.3s ease;
        }}
        
        /* 無効化されたボタンのホバーエフェクトを無効化 */
        .stButton > button:disabled:hover {{
            color: #9ca3af !important;
        }}
        
        /* 進捗状況カード */
        .progress-overview-card {{
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border: 1px solid #e5e7eb;
            border-radius: 16px;
            padding: 2rem;
            margin: 1.5rem 0;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06), 0 2px 8px rgba(0, 0, 0, 0.04);
        }}
        
        .progress-stats {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }}
        
        .stat-item {{
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2.5rem;
            font-weight: 700;
            color: #2563eb;
            line-height: 1;
        }}
        
        .stat-label {{
            font-size: 0.875rem;
            color: #6b7280;
            margin-top: 0.25rem;
        }}
        
        .stat-divider {{
            font-size: 2rem;
            color: #d1d5db;
            font-weight: 300;
        }}
        
        .completion-rate {{
            text-align: center;
            margin-left: 2rem;
            padding-left: 2rem;
            border-left: 2px solid #e5e7eb;
        }}
        
        .rate-number {{
            font-size: 3rem;
            font-weight: 800;
            color: #10b981;
            line-height: 1;
        }}
        
        .rate-label {{
            font-size: 0.875rem;
            color: #6b7280;
            margin-top: 0.25rem;
        }}
        
        .progress-bar-container {{
            width: 100%;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 12px;
            background: #e5e7eb;
            border-radius: 6px;
            overflow: hidden;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #10b981 0%, #059669 100%);
            border-radius: 6px;
            transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        /* レスポンシブ対応 */
        @media (max-width: 768px) {{
            .progress-stats {{
                flex-direction: column;
                gap: 1rem;
            }}
            
            .completion-rate {{
                margin-left: 0;
                padding-left: 0;
                border-left: none;
                border-top: 2px solid #e5e7eb;
                padding-top: 1rem;
            }}
            
            .stat-number {{
                font-size: 2rem;
            }}
            
            .rate-number {{
                font-size: 2.5rem;
            }}
            
            /* サイドバーを非表示 */
            .stSidebar {{
                display: none !important;
            }}
            
            /* メインコンテナの調整 */
            .main .block-container {{
                padding-bottom: 6rem !important;
            }}
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
        
        if st.button("ダッシュボード", use_container_width=True, disabled=True, key="nav_dashboard"):
            pass  # 現在のページ
        
        if st.button("ランキング", use_container_width=True, key="nav_ranking"):
            st.switch_page("pages/ranking.py")
            
        if st.button("匿名投稿", use_container_width=True, key="nav_post"):
            st.switch_page("pages/post.py")
    
    # ヘッダー
    st.markdown('''
    <h1 class="welcome-header">
        <span class="material-icons header-icon" style="font-size: 3rem;">dashboard</span>
        Snow Village Dashboard
    </h1>
    ''', unsafe_allow_html=True)
    
    # タスクシステムの初期化と同期
    init_task_system()
    
    # タスク進捗状況セクション
    display_progress_overview()
    
    # フィルター切り替えボタン
    display_task_filter_toggle()
    
    # ミッションクリア通知の表示
    display_mission_clear_notification()
    
    # タスクの表示と管理
    display_tasks()
    
    # ログアウトボタン
    if st.button("ログアウト", use_container_width=True, type="primary", key="logout_btn"):
        # セッションクリア
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    # 下部ナビゲーションバー（隠しボタン付き）
    display_bottom_navigation()


@st.cache_resource
def init_task_system():
    """タスクシステムの初期化（1回のみ実行）"""
    from task_db import TaskService
    from tasks import sync_yaml_to_db
    
    # データベース初期化
    TaskService()
    
    # YAMLファイルからタスクを同期
    yaml_path = os.path.join(os.path.dirname(__file__), "..", "tasks.yml")
    if os.path.exists(yaml_path):
        sync_yaml_to_db(yaml_path)


def display_progress_overview():
    """進捗状況の概要を表示"""
    from task_db import TaskService
    
    # ユーザー情報を取得
    user_info = st.session_state.user_info
    user = user_info.get('user')
    user_id = user.id
    
    task_service = TaskService()
    tasks = task_service.get_tasks_with_progress(user_id)
    
    if not tasks:
        st.info("現在、利用可能なミッションはありません。")
        return
    
    # 進捗状況の計算
    total_tasks = len(tasks)
    completed_tasks = len([task for task in tasks if task['completed']])
    completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    
    # 進捗状況ヘッダー
    st.markdown('''
    <div class="section-header">
        <span class="material-icons section-icon">analytics</span>
        進捗状況
    </div>
    ''', unsafe_allow_html=True)
    
    # 進捗表示カード
    st.markdown(f'''
    <div class="progress-overview-card">
        <div class="progress-stats">
            <div class="stat-item">
                <div class="stat-number">{completed_tasks}</div>
                <div class="stat-label">完了済み</div>
            </div>
            <div class="stat-divider">/</div>
            <div class="stat-item">
                <div class="stat-number">{total_tasks}</div>
                <div class="stat-label">総ミッション数</div>
            </div>
            <div class="completion-rate">
                <div class="rate-number">{completion_rate:.1f}%</div>
                <div class="rate-label">完了率</div>
            </div>
        </div>
        <div class="progress-bar-container">
            <div class="progress-bar">
                <div class="progress-fill" style="width: {completion_rate}%"></div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def display_task_filter_toggle():
    """タスクフィルターの切り替えボタンを表示"""
    
    # 現在のフィルター状態を取得
    show_only_incomplete = st.session_state.get("show_only_incomplete", False)
    
    # フィルターToggle
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if show_only_incomplete:
            if st.button("📋 すべてのミッションを表示", key="show_all_tasks", type="secondary", use_container_width=True):
                st.session_state["show_only_incomplete"] = False
                st.rerun()
        else:
            if st.button("🎯 未完了のみ表示", key="show_incomplete_only", type="secondary", use_container_width=True):
                st.session_state["show_only_incomplete"] = True
                st.rerun()


@st.dialog("🎉 ミッションクリア！")
def show_mission_clear_dialog():
    """ミッションクリアダイアログ表示"""
    task_title = st.session_state.get("cleared_task_title", "ミッション")
    
    # ダイアログ内容
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem;">
        <h1 style="font-size: 4rem; margin: 1rem 0; color: #10b981;">🎉</h1>
        <h2 style="font-size: 2rem; margin: 1rem 0; color: #10b981; font-weight: 700;">
            ミッションクリア！
        </h2>
        <h3 style="font-size: 1.5rem; margin: 1rem 0; color: #374151; font-weight: 600;">
            『{task_title}』
        </h3>
        <p style="font-size: 1.2rem; margin: 1.5rem 0; color: #6b7280;">
            おめでとうございます！<br>
            ミッションを完了しました！
        </p>
        <p style="font-size: 1rem; margin: 1rem 0; color: #9ca3af;">
            未完了のミッションのみ表示に切り替えます
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # お祝い効果
    st.balloons()
    
    # 確認ボタン
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("ミッション一覧に戻る", type="primary", use_container_width=True):
            # フィルタリングモードに切り替えて状態をクリア
            st.session_state["mission_cleared"] = False
            st.session_state["show_only_incomplete"] = True
            st.rerun()


def display_mission_clear_notification():
    """ミッションクリア通知の管理"""
    
    # ミッションクリア状態をチェック
    if st.session_state.get("mission_cleared", False):
        show_mission_clear_dialog()


def display_tasks():
    """タスクの表示と管理"""
    from task_db import TaskService
    import json
    
    # ユーザー情報を取得
    user_info = st.session_state.user_info
    user = user_info.get('user')
    user_id = user.id
    
    task_service = TaskService()
    tasks = task_service.get_tasks_with_progress(user_id)
    
    if not tasks:
        return
    
    # タスクタイプ別に分類
    quiz_tasks = [task for task in tasks if task.get("task_type") == "quiz"]
    sns_tasks = [task for task in tasks if task.get("task_type") == "sns"]
    
    # クイズタスクセクション
    st.markdown('''
    <div class="task-category">
        <div class="section-header">
            <span class="material-icons section-icon">school</span>
            技術クイズミッション
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    display_enhanced_quiz_tasks(quiz_tasks, task_service, user_id)
    
    # SNSタスクセクション
    st.markdown('''
    <div class="task-category">
        <div class="section-header">
            <span class="material-icons section-icon">camera_alt</span>
            SNS投稿ミッション
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    display_enhanced_sns_tasks(sns_tasks, task_service, user_id)


def display_enhanced_quiz_tasks(tasks, task_service, user_id):
    """改善されたクイズタスクの表示"""
    import json
    
    # フィルタリング機能: 未完了のみ表示するかチェック
    show_only_incomplete = st.session_state.get("show_only_incomplete", False)
    
    for task in tasks:
        task_id = task['id']
        is_completed = task['completed']
        
        # フィルタリング: 完了済みタスクを非表示にする場合はスキップ
        if show_only_incomplete and is_completed:
            continue
        
        # タスクカードHTML（ボタンなし）
        completed_class = "completed" if is_completed else ""
        status_text = "完了" if is_completed else "挑戦可能"
        status_class = "status-completed" if is_completed else "status-pending"
        status_icon = "check_circle" if is_completed else "radio_button_unchecked"
        
        card_html = f"""
        <div class="mission-card {completed_class}">
            <div class="card-content">
                <div class="mission-info">
                    <div class="mission-title">
                        <span class="material-icons mission-type-icon quiz-icon">school</span>
                        {task['title']}
                    </div>
                    <div class="mission-description">
                        {task.get('description', '')}
                    </div>
                    <div class="mission-status {status_class}">
                        <span class="material-icons status-icon">{status_icon}</span>
                        {status_text}
                    </div>
                </div>
            </div>
        </div>
        """
        
        st.markdown(card_html, unsafe_allow_html=True)
        
        # Streamlitボタン（カード外）
        if not is_completed:
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("挑戦", key=f"quiz_btn_{task_id}", type="primary"):
                    st.session_state[f"show_quiz_{task_id}"] = True
                    st.rerun()
        
        # クイズコンテンツ表示
        if not is_completed and st.session_state.get(f"show_quiz_{task_id}", False):
            with st.expander(f"📚 {task['title']} - クイズ", expanded=True):
                display_quiz_content(task, task_service, user_id)


def display_enhanced_sns_tasks(tasks, task_service, user_id):
    """改善されたSNSタスクの表示"""
    import json
    
    # フィルタリング機能: 未完了のみ表示するかチェック
    show_only_incomplete = st.session_state.get("show_only_incomplete", False)
    
    for task in tasks:
        task_id = task['id']
        is_completed = task['completed']
        
        # フィルタリング: 完了済みタスクを非表示にする場合はスキップ
        if show_only_incomplete and is_completed:
            continue
        
        # タスクカードHTML（ボタンなし）
        completed_class = "completed" if is_completed else ""
        status_text = "完了" if is_completed else "投稿可能"
        status_class = "status-completed" if is_completed else "status-pending"
        status_icon = "check_circle" if is_completed else "radio_button_unchecked"
        
        card_html = f"""
        <div class="mission-card {completed_class}">
            <div class="card-content">
                <div class="mission-info">
                    <div class="mission-title">
                        <span class="material-icons mission-type-icon sns-icon">camera_alt</span>
                        {task['title']}
                    </div>
                    <div class="mission-description">
                        {task.get('description', '')}
                    </div>
                    <div class="mission-status {status_class}">
                        <span class="material-icons status-icon">{status_icon}</span>
                        {status_text}
                    </div>
                </div>
            </div>
        </div>
        """
        
        st.markdown(card_html, unsafe_allow_html=True)
        
        # Streamlitボタン（カード外）
        if not is_completed:
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("投稿", key=f"sns_btn_{task_id}", type="primary"):
                    st.session_state[f"show_sns_{task_id}"] = True
                    st.rerun()
        
        # SNSコンテンツ表示
        if not is_completed and st.session_state.get(f"show_sns_{task_id}", False):
            with st.expander(f"📱 {task['title']} - SNS投稿", expanded=True):
                display_sns_content(task, task_service, user_id)




def display_quiz_content(task, task_service, user_id):
    """クイズコンテンツの表示"""
    import json
    
    task_id = task['id']
    content = task.get('content')
    
    if isinstance(content, str):
        content = json.loads(content)
    
    if not content:
        st.error("クイズデータが見つかりません")
        return
    
    question = content.get('question', '')
    options = content.get('options', [])
    correct_answer = content.get('correct_answer', 0)
    
    st.markdown(f"**問題:** {question}")
    
    # 回答選択
    answer_key = f"quiz_answer_{task_id}"
    selected_answer = st.radio(
        "回答を選択してください：",
        options,
        key=answer_key
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("回答する", key=f"submit_quiz_{task_id}"):
            selected_index = options.index(selected_answer)
            if selected_index == correct_answer:
                # ミッションクリア処理
                task_service.mark_task_complete(task_id, user_id)
                # クリア状態とタスク情報をセッションに保存
                st.session_state["mission_cleared"] = True
                st.session_state["cleared_task_title"] = task['title']
                st.session_state["cleared_task_id"] = task_id
                # クイズ表示を非表示にして画面更新
                st.session_state[f"show_quiz_{task_id}"] = False
                st.rerun()
            else:
                st.error(f"❌ 不正解です。正解は: {options[correct_answer]}")
    
    with col2:
        if st.button("閉じる", key=f"close_quiz_content_{task_id}"):
            st.session_state[f"show_quiz_{task_id}"] = False
            st.rerun()


def display_bottom_navigation():
    """下部ナビゲーションバーの表示"""
    
    # 3つのナビゲーションボタン
    st.markdown("### 📱 ページナビゲーション")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏠 ホーム", key="bottom_nav_home", disabled=True, use_container_width=True):
            pass  # 現在のページ
    
    with col2:
        if st.button("🏆 ランキング", key="bottom_nav_ranking", use_container_width=True):
            st.switch_page("pages/ranking.py")
    
    with col3:
        if st.button("📝 匿名投稿", key="bottom_nav_post", use_container_width=True):
            st.switch_page("pages/post.py")


def display_sns_content(task, task_service, user_id):
    """SNSコンテンツの表示"""
    import json
    
    task_id = task['id']
    content = task.get('content')
    
    if isinstance(content, str):
        content = json.loads(content)
    
    if not content:
        st.error("SNS投稿データが見つかりません")
        return
    
    booth_name = content.get('booth_name', '')
    sns_prompt = content.get('sns_prompt', '')
    requirements = content.get('requirements', [])
    
    st.markdown(f"**訪問先:** {booth_name}")
    st.markdown(f"**推奨投稿内容:** {sns_prompt}")
    
    if requirements:
        st.markdown("**要件:**")
        for req in requirements:
            st.markdown(f"- {req}")
    
    st.info("📸 上記の要件を満たしてSNSに投稿したら、下の「完了」ボタンを押してください！")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("完了", key=f"complete_sns_{task_id}"):
            # ミッションクリア処理
            task_service.mark_task_complete(task_id, user_id)
            # クリア状態とタスク情報をセッションに保存
            st.session_state["mission_cleared"] = True
            st.session_state["cleared_task_title"] = task['title']
            st.session_state["cleared_task_id"] = task_id
            # SNS表示を非表示にして画面更新
            st.session_state[f"show_sns_{task_id}"] = False
            st.rerun()
    
    with col2:
        if st.button("閉じる", key=f"close_sns_content_{task_id}"):
            st.session_state[f"show_sns_{task_id}"] = False
            st.rerun()




if __name__ == "__main__":
    main()

