"""
タスク進捗ユースケース
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from typing import List, Optional, Dict, Any
from datetime import datetime
import json

from domain.entities.task_progress import TaskProgress
from domain.entities.task import Task
from infrastructure.repositories.task_progress_repository_impl import TaskProgressRepositoryImpl
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from infrastructure.repositories.progress_repository_impl import ProgressRepositoryImpl
from infrastructure.services.task_loader_service import get_tasks_by_mission_id


class TaskProgressUseCase:
    """タスク進捗ユースケース"""
    
    def __init__(
        self,
        task_progress_repo: TaskProgressRepositoryImpl,
        user_repo: UserRepositoryImpl,
        progress_repo: ProgressRepositoryImpl
    ):
        self.task_progress_repo = task_progress_repo
        self.user_repo = user_repo
        self.progress_repo = progress_repo
    
    async def complete_task(
        self, 
        user_id: int, 
        task_id: int, 
        mission_id: int,
        answer_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        タスクを完了する
        
        Returns:
            Dict containing completion result and rewards
        """
        # 既存の進捗を確認
        existing_progress = await self.task_progress_repo.find_by_user_and_task(user_id, task_id)
        
        if existing_progress and existing_progress.is_completed:
            return {
                'success': False,
                'message': 'このタスクは既に完了済みです',
                'task_completed': False
            }
        
        # タスク進捗を作成または更新
        if existing_progress:
            existing_progress.is_completed = True
            existing_progress.completed_at = datetime.now()
            if answer_data:
                existing_progress.answer_data = json.dumps(answer_data)
            task_progress = await self.task_progress_repo.update(existing_progress)
        else:
            task_progress = TaskProgress(
                id=None,
                user_id=user_id,
                task_id=task_id,
                mission_id=mission_id,
                is_completed=True,
                completed_at=datetime.now(),
                answer_data=json.dumps(answer_data) if answer_data else None
            )
            task_progress = await self.task_progress_repo.create(task_progress)
        
        # ミッション内の完了済みタスク数を取得
        completed_tasks_count = await self.task_progress_repo.count_completed_by_user_and_mission(
            user_id, mission_id
        )
        
        # ミッション内の全タスク数を取得
        mission_tasks = get_tasks_by_mission_id(mission_id)
        total_tasks_count = len(mission_tasks)
        
        # ミッション進捗を更新
        mission_progress = await self.progress_repo.find_by_user_and_mission(user_id, mission_id)
        if mission_progress:
            mission_progress.completed_lessons = completed_tasks_count
            mission_progress.is_completed = (completed_tasks_count >= total_tasks_count)
            if mission_progress.is_completed and not mission_progress.completed_at:
                mission_progress.completed_at = datetime.now()
            await self.progress_repo.update(mission_progress)
        else:
            # 新しいミッション進捗を作成
            from domain.entities.progress import Progress
            mission_progress = Progress(
                id=None,
                user_id=user_id,
                mission_id=mission_id,
                completed_lessons=completed_tasks_count,
                is_completed=(completed_tasks_count >= total_tasks_count),
                completed_at=datetime.now() if completed_tasks_count >= total_tasks_count else None,
                created_at=None,
                updated_at=None
            )
            await self.progress_repo.create(mission_progress)
        
        # 報酬計算（タスクから取得）
        task = next((t for t in mission_tasks if t.id == task_id), None)
        task_xp = task.xp_reward if task else 10
        task_gems = task.gem_reward if task else 0
        
        # ユーザーのXPとジェムを更新
        user = await self.user_repo.find_by_id(user_id)
        if user:
            user.total_xp += task_xp
            user.daily_xp += task_xp
            user.gems += task_gems
            await self.user_repo.update(user)
        
        return {
            'success': True,
            'message': 'タスクが完了しました！',
            'task_completed': True,
            'task_xp': task_xp,
            'gems': task_gems,
            'mission_completed': mission_progress.is_completed if mission_progress else False,
            'completed_tasks': completed_tasks_count,
            'total_tasks': total_tasks_count
        }
    
    async def get_task_progress(self, user_id: int, task_id: int) -> Optional[TaskProgress]:
        """ユーザーIDとタスクIDでタスク進捗を取得"""
        return await self.task_progress_repo.find_by_user_and_task(user_id, task_id)
    
    async def get_mission_task_progress(self, user_id: int, mission_id: int) -> List[TaskProgress]:
        """ユーザーIDとミッションIDでタスク進捗一覧を取得"""
        return await self.task_progress_repo.find_by_user_and_mission(user_id, mission_id)
    
    async def get_completed_tasks_count(self, user_id: int, mission_id: int) -> int:
        """ユーザーIDとミッションIDで完了済みタスク数を取得"""
        return await self.task_progress_repo.count_completed_by_user_and_mission(user_id, mission_id)
    
    async def is_task_completed(self, user_id: int, task_id: int) -> bool:
        """タスクが完了済みかチェック"""
        progress = await self.task_progress_repo.find_by_user_and_task(user_id, task_id)
        return progress is not None and progress.is_completed