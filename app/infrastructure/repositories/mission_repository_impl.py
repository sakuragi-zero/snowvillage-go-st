from typing import Optional, List

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from domain.entities.mission import Mission
from domain.repositories.mission_repository import MissionRepository
from ..database.connection import db


class MissionRepositoryImpl(MissionRepository):
    """ミッションリポジトリ実装"""
    
    async def create(self, mission: Mission) -> Mission:
        """ミッションを作成"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO missions (title, icon, description, lessons, xp_reward, gem_reward, order_index)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (mission.title, mission.icon, mission.description, mission.lessons,
                  mission.xp_reward, mission.gem_reward, mission.order_index))
            
            result = cursor.fetchone()
            mission.id = result['id']
            return mission
    
    async def get_by_id(self, mission_id: int) -> Optional[Mission]:
        """IDでミッションを取得"""
        with db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM missions WHERE id = %s", (mission_id,))
            row = cursor.fetchone()
            
            if row:
                return Mission(
                    id=row['id'],
                    title=row['title'],
                    icon=row['icon'],
                    description=row['description'],
                    lessons=row['lessons'],
                    xp_reward=row['xp_reward'],
                    gem_reward=row['gem_reward'],
                    order_index=row['order_index']
                )
            return None
    
    async def list_all(self) -> List[Mission]:
        """全ミッションを順序付きで取得"""
        with db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM missions ORDER BY order_index, id")
            rows = cursor.fetchall()
            
            return [
                Mission(
                    id=row['id'],
                    title=row['title'],
                    icon=row['icon'],
                    description=row['description'],
                    lessons=row['lessons'],
                    xp_reward=row['xp_reward'],
                    gem_reward=row['gem_reward'],
                    order_index=row['order_index']
                ) for row in rows
            ]
    
    async def update(self, mission: Mission) -> Mission:
        """ミッションを更新"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE missions 
                SET title = %s, icon = %s, description = %s, lessons = %s,
                    xp_reward = %s, gem_reward = %s, order_index = %s
                WHERE id = %s
            """, (mission.title, mission.icon, mission.description, mission.lessons,
                  mission.xp_reward, mission.gem_reward, mission.order_index, mission.id))
            
            return mission
    
    async def delete(self, mission_id: int) -> bool:
        """ミッションを削除"""
        with db.get_cursor() as cursor:
            cursor.execute("DELETE FROM missions WHERE id = %s", (mission_id,))
            return cursor.rowcount > 0