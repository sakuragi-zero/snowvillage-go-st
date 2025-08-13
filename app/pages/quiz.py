"""
クイズ表示ページ
技術系クイズの問題を表示し、回答処理を行う
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
    page_title="Snow Village - クイズ",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# スタイル適用
st.markdown(get_main_styles(), unsafe_allow_html=True)

def render_quiz(task):
    """クイズを描画"""
    
    st.markdown(f"# 🧠 {task.title}")
    st.markdown(f"**{task.description}**")
    st.markdown("---")
    
    # 問題文
    st.markdown(f"## 問題")
    st.markdown(f"### {task.question}")
    
    # 選択肢
    st.markdown("### 選択肢を選んでください:")
    
    # セッション状態の初期化
    if 'quiz_answered' not in st.session_state:
        st.session_state.quiz_answered = False
    if 'selected_choice' not in st.session_state:
        st.session_state.selected_choice = None
    
    # 選択肢表示
    choices = task.choices
    if not st.session_state.quiz_answered:
        # 回答前
        selected = st.radio(
            "選択してください:",
            options=[choice.id for choice in choices],
            format_func=lambda x: next(choice.text for choice in choices if choice.id == x),
            key="quiz_choice"
        )
        
        if st.button("回答する", type="primary", use_container_width=True):
            st.session_state.selected_choice = selected
            st.session_state.quiz_answered = True
            st.rerun()
    
    else:
        # 回答後
        selected_choice_id = st.session_state.selected_choice
        selected_choice = next(choice for choice in choices if choice.id == selected_choice_id)
        
        # 全選択肢を表示（正解・不正解を示す）
        for choice in choices:
            if choice.id == selected_choice_id:
                if choice.is_correct:
                    st.success(f"✅ {choice.text} （あなたの回答）")
                else:
                    st.error(f"❌ {choice.text} （あなたの回答）")
            elif choice.is_correct:
                st.success(f"✅ {choice.text} （正解）")
            else:
                st.info(f"📝 {choice.text}")
        
        # 結果表示
        if selected_choice.is_correct:
            st.balloons()
            st.success("🎉 正解です！")
        else:
            st.error("❌ 不正解です。")
        
        # 解説表示
        if task.explanation:
            st.markdown("### 💡 解説")
            st.info(task.explanation)
        
        # 報酬表示
        st.markdown("### 🎁 獲得報酬")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("XP", f"+{task.xp_reward}")
        with col2:
            st.metric("ジェム", f"+{task.gem_reward}")
        
        # 完了ボタン
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
                    "selected_choice": st.session_state.selected_choice,
                    "is_correct": selected_choice.is_correct,
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
                    st.success("🎉 タスクが完了しました！")
                    if result.get('mission_completed'):
                        st.balloons()
                        st.success("🏆 ミッションも完了しました！")
                else:
                    st.warning(result['message'])
                
            except Exception as e:
                st.error(f"進捗保存エラー: {e}")
            
            # セッション状態をクリア
            if 'quiz_answered' in st.session_state:
                del st.session_state.quiz_answered
            if 'selected_choice' in st.session_state:
                del st.session_state.selected_choice
            
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
        if task.task_type != TaskType.QUIZ:
            st.error("このタスクはクイズタイプではありません。")
            st.switch_page("pages/tasks.py")
            st.stop()
        
        # ヘッダー
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("← タスク一覧に戻る"):
                # セッション状態をクリア
                if 'quiz_answered' in st.session_state:
                    del st.session_state.quiz_answered
                if 'selected_choice' in st.session_state:
                    del st.session_state.selected_choice
                st.switch_page("pages/tasks.py")
        
        # クイズ表示
        render_quiz(task)
                
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        st.error("タスク一覧に戻ります。")
        if st.button("タスク一覧に戻る"):
            st.switch_page("pages/tasks.py")

if __name__ == "__main__":
    main()