"""セッション管理システム"""

import streamlit as st
import secrets
from typing import Optional
from datetime import datetime, timedelta
from app.database.models import User
from app.database.db_manager import DatabaseManager


class SessionManager:
    """Streamlitセッション管理クラス"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.session_duration = timedelta(hours=24)  # セッション持続時間
    
    def create_session(self, user: User) -> str:
        """
        新しいセッションを作成
        
        Args:
            user: ユーザーオブジェクト
            
        Returns:
            セッションID
        """
        session_id = secrets.token_urlsafe(32)
        expires_at = datetime.now() + self.session_duration
        
        try:
            with self.db.get_connection() as conn:
                # 既存のセッションを削除
                conn.execute("""
                    DELETE FROM sessions WHERE user_id = ?
                """, (user.id,))
                
                # 新しいセッションを作成
                conn.execute("""
                    INSERT INTO sessions (id, user_id, expires_at)
                    VALUES (?, ?, ?)
                """, (session_id, user.id, expires_at.isoformat()))
                
                conn.commit()
                
        except Exception as e:
            st.error(f"セッション作成エラー: {e}")
        
        return session_id
    
    def get_session_user(self, session_id: str) -> Optional[User]:
        """
        セッションIDからユーザーを取得
        
        Args:
            session_id: セッションID
            
        Returns:
            Userオブジェクト、無効な場合はNone
        """
        try:
            with self.db.get_connection() as conn:
                row = conn.execute("""
                    SELECT u.* FROM users u
                    JOIN sessions s ON u.id = s.user_id
                    WHERE s.id = ? AND s.expires_at > ?
                """, (session_id, datetime.now().isoformat())).fetchone()
                
                if row:
                    return User.from_db_row(row)
                return None
                
        except Exception as e:
            st.error(f"セッション取得エラー: {e}")
            return None
    
    def delete_session(self, session_id: str):
        """
        セッションを削除（ログアウト）
        
        Args:
            session_id: セッションID
        """
        try:
            with self.db.get_connection() as conn:
                conn.execute("""
                    DELETE FROM sessions WHERE id = ?
                """, (session_id,))
                conn.commit()
                
        except Exception as e:
            st.error(f"セッション削除エラー: {e}")
    
    def cleanup_expired_sessions(self):
        """期限切れセッションを削除"""
        try:
            with self.db.get_connection() as conn:
                conn.execute("""
                    DELETE FROM sessions WHERE expires_at <= ?
                """, (datetime.now().isoformat(),))
                conn.commit()
                
        except Exception as e:
            st.error(f"期限切れセッション削除エラー: {e}")
    
    def login_user(self, user: User):
        """
        Streamlitセッションにユーザーをログイン
        
        Args:
            user: ユーザーオブジェクト
        """
        # セッションIDを作成してStreamlitセッションに保存
        session_id = self.create_session(user)
        
        st.session_state.user_id = user.id
        st.session_state.user_name = user.name
        st.session_state.session_id = session_id
        st.session_state.logged_in = True
        
        # 期限切れセッションを清理
        self.cleanup_expired_sessions()
    
    def logout_user(self):
        """ユーザーをログアウト"""
        if 'session_id' in st.session_state:
            self.delete_session(st.session_state.session_id)
        
        # Streamlitセッションをクリア
        for key in ['user_id', 'user_name', 'session_id', 'logged_in']:
            if key in st.session_state:
                del st.session_state[key]
    
    def is_logged_in(self) -> bool:
        """
        ログイン状態を確認
        
        Returns:
            ログイン状態
        """
        if not st.session_state.get('logged_in', False):
            return False
        
        session_id = st.session_state.get('session_id')
        if not session_id:
            return False
        
        # セッションの有効性を確認
        user = self.get_session_user(session_id)
        if not user:
            self.logout_user()
            return False
        
        return True
    
    def get_current_user(self) -> Optional[User]:
        """
        現在のログインユーザーを取得
        
        Returns:
            現在のユーザー、ログインしていない場合はNone
        """
        if not self.is_logged_in():
            return None
        
        session_id = st.session_state.get('session_id')
        return self.get_session_user(session_id)