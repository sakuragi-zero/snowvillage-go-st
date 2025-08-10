from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.mission import Mission


class MissionRepository(ABC):
    """ミッションリポジトリインターフェース"""
    
    @abstractmethod
    async def create(self, mission: Mission) -> Mission:
        """ミッションを作成"""
        pass
    
    @abstractmethod
    async def get_by_id(self, mission_id: int) -> Optional[Mission]:
        """IDでミッションを取得"""
        pass
    
    @abstractmethod
    async def list_all(self) -> List[Mission]:
        """全ミッションを順序付きで取得"""
        pass
    
    @abstractmethod
    async def update(self, mission: Mission) -> Mission:
        """ミッションを更新"""
        pass
    
    @abstractmethod
    async def delete(self, mission_id: int) -> bool:
        """ミッションを削除"""
        pass