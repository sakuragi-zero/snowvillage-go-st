"""
Slack Bot クライアント
匿名投稿機能を提供
"""
import streamlit as st
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime
import logging

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SlackClient:
    """Slack API クライアント"""
    
    def __init__(self):
        """初期化"""
        self.client = None
        self.channel_id = None
        self.bot_name = None
        self._init_client()
    
    def _init_client(self):
        """Slackクライアントを初期化"""
        try:
            # Streamlit secrets から設定を取得
            slack_config = st.secrets.get("slack", {})
            bot_token = slack_config.get("bot_token")
            self.channel_id = slack_config.get("channel_id")
            self.bot_name = slack_config.get("bot_name", "Snow Village Bot")
            
            if not bot_token:
                logger.warning("Slack bot token not found in secrets")
                return
            
            if not self.channel_id:
                logger.warning("Slack channel ID not found in secrets")
                return
            
            # WebClientを初期化
            self.client = WebClient(token=bot_token)
            
            # 接続テスト
            try:
                response = self.client.auth_test()
                logger.info(f"Slack client initialized successfully. Bot user: {response['user']}")
            except SlackApiError as e:
                logger.error(f"Slack auth test failed: {e.response['error']}")
                self.client = None
                
        except Exception as e:
            logger.error(f"Failed to initialize Slack client: {e}")
            self.client = None
    
    def is_configured(self) -> bool:
        """Slack設定が正しく行われているかチェック"""
        return self.client is not None and self.channel_id is not None
    
    def send_anonymous_message(self, message: str, username: str = None) -> tuple[bool, str]:
        """
        匿名メッセージをSlackに送信
        
        Args:
            message: 送信するメッセージ
            username: 投稿者のユーザー名（Slackには表示されない）
        
        Returns:
            tuple[bool, str]: (成功フラグ, メッセージ)
        """
        if not self.is_configured():
            return False, "Slack設定が正しく行われていません"
        
        if not message or not message.strip():
            return False, "メッセージが空です"
        
        try:
            # 送信時刻を取得
            timestamp = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
            
            # 匿名投稿フォーマット
            formatted_message = f"""🏔️ **Snow Village 匿名投稿**

📝 **メッセージ:**
{message.strip()}

🕐 **投稿時刻:** {timestamp}
👤 **投稿者:** 匿名ユーザー"""
            
            # Slackに送信
            response = self.client.chat_postMessage(
                channel=self.channel_id,
                text=formatted_message,
                username=self.bot_name,
                icon_emoji=":snowflake:"
            )
            
            if response["ok"]:
                logger.info(f"Message sent successfully. Timestamp: {response['ts']}")
                return True, "メッセージが正常に送信されました"
            else:
                logger.error(f"Failed to send message: {response}")
                return False, "メッセージの送信に失敗しました"
                
        except SlackApiError as e:
            error_code = e.response["error"]
            logger.error(f"Slack API error: {error_code}")
            
            # エラーメッセージをユーザーフレンドリーに変換
            if error_code == "channel_not_found":
                return False, "指定されたチャンネルが見つかりません"
            elif error_code == "not_in_channel":
                return False, "ボットがチャンネルに参加していません"
            elif error_code == "invalid_auth":
                return False, "認証情報が無効です"
            else:
                return False, f"Slack API エラー: {error_code}"
                
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return False, f"予期しないエラーが発生しました: {str(e)}"
    
    def test_connection(self) -> tuple[bool, str]:
        """
        Slack接続をテスト
        
        Returns:
            tuple[bool, str]: (成功フラグ, メッセージ)
        """
        if not self.client:
            return False, "Slackクライアントが初期化されていません"
        
        try:
            # 認証テスト
            auth_response = self.client.auth_test()
            bot_user = auth_response["user"]
            
            # チャンネル情報取得テスト
            channel_response = self.client.conversations_info(channel=self.channel_id)
            channel_name = channel_response["channel"]["name"]
            
            return True, f"接続成功 - Bot: @{bot_user}, Channel: #{channel_name}"
            
        except SlackApiError as e:
            error_code = e.response["error"]
            if error_code == "channel_not_found":
                return False, "チャンネルが見つかりません"
            elif error_code == "invalid_auth":
                return False, "認証情報が無効です"
            else:
                return False, f"Slack API エラー: {error_code}"
                
        except Exception as e:
            return False, f"接続テストに失敗しました: {str(e)}"