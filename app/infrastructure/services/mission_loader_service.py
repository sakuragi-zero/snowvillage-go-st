"""
ミッション読み込みサービス
YMLファイルからミッションデータを動的に読み込む
"""

import os
import yaml
from typing import List, Dict, Any
from pathlib import Path

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from domain.entities.mission import Mission


class MissionLoaderService:
    """YMLファイルからミッションを読み込むサービス"""
    
    def __init__(self, yml_path: str = None):
        """
        初期化
        
        Args:
            yml_path: ミッションYMLファイルのパス（デフォルトは data/missions.yml）
        """
        if yml_path is None:
            # デフォルトパスを設定
            base_dir = Path(__file__).parent.parent.parent
            yml_path = base_dir / "data" / "missions.yml"
        
        self.yml_path = Path(yml_path)
        self._validate_yml_file()
    
    def _validate_yml_file(self):
        """YMLファイルの存在確認"""
        if not self.yml_path.exists():
            raise FileNotFoundError(f"ミッションYMLファイルが見つかりません: {self.yml_path}")
    
    def load_missions(self) -> List[Mission]:
        """
        YMLファイルからミッションを読み込む
        
        Returns:
            List[Mission]: ミッションリスト（order_indexでソート済み）
        
        Raises:
            FileNotFoundError: YMLファイルが見つからない場合
            yaml.YAMLError: YAML解析エラーの場合
            ValueError: ミッションデータが不正な場合
        """
        try:
            with open(self.yml_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
            
            if 'missions' not in data:
                raise ValueError("YMLファイルに'missions'キーが見つかりません")
            
            missions = []
            for mission_data in data['missions']:
                mission = self._create_mission_from_dict(mission_data)
                if mission.is_valid():
                    missions.append(mission)
                else:
                    print(f"警告: 無効なミッションデータをスキップしました - ID: {mission_data.get('id', 'Unknown')}")
            
            # order_indexでソート
            missions.sort(key=lambda m: m.order_index)
            
            return missions
            
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"YAML解析エラー: {e}")
        except Exception as e:
            raise Exception(f"ミッション読み込みエラー: {e}")
    
    def _create_mission_from_dict(self, mission_data: Dict[str, Any]) -> Mission:
        """
        辞書データからMissionオブジェクトを作成
        
        Args:
            mission_data: ミッションの辞書データ
        
        Returns:
            Mission: Missionオブジェクト
        
        Raises:
            KeyError: 必須フィールドが不足している場合
            TypeError: データ型が不正な場合
        """
        required_fields = ['id', 'title', 'icon', 'description', 'lessons', 'xp_reward', 'gem_reward']
        
        # 必須フィールドの確認
        for field in required_fields:
            if field not in mission_data:
                raise KeyError(f"必須フィールド '{field}' が見つかりません")
        
        try:
            return Mission(
                id=int(mission_data['id']),
                title=str(mission_data['title']),
                icon=str(mission_data['icon']),
                description=str(mission_data['description']),
                lessons=int(mission_data['lessons']),
                xp_reward=int(mission_data['xp_reward']),
                gem_reward=int(mission_data['gem_reward']),
                order_index=int(mission_data.get('order_index', 0))
            )
        except (ValueError, TypeError) as e:
            raise TypeError(f"データ型エラー: {e}")
    
    def reload_missions(self) -> List[Mission]:
        """
        ミッションを再読み込み（開発時やミッション追加時に使用）
        
        Returns:
            List[Mission]: 更新されたミッションリスト
        """
        self._validate_yml_file()
        return self.load_missions()
    
    def get_mission_by_id(self, mission_id: int) -> Mission:
        """
        IDでミッションを取得
        
        Args:
            mission_id: ミッションID
        
        Returns:
            Mission: 指定されたIDのミッション
        
        Raises:
            ValueError: 指定されたIDのミッションが見つからない場合
        """
        missions = self.load_missions()
        for mission in missions:
            if mission.id == mission_id:
                return mission
        
        raise ValueError(f"ID {mission_id} のミッションが見つかりません")
    
    def get_missions_count(self) -> int:
        """
        ミッション総数を取得
        
        Returns:
            int: ミッション総数
        """
        return len(self.load_missions())


# シングルトンインスタンス（グローバルに使用可能）
mission_loader = MissionLoaderService()


def get_missions() -> List[Mission]:
    """
    ミッション一覧を取得（便利関数）
    
    Returns:
        List[Mission]: ミッションリスト
    """
    return mission_loader.load_missions()


def get_mission_by_id(mission_id: int) -> Mission:
    """
    IDでミッションを取得（便利関数）
    
    Args:
        mission_id: ミッションID
    
    Returns:
        Mission: 指定されたIDのミッション
    """
    return mission_loader.get_mission_by_id(mission_id)