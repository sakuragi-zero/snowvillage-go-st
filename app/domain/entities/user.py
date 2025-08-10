from dataclasses import dataclass
from datetime import datetime, date, timedelta
from typing import List, Optional


@dataclass
class User:
    """ユーザーエンティティ"""
    id: Optional[int]
    username: str
    email: str
    created_at: Optional[datetime]
    last_login: Optional[date]
    streak: int = 0
    total_xp: int = 0
    daily_xp: int = 0
    gems: int = 50
    
    def reset_daily_xp(self) -> None:
        """日次XPをリセット"""
        self.daily_xp = 0
    
    def add_xp(self, amount: int) -> None:
        """XPを追加"""
        self.total_xp += amount
        self.daily_xp += amount
    
    def add_gems(self, amount: int) -> None:
        """ジェムを追加"""
        self.gems += amount
    
    def update_streak(self, login_date: date) -> None:
        """ストリークを更新"""
        if self.last_login is None:
            self.streak = 1
        elif login_date == self.last_login:
            return  # 同日ログインは何もしない
        elif login_date == self.last_login + timedelta(days=1):
            self.streak += 1
        else:
            self.streak = 1
        
        self.last_login = login_date