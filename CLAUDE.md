# CLAUDE.md

このファイルは、このリポジトリでコードを操作する際にClaude Code (claude.ai/code) にガイダンスを提供します。

## 環境設定

これはLangChain Academy用のPython 3.11+教育リポジトリです。環境を設定してください：

```bash
python3 -m venv lc-academy-env
source lc-academy-env/bin/activate  # Mac/Linux/WSL
# または
lc-academy-env\scripts\activate  # Windows
pip install -r requirements.txt
```

## 必要なAPIキー

以下の環境変数を設定してください：
- `OPENAI_API_KEY` - 全モジュールで必要
- `LANGCHAIN_API_KEY` と `LANGCHAIN_TRACING_V2=true` - LangSmithトレーシング用
- `TAVILY_API_KEY` - Module 4（ウェブ検索）で必要

## 共通コマンド

**Jupyterノートブックの実行:**
```bash
jupyter notebook
```

**LangGraph Studioの開始 (任意のmodule-x/studio/ディレクトリから実行):**
```bash
langgraph dev
# Studio UIを開く: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```

**全studioディレクトリ用の.envファイルの設定:**
```bash
for i in {1..6}; do
  echo "OPENAI_API_KEY=\"$OPENAI_API_KEY\"" > module-$i/studio/.env
done
echo "TAVILY_API_KEY=\"$TAVILY_API_KEY\"" >> module-4/studio/.env
```

## コードベースアーキテクチャ

### モジュール進行
- **Module 0**: 基本的なLangChainセットアップとチャットモデル
- **Module 1**: LangGraphの基礎 - シンプルなグラフ、エージェント、ルーティング
- **Module 2**: 状態管理 - スキーマ、外部メモリ、メッセージフィルタリング
- **Module 3**: Human-in-the-loop - ブレークポイント、割り込み、状態編集
- **Module 4**: 高度なパターン - map-reduce、並列化、サブグラフ
- **Module 5**: メモリシステム - 永続ストア、コレクション、ユーザープロファイル
- **Module 6**: 本番デプロイメント - アシスタント、設定、LangGraph Cloud

### 主要な構造パターン
- 各モジュールには学習ノートブック（`.ipynb`）と`studio/`ディレクトリが含まれています
- Studioディレクトリには`langgraph.json`で参照されるデプロイ可能なグラフ実装が含まれています
- グラフ定義は以下の形式を使用: `"graph_name": "./file.py:graph_variable"`
- 状態の進化: シンプルなdict → TypedDict → Pydanticスキーマ → メモリストア

### コア技術
- **LangGraph**: 状態ベースのエージェントフレームワーク（主要焦点）
- **LangChain**: LLM統合とコンポーネント
- **LangGraph Studio**: ビジュアルグラフ開発環境
- **Trustcall**: スキーマベースのメモリ更新（Module 5）
- **SQLiteチェックポイント**: 組み込み状態永続化

## 開発ガイドライン

- グラフを操作する際は、概念を理解するために必ず対応するノートブックを最初に確認してください
- Studioグラフはノートブックの例を反映するが、本番対応である必要があります
- 状態スキーマはモジュール全体でシンプルから複雑へと進歩します
- メモリパターン: 短期（チェックポイント）→ 長期（ストア）→ セマンティック（スキーマ）
- デプロイメント前にLangGraph Studioを使用してグラフをテストしてください