import streamlit as st
from typing import List, Dict, Any
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from domain.entities.user import User


def get_achievements(user: User, completed_missions_count: int, total_missions_count: int) -> List[Dict[str, Any]]:
    """実績リストを生成"""
    return [
        {
            "name": "初心者", 
            "desc": "最初のミッションを完了", 
            "icon": "🌱", 
            "unlocked": completed_missions_count >= 1
        },
        {
            "name": "学習者", 
            "desc": "3つのミッションを完了", 
            "icon": "📚", 
            "unlocked": completed_missions_count >= 3
        },
        {
            "name": "マスター", 
            "desc": "すべてのミッションを完了", 
            "icon": "🎓", 
            "unlocked": completed_missions_count >= total_missions_count
        },
        {
            "name": "継続は力", 
            "desc": "7日連続ログイン", 
            "icon": "🔥", 
            "unlocked": user.streak >= 7
        },
        {
            "name": "XPハンター", 
            "desc": "500XP獲得", 
            "icon": "⚡", 
            "unlocked": user.total_xp >= 500
        },
        {
            "name": "ジェムコレクター", 
            "desc": "100ジェム保有", 
            "icon": "💎", 
            "unlocked": user.gems >= 100
        },
    ]


def display_achievements(achievements: List[Dict[str, Any]]):
    """実績を表示"""
    cols = st.columns(3)
    
    for i, achievement in enumerate(achievements):
        col = cols[i % 3]
        with col:
            if achievement['unlocked']:
                st.markdown(f"""
                <div class="achievement-card achievement-unlocked">
                    <div style="font-size: 40px;">{achievement['icon']}</div>
                    <h4>{achievement['name']}</h4>
                    <p style="font-size: 14px; color: #666666;">{achievement['desc']}</p>
                    <p style="color: #58cc02; font-weight: bold;">✓ 獲得済み</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="achievement-card achievement-locked">
                    <div style="font-size: 40px;">🔒</div>
                    <h4>{achievement['name']}</h4>
                    <p style="font-size: 14px; color: #666666;">{achievement['desc']}</p>
                    <p style="color: #999999;">未獲得</p>
                </div>
                """, unsafe_allow_html=True)