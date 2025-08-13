"""
ログイン後のダッシュボードページ
クリーンアーキテクチャに基づいた実装
"""
import streamlit as st
import pandas as pd
import asyncio
import time
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
    initial_sidebar_state="expanded"
)

# スタイル適用
st.markdown(get_main_styles(), unsafe_allow_html=True)


# ミッション読み込みサービス
from infrastructure.services.mission_loader_service import get_missions
from infrastructure.services.task_loader_service import get_tasks_by_mission_id


class DashboardPage:
    """ダッシュボードページクラス"""
    
    def __init__(self):
        self.user_repo = UserRepositoryImpl()
        self.progress_repo = ProgressRepositoryImpl()
        self.progress_use_case = ProgressUseCase(self.user_repo, self.progress_repo)
        
        # 認証ユーザー確認
        if 'authenticated_user' not in st.session_state or st.session_state.authenticated_user is None:
            st.error("認証が必要です。ログインページに戻ります。")
            st.switch_page("launch_screen.py")
            st.stop()
        
        self.current_user = st.session_state.authenticated_user
        self.current_user_id = self.current_user.id
        
        # データベース初期化
        db.create_tables()
        
        # ミッション読み込み
        self.missions = get_missions()
        
    def initialize_session_state(self):
        """セッション状態の初期化"""
        # 認証ユーザーの情報を使用
        if 'user_data' not in st.session_state:
            st.session_state.user_data = {
                'id': self.current_user.id,
                'username': self.current_user.username,
                'email': self.current_user.email,
                'streak': self.current_user.streak,
                'total_xp': self.current_user.total_xp,
                'daily_xp': self.current_user.daily_xp,
                'gems': self.current_user.gems,
                'last_login': self.current_user.last_login,
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
        """認証済みユーザーを取得（既に認証済みなのでそのまま返す）"""
        # ログイン情報を更新
        user = self.run_async_function(self.progress_use_case.update_user_login(self.current_user.id))
        return user if user else self.current_user
    
    def handle_lesson_completion(self, mission_id: int):
        """レッスン完了処理"""
        mission = next(m for m in self.missions if m.id == mission_id)
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
        st.markdown("## ロードマップ")
        
        # 完了済みミッション取得
        completed_missions = set(self.run_async_function(
            self.progress_use_case.get_completed_missions(user.id)
        ))
        
        # 進捗パス表示
        display_progress_path(self.missions, completed_missions)
        
        st.markdown("---")
        st.markdown("## 現在のミッション")
        
        # ミッションカード表示
        cols = st.columns(3)
        for i, mission in enumerate(self.missions):
            col = cols[i % 3]
            
            with col:
                # 進捗取得
                progress = self.run_async_function(
                    self.progress_use_case.get_mission_progress(user.id, mission.id)
                )
                
                # YMLベースでタスク数を取得して進捗を更新
                mission_tasks = get_tasks_by_mission_id(mission.id)
                total_tasks = len(mission_tasks)
                
                # 進捗が存在しない場合は初期化
                if progress is None:
                    from domain.entities.progress import Progress
                    progress = Progress(
                        id=None,
                        user_id=user.id,
                        mission_id=mission.id,
                        completed_lessons=0,
                        is_completed=False,
                        completed_at=None,
                        created_at=None,
                        updated_at=None
                    )
                
                # lessonsをYMLベースのタスク数で更新
                mission.lessons = total_tasks
                
                # ロック判定
                is_locked = i > 0 and self.missions[i-1].id not in completed_missions
                
                # ミッションカード表示
                display_mission_card(
                    mission=mission,
                    progress=progress,
                    is_locked=is_locked
                )
    
    def render_progress_tab(self, user: User):
        """進捗タブを描画"""
        st.markdown("## 進捗")
        
        # 進捗データ取得
        user_progress = self.run_async_function(self.progress_use_case.get_user_progress(user.id))
        progress_dict = {p.mission_id: p for p in user_progress}
        
        # 進捗データの準備
        progress_data = []
        for mission in self.missions:
            progress = progress_dict.get(mission.id)
            completed_lessons = progress.completed_lessons if progress else 0
            is_completed = progress.is_completed if progress else False
            
            # YMLベースでタスク数を取得
            mission_tasks = get_tasks_by_mission_id(mission.id)
            total_tasks = len(mission_tasks)
            
            # ゼロ除算を防ぐ
            completion_rate = 0 if total_tasks == 0 else (completed_lessons / total_tasks * 100)
            
            progress_data.append({
                'ミッション': mission.title,
                '進捗': f"{completed_lessons}/{total_tasks}",
                '完了率': f"{completion_rate:.0f}%",
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
        
        # YMLベースで総タスク数を計算
        total_tasks = 0
        for mission in self.missions:
            mission_tasks = get_tasks_by_mission_id(mission.id)
            total_tasks += len(mission_tasks)
        
        with col1:
            st.metric("完了ミッション数", f"{completed_count}/{len(self.missions)}")
        with col2:
            st.metric("総タスク進捗", f"{total_lessons_completed}/{total_tasks}")
    
    def render_achievements_tab(self, user: User):
        """実績タブを描画"""
        st.markdown("## 🏆 実績")
        
        completed_count = len(self.run_async_function(
            self.progress_use_case.get_completed_missions(user.id)
        ))
        
        achievements = get_achievements(user, completed_count, len(self.missions))
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
    
    def render_sidebar(self, user: User):
        """サイドバーを描画"""
        with st.sidebar:
            # ロゴとタイトル
            st.markdown("### ❄️ Snow Village")
            st.markdown("---")
            
            # ユーザー情報
            st.markdown("#### ユーザー情報")
            st.markdown(f"**名前:** {user.username}")
            st.markdown(f"**総XP:** {user.total_xp:,}")
            st.markdown(f"**ジェム:** {user.gems:,}")
            st.markdown(f"**ストリーク:** {user.streak}日")
            
            st.markdown("---")
            
            # ナビゲーション
            st.markdown("#### ナビゲーション")
            st.markdown("📊 **現在のページ:** ダッシュボード")
            
            # 余白を作る
            st.markdown("<div style='height: 300px;'></div>", unsafe_allow_html=True)
            
            # ログアウトボタン（サイドバーの下部）
            st.markdown("---")
            if st.button("🚪 ログアウト", use_container_width=True):
                # セッション状態をクリア
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.success("ログアウトしました")
                time.sleep(1)
                st.switch_page("launch_screen.py")

    def run(self):
        """メインアプリケーション実行"""
        self.initialize_session_state()
        
        # ユーザー取得
        user = self.get_or_create_user()
        
        # サイドバー描画
        self.render_sidebar(user)
        
        # メインコンテンツ
        st.markdown(f"<h2 class='main-welcome'>こんにちは、{user.username}さん！</h2>", unsafe_allow_html=True)
        
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