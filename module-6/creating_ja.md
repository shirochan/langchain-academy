# デプロイメントの作成

モジュール5で作成した`task_maistro`アプリケーションのデプロイメントを作成しましょう。

## コード構造

LangGraph Platformのデプロイメントを作成するには、[以下の情報](https://langchain-ai.github.io/langgraph/concepts/application_structure/)を提供する必要があります：

* [LangGraph API設定ファイル](https://langchain-ai.github.io/langgraph/concepts/application_structure/#configuration-file) - `langgraph.json`
* アプリケーションのロジックを実装するグラフ - 例：`task_maistro.py`
* アプリケーションの実行に必要な依存関係を指定するファイル - `requirements.txt`
* アプリケーションの実行に必要な環境変数 - `.env`または`docker-compose.yml`

これらは既に`module-6/deployment`ディレクトリに存在しています！

## CLI

[LangGraph CLI](https://langchain-ai.github.io/langgraph/concepts/langgraph_cli/)は、LangGraph Platformのデプロイメントを作成するためのコマンドラインインターフェースです。

## 自己ホスト型デプロイメントの作成

[自己ホスト型デプロイメント](https://langchain-ai.github.io/langgraph/how-tos/deploy-self-hosted/#how-to-do-a-self-hosted-deployment-of-langgraph)を作成するために、以下の手順に従います。

### LangGraphサーバーのDockerイメージのビルド

まず、langgraph CLIを使用して[LangGraphサーバー](https://docs.google.com/presentation/d/18MwIaNR2m4Oba6roK_2VQcBE_8Jq_SI7VHTXJdl7raU/edit#slide=id.g313fb160676_0_32)のDockerイメージを作成します。

これにより、グラフと依存関係がDockerイメージにパッケージ化されます。

Dockerイメージは、アプリケーションを実行するために必要なコードと依存関係を含むDockerコンテナのテンプレートです。

[Docker](https://docs.docker.com/engine/install/)がインストールされていることを確認し、以下のコマンドを実行してDockerイメージ`my-image`を作成します：

```bash
$ cd module-6/deployment
$ langgraph build -t my-image
```

### RedisとPostgreSQLのセットアップ

RedisとPostgreSQLが既に実行されている場合（例：ローカルまたは他のサーバー上）、RedisとPostgreSQLのURIを指定して、LangGraphサーバーコンテナを[単独で](https://langchain-ai.github.io/langgraph/how-tos/deploy-self-hosted/#running-the-application-locally)実行できます：

```bash
docker run \
    --env-file .env \
    -p 8123:8000 \
    -e REDIS_URI="foo" \
    -e DATABASE_URI="bar" \
    -e LANGSMITH_API_KEY="baz" \
    my-image
```

または、提供されている`docker-compose.yml`ファイルを使用して、定義されたサービスに基づいて3つの別々のコンテナを作成できます：

* `langgraph-redis`: 公式Redisイメージを使用して新しいコンテナを作成します。
* `langgraph-postgres`: 公式Postgresイメージを使用して新しいコンテナを作成します。
* `langgraph-api`: 事前にビルドしたイメージを使用して新しいコンテナを作成します。

`docker-compose-example.yml`をコピーし、デプロイされた`task_maistro`アプリを実行するために以下の環境変数を追加します：

* `IMAGE_NAME`（例：`my-image`）
* `LANGCHAIN_API_KEY`
* `OPENAI_API_KEY`

次に、[デプロイメントを起動](https://langchain-ai.github.io/langgraph/how-tos/deploy-self-hosted/#using-docker-compose)します：

```bash
$ cd module-6/deployment
$ docker compose up
``` 