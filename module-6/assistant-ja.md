# アシスタント

[アシスタント](https://langchain-ai.github.io/langgraph/concepts/assistants/#resources)は、開発者が実験のためにエージェントを簡単に修正・バージョン管理できる方法を提供します。

## グラフに設定を提供する

`task_maistro`グラフは既にアシスタントを使用するように設定されています！

グラフ内で定義され読み込まれる`configuration.py`ファイルがあります。

グラフノード内で設定可能なフィールド（`user_id`、`todo_category`、`task_maistro_role`）にアクセスします。

## アシスタントの作成

では、これまで構築してきた`task_maistro`アプリケーションでアシスタントの実用的なユースケースは何でしょうか？

私にとっては、異なるカテゴリのタスクに対して別々のToDoリストを持つことができることです。

例えば、個人タスク用と仕事タスク用に別々のアシスタントが欲しいです。

これらは`todo_category`と`task_maistro_role`の設定可能なフィールドを使用して簡単に設定できます。

![スクリーンショット](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/673d50597f4e9eae9abf4869_Screenshot%202024-11-19%20at%206.57.01%E2%80%AFPM.png)

## アシスタントの実装

### 個人用アシスタント

これは私の個人タスクを管理するために使用する個人用アシスタントです。

```python
from langgraph_sdk import get_client
url_for_cli_deployment = "http://localhost:8123"
client = get_client(url=url_for_cli_deployment)

personal_assistant = await client.assistants.create(
    # "task_maistro"はデプロイしたグラフの名前
    "task_maistro", 
    config={"configurable": {"todo_category": "personal"}}
)
```

このアシスタントを便利のために`user_id`を含めるように更新し、[新しいバージョンを作成](https://langchain-ai.github.io/langgraph/cloud/how-tos/assistant_versioning/#create-a-new-version-for-your-assistant)します。

```python
task_maistro_role = """あなたは親切で整理された個人タスクアシスタントです。主な焦点は、ユーザーが個人タスクと約束事を管理するのを支援することです。具体的には：

- 個人タスクの追跡と整理を支援
- 'todo summary'を提供する際：
  1. 期限別にすべての現在のタスクをリスト化（期限切れ、今日、今週、将来）
  2. 期限が設定されていないタスクを強調し、期限の追加を優しく促す
  3. 重要そうだが時間見積もりがないタスクに注意を払う
- 期限なしで新しいタスクが追加された場合、積極的に期限を尋ねる
- ユーザーが責任を果たすのを支援しながら、支援的なトーンを維持
- 期限と重要性に基づいてタスクの優先順位付けを支援

コミュニケーションスタイルは励ましと支援に満ち、決して批判的にならないようにします。

タスクに期限がない場合、「[タスク]にまだ期限が設定されていないことに気づきました。より良く追跡するために期限を追加しませんか？」のような応答をします。"""

configurations = {"todo_category": "personal", 
                  "user_id": "lance",
                  "task_maistro_role": task_maistro_role}

personal_assistant = await client.assistants.update(
    personal_assistant["assistant_id"],
    config={"configurable": configurations}
)
```

### 仕事用アシスタント

次に、仕事用のアシスタントを作成します。これは仕事のタスクに使用します。

```python
task_maistro_role = """あなたは集中力があり効率的な仕事タスクアシスタントです。

主な焦点は、ユーザーが現実的な時間枠で仕事の約束事を管理するのを支援することです。

具体的には：

- 仕事タスクの追跡と整理を支援
- 'todo summary'を提供する際：
  1. 期限別にすべての現在のタスクをリスト化（期限切れ、今日、今週、将来）
  2. 期限が設定されていないタスクを強調し、期限の追加を優しく促す
  3. 重要そうだが時間見積もりがないタスクに注意を払う
- 新しいタスクについて議論する際、タスクタイプに基づいて現実的な時間枠を提案：
  • 開発者向け機能：通常1日
  • コースレッスンのレビュー/フィードバック：通常2日
  • ドキュメントスプリント：通常3日
- 期限とチーム依存関係に基づいてタスクの優先順位付けを支援
- ユーザーが責任を果たすのを支援しながら、プロフェッショナルなトーンを維持

コミュニケーションスタイルは支援的だが実践的であるべきです。

タスクに期限がない場合、「[タスク]にまだ期限が設定されていないことに気づきました。同様のタスクに基づくと、これには[提案された時間枠]かかるかもしれません。これを考慮して期限を設定しませんか？」のような応答をします。"""

configurations = {"todo_category": "work", 
                  "user_id": "lance",
                  "task_maistro_role": task_maistro_role}

work_assistant = await client.assistants.create(
    # "task_maistro"はデプロイしたグラフの名前
    "task_maistro", 
    config={"configurable": configurations}
)
```

## アシスタントの使用

アシスタントはデプロイメントの`Postgres`に保存されます。

これにより、SDKを使用してアシスタントを簡単に[検索](https://langchain-ai.github.io/langgraph/cloud/how-tos/configuration_cloud/)できます。

```python
assistants = await client.assistants.search()
for assistant in assistants:
    print({
        'assistant_id': assistant['assistant_id'],
        'version': assistant['version'],
        'config': assistant['config']
    })
```

SDKを使用して簡単に管理できます。例えば、使用しなくなったアシスタントを削除できます。

```python
await client.assistants.delete("assistant_id")
```

`personal`と`work`アシスタントのIDを設定しましょう。

```python
work_assistant_id = assistants[0]['assistant_id']
personal_assistant_id = assistants[1]['assistant_id']
```

### 仕事用アシスタント

仕事用アシスタントにいくつかのToDoを追加しましょう。

```python
from langchain_core.messages import HumanMessage
from langchain_core.messages import convert_to_messages

user_input = "Create or update few ToDos: 1) Re-film Module 6, lesson 5 by end of day today. 2) Update audioUX by next Monday."
thread = await client.threads.create()
async for chunk in client.runs.stream(thread["thread_id"], 
                                      work_assistant_id,
                                      input={"messages": [HumanMessage(content=user_input)]},
                                      stream_mode="values"):

    if chunk.event == 'values':
        state = chunk.data
        convert_to_messages(state["messages"])[-1].pretty_print()
```

別のToDoを作成しましょう。

```python
user_input = "Create another ToDo: Finalize set of report generation tutorials."
thread = await client.threads.create()
async for chunk in client.runs.stream(thread["thread_id"], 
                                      work_assistant_id,
                                      input={"messages": [HumanMessage(content=user_input)]},
                                      stream_mode="values"):

    if chunk.event == 'values':
        state = chunk.data
        convert_to_messages(state["messages"])[-1].pretty_print()
```

アシスタントは指示を使用してタスク作成を促します！

期限を指定するよう私に尋ねています :)

```python
user_input = "OK, for this task let's get it done by next Tuesday."
async for chunk in client.runs.stream(thread["thread_id"], 
                                      work_assistant_id,
                                      input={"messages": [HumanMessage(content=user_input)]},
                                      stream_mode="values"):

    if chunk.event == 'values':
        state = chunk.data
        convert_to_messages(state["messages"])[-1].pretty_print()
```

### 個人用アシスタント

同様に、個人用アシスタントにToDoを追加できます。

```python
user_input = "Create ToDos: 1) Check on swim lessons for the baby this weekend. 2) For winter travel, check AmEx points."
thread = await client.threads.create()
async for chunk in client.runs.stream(thread["thread_id"], 
                                      personal_assistant_id,
                                      input={"messages": [HumanMessage(content=user_input)]},
                                      stream_mode="values"):

    if chunk.event == 'values':
        state = chunk.data
        convert_to_messages(state["messages"])[-1].pretty_print()
```

ToDoの要約を取得しましょう。

```python
user_input = "Give me a todo summary."
thread = await client.threads.create()
async for chunk in client.runs.stream(thread["thread_id"], 
                                      personal_assistant_id,
                                      input={"messages": [HumanMessage(content=user_input)]},
                                      stream_mode="values"):

    if chunk.event == 'values':
        state = chunk.data
        convert_to_messages(state["messages"])[-1].pretty_print()
``` 