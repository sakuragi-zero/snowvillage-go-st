"""
タスク一覧ページ
選択されたミッションのタスク一覧を表示
"""
import streamlit as st
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from infrastructure.services.task_loader_service import get_tasks_by_mission_id
from infrastructure.services.mission_loader_service import get_mission_by_id
from domain.entities.task import TaskType
from presentation.components.styles import get_main_styles

# ページ設定
st.set_page_config(
    page_title="Snow Village - タスク一覧",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# スタイル適用
st.markdown(get_main_styles(), unsafe_allow_html=True)

def render_task_card(task, mission_title):
    """タスクカードを描画"""
    
    # タスクタイプによるアイコン
    type_icon = "🧠" if task.task_type == TaskType.QUIZ else "📍"
    type_text = "クイズ" if task.task_type == TaskType.QUIZ else "ブース訪問"
    
    # カードHTML
    card_html = f"""
    <div class="mission-card" style="margin-bottom: 1rem;">
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <div style="font-size: 30px; margin-right: 10px;">{type_icon}</div>
            <div>
                <h3 style="margin: 0; color: #000000 !important;">{task.title}</h3>
                <p style="margin: 0; font-size: 12px; color: #666666 !important;">{type_text}</p>
            </div>
        </div>
        <p style="font-size: 14px; color: #000000 !important; margin-bottom: 10px;">{task.description}</p>
        <p style="font-size: 12px; color: #666666 !important; margin: 0;">
            報酬: {task.xp_reward}XP, {task.gem_reward}💎
        </p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    
    # ボタン
    if st.button(f"開始", key=f"start_task_{task.id}", use_container_width=True):
        # タスクを開始 - セッション状態に保存して問題画面に遷移
        st.session_state.current_task_id = task.id
        st.session_state.current_mission_id = task.mission_id
        if task.task_type == TaskType.QUIZ:
            st.switch_page("pages/quiz.py")
        else:
            st.switch_page("pages/booth_visit.py")

def main():
    """メイン関数"""
    
    # 認証チェック
    if 'authenticated_user' not in st.session_state or st.session_state.authenticated_user is None:
        st.error("認証が必要です。ログインページに戻ります。")
        st.switch_page("launch_screen.py")
        st.stop()
    
    # ミッションIDの取得
    if 'current_mission_id' not in st.session_state:
        st.error("ミッションが選択されていません。ダッシュボードに戻ります。")
        st.switch_page("pages/dashboard.py")
        st.stop()
    
    mission_id = st.session_state.current_mission_id
    
    try:
        # ミッション情報を取得
        mission = get_mission_by_id(mission_id)
        
        # タスク一覧を取得
        tasks = get_tasks_by_mission_id(mission_id)
        
        # ヘッダー
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("← ダッシュボードに戻る"):
                st.switch_page("pages/dashboard.py")
        
        st.markdown(f"# {mission.icon} {mission.title}")
        st.markdown(f"**{mission.description}**")
        st.markdown("---")
        
        if not tasks:
            st.warning(f"ミッション「{mission.title}」にはまだタスクがありません。")
            return
        
        st.markdown(f"## タスク一覧 ({len(tasks)}個)")
        
        # タスクカード表示
        cols = st.columns(2)
        for i, task in enumerate(tasks):
            col = cols[i % 2]
            
            with col:
                render_task_card(task, mission.title)
                
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        st.error("ダッシュボードに戻ります。")
        if st.button("ダッシュボードに戻る"):
            st.switch_page("pages/dashboard.py")

if __name__ == "__main__":
    main()