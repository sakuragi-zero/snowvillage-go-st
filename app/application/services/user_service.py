"""
ユーザー管理サービス
既存のデータベースマネージャーと新しいユーザーエンティティを統合
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from typing import Optional, Tuple
from datetime import datetime, date
import asyncio

from domain.entities.user import User
from domain.repositories.user_repository import UserRepository
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from database_manager import DatabaseManager


class UserService:
    """ユーザー統合管理サービス"""
    
    def __init__(self):
        self.user_repo = UserRepositoryImpl()
        self.legacy_db = DatabaseManager()
    
    def run_async(self, coro):
        """非同期関数を実行するヘルパー"""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)
    
    def migrate_legacy_user(self, username: str) -> Optional[User]:
        """レガシーユーザーを新システムに移行"""
        # 新システムでユーザー確認
        existing_user = self.run_async(self.user_repo.get_by_username(username))
        if existing_user:
            return existing_user
        
        # レガシーシステムでユーザー存在確認
        if self.legacy_db.check_user_exists(username):
            # 新システムにユーザーを作成
            new_user = User(
                id=None,
                username=username,
                email=f"{username}@snowvillage.example",  # デフォルトメール
                created_at=None,
                last_login=date.today(),
                streak=1,
                total_xp=0,
                daily_xp=0,
                gems=50
            )
            
            return self.run_async(self.user_repo.create(new_user))
        
        return None
    
    def register_new_user(self, username: str) -> Tuple[bool, str, Optional[User]]:
        """新規ユーザー登録（両システムに登録）"""
        # レガシーシステムに登録
        legacy_success, legacy_message = self.legacy_db.register_user(username)
        
        if legacy_success:
            # 新システムにも登録
            new_user = User(
                id=None,
                username=username,
                email=f"{username}@snowvillage.example",
                created_at=None,
                last_login=date.today(),
                streak=1,
                total_xp=0,
                daily_xp=0,
                gems=50
            )
            
            try:
                created_user = self.run_async(self.user_repo.create(new_user))
                return True, "登録が完了しました！", created_user
            except Exception as e:
                print(f"新システム登録エラー: {e}")
                return True, "登録が完了しました！", new_user
        
        return False, legacy_message, None
    
    def login_user(self, username: str) -> Tuple[bool, str, Optional[User]]:
        """ユーザーログイン（統合処理）"""
        # レガシーシステムでログイン処理
        legacy_success, legacy_message = self.legacy_db.login_user(username)
        
        if legacy_success:
            # 新システムでユーザー取得または移行
            user = self.migrate_legacy_user(username)
            if user:
                # ログイン日時更新
                user.update_streak(date.today())
                updated_user = self.run_async(self.user_repo.update(user))
                return True, "ログインしました！", updated_user
            else:
                return False, "ユーザー移行に失敗しました", None
        
        return False, legacy_message, None