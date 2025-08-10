import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from domain.entities.user import User


def display_user_metrics(user: User):
    """ユーザーメトリクスを表示"""
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <h3>🔥 {user.streak}日</h3>
            <p>ストリーク</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <h3>⚡ {user.daily_xp} XP</h3>
            <p>今日のXP</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <h3>📊 {user.total_xp} XP</h3>
            <p>総XP</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-container">
            <h3>💎 {user.gems}</h3>
            <p>ジェム</p>
        </div>
        """, unsafe_allow_html=True)