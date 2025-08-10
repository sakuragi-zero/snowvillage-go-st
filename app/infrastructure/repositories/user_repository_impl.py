from typing import Optional, List
from datetime import datetime
import psycopg2.extras

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from domain.entities.user import User
from domain.repositories.user_repository import UserRepository
from ..database.connection import db


class UserRepositoryImpl(UserRepository):
    """ユーザーリポジトリ実装"""
    
    async def create(self, user: User) -> User:
        """ユーザーを作成"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO users (username, email, last_login, streak, total_xp, daily_xp, gems)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id, created_at
            """, (user.username, user.email, user.last_login, user.streak, 
                  user.total_xp, user.daily_xp, user.gems))
            
            result = cursor.fetchone()
            user.id = result['id']
            user.created_at = result['created_at']
            return user
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """IDでユーザーを取得"""
        with db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            row = cursor.fetchone()
            
            if row:
                return User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    created_at=row['created_at'],
                    last_login=row['last_login'],
                    streak=row['streak'],
                    total_xp=row['total_xp'],
                    daily_xp=row['daily_xp'],
                    gems=row['gems']
                )
            return None
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """ユーザー名でユーザーを取得"""
        with db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            row = cursor.fetchone()
            
            if row:
                return User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    created_at=row['created_at'],
                    last_login=row['last_login'],
                    streak=row['streak'],
                    total_xp=row['total_xp'],
                    daily_xp=row['daily_xp'],
                    gems=row['gems']
                )
            return None
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """メールアドレスでユーザーを取得"""
        with db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            row = cursor.fetchone()
            
            if row:
                return User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    created_at=row['created_at'],
                    last_login=row['last_login'],
                    streak=row['streak'],
                    total_xp=row['total_xp'],
                    daily_xp=row['daily_xp'],
                    gems=row['gems']
                )
            return None
    
    async def update(self, user: User) -> User:
        """ユーザーを更新"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE users 
                SET username = %s, email = %s, last_login = %s, streak = %s,
                    total_xp = %s, daily_xp = %s, gems = %s
                WHERE id = %s
            """, (user.username, user.email, user.last_login, user.streak,
                  user.total_xp, user.daily_xp, user.gems, user.id))
            
            return user
    
    async def delete(self, user_id: int) -> bool:
        """ユーザーを削除"""
        with db.get_cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            return cursor.rowcount > 0
    
    async def list_all(self) -> List[User]:
        """全ユーザーを取得"""
        with db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM users ORDER BY created_at")
            rows = cursor.fetchall()
            
            return [
                User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    created_at=row['created_at'],
                    last_login=row['last_login'],
                    streak=row['streak'],
                    total_xp=row['total_xp'],
                    daily_xp=row['daily_xp'],
                    gems=row['gems']
                ) for row in rows
            ]