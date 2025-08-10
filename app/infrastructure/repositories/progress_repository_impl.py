from typing import Optional, List
from datetime import datetime

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from domain.entities.progress import Progress
from domain.repositories.progress_repository import ProgressRepository
from ..database.connection import db


class ProgressRepositoryImpl(ProgressRepository):
    """進捗リポジトリ実装"""
    
    async def create(self, progress: Progress) -> Progress:
        """進捗を作成"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO progress (user_id, mission_id, completed_lessons, is_completed, completed_at)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (user_id, mission_id) 
                DO UPDATE SET 
                    completed_lessons = EXCLUDED.completed_lessons,
                    is_completed = EXCLUDED.is_completed,
                    completed_at = EXCLUDED.completed_at
                RETURNING id, created_at, updated_at
            """, (progress.user_id, progress.mission_id, progress.completed_lessons,
                  progress.is_completed, progress.completed_at))
            
            result = cursor.fetchone()
            progress.id = result['id']
            progress.created_at = result['created_at']
            progress.updated_at = result['updated_at']
            return progress
    
    async def get_by_user_and_mission(self, user_id: int, mission_id: int) -> Optional[Progress]:
        """ユーザーとミッションで進捗を取得"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT * FROM progress 
                WHERE user_id = %s AND mission_id = %s
            """, (user_id, mission_id))
            
            row = cursor.fetchone()
            if row:
                return Progress(
                    id=row['id'],
                    user_id=row['user_id'],
                    mission_id=row['mission_id'],
                    completed_lessons=row['completed_lessons'],
                    is_completed=row['is_completed'],
                    completed_at=row['completed_at'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
            return None
    
    async def get_by_user_id(self, user_id: int) -> List[Progress]:
        """ユーザーの全進捗を取得"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT * FROM progress 
                WHERE user_id = %s 
                ORDER BY mission_id
            """, (user_id,))
            
            rows = cursor.fetchall()
            return [
                Progress(
                    id=row['id'],
                    user_id=row['user_id'],
                    mission_id=row['mission_id'],
                    completed_lessons=row['completed_lessons'],
                    is_completed=row['is_completed'],
                    completed_at=row['completed_at'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                ) for row in rows
            ]
    
    async def update(self, progress: Progress) -> Progress:
        """進捗を更新"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE progress 
                SET completed_lessons = %s, is_completed = %s, completed_at = %s
                WHERE id = %s
                RETURNING updated_at
            """, (progress.completed_lessons, progress.is_completed, 
                  progress.completed_at, progress.id))
            
            result = cursor.fetchone()
            progress.updated_at = result['updated_at']
            return progress
    
    async def delete(self, progress_id: int) -> bool:
        """進捗を削除"""
        with db.get_cursor() as cursor:
            cursor.execute("DELETE FROM progress WHERE id = %s", (progress_id,))
            return cursor.rowcount > 0
    
    async def get_completed_missions(self, user_id: int) -> List[int]:
        """ユーザーの完了済みミッションIDリストを取得"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT mission_id FROM progress 
                WHERE user_id = %s AND is_completed = true
                ORDER BY mission_id
            """, (user_id,))
            
            rows = cursor.fetchall()
            return [row['mission_id'] for row in rows]