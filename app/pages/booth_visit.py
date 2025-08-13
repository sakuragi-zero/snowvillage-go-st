"""
ブース訪問ページ
ブース訪問系タスクを表示し、SNS投稿を促す
"""
import streamlit as st
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from infrastructure.services.task_loader_service import get_task_by_id
from domain.entities.task import TaskType
from presentation.components.styles import get_main_styles
from infrastructure.repositories.task_progress_repository_impl import TaskProgressRepositoryImpl
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from infrastructure.repositories.progress_repository_impl import ProgressRepositoryImpl
from application.use_cases.task_progress_use_case import TaskProgressUseCase
import asyncio
from datetime import datetime

# ページ設定
st.set_page_config(
    page_title="Snow Village - ブース訪問",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# スタイル適用
st.markdown(get_main_styles(), unsafe_allow_html=True)

def render_booth_visit(task):
    """ブース訪問タスクを描画"""
    
    st.markdown(f"# 📍 {task.title}")
    st.markdown(f"**{task.description}**")
    st.markdown("---")
    
    # ブース情報
    st.markdown(f"## 🏢 訪問先")
    st.markdown(f"### {task.booth_name}")
    
    # 投稿内容
    st.markdown("## 📱 SNS投稿")
    st.markdown("以下の内容をSNSに投稿してタスクを完了させましょう！")
    
    # 投稿テキスト表示
    st.markdown("### 投稿内容:")
    st.code(task.twitter_text, language=None)
    
    # Twitter投稿ボタン
    if task.twitter_url:
        st.markdown("### 🐦 Twitterに投稿")
        twitter_button_html = f"""
        <div style="margin: 20px 0;">
            <a href="{task.twitter_url}" target="_blank" style="
                display: inline-block;
                background-color: #1DA1F2;
                color: white;
                padding: 12px 24px;
                text-decoration: none;
                border-radius: 25px;
                font-weight: bold;
                font-size: 16px;
                transition: background-color 0.3s;
            ">
                🐦 Twitterで投稿する
            </a>
        </div>
        """
        st.markdown(twitter_button_html, unsafe_allow_html=True)
    
    # 手動投稿用の説明
    st.markdown("### 📝 手動で投稿する場合")
    st.info("""
    1. 上記のブースを実際に訪問してください
    2. 投稿内容をコピーしてTwitter(X)に投稿してください
    3. 投稿が完了したら下の「完了」ボタンを押してください
    """)
    
    # 報酬表示
    st.markdown("### 🎁 獲得報酬")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("XP", f"+{task.xp_reward}")
    with col2:
        st.metric("ジェム", f"+{task.gem_reward}")
    
    # 完了確認
    st.markdown("---")
    st.markdown("### ✅ タスク完了確認")
    
    completed = st.checkbox("ブースを訪問し、SNSに投稿しました", key="booth_visit_completed")
    
    if completed:
        if st.button("タスク完了", type="primary", use_container_width=True):
            # 進捗を保存
            try:
                # ユーザー情報を取得
                current_user = st.session_state.authenticated_user
                
                # タスク進捗ユースケースを初期化
                task_progress_repo = TaskProgressRepositoryImpl()
                user_repo = UserRepositoryImpl()
                progress_repo = ProgressRepositoryImpl()
                task_progress_use_case = TaskProgressUseCase(task_progress_repo, user_repo, progress_repo)
                
                # 回答データを準備
                answer_data = {
                    "booth_visited": task.booth_name,
                    "twitter_posted": True,
                    "completed_at": str(datetime.now())
                }
                
                # 非同期関数を実行
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    task_progress_use_case.complete_task(
                        user_id=current_user.id,
                        task_id=task.id,
                        mission_id=task.mission_id,
                        answer_data=answer_data
                    )
                )
                loop.close()
                
                if result['success']:
                    st.balloons()
                    st.success("🎉 タスクが完了しました！ご参加ありがとうございます！")
                    if result.get('mission_completed'):
                        st.success("🏆 ミッションも完了しました！")
                else:
                    st.warning(result['message'])
                
            except Exception as e:
                st.error(f"進捗保存エラー: {e}")
            
            # タスク一覧に戻る
            st.switch_page("pages/tasks.py")

def main():
    """メイン関数"""
    
    # 認証チェック
    if 'authenticated_user' not in st.session_state or st.session_state.authenticated_user is None:
        st.error("認証が必要です。ログインページに戻ります。")
        st.switch_page("launch_screen.py")
        st.stop()
    
    # タスクIDの取得
    if 'current_task_id' not in st.session_state:
        st.error("タスクが選択されていません。ダッシュボードに戻ります。")
        st.switch_page("pages/dashboard.py")
        st.stop()
    
    task_id = st.session_state.current_task_id
    
    try:
        # タスク情報を取得
        task = get_task_by_id(task_id)
        
        # タスクタイプの確認
        if task.task_type != TaskType.BOOTH_VISIT:
            st.error("このタスクはブース訪問タイプではありません。")
            st.switch_page("pages/tasks.py")
            st.stop()
        
        # ヘッダー
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("← タスク一覧に戻る"):
                st.switch_page("pages/tasks.py")
        
        # ブース訪問タスク表示
        render_booth_visit(task)
                
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        st.error("タスク一覧に戻ります。")
        if st.button("タスク一覧に戻る"):
            st.switch_page("pages/tasks.py")

if __name__ == "__main__":
    main()