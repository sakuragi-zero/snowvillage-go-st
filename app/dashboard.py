"""
ログイン後のダッシュボードページ
クリーンアーキテクチャに基づいた実装
"""
import streamlit as st
import pandas as pd
import asyncio
from datetime import datetime
from typing import List, Dict, Any

# ドメイン層
from domain.entities.user import User
from domain.entities.mission import Mission
from domain.entities.progress import Progress

# アプリケーション層
from application.use_cases.progress_use_case import ProgressUseCase

# インフラストラクチャ層
from infrastructure.database.connection import db
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from infrastructure.repositories.progress_repository_impl import ProgressRepositoryImpl

# プレゼンテーション層
from presentation.components.styles import get_main_styles
from presentation.components.metrics import display_user_metrics
from presentation.components.mission_card import display_mission_card
from presentation.components.progress_path import display_progress_path
from presentation.components.achievements import get_achievements, display_achievements


# ページ設定
st.set_page_config(
    page_title="Snow Village - ミッション学習",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# スタイル適用
st.markdown(get_main_styles(), unsafe_allow_html=True)


# ミッションデータ（本来はデータベースから取得）
MISSIONS = [
    Mission(1, '基本の挨拶', '👋', '基本的な挨拶を学びましょう', 5, 50, 10, 0),
    Mission(2, '自己紹介', '🙋', '自己紹介の方法を学びましょう', 7, 70, 15, 1),
    Mission(3, '家族について', '👨‍👩‍👧‍👦', '家族に関する表現を学びましょう', 6, 60, 12, 2),
    Mission(4, '食べ物と飲み物', '🍽️', '食事に関する表現を学びましょう', 8, 80, 20, 3),
    Mission(5, '時間と日付', '⏰', '時間の表現を学びましょう', 6, 65, 15, 4)
]


class DashboardPage:
    """ダッシュボードページクラス"""
    
    def __init__(self):
        self.user_repo = UserRepositoryImpl()
        self.progress_repo = ProgressRepositoryImpl()
        self.progress_use_case = ProgressUseCase(self.user_repo, self.progress_repo)
        self.current_user_id = 1  # デモ用、実際は認証から取得
        
        # データベース初期化
        db.create_tables()
        
    def initialize_session_state(self):
        """セッション状態の初期化"""
        if 'user_data' not in st.session_state:
            st.session_state.user_data = {
                'id': self.current_user_id,
                'username': 'testuser',
                'email': 'test@example.com',
                'streak': 0,
                'total_xp': 0,
                'daily_xp': 0,
                'gems': 50,
                'last_login': datetime.now().date(),
            }
    
    def run_async_function(self, coro):
        """非同期関数を実行するヘルパー"""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)
    
    def get_or_create_user(self) -> User:
        """ユーザーを取得または作成"""
        user = self.run_async_function(self.user_repo.get_by_id(self.current_user_id))
        
        if user is None:
            # ユーザーが存在しない場合は作成
            new_user = User(
                id=None,
                username=st.session_state.user_data['username'],
                email=st.session_state.user_data['email'],
                created_at=None,
                last_login=st.session_state.user_data['last_login'],
                streak=st.session_state.user_data['streak'],
                total_xp=st.session_state.user_data['total_xp'],
                daily_xp=st.session_state.user_data['daily_xp'],
                gems=st.session_state.user_data['gems']
            )
            user = self.run_async_function(self.user_repo.create(new_user))
        else:
            # ログイン情報を更新
            user = self.run_async_function(self.progress_use_case.update_user_login(user.id))
        
        return user
    
    def handle_lesson_completion(self, mission_id: int):
        """レッスン完了処理"""
        mission = next(m for m in MISSIONS if m.id == mission_id)
        result = self.run_async_function(
            self.progress_use_case.complete_lesson(self.current_user_id, mission)
        )
        
        # 成功メッセージ
        if result['mission_completed']:
            st.success(f"🎉 {mission.title}を完了しました！ +{result['mission_xp']}XP, +{result['gems']}💎")
        else:
            st.success(f"レッスン完了！ +{result['lesson_xp']}XP")
        
        st.rerun()
    
    def render_learning_tab(self, user: User):
        """学習タブを描画"""
        st.markdown("## 学習パス")
        
        # 完了済みミッション取得
        completed_missions = set(self.run_async_function(
            self.progress_use_case.get_completed_missions(user.id)
        ))
        
        # 進捗パス表示
        display_progress_path(MISSIONS, completed_missions)
        
        st.markdown("---")
        st.markdown("## 現在のミッション")
        
        # ミッションカード表示
        cols = st.columns(3)
        for i, mission in enumerate(MISSIONS):
            col = cols[i % 3]
            
            with col:
                # 進捗取得
                progress = self.run_async_function(
                    self.progress_use_case.get_mission_progress(user.id, mission.id)
                )
                
                # ロック判定
                is_locked = i > 0 and MISSIONS[i-1].id not in completed_missions
                
                # ミッションカード表示
                display_mission_card(
                    mission=mission,
                    progress=progress,
                    is_locked=is_locked,
                    on_lesson_click=self.handle_lesson_completion
                )
    
    def render_progress_tab(self, user: User):
        """進捗タブを描画"""
        st.markdown("## 学習進捗")
        
        # 進捗データ取得
        user_progress = self.run_async_function(self.progress_use_case.get_user_progress(user.id))
        progress_dict = {p.mission_id: p for p in user_progress}
        
        # 進捗データの準備
        progress_data = []
        for mission in MISSIONS:
            progress = progress_dict.get(mission.id)
            completed_lessons = progress.completed_lessons if progress else 0
            is_completed = progress.is_completed if progress else False
            
            progress_data.append({
                'ミッション': mission.title,
                '進捗': f"{completed_lessons}/{mission.lessons}",
                '完了率': f"{(completed_lessons / mission.lessons * 100):.0f}%",
                'ステータス': '✅ 完了' if is_completed else '📚 学習中' if completed_lessons > 0 else '🔒 未開始',
                'XP報酬': mission.xp_reward,
                'ジェム報酬': mission.gem_reward
            })
        
        df = pd.DataFrame(progress_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # 統計情報
        col1, col2 = st.columns(2)
        completed_count = len([p for p in user_progress if p.is_completed])
        total_lessons_completed = sum(p.completed_lessons for p in user_progress)
        total_lessons = sum(m.lessons for m in MISSIONS)
        
        with col1:
            st.metric("完了ミッション数", f"{completed_count}/{len(MISSIONS)}")
        with col2:
            st.metric("総レッスン進捗", f"{total_lessons_completed}/{total_lessons}")
    
    def render_achievements_tab(self, user: User):
        """実績タブを描画"""
        st.markdown("## 🏆 実績")
        
        completed_count = len(self.run_async_function(
            self.progress_use_case.get_completed_missions(user.id)
        ))
        
        achievements = get_achievements(user, completed_count, len(MISSIONS))
        display_achievements(achievements)
    
    def render_debug_section(self, user: User):
        """デバッグセクション"""
        with st.expander("🔧 デバッグ情報"):
            st.write("ユーザー情報:")
            st.json({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'streak': user.streak,
                'total_xp': user.total_xp,
                'daily_xp': user.daily_xp,
                'gems': user.gems,
                'last_login': str(user.last_login)
            })
            
            if st.button("ユーザーデータリセット"):
                # データベースから進捗とユーザーを削除
                self.run_async_function(self.user_repo.delete(user.id))
                st.session_state.clear()
                st.rerun()
    
    def run(self):
        """メインアプリケーション実行"""
        self.initialize_session_state()
        
        # ユーザー取得
        user = self.get_or_create_user()
        
        # ヘッダーメトリクス
        display_user_metrics(user)
        st.markdown("---")
        
        # タブ
        tab1, tab2, tab3 = st.tabs(["🎯 学習", "📊 進捗", "🏆 実績"])
        
        with tab1:
            self.render_learning_tab(user)
        
        with tab2:
            self.render_progress_tab(user)
        
        with tab3:
            self.render_achievements_tab(user)
        
        # デバッグセクション（開発時のみ）
        self.render_debug_section(user)


if __name__ == "__main__":
    dashboard = DashboardPage()
    dashboard.run()