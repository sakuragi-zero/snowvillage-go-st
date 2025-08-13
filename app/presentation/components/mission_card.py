import streamlit as st
from typing import Optional
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from domain.entities.mission import Mission
from domain.entities.progress import Progress


def display_mission_card(
    mission: Mission, 
    progress: Optional[Progress] = None,
    is_locked: bool = False
):
    """ミッションカードを表示"""
    
    # 進捗情報を計算
    completed_lessons = progress.completed_lessons if progress else 0
    is_completed = progress.is_completed if progress else False
    progress_percent = (completed_lessons / mission.lessons * 100) if mission.lessons > 0 else 0
    
    # カードのクラス決定
    card_class = ""
    if is_completed:
        card_class = "completed-card"
    elif is_locked:
        card_class = "locked-card"
    
    # ステータステキスト
    status_text = ""
    if is_completed:
        status_text = "完了 ✓"
    elif is_locked:
        status_text = "ロック中 🔒"
    else:
        status_text = f"{completed_lessons}/{mission.lessons} タスク数"
    
    # カードHTML
    card_html = f"""
    <div class="mission-card {card_class}">
        <div style="font-size: 50px; margin-bottom: 10px;">{mission.icon}</div>
        <h3>{mission.title}</h3>
        <p style="font-size: 14px;">{mission.description}</p>
        <div class="progress-container">
            <div class="progress-bar" style="width: {progress_percent}%;"></div>
        </div>
        <p style="margin: 5px 0; font-size: 14px; color: #000000 !important;">
            {status_text}
        </p>
        <p style="font-size: 12px; color: #666666 !important;">
            報酬: {mission.xp_reward}XP, {mission.gem_reward}💎
        </p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    
    # ボタン
    if not is_locked and not is_completed:
        if st.button(f"挑戦する", key=f"learn_{mission.id}"):
            # タスク画面に遷移
            st.session_state.current_mission_id = mission.id
            st.switch_page("pages/tasks.py")
    elif is_completed:
        st.button("完了済み ✓", key=f"completed_{mission.id}", disabled=True)
    else:
        st.button("🔒 ロック中", key=f"locked_{mission.id}", disabled=True)