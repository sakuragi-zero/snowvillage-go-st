"""
タスク読み込みサービス
YMLファイルからタスクデータを動的に読み込む
"""

import os
import yaml
from typing import List, Dict, Any
from pathlib import Path

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from domain.entities.task import Task, TaskType, Choice


class TaskLoaderService:
    """YMLファイルからタスクを読み込むサービス"""
    
    def __init__(self, yml_path: str = None):
        """
        初期化
        
        Args:
            yml_path: タスクYMLファイルのパス（デフォルトは data/tasks.yml）
        """
        if yml_path is None:
            # デフォルトパスを設定
            base_dir = Path(__file__).parent.parent.parent
            yml_path = base_dir / "data" / "tasks.yml"
        
        self.yml_path = Path(yml_path)
        self._validate_yml_file()
    
    def _validate_yml_file(self):
        """YMLファイルの存在確認"""
        if not self.yml_path.exists():
            raise FileNotFoundError(f"タスクYMLファイルが見つかりません: {self.yml_path}")
    
    def load_tasks(self) -> List[Task]:
        """
        YMLファイルからタスクを読み込む
        
        Returns:
            List[Task]: タスクリスト（order_indexでソート済み）
        
        Raises:
            FileNotFoundError: YMLファイルが見つからない場合
            yaml.YAMLError: YAML解析エラーの場合
            ValueError: タスクデータが不正な場合
        """
        try:
            with open(self.yml_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
            
            if 'tasks' not in data:
                raise ValueError("YMLファイルに'tasks'キーが見つかりません")
            
            tasks = []
            for task_data in data['tasks']:
                task = self._create_task_from_dict(task_data)
                if task.is_valid():
                    tasks.append(task)
                else:
                    print(f"警告: 無効なタスクデータをスキップしました - ID: {task_data.get('id', 'Unknown')}")
            
            # mission_id、order_indexでソート
            tasks.sort(key=lambda t: (t.mission_id, t.order_index))
            
            return tasks
            
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"YAML解析エラー: {e}")
        except Exception as e:
            raise Exception(f"タスク読み込みエラー: {e}")
    
    def _create_task_from_dict(self, task_data: Dict[str, Any]) -> Task:
        """
        辞書データからTaskオブジェクトを作成
        
        Args:
            task_data: タスクの辞書データ
        
        Returns:
            Task: Taskオブジェクト
        
        Raises:
            KeyError: 必須フィールドが不足している場合
            TypeError: データ型が不正な場合
        """
        required_fields = ['id', 'mission_id', 'title', 'description', 'task_type']
        
        # 必須フィールドの確認
        for field in required_fields:
            if field not in task_data:
                raise KeyError(f"必須フィールド '{field}' が見つかりません")
        
        try:
            # 基本フィールド
            task = Task(
                id=int(task_data['id']),
                mission_id=int(task_data['mission_id']),
                title=str(task_data['title']),
                description=str(task_data['description']),
                task_type=TaskType(task_data['task_type']),
                order_index=int(task_data.get('order_index', 0)),
                xp_reward=int(task_data.get('xp_reward', 10)),
                gem_reward=int(task_data.get('gem_reward', 0))
            )
            
            # タスクタイプ別の追加フィールド
            if task.task_type == TaskType.QUIZ:
                task.question = task_data.get('question')
                task.explanation = task_data.get('explanation')
                
                # 選択肢の処理
                if 'choices' in task_data:
                    choices = []
                    for choice_data in task_data['choices']:
                        choice = Choice(
                            id=str(choice_data['id']),
                            text=str(choice_data['text']),
                            is_correct=bool(choice_data.get('is_correct', False))
                        )
                        choices.append(choice)
                    task.choices = choices
                    
            elif task.task_type == TaskType.BOOTH_VISIT:
                task.booth_name = task_data.get('booth_name')
                task.twitter_text = task_data.get('twitter_text')
                task.twitter_url = task_data.get('twitter_url')
            
            return task
            
        except (ValueError, TypeError) as e:
            raise TypeError(f"データ型エラー: {e}")
    
    def get_tasks_by_mission_id(self, mission_id: int) -> List[Task]:
        """
        ミッションIDでタスクを取得
        
        Args:
            mission_id: ミッションID
        
        Returns:
            List[Task]: 指定されたミッションのタスクリスト
        """
        tasks = self.load_tasks()
        return [task for task in tasks if task.mission_id == mission_id]
    
    def get_task_by_id(self, task_id: int) -> Task:
        """
        IDでタスクを取得
        
        Args:
            task_id: タスクID
        
        Returns:
            Task: 指定されたIDのタスク
        
        Raises:
            ValueError: 指定されたIDのタスクが見つからない場合
        """
        tasks = self.load_tasks()
        for task in tasks:
            if task.id == task_id:
                return task
        
        raise ValueError(f"ID {task_id} のタスクが見つかりません")
    
    def reload_tasks(self) -> List[Task]:
        """
        タスクを再読み込み（開発時やタスク追加時に使用）
        
        Returns:
            List[Task]: 更新されたタスクリスト
        """
        self._validate_yml_file()
        return self.load_tasks()


# シングルトンインスタンス（グローバルに使用可能）
task_loader = TaskLoaderService()


def get_tasks() -> List[Task]:
    """
    タスク一覧を取得（便利関数）
    
    Returns:
        List[Task]: タスクリスト
    """
    return task_loader.load_tasks()


def get_tasks_by_mission_id(mission_id: int) -> List[Task]:
    """
    ミッションIDでタスクを取得（便利関数）
    
    Args:
        mission_id: ミッションID
    
    Returns:
        List[Task]: 指定されたミッションのタスクリスト
    """
    return task_loader.get_tasks_by_mission_id(mission_id)


def get_task_by_id(task_id: int) -> Task:
    """
    IDでタスクを取得（便利関数）
    
    Args:
        task_id: タスクID
    
    Returns:
        Task: 指定されたIDのタスク
    """
    return task_loader.get_task_by_id(task_id)