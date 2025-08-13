"""
タスク進捗リポジトリ実装
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from typing import List, Optional
from datetime import datetime
import json

from domain.entities.task_progress import TaskProgress
from infrastructure.database.connection import db


class TaskProgressRepositoryImpl:
    """タスク進捗リポジトリ実装"""
    
    async def create(self, task_progress: TaskProgress) -> TaskProgress:
        """タスク進捗を作成"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO task_progress (user_id, task_id, mission_id, is_completed, completed_at, answer_data)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id, created_at, updated_at
            """, [
                task_progress.user_id,
                task_progress.task_id, 
                task_progress.mission_id,
                task_progress.is_completed,
                task_progress.completed_at,
                task_progress.answer_data
            ])
            
            result = cursor.fetchone()
            task_progress.id = result['id']
            task_progress.created_at = result['created_at']
            task_progress.updated_at = result['updated_at']
            
            return task_progress
    
    async def update(self, task_progress: TaskProgress) -> TaskProgress:
        """タスク進捗を更新"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE task_progress 
                SET is_completed = %s, completed_at = %s, answer_data = %s
                WHERE id = %s
                RETURNING updated_at
            """, [
                task_progress.is_completed,
                task_progress.completed_at,
                task_progress.answer_data,
                task_progress.id
            ])
            
            result = cursor.fetchone()
            task_progress.updated_at = result['updated_at']
            
            return task_progress
    
    async def find_by_user_and_task(self, user_id: int, task_id: int) -> Optional[TaskProgress]:
        """ユーザーIDとタスクIDでタスク進捗を取得"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT * FROM task_progress 
                WHERE user_id = %s AND task_id = %s
            """, [user_id, task_id])
            
            row = cursor.fetchone()
            if row:
                return TaskProgress(
                    id=row['id'],
                    user_id=row['user_id'],
                    task_id=row['task_id'],
                    mission_id=row['mission_id'],
                    is_completed=row['is_completed'],
                    completed_at=row['completed_at'],
                    answer_data=row['answer_data'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
            return None
    
    async def find_by_user_and_mission(self, user_id: int, mission_id: int) -> List[TaskProgress]:
        """ユーザーIDとミッションIDでタスク進捗一覧を取得"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT * FROM task_progress 
                WHERE user_id = %s AND mission_id = %s
                ORDER BY task_id
            """, [user_id, mission_id])
            
            rows = cursor.fetchall()
            return [TaskProgress(
                id=row['id'],
                user_id=row['user_id'],
                task_id=row['task_id'],
                mission_id=row['mission_id'],
                is_completed=row['is_completed'],
                completed_at=row['completed_at'],
                answer_data=row['answer_data'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            ) for row in rows]
    
    async def count_completed_by_user_and_mission(self, user_id: int, mission_id: int) -> int:
        """ユーザーIDとミッションIDで完了済みタスク数を取得"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) as count FROM task_progress 
                WHERE user_id = %s AND mission_id = %s AND is_completed = TRUE
            """, [user_id, mission_id])
            
            result = cursor.fetchone()
            return result['count']
    
    async def find_by_user(self, user_id: int) -> List[TaskProgress]:
        """ユーザーIDでタスク進捗一覧を取得"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT * FROM task_progress 
                WHERE user_id = %s
                ORDER BY mission_id, task_id
            """, [user_id])
            
            rows = cursor.fetchall()
            return [TaskProgress(
                id=row['id'],
                user_id=row['user_id'],
                task_id=row['task_id'],
                mission_id=row['mission_id'],
                is_completed=row['is_completed'],
                completed_at=row['completed_at'],
                answer_data=row['answer_data'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            ) for row in rows]
    
    async def delete_by_user_and_task(self, user_id: int, task_id: int) -> bool:
        """ユーザーIDとタスクIDでタスク進捗を削除"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                DELETE FROM task_progress 
                WHERE user_id = %s AND task_id = %s
            """, [user_id, task_id])
            
            return cursor.rowcount > 0