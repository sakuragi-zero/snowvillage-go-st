from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum


class TaskType(Enum):
    """タスクタイプ列挙"""
    QUIZ = "quiz"  # 技術系クイズ
    BOOTH_VISIT = "booth_visit"  # ブース訪問系


@dataclass
class Choice:
    """選択肢エンティティ"""
    id: str
    text: str
    is_correct: bool = False


@dataclass
class Task:
    """タスクエンティティ"""
    id: int
    mission_id: int
    title: str
    description: str
    task_type: TaskType
    order_index: int = 0
    
    # クイズ系タスク用
    question: Optional[str] = None
    choices: Optional[List[Choice]] = None
    explanation: Optional[str] = None
    
    # ブース訪問系タスク用
    booth_name: Optional[str] = None
    twitter_text: Optional[str] = None
    twitter_url: Optional[str] = None
    
    # 報酬
    xp_reward: int = 10
    gem_reward: int = 0
    
    def is_valid(self) -> bool:
        """タスクデータの妥当性を検証"""
        basic_valid = (
            self.mission_id > 0 and
            len(self.title.strip()) > 0 and
            len(self.description.strip()) > 0 and
            self.xp_reward > 0
        )
        
        if self.task_type == TaskType.QUIZ:
            return (
                basic_valid and
                self.question is not None and
                self.choices is not None and
                len(self.choices) >= 2 and
                any(choice.is_correct for choice in self.choices)
            )
        elif self.task_type == TaskType.BOOTH_VISIT:
            return (
                basic_valid and
                self.booth_name is not None and
                len(self.booth_name.strip()) > 0 and
                self.twitter_text is not None and
                len(self.twitter_text.strip()) > 0
            )
        
        return basic_valid