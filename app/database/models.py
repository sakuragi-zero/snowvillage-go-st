"""データベースモデル定義"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
import json


@dataclass
class User:
    """ユーザーモデル"""
    id: Optional[int] = None
    name: str = ""
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    total_score: int = 0
    completed_challenges: int = 0
    
    @classmethod
    def from_db_row(cls, row) -> 'User':
        """データベース行からUserオブジェクトを作成"""
        return cls(
            id=row['id'],
            name=row['name'],
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
            last_login=datetime.fromisoformat(row['last_login']) if row['last_login'] else None,
            total_score=row['total_score'],
            completed_challenges=row['completed_challenges']
        )


@dataclass
class Challenge:
    """チャレンジモデル"""
    id: Optional[int] = None
    title: str = ""
    description: str = ""
    category: str = ""
    difficulty: int = 1
    question: str = ""
    correct_answer: str = ""
    options: List[str] = None
    points: int = 10
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.options is None:
            self.options = []
    
    @classmethod
    def from_db_row(cls, row) -> 'Challenge':
        """データベース行からChallengeオブジェクトを作成"""
        options = []
        if row['options']:
            try:
                options = json.loads(row['options'])
            except json.JSONDecodeError:
                options = []
        
        return cls(
            id=row['id'],
            title=row['title'],
            description=row['description'],
            category=row['category'],
            difficulty=row['difficulty'],
            question=row['question'],
            correct_answer=row['correct_answer'],
            options=options,
            points=row['points'],
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None
        )
    
    def get_options_json(self) -> str:
        """選択肢をJSON文字列として取得"""
        return json.dumps(self.options, ensure_ascii=False)


@dataclass
class UserProgress:
    """ユーザー進捗モデル"""
    id: Optional[int] = None
    user_id: int = 0
    challenge_id: int = 0
    completed: bool = False
    score: int = 0
    attempts: int = 0
    completed_at: Optional[datetime] = None
    
    @classmethod
    def from_db_row(cls, row) -> 'UserProgress':
        """データベース行からUserProgressオブジェクトを作成"""
        return cls(
            id=row['id'],
            user_id=row['user_id'],
            challenge_id=row['challenge_id'],
            completed=bool(row['completed']),
            score=row['score'],
            attempts=row['attempts'],
            completed_at=datetime.fromisoformat(row['completed_at']) if row['completed_at'] else None
        )