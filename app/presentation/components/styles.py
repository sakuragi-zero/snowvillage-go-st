"""Streamlitコンポーネント用のCSSスタイル定義"""
import os
import base64

def get_dashboard_background_image() -> str:
    """背景画像をBase64エンコードして取得"""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    bg_path = os.path.join(base_dir, "frontend", "public", "dashboard.png")
    
    if os.path.exists(bg_path):
        with open(bg_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

def get_main_styles() -> str:
    """メインスタイルを返す（白い文字を黒に修正済み）"""
    bg_base64 = get_dashboard_background_image()
    
    # 背景スタイルを設定
    if bg_base64:
        bg_style = f"background: url(data:image/png;base64,{bg_base64}) no-repeat center center fixed; background-size: cover;"
    else:
        bg_style = "background: linear-gradient(135deg, #1a237e, #283593, #3949ab, #42a5f5);"
    
    # f-stringを使わないでCSSを返す
    return """
<style>
    /* メインアプリの背景 */
    .stApp {
        """ + bg_style + """
    }
    
    /* メインコンテナ */
    .main {
        padding: 0rem 1rem;
        color: #000000 !important;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        margin: 1rem;
    }
    
    /* 見出しの色を黒に */
    h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
    }
    
    /* パラグラフの色を黒に */
    p {
        color: #000000 !important;
    }
    
    /* カードスタイル */
    .mission-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 20px rgba(0,0,0,0.2);
        text-align: center;
        transition: transform 0.2s;
        color: #000000 !important;
    }
    
    .mission-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
    }
    
    .mission-card h3 {
        color: #000000 !important;
        margin: 10px 0;
    }
    
    .mission-card p {
        color: #666666 !important;
    }
    
    .completed-card {
        background: #f0fdf4;
        border: 3px solid #58cc02;
    }
    
    .locked-card {
        background: #f5f5f5;
        opacity: 0.6;
    }
    
    /* プログレスバー */
    .progress-container {
        background: #e0e0e0;
        height: 10px;
        border-radius: 5px;
        overflow: hidden;
        margin: 10px 0;
    }
    
    .progress-bar {
        background: #58cc02;
        height: 100%;
        transition: width 0.3s ease;
    }
    
    /* ボタンスタイル */
    .stButton > button {
        background-color: #58cc02;
        color: white !important;
        border-radius: 10px;
        padding: 10px 30px;
        font-weight: bold;
        border: none;
        transition: background-color 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #45a000;
        color: white !important;
    }
    
    /* メトリクススタイル */
    .metric-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 15px rgba(0,0,0,0.2);
        color: #000000 !important;
    }
    
    .metric-container h3 {
        color: #000000 !important;
        margin: 5px 0;
    }
    
    .metric-container p {
        color: #666666 !important;
        margin: 0;
        font-size: 14px;
    }
    
    /* パスノード */
    .path-node {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: #e0e0e0;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        margin: 20px auto;
        color: #000000;
    }
    
    .path-node.completed {
        background: #58cc02;
        color: white;
    }
    
    .path-node.current {
        background: #1cb0f6;
        color: white;
        animation: pulse 2s infinite;
    }
    
    /* 実績カードスタイル */
    .achievement-card {
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 10px 0;
        color: #000000 !important;
    }
    
    .achievement-card h4 {
        color: #000000 !important;
        margin: 10px 0;
    }
    
    .achievement-unlocked {
        background: #f0fdf4;
        border: 2px solid #58cc02;
    }
    
    .achievement-locked {
        background: #f5f5f5;
        border: 2px solid #e0e0e0;
        opacity: 0.6;
    }
    
    /* タブのテキスト色 */
    .stTabs [data-baseweb="tab-list"] button {
        color: #000000 !important;
    }
    
    /* データフレームのテキスト色 */
    .stDataFrame {
        color: #000000 !important;
    }
    
    /* メインコンテンツの挨拶文を水色に */
    .main-welcome {
        color: #4FC3F7 !important;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* サイドバーのスタイル */
    .css-1d391kg {
        background: rgba(248, 249, 250, 0.95) !important;
        backdrop-filter: blur(10px);
    }
    
    .css-1lcbmhc {
        background: rgba(248, 249, 250, 0.95) !important;
        backdrop-filter: blur(10px);
    }
    
    /* サイドバー全体のテキスト色を水色に */
    .stSidebar {
        color: #4FC3F7 !important;
    }
    
    .stSidebar .markdown-text-container {
        color: #4FC3F7 !important;
    }
    
    .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4, .stSidebar h5, .stSidebar h6 {
        color: #4FC3F7 !important;
    }
    
    .stSidebar p {
        color: #4FC3F7 !important;
    }
    
    .stSidebar strong {
        color: #4FC3F7 !important;
    }
    
    /* サイドバーのボタンスタイル（水色テーマ） */
    .stSidebar .stButton > button {
        background-color: #4FC3F7 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    
    .stSidebar .stButton > button:hover {
        background-color: #29B6F6 !important;
        color: white !important;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
</style>
"""