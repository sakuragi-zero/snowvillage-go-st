from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.user import User


class UserRepository(ABC):
    """ユーザーリポジトリインターフェース"""
    
    @abstractmethod
    async def create(self, user: User) -> User:
        """ユーザーを作成"""
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """IDでユーザーを取得"""
        pass
    
    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        """ユーザー名でユーザーを取得"""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """メールアドレスでユーザーを取得"""
        pass
    
    @abstractmethod
    async def update(self, user: User) -> User:
        """ユーザーを更新"""
        pass
    
    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        """ユーザーを削除"""
        pass
    
    @abstractmethod
    async def list_all(self) -> List[User]:
        """全ユーザーを取得"""
        pass