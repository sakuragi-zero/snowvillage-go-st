from typing import List, Optional, Dict, Any
from datetime import datetime, date

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from domain.entities.user import User
from domain.entities.progress import Progress
from domain.entities.mission import Mission
from domain.repositories.user_repository import UserRepository
from domain.repositories.progress_repository import ProgressRepository


class ProgressUseCase:
    """進捗管理ユースケース"""
    
    def __init__(self, user_repo: UserRepository, progress_repo: ProgressRepository):
        self.user_repo = user_repo
        self.progress_repo = progress_repo
    
    async def complete_lesson(self, user_id: int, mission: Mission) -> Dict[str, Any]:
        """レッスンを完了し、進捗を更新"""
        # 既存の進捗を取得または新規作成
        progress = await self.progress_repo.get_by_user_and_mission(user_id, mission.id)
        
        if progress is None:
            progress = Progress(
                id=None,
                user_id=user_id,
                mission_id=mission.id,
                completed_lessons=0,
                is_completed=False,
                completed_at=None,
                created_at=None,
                updated_at=None
            )
        
        # レッスンを完了
        mission_completed = progress.complete_lesson(mission.lessons)
        
        # 進捗を保存
        await self.progress_repo.create(progress)
        
        # ユーザーのXPとジェムを更新
        user = await self.user_repo.get_by_id(user_id)
        if user:
            user.add_xp(10)  # レッスンあたり10XP
            
            if mission_completed:
                user.add_xp(mission.xp_reward)
                user.add_gems(mission.gem_reward)
            
            await self.user_repo.update(user)
        
        return {
            'mission_completed': mission_completed,
            'lesson_xp': 10,
            'mission_xp': mission.xp_reward if mission_completed else 0,
            'gems': mission.gem_reward if mission_completed else 0,
            'progress': progress
        }
    
    async def get_user_progress(self, user_id: int) -> List[Progress]:
        """ユーザーの全進捗を取得"""
        return await self.progress_repo.get_by_user_id(user_id)
    
    async def get_mission_progress(self, user_id: int, mission_id: int) -> Optional[Progress]:
        """特定ミッションの進捗を取得"""
        return await self.progress_repo.get_by_user_and_mission(user_id, mission_id)
    
    async def get_completed_missions(self, user_id: int) -> List[int]:
        """完了済みミッション一覧を取得"""
        return await self.progress_repo.get_completed_missions(user_id)
    
    async def update_user_login(self, user_id: int, login_date: date = None) -> User:
        """ユーザーのログイン情報を更新（ストリーク管理）"""
        if login_date is None:
            login_date = datetime.now().date()
        
        user = await self.user_repo.get_by_id(user_id)
        if user:
            # 日が変わった場合は日次XPをリセット
            if user.last_login != login_date:
                user.reset_daily_xp()
            
            user.update_streak(login_date)
            await self.user_repo.update(user)
        
        return user