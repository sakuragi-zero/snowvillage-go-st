"""認証管理システム"""

import streamlit as st
from typing import Optional
from datetime import datetime
from app.database.models import User
from app.database.db_manager import DatabaseManager


class AuthManager:
    """ユーザー認証管理クラス"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    def create_user(self, name: str) -> Optional[User]:
        """
        新規ユーザーを作成
        
        Args:
            name: ユーザー名
            
        Returns:
            作成されたUserオブジェクト、失敗時はNone
        """
        try:
            with self.db.get_connection() as conn:
                cursor = conn.execute("""
                    INSERT INTO users (name, created_at, last_login)
                    VALUES (?, ?, ?)
                """, (name, datetime.now().isoformat(), datetime.now().isoformat()))
                
                user_id = cursor.lastrowid
                conn.commit()
                
                # 作成されたユーザーを取得
                return self.get_user_by_id(user_id)
                
        except Exception as e:
            st.error(f"ユーザー作成エラー: {e}")
            return None
    
    def get_user_by_name(self, name: str) -> Optional[User]:
        """
        名前でユーザーを取得
        
        Args:
            name: ユーザー名
            
        Returns:
            Userオブジェクト、見つからない場合はNone
        """
        try:
            with self.db.get_connection() as conn:
                row = conn.execute("""
                    SELECT * FROM users WHERE name = ?
                """, (name,)).fetchone()
                
                if row:
                    return User.from_db_row(row)
                return None
                
        except Exception as e:
            st.error(f"ユーザー取得エラー: {e}")
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        IDでユーザーを取得
        
        Args:
            user_id: ユーザーID
            
        Returns:
            Userオブジェクト、見つからない場合はNone
        """
        try:
            with self.db.get_connection() as conn:
                row = conn.execute("""
                    SELECT * FROM users WHERE id = ?
                """, (user_id,)).fetchone()
                
                if row:
                    return User.from_db_row(row)
                return None
                
        except Exception as e:
            st.error(f"ユーザー取得エラー: {e}")
            return None
    
    def update_last_login(self, user_id: int):
        """
        最終ログイン時刻を更新
        
        Args:
            user_id: ユーザーID
        """
        try:
            with self.db.get_connection() as conn:
                conn.execute("""
                    UPDATE users 
                    SET last_login = ? 
                    WHERE id = ?
                """, (datetime.now().isoformat(), user_id))
                conn.commit()
                
        except Exception as e:
            st.error(f"最終ログイン更新エラー: {e}")
    
    def authenticate_or_create_user(self, name: str) -> Optional[User]:
        """
        ユーザーを認証、存在しない場合は新規作成
        
        Args:
            name: ユーザー名
            
        Returns:
            Userオブジェクト、失敗時はNone
        """
        if not name or not name.strip():
            return None
        
        name = name.strip()
        
        # 既存ユーザーを検索
        user = self.get_user_by_name(name)
        
        if user:
            # 既存ユーザーの最終ログイン更新
            self.update_last_login(user.id)
            return user
        else:
            # 新規ユーザー作成
            return self.create_user(name)
    
    def get_user_stats(self, user_id: int) -> dict:
        """
        ユーザーの統計情報を取得
        
        Args:
            user_id: ユーザーID
            
        Returns:
            統計情報の辞書
        """
        try:
            with self.db.get_connection() as conn:
                # 完了したチャレンジ数
                completed_count = conn.execute("""
                    SELECT COUNT(*) as count 
                    FROM user_progress 
                    WHERE user_id = ? AND completed = 1
                """, (user_id,)).fetchone()['count']
                
                # 総スコア
                total_score = conn.execute("""
                    SELECT COALESCE(SUM(score), 0) as total 
                    FROM user_progress 
                    WHERE user_id = ?
                """, (user_id,)).fetchone()['total']
                
                # 総チャレンジ数
                total_challenges = conn.execute("""
                    SELECT COUNT(*) as count 
                    FROM challenges
                """).fetchone()['count']
                
                return {
                    'completed_challenges': completed_count,
                    'total_score': total_score,
                    'total_challenges': total_challenges,
                    'completion_rate': (completed_count / total_challenges * 100) if total_challenges > 0 else 0
                }
                
        except Exception as e:
            st.error(f"統計情報取得エラー: {e}")
            return {
                'completed_challenges': 0,
                'total_score': 0,
                'total_challenges': 0,
                'completion_rate': 0
            }