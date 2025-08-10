from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Progress:
    """進捗エンティティ"""
    id: Optional[int]
    user_id: int
    mission_id: int
    completed_lessons: int
    is_completed: bool
    completed_at: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    def complete_lesson(self, total_lessons: int) -> bool:
        """レッスンを完了し、ミッション完了判定を行う"""
        if self.is_completed:
            return False
        
        self.completed_lessons = min(self.completed_lessons + 1, total_lessons)
        
        if self.completed_lessons >= total_lessons and not self.is_completed:
            self.is_completed = True
            self.completed_at = datetime.now()
            return True
        
        return False
    
    def get_progress_percentage(self, total_lessons: int) -> float:
        """進捗パーセンテージを取得"""
        if total_lessons <= 0:
            return 0.0
        return min((self.completed_lessons / total_lessons) * 100, 100.0)
    
    def reset_progress(self) -> None:
        """進捗をリセット"""
        self.completed_lessons = 0
        self.is_completed = False
        self.completed_at = None