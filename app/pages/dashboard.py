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
        
        .task-container {{
            background: #ffffff;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}
        
        .logout-btn {{
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
        }}
        
        .stButton > button:disabled {{
            background: #ccc;
            color: #666;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    # サイドバーにユーザー情報を表示
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.markdown(f"### Hello, {user.username}! 🎉")
        st.markdown("**ユーザー情報**")
        st.markdown(f"**ユーザー名:** {user.username}")
        st.markdown(f"**登録日時:** {user.created_at.strftime('%Y年%m月%d日 %H:%M')}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ヘッダー
    st.markdown('<h1 class="welcome-header">❄️ Snow Village Dashboard</h1>', unsafe_allow_html=True)
    
    # タスク管理セクション
    st.markdown('<div class="task-container">', unsafe_allow_html=True)
    st.markdown("### 🎯 ミッション進捗管理")
    
    # タスクシステムの初期化と同期
    init_task_system()
    
    # タスクの表示と管理
    display_tasks()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ログアウトボタン
    st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
    if st.button("ログアウト", use_container_width=True, type="primary"):
        # セッションクリア
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


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


def display_tasks():
    """タスクの表示と管理"""
    from task_db import TaskService
    import json
    
    task_service = TaskService()
    tasks = task_service.get_tasks_with_progress()
    
    if not tasks:
        st.info("現在、利用可能なミッションはありません。")
        return
    
    # タスクタイプ別に分類
    quiz_tasks = [task for task in tasks if task.get("task_type") == "quiz"]
    sns_tasks = [task for task in tasks if task.get("task_type") == "sns"]
    
    st.markdown("### 🧠 技術クイズミッション")
    display_quiz_tasks(quiz_tasks, task_service)
    
    st.markdown("### 📱 SNS投稿ミッション")
    display_sns_tasks(sns_tasks, task_service)


def display_quiz_tasks(tasks, task_service):
    """クイズタスクの表示"""
    import json
    
    for task in tasks:
        task_id = task['id']
        is_completed = task['completed']
        
        # タスクカード
        with st.container():
            col1, col2 = st.columns([4, 1])
            
            with col1:
                if is_completed:
                    st.markdown(f"✅ **{task['title']}** (完了済み)")
                else:
                    st.markdown(f"🧠 **{task['title']}**")
                st.caption(task.get('description', ''))
            
            with col2:
                if is_completed:
                    st.success("完了")
                else:
                    challenge_key = f"challenge_quiz_{task_id}"
                    if st.button("挑戦", key=f"btn_quiz_{task_id}", disabled=is_completed):
                        st.session_state[challenge_key] = True
        
        # 折りたたみ式クイズ表示
        if not is_completed and st.session_state.get(f"challenge_quiz_{task_id}", False):
            with st.expander(f"📚 {task['title']} - クイズ", expanded=True):
                display_quiz_content(task, task_service)
        
        st.divider()


def display_sns_tasks(tasks, task_service):
    """SNSタスクの表示"""
    import json
    
    for task in tasks:
        task_id = task['id']
        is_completed = task['completed']
        
        # タスクカード
        with st.container():
            col1, col2 = st.columns([4, 1])
            
            with col1:
                if is_completed:
                    st.markdown(f"✅ **{task['title']}** (完了済み)")
                else:
                    st.markdown(f"📱 **{task['title']}**")
                st.caption(task.get('description', ''))
            
            with col2:
                if is_completed:
                    st.success("完了")
                else:
                    challenge_key = f"challenge_sns_{task_id}"
                    if st.button("挑戦", key=f"btn_sns_{task_id}", disabled=is_completed):
                        st.session_state[challenge_key] = True
        
        # 折りたたみ式SNS投稿表示
        if not is_completed and st.session_state.get(f"challenge_sns_{task_id}", False):
            with st.expander(f"📱 {task['title']} - SNS投稿", expanded=True):
                display_sns_content(task, task_service)
        
        st.divider()


def display_quiz_content(task, task_service):
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
                st.success("🎉 正解です！ミッション完了！")
                task_service.mark_task_complete(task_id)
                st.session_state[f"challenge_quiz_{task_id}"] = False
                st.rerun()
            else:
                st.error(f"❌ 不正解です。正解は: {options[correct_answer]}")
    
    with col2:
        if st.button("閉じる", key=f"close_quiz_{task_id}"):
            st.session_state[f"challenge_quiz_{task_id}"] = False
            st.rerun()


def display_sns_content(task, task_service):
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
            st.success("🎉 SNS投稿ミッション完了！")
            task_service.mark_task_complete(task_id)
            st.session_state[f"challenge_sns_{task_id}"] = False
            st.rerun()
    
    with col2:
        if st.button("閉じる", key=f"close_sns_{task_id}"):
            st.session_state[f"challenge_sns_{task_id}"] = False
            st.rerun()




if __name__ == "__main__":
    main()

