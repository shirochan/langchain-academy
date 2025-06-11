![LangChain Academy](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/66e9eba1020525eea7873f96_LCA-big-green%20(2).svg)

## はじめに

LangChain Academyへようこそ！ 
これはLangChainエコシステム内の基礎的概念に焦点を当てたモジュール群です。
Module 0は基本的なセットアップで、Module 1-4はLangGraphに焦点を当て、段階的により高度なテーマを追加していきます。
各モジュールフォルダには、ノートブックのセットがあります。各ノートブックにはLangChain Academyが付随しており、
トピックを案内します。各モジュールには`studio`サブディレクトリもあり、LangGraph APIとStudioを使用して
探索する関連グラフのセットが含まれています。

## セットアップ

### Pythonバージョン

このコースを最大限に活用するために、Python 3.11以降を使用していることを確認してください。 
このバージョンはLangGraphとの最適な互換性のために必要です。古いバージョンを使用している場合は、
アップグレードすることですべてがスムーズに動作します。
```
python3 --version
```

### リポジトリのクローン
```
git clone https://github.com/langchain-ai/langchain-academy.git
$ cd langchain-academy
```

### 環境の作成と依存関係のインストール
#### Mac/Linux/WSL
```
$ python3 -m venv lc-academy-env
$ source lc-academy-env/bin/activate
$ pip install -r requirements.txt
```
#### Windows Powershell
```
PS> python3 -m venv lc-academy-env
PS> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
PS> lc-academy-env\scripts\activate
PS> pip install -r requirements.txt
```

### ノートブックの実行
Jupyterがセットアップされていない場合は、[こちら](https://jupyter.org/install)のインストール手順に従ってください。
```
$ jupyter notebook
```

### 環境変数の設定
環境変数の設定方法を簡単に説明します。`python-dotenv`ライブラリで
`.env`ファイルを使用することもできます。
#### Mac/Linux/WSL
```
$ export API_ENV_VAR="your-api-key-here"
```
#### Windows Powershell
```
PS> $env:API_ENV_VAR = "your-api-key-here"
```

### OpenAI APIキーの設定
* OpenAI APIキーをお持ちでない場合は、[こちら](https://openai.com/index/openai-api/)でサインアップできます。
* 環境で`OPENAI_API_KEY`を設定してください

### LangSmith APIのサインアップと設定
* [こちら](https://smith.langchain.com/)でLangSmithにサインアップし、LangSmithについて詳しく知り、
* ワークフロー内での使用方法は[こちら](https://www.langchain.com/langsmith)、関連ライブラリの[ドキュメント](https://docs.smith.langchain.com/)をご覧ください！
* 環境で`LANGCHAIN_API_KEY`、`LANGCHAIN_TRACING_V2=true`を設定してください

### ウェブ検索用のTavily APIの設定

* Tavily Search APIは、LLMとRAG向けに最適化された検索エンジンで、効率的で
高速かつ持続的な検索結果を目的としています。
* APIキーは[こちら](https://tavily.com/)でサインアップできます。
サインアップは簡単で、非常に寛大な無料枠を提供しています。一部のレッスン（Module 4）でTavilyを使用します。

* 環境で`TAVILY_API_KEY`を設定してください。

### LangGraph Studioの設定

* LangGraph Studioは、エージェントの表示とテスト用のカスタムIDEです。
* StudioはMac、Windows、Linuxでローカルに実行し、ブラウザで開くことができます。
* ローカルStudio開発サーバーについては[こちら](https://langchain-ai.github.io/langgraph/concepts/langgraph_studio/#local-development-server)と[こちら](https://langchain-ai.github.io/langgraph/how-tos/local-studio/#run-the-development-server)のドキュメントをご覧ください。
* LangGraph Studio用のグラフは`module-x/studio/`フォルダにあります。
* ローカル開発サーバーを開始するには、各モジュールの`/studio`ディレクトリでターミナルで次のコマンドを実行します：

```
langgraph dev
```

次の出力が表示されます：
```
- 🚀 API: http://127.0.0.1:2024
- 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
- 📚 API Docs: http://127.0.0.1:2024/docs
```

ブラウザを開き、Studio UI: `https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024`に移動します。

* Studioを使用するには、関連するAPIキーで.envファイルを作成する必要があります
* 例として、module 1から6用にこれらのファイルを作成するには、コマンドラインから次を実行します：
```
for i in {1..6}; do
  cp module-$i/studio/.env.example module-$i/studio/.env
  echo "OPENAI_API_KEY=\"$OPENAI_API_KEY\"" > module-$i/studio/.env
done
echo "TAVILY_API_KEY=\"$TAVILY_API_KEY\"" >> module-4/studio/.env
```
