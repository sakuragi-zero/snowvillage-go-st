import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json

# ページ設定
st.set_page_config(
    page_title="ミッション学習アプリ",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# カスタムCSS
st.markdown("""
<style>
    /* メインコンテナ */
    .main {
        padding: 0rem 1rem;
    }
    
    /* カードスタイル */
    .mission-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.2s;
    }
    
    .mission-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
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
        color: white;
        border-radius: 10px;
        padding: 10px 30px;
        font-weight: bold;
        border: none;
        transition: background-color 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #45a000;
    }
    
    /* メトリクススタイル */
    .metric-container {
        background: white;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
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
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'streak': 0,
        'total_xp': 0,
        'daily_xp': 0,
        'gems': 50,
        'last_login': datetime.now().date(),
        'completed_missions': [],
        'current_mission': 0,
        'mission_progress': {}
    }

# ミッションデータ
MISSIONS = [
    {
        'id': 1,
        'title': '基本の挨拶',
        'icon': '👋',
        'description': '基本的な挨拶を学びましょう',
        'lessons': 5,
        'xp_reward': 50,
        'gem_reward': 10
    },
    {
        'id': 2,
        'title': '自己紹介',
        'icon': '🙋',
        'description': '自己紹介の方法を学びましょう',
        'lessons': 7,
        'xp_reward': 70,
        'gem_reward': 15
    },
    {
        'id': 3,
        'title': '家族について',
        'icon': '👨‍👩‍👧‍👦',
        'description': '家族に関する表現を学びましょう',
        'lessons': 6,
        'xp_reward': 60,
        'gem_reward': 12
    },
    {
        'id': 4,
        'title': '食べ物と飲み物',
        'icon': '🍽️',
        'description': '食事に関する表現を学びましょう',
        'lessons': 8,
        'xp_reward': 80,
        'gem_reward': 20
    },
    {
        'id': 5,
        'title': '時間と日付',
        'icon': '⏰',
        'description': '時間の表現を学びましょう',
        'lessons': 6,
        'xp_reward': 65,
        'gem_reward': 15
    }
]

# ストリーク更新関数
def update_streak():
    today = datetime.now().date()
    last_login = st.session_state.user_data['last_login']
    
    if isinstance(last_login, str):
        last_login = datetime.strptime(last_login, '%Y-%m-%d').date()
    
    if today == last_login:
        return
    elif today == last_login + timedelta(days=1):
        st.session_state.user_data['streak'] += 1
    else:
        st.session_state.user_data['streak'] = 1
    
    st.session_state.user_data['last_login'] = today

# XP追加関数
def add_xp(amount):
    st.session_state.user_data['total_xp'] += amount
    st.session_state.user_data['daily_xp'] += amount

# ジェム追加関数
def add_gems(amount):
    st.session_state.user_data['gems'] += amount

# ミッション完了関数
def complete_mission(mission_id):
    if mission_id not in st.session_state.user_data['completed_missions']:
        st.session_state.user_data['completed_missions'].append(mission_id)
        mission = next(m for m in MISSIONS if m['id'] == mission_id)
        add_xp(mission['xp_reward'])
        add_gems(mission['gem_reward'])
        st.success(f"🎉 {mission['title']}を完了しました！ +{mission['xp_reward']}XP, +{mission['gem_reward']}💎")

# レッスン進捗更新関数
def update_lesson_progress(mission_id):
    if mission_id not in st.session_state.user_data['mission_progress']:
        st.session_state.user_data['mission_progress'][mission_id] = 0
    
    mission = next(m for m in MISSIONS if m['id'] == mission_id)
    current_progress = st.session_state.user_data['mission_progress'][mission_id]
    
    if current_progress < mission['lessons']:
        st.session_state.user_data['mission_progress'][mission_id] += 1
        add_xp(10)  # レッスンごとに10XP
        
        if st.session_state.user_data['mission_progress'][mission_id] == mission['lessons']:
            complete_mission(mission_id)

# メインアプリ
def main():
    update_streak()
    
    # ヘッダー
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <h3>🔥 {st.session_state.user_data['streak']}日</h3>
            <p style="margin: 0; color: #666;">ストリーク</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <h3>⚡ {st.session_state.user_data['daily_xp']} XP</h3>
            <p style="margin: 0; color: #666;">今日のXP</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <h3>📊 {st.session_state.user_data['total_xp']} XP</h3>
            <p style="margin: 0; color: #666;">総XP</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-container">
            <h3>💎 {st.session_state.user_data['gems']}</h3>
            <p style="margin: 0; color: #666;">ジェム</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # タブ
    tab1, tab2, tab3 = st.tabs(["🎯 学習", "📊 進捗", "🏆 実績"])
    
    with tab1:
        st.markdown("## 学習パス")
        
        # 進捗パスの表示
        path_html = ""
        for i, mission in enumerate(MISSIONS):
            mission_id = mission['id']
            is_completed = mission_id in st.session_state.user_data['completed_missions']
            is_current = (i == 0 and not is_completed) or (i > 0 and MISSIONS[i-1]['id'] in st.session_state.user_data['completed_missions'] and not is_completed)
            is_locked = i > 0 and MISSIONS[i-1]['id'] not in st.session_state.user_data['completed_missions']
            
            # ノードのクラス
            node_class = ""
            node_content = mission['icon']
            if is_completed:
                node_class = "completed"
                node_content = "✓"
            elif is_current:
                node_class = "current"
            elif is_locked:
                node_content = "🔒"
            
            path_html += f'<div class="path-node {node_class}">{node_content}</div>'
            
            if i < len(MISSIONS) - 1:
                line_class = "completed" if is_completed else ""
                path_html += f'<div style="width: 4px; height: 40px; background: {"#58cc02" if is_completed else "#e0e0e0"}; margin: 0 auto;"></div>'
        
        st.markdown(f'<div style="background: white; border-radius: 15px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">{path_html}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ミッションカード
        st.markdown("## 現在のミッション")
        
        cols = st.columns(3)
        for i, mission in enumerate(MISSIONS):
            col = cols[i % 3]
            mission_id = mission['id']
            is_completed = mission_id in st.session_state.user_data['completed_missions']
            is_locked = i > 0 and MISSIONS[i-1]['id'] not in st.session_state.user_data['completed_missions']
            
            with col:
                card_class = ""
                if is_completed:
                    card_class = "completed-card"
                elif is_locked:
                    card_class = "locked-card"
                
                # ミッションカードのHTML
                progress = st.session_state.user_data['mission_progress'].get(mission_id, 0)
                progress_percent = (progress / mission['lessons']) * 100 if mission['lessons'] > 0 else 0
                
                card_html = f"""
                <div class="mission-card {card_class}">
                    <div style="font-size: 50px; margin-bottom: 10px;">{mission['icon']}</div>
                    <h3 style="margin: 10px 0;">{mission['title']}</h3>
                    <p style="color: #666; font-size: 14px;">{mission['description']}</p>
                    <div class="progress-container">
                        <div class="progress-bar" style="width: {progress_percent}%;"></div>
                    </div>
                    <p style="margin: 5px 0; font-size: 14px;">
                        {"完了 ✓" if is_completed else f"{progress}/{mission['lessons']} レッスン" if not is_locked else "ロック中 🔒"}
                    </p>
                    <p style="color: #666; font-size: 12px;">
                        報酬: {mission['xp_reward']}XP, {mission['gem_reward']}💎
                    </p>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                
                # ボタン
                if not is_locked and not is_completed:
                    if st.button(f"学習する", key=f"learn_{mission_id}"):
                        update_lesson_progress(mission_id)
                        st.rerun()
                elif is_completed:
                    st.button("完了済み ✓", key=f"completed_{mission_id}", disabled=True)
                else:
                    st.button("🔒 ロック中", key=f"locked_{mission_id}", disabled=True)
    
    with tab2:
        st.markdown("## 学習進捗")
        
        # 進捗データの準備
        progress_data = []
        for mission in MISSIONS:
            mission_id = mission['id']
            is_completed = mission_id in st.session_state.user_data['completed_missions']
            progress = st.session_state.user_data['mission_progress'].get(mission_id, 0)
            
            progress_data.append({
                'ミッション': mission['title'],
                '進捗': f"{progress}/{mission['lessons']}",
                '完了率': f"{(progress / mission['lessons'] * 100):.0f}%",
                'ステータス': '✅ 完了' if is_completed else '📚 学習中' if progress > 0 else '🔒 未開始',
                'XP報酬': mission['xp_reward'],
                'ジェム報酬': mission['gem_reward']
            })
        
        df = pd.DataFrame(progress_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # 統計情報
        col1, col2 = st.columns(2)
        with col1:
            st.metric("完了ミッション数", f"{len(st.session_state.user_data['completed_missions'])}/{len(MISSIONS)}")
        with col2:
            total_progress = sum(st.session_state.user_data['mission_progress'].values())
            total_lessons = sum(m['lessons'] for m in MISSIONS)
            st.metric("総レッスン進捗", f"{total_progress}/{total_lessons}")
    
    with tab3:
        st.markdown("## 🏆 実績")
        
        achievements = [
            {"name": "初心者", "desc": "最初のミッションを完了", "icon": "🌱", "unlocked": len(st.session_state.user_data['completed_missions']) >= 1},
            {"name": "学習者", "desc": "3つのミッションを完了", "icon": "📚", "unlocked": len(st.session_state.user_data['completed_missions']) >= 3},
            {"name": "マスター", "desc": "すべてのミッションを完了", "icon": "🎓", "unlocked": len(st.session_state.user_data['completed_missions']) >= len(MISSIONS)},
            {"name": "継続は力", "desc": "7日連続ログイン", "icon": "🔥", "unlocked": st.session_state.user_data['streak'] >= 7},
            {"name": "XPハンター", "desc": "500XP獲得", "icon": "⚡", "unlocked": st.session_state.user_data['total_xp'] >= 500},
            {"name": "ジェムコレクター", "desc": "100ジェム保有", "icon": "💎", "unlocked": st.session_state.user_data['gems'] >= 100},
        ]
        
        cols = st.columns(3)
        for i, achievement in enumerate(achievements):
            col = cols[i % 3]
            with col:
                if achievement['unlocked']:
                    st.markdown(f"""
                    <div style="background: #f0fdf4; border: 2px solid #58cc02; border-radius: 10px; padding: 20px; text-align: center; margin: 10px 0;">
                        <div style="font-size: 40px;">{achievement['icon']}</div>
                        <h4>{achievement['name']}</h4>
                        <p style="font-size: 14px; color: #666;">{achievement['desc']}</p>
                        <p style="color: #58cc02; font-weight: bold;">✓ 獲得済み</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: #f5f5f5; border: 2px solid #e0e0e0; border-radius: 10px; padding: 20px; text-align: center; margin: 10px 0; opacity: 0.6;">
                        <div style="font-size: 40px;">🔒</div>
                        <h4>{achievement['name']}</h4>
                        <p style="font-size: 14px; color: #666;">{achievement['desc']}</p>
                        <p style="color: #999;">未獲得</p>
                    </div>
                    """, unsafe_allow_html=True)

# デバッグ情報（開発時のみ表示）
def show_debug_info():
    with st.expander("🔧 デバッグ情報"):
        st.json(st.session_state.user_data)
        if st.button("データリセット"):
            st.session_state.user_data = {
                'streak': 0,
                'total_xp': 0,
                'daily_xp': 0,
                'gems': 50,
                'last_login': datetime.now().date(),
                'completed_missions': [],
                'current_mission': 0,
                'mission_progress': {}
            }
            st.rerun()

if __name__ == "__main__":
    main()
    # show_debug_info()  # 開発時はコメントアウトを外す