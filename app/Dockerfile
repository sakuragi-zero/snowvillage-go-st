FROM python:3.12-slim

WORKDIR /app

# システムの依存関係をインストール
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# uvをインストール
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# プロジェクトファイルをコピー
COPY pyproject.toml uv.lock* ./

# 依存関係をインストール
RUN uv sync --frozen

# アプリケーションコードをコピー
COPY . .

# Streamlitの設定
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# ポート8501を公開
EXPOSE 8501

# アプリケーションを起動
CMD ["uv", "run", "streamlit", "run", "launch_screen.py"]