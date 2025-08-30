"""
Slack Webhook クライアント
匿名投稿機能を提供
"""
import streamlit as st
import requests
import json
from datetime import datetime
import logging
import os

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SlackClient:
    """Slack Webhook クライアント"""
    
    def __init__(self):
        """初期化"""
        self.webhook_url = None
        self.bot_name = None
        self._init_client()
    
    def _init_client(self):
        """Slackクライアントを初期化"""
        try:
            # Streamlit secrets または環境変数から設定を取得
            try:
                slack_config = st.secrets.get("slack", {})
                self.webhook_url = slack_config.get("webhook_url")
                self.bot_name = slack_config.get("bot_name", "Snow Village Bot")
            except:
                # secrets が利用できない場合は環境変数から取得
                self.webhook_url = os.getenv("SLACK_WEBHOOK_URL")
                self.bot_name = os.getenv("SLACK_BOT_NAME", "Snow Village Bot")
            
            # デフォルトのWebhook URL（提供されたもの）
            if not self.webhook_url:
                self.webhook_url = "https://hooks.slack.com/services/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"
                logger.info("Using default Slack webhook URL")
            
            if self.webhook_url:
                logger.info("Slack webhook client initialized successfully")
            else:
                logger.warning("Slack webhook URL not configured")
                
        except Exception as e:
            logger.error(f"Failed to initialize Slack client: {e}")
            self.webhook_url = None
    
    def is_configured(self) -> bool:
        """Slack設定が正しく行われているかチェック"""
        return self.webhook_url is not None
    
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
            formatted_message = f"""*Snow Village 匿名投稿* :snowflake:

*メッセージ:*
{message.strip()}

*投稿時刻:* {timestamp}"""
            
            # Webhook用のペイロード
            payload = {
                "text": formatted_message,
                "username": self.bot_name,
                "icon_emoji": ":snowflake:"
            }
            
            # Slackに送信
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                logger.info("Message sent successfully via webhook")
                return True, "メッセージが正常に送信されました"
            else:
                logger.error(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")
                return False, f"メッセージの送信に失敗しました (Status: {response.status_code})"
                
        except requests.exceptions.Timeout:
            logger.error("Request timeout")
            return False, "送信がタイムアウトしました"
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            return False, f"ネットワークエラーが発生しました: {str(e)}"
                
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return False, f"予期しないエラーが発生しました: {str(e)}"
    
