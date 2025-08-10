import streamlit as st
from typing import List, Set
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from domain.entities.mission import Mission


def display_progress_path(missions: List[Mission], completed_mission_ids: Set[int]):
    """学習パスを表示"""
    path_html = ""
    
    for i, mission in enumerate(missions):
        mission_id = mission.id
        is_completed = mission_id in completed_mission_ids
        
        # 現在のミッション判定（未完了かつ前のミッションが完了済み）
        is_current = False
        if i == 0 and not is_completed:
            is_current = True
        elif i > 0 and missions[i-1].id in completed_mission_ids and not is_completed:
            is_current = True
        
        is_locked = i > 0 and missions[i-1].id not in completed_mission_ids
        
        # ノードのクラスとコンテンツ
        node_class = ""
        node_content = mission.icon
        if is_completed:
            node_class = "completed"
            node_content = "✓"
        elif is_current:
            node_class = "current"
        elif is_locked:
            node_content = "🔒"
        
        path_html += f'<div class="path-node {node_class}">{node_content}</div>'
        
        # 接続線
        if i < len(missions) - 1:
            line_color = "#58cc02" if is_completed else "#e0e0e0"
            path_html += f'<div style="width: 4px; height: 40px; background: {line_color}; margin: 0 auto;"></div>'
    
    # パス全体をコンテナで囲む
    container_html = f"""
    <div style="background: white; border-radius: 15px; padding: 30px; 
                box-shadow: 0 2px 10px rgba(0,0,0,0.1); color: #000000;">
        {path_html}
    </div>
    """
    
    st.markdown(container_html, unsafe_allow_html=True)