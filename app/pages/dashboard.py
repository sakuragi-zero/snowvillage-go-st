"""
Simple Dashboard Page
"""
import streamlit as st
import os
import base64

# ページ設定
st.set_page_config(
    page_title="Snow Village - Dashboard",
    page_icon="ac_unit",
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
    bg_path = os.path.join(base_dir, "frontend", "public", "SnowVillageGo.png")
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
            background: linear-gradient(135deg, #1a237e, #3949ab, #42a5f5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 2.5rem;
            letter-spacing: -0.8px;
            line-height: 1.1;
            position: relative;
        }}
        
        .welcome-header::before {{
            content: '';
            position: absolute;
            top: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 120%;
            height: calc(100% + 20px);
            background: rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            z-index: -1;
            backdrop-filter: blur(8px);
            box-shadow: 0 4px 20px rgba(255, 255, 255, 0.1);
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
            justify-content: center;
            margin: 2.5rem 0 1.5rem 0;
            background: linear-gradient(135deg, #1a237e, #3949ab);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 1.8rem;
            font-weight: 700;
            position: relative;
            padding: 1rem 0;
        }}
        
        .section-header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 80%;
            height: 100%;
            background: rgba(255, 255, 255, 0.15);
            border-radius: 15px;
            z-index: -1;
            backdrop-filter: blur(5px);
        }}
        
        .section-icon {{
            margin-right: 0.75rem;
            background: linear-gradient(135deg, #1a237e, #3949ab);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2rem;
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
            gap: 1rem;
            margin-bottom: 1.5rem;
            flex-wrap: nowrap;
        }}
        
        .stat-item {{
            text-align: center;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            flex-shrink: 0;
            white-space: nowrap;
        }}
        
        .stat-item-unified {{
            text-align: center;
            flex-shrink: 0;
        }}
        
        .stat-number {{
            font-size: 2.5rem;
            font-weight: 700;
            color: #2563eb;
            line-height: 1;
            white-space: nowrap;
        }}
        
        .stat-label {{
            font-size: 0.875rem;
            color: #6b7280;
            white-space: nowrap;
            margin-top: 0.25rem;
        }}
        
        .stat-divider {{
            font-size: 2rem;
            color: #d1d5db;
            font-weight: 300;
            flex-shrink: 0;
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
        
        /* 報酬セクション */
        .reward-progress {{
            margin-top: 1.5rem;
            text-align: center;
        }}
        
        .reward-info {{
            margin-bottom: 1rem;
            padding: 0.8rem;
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.05));
            border-radius: 12px;
            border: 1px solid rgba(16, 185, 129, 0.2);
        }}
        
        .earned-rewards {{
            min-height: 2rem;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        /* ジャンプナビゲーション */
        .jump-navigation {{
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin: 2rem 0;
            flex-wrap: wrap;
        }}
        
        .jump-button {{
            background: linear-gradient(135deg, #bfdbfe 0%, #93c5fd 100%);
            color: #1e40af;
            border: none;
            border-radius: 25px;
            padding: 0.75rem 1.5rem;
            font-size: 0.875rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15);
        }}
        
        .jump-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(37, 99, 235, 0.25);
            background: linear-gradient(135deg, #a3d2f7 0%, #7bb3f0 100%);
        }}
        
        .jump-button.swt {{
            background: linear-gradient(135deg, #bbf7d0 0%, #86efac 100%);
            color: #065f46;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.15);
        }}
        
        .jump-button.swt:hover {{
            box-shadow: 0 8px 20px rgba(16, 185, 129, 0.25);
            background: linear-gradient(135deg, #a7f3d0 0%, #6ee7b7 100%);
        }}
        
        .jump-button.sns {{
            background: linear-gradient(135deg, #fecaca 0%, #fca5a5 100%);
            color: #991b1b;
            box-shadow: 0 4px 12px rgba(220, 38, 38, 0.15);
        }}
        
        .jump-button.sns:hover {{
            box-shadow: 0 8px 20px rgba(220, 38, 38, 0.25);
            background: linear-gradient(135deg, #fed7d7 0%, #f87171 100%);
        }}
        
        .swt-icon {{ color: #10b981; }}
        
        /* セクションアンカー */
        .section-anchor {{
            position: relative;
            top: -100px;
            visibility: hidden;
        }}
        
        /* スムーススクロール */
        html {{
            scroll-behavior: smooth;
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

        /* レスポンシブ対応 */
        @media (max-width: 768px) {{
            .welcome-header {{
                font-size: 2.2rem;
                margin-bottom: 2rem;
                letter-spacing: -0.5px;
            }}
            
            .welcome-header::before {{
                width: 110%;
            }}
            
            .section-header {{
                font-size: 1.5rem;
                margin: 2rem 0 1rem 0;
                padding: 0.8rem 0;
            }}
            
            .section-header::before {{
                width: 90%;
            }}
            
            .section-icon {{
                font-size: 1.5rem;
                margin-right: 0.5rem;
            }}
            
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
            
            
            /* メインコンテナの調整 */
            .main .block-container {{
                padding-bottom: 6rem !important;
            }}
            
            /* ジャンプナビゲーションのレスポンシブ対応 */
            .jump-navigation {{
                flex-direction: column;
                align-items: center;
                gap: 0.75rem;
            }}
            
            .jump-button {{
                width: 90%;
                justify-content: center;
            }}
        }}
        
    </style>
    """, unsafe_allow_html=True)
    
    
    # ヘッダー
    st.markdown('''
    <h1 class="welcome-header">
        SnowVillage<br>
        Community<br>
        Mission
    </h1>
    ''', unsafe_allow_html=True)
    
    # タスクシステムの初期化と同期
    init_task_system()
    
    # ナビゲーションボタン（進捗状況の上）
    display_navigation_buttons()
    
    # タスク進捗状況セクション
    display_progress_overview()
    
    # フィルター切り替えボタン
    display_task_filter_toggle()
    
    # ジャンプナビゲーション
    display_jump_navigation()
    
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
    
    # 報酬情報の計算
    earned_rewards = [milestone for milestone in MILESTONE_REWARDS.keys() if milestone <= completed_tasks]
    next_milestone = get_next_milestone(completed_tasks)
    
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
            <div class="stat-item-unified">
                <div class="stat-number">{completed_tasks}/{total_tasks}</div>
                <div class="stat-label">ミッション完了</div>
            </div>
            <div class="completion-rate">
                <div class="rate-number">{completion_rate:.1f}%</div>
                <div class="rate-label">完了率</div>
            </div>
            <div class="stat-item-unified">
                <div class="stat-number">{len(earned_rewards)}</div>
                <div class="stat-label">獲得報酬</div>
            </div>
        </div>
        <div class="progress-bar-container">
            <div class="progress-bar">
                <div class="progress-fill" style="width: {completion_rate}%"></div>
            </div>
        </div>
        <div class="reward-progress">
            <div class="reward-info">
                <span style="color: #10b981; font-weight: 600;">🎁 次の報酬まで: {next_milestone - completed_tasks if next_milestone != "最大" else 0}ミッション</span>
            </div>
            <div class="earned-rewards">
                {generate_earned_rewards_html(earned_rewards)}
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def generate_earned_rewards_html(earned_rewards):
    """獲得済み報酬のHTML生成"""
    if not earned_rewards:
        return '<span style="color: #9ca3af; font-size: 0.9rem;">まだ報酬はありません</span>'
    
    rewards_html = '<div style="display: flex; gap: 0.5rem; justify-content: center; flex-wrap: wrap; margin-top: 0.5rem;">'
    for milestone in earned_rewards:
        reward = MILESTONE_REWARDS[milestone]
        rewards_html += f'''
            <div style="display: flex; align-items: center; background: {reward['color']}22; 
                        border: 1px solid {reward['color']}44; border-radius: 20px; 
                        padding: 0.3rem 0.8rem; font-size: 0.8rem;">
                <span style="margin-right: 0.3rem;">{reward['icon']}</span>
                <span style="color: {reward['color']}; font-weight: 600;">{milestone}</span>
            </div>
        '''
    rewards_html += '</div>'
    return rewards_html


def display_task_filter_toggle():
    """タスクフィルターの切り替えボタンを表示"""
    
    # 現在のフィルター状態を取得
    show_only_incomplete = st.session_state.get("show_only_incomplete", False)
    
    # フィルターToggle
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if show_only_incomplete:
            if st.button("すべてのミッションを表示", key="show_all_tasks", type="secondary", use_container_width=True):
                st.session_state["show_only_incomplete"] = False
                st.rerun()
        else:
            if st.button("未完了のみ表示", key="show_incomplete_only", type="secondary", use_container_width=True):
                st.session_state["show_only_incomplete"] = True
                st.rerun()


def display_jump_navigation():
    """ジャンプナビゲーションの表示"""
    st.markdown("""
    <div class="jump-navigation">
        <a href="#swt-section" class="jump-button swt">
            <span class="material-icons" style="font-size: 1rem;">celebration</span>
            SWTエンジョイミッション
        </a>
        <a href="#sns-section" class="jump-button sns">
            <span class="material-icons" style="font-size: 1rem;">camera_alt</span>
            SNS投稿ミッション
        </a>
        <a href="#quiz-section" class="jump-button">
            <span class="material-icons" style="font-size: 1rem;">school</span>
            技術クイズミッション
        </a>
    </div>
    """, unsafe_allow_html=True)


# マイルストーン報酬の定義
MILESTONE_REWARDS = {
    5: {"name": "初心者報酬", "description": "5つのミッション完了", "icon": "🏅", "color": "#10b981"},
    10: {"name": "冒険者報酬", "description": "10のミッション完了", "icon": "🏆", "color": "#f59e0b"},
    15: {"name": "探検家報酬", "description": "15のミッション完了", "icon": "🎖️", "color": "#8b5cf6"},
    20: {"name": "勇者報酬", "description": "20のミッション完了", "icon": "👑", "color": "#ef4444"},
    25: {"name": "マスター報酬", "description": "25のミッション完了", "icon": "💎", "color": "#06b6d4"},
    30: {"name": "伝説報酬", "description": "30のミッション完了", "icon": "✨", "color": "#d946ef"}
}

@st.dialog("ミッションクリア！")
def show_mission_clear_dialog():
    """ミッションクリアダイアログ表示"""
    task_title = st.session_state.get("cleared_task_title", "ミッション")
    
    # ダイアログ内容
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem;">
        <h1 style="font-size: 4rem; margin: 1rem 0; color: #10b981;">🎉</h1>
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


@st.dialog("🎁 報酬獲得！")
def show_reward_dialog():
    """報酬獲得ダイアログ表示"""
    completed_count = st.session_state.get("completed_count_for_reward", 0)
    reward = MILESTONE_REWARDS.get(completed_count, {})
    
    if not reward:
        return
    
    # ダイアログ内容
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem;">
        <h1 style="font-size: 5rem; margin: 1rem 0; color: {reward['color']};">{reward['icon']}</h1>
        <h2 style="font-size: 2.5rem; margin: 1rem 0; color: {reward['color']}; font-weight: 800;">
            {reward['name']}
        </h2>
        <p style="font-size: 1.3rem; margin: 1.5rem 0; color: #374151; font-weight: 600;">
            {reward['description']}達成！
        </p>
        <div style="background: linear-gradient(135deg, {reward['color']}22, {reward['color']}11); 
                    border: 2px solid {reward['color']}44; 
                    border-radius: 15px; 
                    padding: 1.5rem; 
                    margin: 2rem 0;">
            <p style="font-size: 1.1rem; color: #374151; font-weight: 600; margin: 0;">
                🎉 おめでとうございます！<br>
                マイルストーン報酬を獲得しました！
            </p>
        </div>
        <p style="font-size: 0.9rem; margin: 1rem 0; color: #9ca3af;">
            次のマイルストーン: {get_next_milestone(completed_count)}ミッション完了
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 特別な効果
    st.balloons()
    
    # 確認ボタン
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("素晴らしい！", type="primary", use_container_width=True):
            # 報酬ダイアログを閉じる
            st.session_state["reward_earned"] = False
            st.session_state["show_only_incomplete"] = True
            st.rerun()


def get_next_milestone(current_count):
    """次のマイルストーンを取得"""
    milestones = sorted(MILESTONE_REWARDS.keys())
    for milestone in milestones:
        if milestone > current_count:
            return milestone
    return "最大"


def check_milestone_reward(completed_count):
    """マイルストーン報酬をチェック"""
    return completed_count in MILESTONE_REWARDS


def display_mission_clear_notification():
    """ミッションクリア通知の管理"""
    
    # 報酬獲得状態をチェック（優先して表示）
    if st.session_state.get("reward_earned", False):
        show_reward_dialog()
    # ミッションクリア状態をチェック
    elif st.session_state.get("mission_cleared", False):
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
    swt_tasks = [task for task in tasks if task.get("task_type") == "swt"]
    sns_tasks = [task for task in tasks if task.get("task_type") == "sns"]
    quiz_tasks = [task for task in tasks if task.get("task_type") == "quiz"]
    
    # SWTエンジョイミッションセクション
    st.markdown('''
    <div id="swt-section" class="section-anchor"></div>
    <div class="task-category">
        <div class="section-header">
            <span class="material-icons section-icon">celebration</span>
            SWTエンジョイミッション
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    display_enhanced_swt_tasks(swt_tasks, task_service, user_id)
    
    # SNSタスクセクション
    st.markdown('''
    <div id="sns-section" class="section-anchor"></div>
    <div class="task-category">
        <div class="section-header">
            <span class="material-icons section-icon">camera_alt</span>
            SNS投稿ミッション
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    display_enhanced_sns_tasks(sns_tasks, task_service, user_id)
    
    # クイズタスクセクション
    st.markdown('''
    <div id="quiz-section" class="section-anchor"></div>
    <div class="task-category">
        <div class="section-header">
            <span class="material-icons section-icon">school</span>
            技術クイズミッション
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    display_enhanced_quiz_tasks(quiz_tasks, task_service, user_id)


def display_enhanced_swt_tasks(tasks, task_service, user_id):
    """SWTエンジョイミッションの表示"""
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
        status_text = "完了" if is_completed else "参加可能"
        status_class = "status-completed" if is_completed else "status-pending"
        status_icon = "check_circle" if is_completed else "radio_button_unchecked"
        
        card_html = f"""
        <div class="mission-card {completed_class}">
            <div class="card-content">
                <div class="mission-info">
                    <div class="mission-title">
                        <span class="material-icons mission-type-icon swt-icon">celebration</span>
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
                if st.button("参加", key=f"swt_btn_{task_id}", type="primary"):
                    st.session_state[f"show_swt_{task_id}"] = True
                    st.rerun()
        
        # SWTコンテンツ表示
        if not is_completed and st.session_state.get(f"show_swt_{task_id}", False):
            with st.expander(f"🎉 {task['title']} - SWTエンジョイ", expanded=True):
                display_swt_content(task, task_service, user_id)


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
                
                # 完了数を再計算してマイルストーン報酬チェック
                tasks = task_service.get_tasks_with_progress(user_id)
                completed_count = len([task for task in tasks if task['completed']])
                
                # クリア状態とタスク情報をセッションに保存
                st.session_state["mission_cleared"] = True
                st.session_state["cleared_task_title"] = task['title']
                st.session_state["cleared_task_id"] = task_id
                
                # マイルストーン報酬チェック
                if check_milestone_reward(completed_count):
                    st.session_state["reward_earned"] = True
                    st.session_state["completed_count_for_reward"] = completed_count
                
                # クイズ表示を非表示にして画面更新
                st.session_state[f"show_quiz_{task_id}"] = False
                st.rerun()
            else:
                st.error(f"不正解です。正解は: {options[correct_answer]}")
    
    with col2:
        if st.button("閉じる", key=f"close_quiz_content_{task_id}"):
            st.session_state[f"show_quiz_{task_id}"] = False
            st.rerun()


def display_navigation_buttons():
    """ナビゲーションボタンの表示（進捗状況の上）"""
    
    # 3つのナビゲーションボタン - Material UIアイコン付き
    st.markdown("""
    <style>
        /* ナビゲーションボタン内のMaterial Icons */
        .nav-button-icon {
            font-size: 1.2rem;
            margin-right: 0.5rem;
            vertical-align: middle;
        }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1], gap="small")
    
    with col1:
        mission_button = st.button(
            "ミッションに挑戦", 
            key="top_nav_mission",
            disabled=True,
            use_container_width=True
        )
    
    with col2:
        ranking_button = st.button(
            "ランキング", 
            key="top_nav_ranking", 
            use_container_width=True
        )
        if ranking_button:
            st.switch_page("pages/ranking.py")
    
    with col3:
        post_button = st.button(
            "匿名質問", 
            key="top_nav_post", 
            use_container_width=True
        )
        if post_button:
            st.switch_page("pages/post.py")


def display_swt_content(task, task_service, user_id):
    """SWTコンテンツの表示"""
    import json
    
    task_id = task['id']
    content = task.get('content')
    
    if isinstance(content, str):
        content = json.loads(content)
    
    if not content:
        st.error("SWTエンジョイデータが見つかりません")
        return
    
    event_name = content.get('event_name', '')
    description = content.get('description', '')
    requirements = content.get('requirements', [])
    location = content.get('location', '')
    
    if event_name:
        st.markdown(f"**イベント名:** {event_name}")
    if location:
        st.markdown(f"**開催場所:** {location}")
    if description:
        st.markdown(f"**内容:** {description}")
    
    if requirements:
        st.markdown("**参加条件:**")
        for req in requirements:
            st.markdown(f"- {req}")
    
    st.info("上記のSWTエンジョイミッションに参加したら、下の「完了」ボタンを押してください！")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("完了", key=f"complete_swt_{task_id}"):
            # ミッションクリア処理
            task_service.mark_task_complete(task_id, user_id)
            
            # 完了数を再計算してマイルストーン報酬チェック
            tasks = task_service.get_tasks_with_progress(user_id)
            completed_count = len([task for task in tasks if task['completed']])
            
            # クリア状態とタスク情報をセッションに保存
            st.session_state["mission_cleared"] = True
            st.session_state["cleared_task_title"] = task['title']
            st.session_state["cleared_task_id"] = task_id
            
            # マイルストーン報酬チェック
            if check_milestone_reward(completed_count):
                st.session_state["reward_earned"] = True
                st.session_state["completed_count_for_reward"] = completed_count
            
            # SWT表示を非表示にして画面更新
            st.session_state[f"show_swt_{task_id}"] = False
            st.rerun()
    
    with col2:
        if st.button("閉じる", key=f"close_swt_content_{task_id}"):
            st.session_state[f"show_swt_{task_id}"] = False
            st.rerun()


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
    
    st.info("上記の要件を満たしてSNSに投稿したら、下の「完了」ボタンを押してください！")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("完了", key=f"complete_sns_{task_id}"):
            # ミッションクリア処理
            task_service.mark_task_complete(task_id, user_id)
            
            # 完了数を再計算してマイルストーン報酬チェック
            tasks = task_service.get_tasks_with_progress(user_id)
            completed_count = len([task for task in tasks if task['completed']])
            
            # クリア状態とタスク情報をセッションに保存
            st.session_state["mission_cleared"] = True
            st.session_state["cleared_task_title"] = task['title']
            st.session_state["cleared_task_id"] = task_id
            
            # マイルストーン報酬チェック
            if check_milestone_reward(completed_count):
                st.session_state["reward_earned"] = True
                st.session_state["completed_count_for_reward"] = completed_count
            
            # SNS表示を非表示にして画面更新
            st.session_state[f"show_sns_{task_id}"] = False
            st.rerun()
    
    with col2:
        if st.button("閉じる", key=f"close_sns_content_{task_id}"):
            st.session_state[f"show_sns_{task_id}"] = False
            st.rerun()




if __name__ == "__main__":
    main()

