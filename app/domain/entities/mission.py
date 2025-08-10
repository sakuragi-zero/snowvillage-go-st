from dataclasses import dataclass
from typing import Optional


@dataclass
class Mission:
    """ミッションエンティティ"""
    id: int
    title: str
    icon: str
    description: str
    lessons: int
    xp_reward: int
    gem_reward: int
    order_index: int = 0
    
    def is_valid(self) -> bool:
        """ミッションデータの妥当性を検証"""
        return (
            self.lessons > 0 and
            self.xp_reward > 0 and
            self.gem_reward >= 0 and
            len(self.title.strip()) > 0 and
            len(self.description.strip()) > 0
        )