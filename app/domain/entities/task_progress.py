from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class TaskProgress:
    """タスク進捗エンティティ"""
    id: Optional[int]
    user_id: int
    task_id: int
    mission_id: int
    is_completed: bool = False
    completed_at: Optional[datetime] = None
    answer_data: Optional[str] = None  # JSON形式で回答データを保存
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def is_valid(self) -> bool:
        """タスク進捗データの妥当性を検証"""
        return (
            self.user_id > 0 and
            self.task_id > 0 and
            self.mission_id > 0
        )