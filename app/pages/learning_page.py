"""学習メインページ"""

import streamlit as st
from typing import List
from app.database.models import User, Challenge
from app.database.db_manager import DatabaseManager
from app.auth.auth_manager import AuthManager
from app.auth.session_manager import SessionManager


class LearningPage:
    """学習メインページクラス"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.auth_manager = AuthManager(db)
        self.session_manager = SessionManager(db)
    
    def render(self):
        """学習ページをレンダリング"""
        # ログイン確認
        if not self.session_manager.is_logged_in():
            st.error("ログインが必要です。")
            st.stop()
        
        current_user = self.session_manager.get_current_user()
        if not current_user:
            st.error("ユーザー情報を取得できませんでした。")
            st.stop()
        
        # ページスタイル
        self._render_styles()
        
        # ヘッダー
        self._render_header(current_user)
        
        # ユーザー統計
        self._render_user_stats(current_user)
        
        # チャレンジ一覧
        self._render_challenges()
    
    def _render_styles(self):
        """ページスタイルを適用"""
        st.markdown("""
        <style>
        .main-header {
            background: linear-gradient(135deg, #1e2a78, #3730a3, #4338ca);
            color: white;
            padding: 2rem;
            border-radius: 16px;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .stats-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            text-align: center;
            margin-bottom: 1rem;
        }
        
        .challenge-card {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .challenge-card:hover {
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            transform: translateY(-2px);
        }
        
        .difficulty-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            color: white;
            margin-left: 0.5rem;
        }
        
        .difficulty-1 { background: #10b981; }
        .difficulty-2 { background: #f59e0b; }
        .difficulty-3 { background: #ef4444; }
        
        .logout-btn {
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 8px;
            padding: 0.5rem 1rem;
            cursor: pointer;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def _render_header(self, user: User):
        """ヘッダーを表示"""
        st.markdown(f"""
        <div class="main-header">
            <h1>❄️ SnowVillage GO</h1>
            <h2>ようこそ、{user.name} さん！</h2>
            <p>Snowflakeを学んで、クエストをクリアしよう！</p>
        </div>
        """, unsafe_allow_html=True)
        
        # ログアウトボタン
        col1, col2, col3 = st.columns([4, 1, 1])
        with col3:
            if st.button("🚪 ログアウト", key="logout_btn"):
                self.session_manager.logout_user()
                st.rerun()
    
    def _render_user_stats(self, user: User):
        """ユーザー統計を表示"""
        stats = self.auth_manager.get_user_stats(user.id)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stats-card">
                <h3>🏆 総スコア</h3>
                <h2>{stats['total_score']}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stats-card">
                <h3>✅ 完了済み</h3>
                <h2>{stats['completed_challenges']}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stats-card">
                <h3>📊 進捗率</h3>
                <h2>{stats['completion_rate']:.1f}%</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="stats-card">
                <h3>🎯 全チャレンジ</h3>
                <h2>{stats['total_challenges']}</h2>
            </div>
            """, unsafe_allow_html=True)
    
    def _render_challenges(self):
        """チャレンジ一覧を表示"""
        st.markdown("## 🎮 チャレンジ一覧")
        
        challenges = self._get_challenges()
        current_user = self.session_manager.get_current_user()
        
        if not challenges:
            st.info("チャレンジがまだありません。")
            return
        
        for challenge in challenges:
            # チャレンジの進捗状況を取得
            progress = self._get_challenge_progress(current_user.id, challenge.id)
            
            # チャレンジカード
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    # ステータスアイコン
                    status_icon = "✅" if progress and progress.completed else "⭕"
                    
                    st.markdown(f"""
                    <div class="challenge-card">
                        <h3>{status_icon} {challenge.title} 
                            <span class="difficulty-badge difficulty-{challenge.difficulty}">
                                レベル {challenge.difficulty}
                            </span>
                        </h3>
                        <p><strong>カテゴリ:</strong> {challenge.category}</p>
                        <p>{challenge.description}</p>
                        <p><strong>獲得ポイント:</strong> {challenge.points} pt</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    button_text = "再挑戦" if progress and progress.completed else "挑戦する"
                    button_key = f"challenge_{challenge.id}"
                    
                    if st.button(f"🎯 {button_text}", key=button_key, use_container_width=True):
                        # チャレンジページに遷移
                        st.session_state.current_challenge_id = challenge.id
                        st.session_state.page = "challenge"
                        st.rerun()
    
    def _get_challenges(self) -> List[Challenge]:
        """全チャレンジを取得"""
        try:
            with self.db.get_connection() as conn:
                rows = conn.execute("""
                    SELECT * FROM challenges 
                    ORDER BY difficulty, id
                """).fetchall()
                
                return [Challenge.from_db_row(row) for row in rows]
                
        except Exception as e:
            st.error(f"チャレンジ取得エラー: {e}")
            return []
    
    def _get_challenge_progress(self, user_id: int, challenge_id: int):
        """チャレンジの進捗状況を取得"""
        try:
            with self.db.get_connection() as conn:
                row = conn.execute("""
                    SELECT * FROM user_progress 
                    WHERE user_id = ? AND challenge_id = ?
                """, (user_id, challenge_id)).fetchone()
                
                if row:
                    from app.database.models import UserProgress
                    return UserProgress.from_db_row(row)
                return None
                
        except Exception as e:
            st.error(f"進捗取得エラー: {e}")
            return None