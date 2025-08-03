"""
問題一覧ページ
ユーザーが挑戦できる問題の一覧を表示します。
"""

import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def problem_list_page():
    """問題一覧ページのUI"""
    st.set_page_config(
        page_title="問題一覧 - Snow Village",
        page_icon="❄️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # サイドバーを非表示
    st.markdown("<style>[data-testid='stSidebar'] { display: none; }</style>", unsafe_allow_html=True)
    
    # ユーザー情報の確認
    if "user_info" not in st.session_state or not st.session_state.user_info:
        st.error("ログインが必要です")
        if st.button("ログイン画面に戻る"):
            st.switch_page("main.py")
        return
    
    user_name = st.session_state.user_info.get("name", "ゲスト")
    
    # ヘッダー
    st.markdown(f"""
    <style>
        .stApp {{
            background: linear-gradient(135deg, #1a237e, #283593, #3949ab, #42a5f5);
        }}
        .header {{
            text-align: center;
            color: white;
            padding: 2rem 0;
        }}
        .problem-card {{
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            color: white;
        }}
        .difficulty-easy {{ border-left: 4px solid #4caf50; }}
        .difficulty-medium {{ border-left: 4px solid #ff9800; }}
        .difficulty-hard {{ border-left: 4px solid #f44336; }}
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="header">
        <h1>🎯 問題一覧</h1>
        <p>こんにちは、{user_name}さん！挑戦する問題を選んでください</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 問題リスト（サンプル）
    problems = [
        {
            "id": 1,
            "title": "基本クエリ入門",
            "description": "SELECTステートメントの基本を学びましょう",
            "difficulty": "easy",
            "points": 10
        },
        {
            "id": 2,
            "title": "データフィルタリング",
            "description": "WHERE句を使ったデータの絞り込み",
            "difficulty": "easy", 
            "points": 15
        },
        {
            "id": 3,
            "title": "集計とグルーピング",
            "description": "GROUP BYとHAVINGを使った集計処理",
            "difficulty": "medium",
            "points": 25
        },
        {
            "id": 4,
            "title": "複雑なJOIN操作",
            "description": "複数テーブルの結合とサブクエリ",
            "difficulty": "hard",
            "points": 40
        }
    ]
    
    # 問題カードの表示
    for problem in problems:
        difficulty_class = f"difficulty-{problem['difficulty']}"
        difficulty_text = {"easy": "初級", "medium": "中級", "hard": "上級"}[problem['difficulty']]
        
        st.markdown(f"""
        <div class="problem-card {difficulty_class}">
            <h3>問題 {problem['id']}: {problem['title']}</h3>
            <p>{problem['description']}</p>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span>難易度: {difficulty_text} | ポイント: {problem['points']}pt</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button(f"挑戦する", key=f"challenge_{problem['id']}"):
                st.session_state.selected_problem = problem
                st.info(f"問題{problem['id']}を選択しました（実装中）")
        with col2:
            if st.button(f"詳細", key=f"detail_{problem['id']}"):
                st.info(f"問題{problem['id']}の詳細（実装中）")
    
    # フッター
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("ログアウト"):
            del st.session_state.user_info
            st.switch_page("main.py")
    with col2:
        st.markdown(f"**総スコア**: 0 pt")

if __name__ == "__main__":
    problem_list_page()