# Python 3.11をベースとしたイメージを使用
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムパッケージを更新し、必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Pythonの依存関係をコピーしてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# プロジェクトファイルをコピー
COPY . .

# Jupyter設定ディレクトリを作成
RUN mkdir -p /root/.jupyter

# Jupyter Notebookのポートを公開
EXPOSE 8888

# LangGraph Studioのポートも公開
EXPOSE 2024

# Jupyter Notebookを起動
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]