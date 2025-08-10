from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.progress import Progress


class ProgressRepository(ABC):
    """進捗リポジトリインターフェース"""
    
    @abstractmethod
    async def create(self, progress: Progress) -> Progress:
        """進捗を作成"""
        pass
    
    @abstractmethod
    async def get_by_user_and_mission(self, user_id: int, mission_id: int) -> Optional[Progress]:
        """ユーザーとミッションで進捗を取得"""
        pass
    
    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> List[Progress]:
        """ユーザーの全進捗を取得"""
        pass
    
    @abstractmethod
    async def update(self, progress: Progress) -> Progress:
        """進捗を更新"""
        pass
    
    @abstractmethod
    async def delete(self, progress_id: int) -> bool:
        """進捗を削除"""
        pass
    
    @abstractmethod
    async def get_completed_missions(self, user_id: int) -> List[int]:
        """ユーザーの完了済みミッションIDリストを取得"""
        pass