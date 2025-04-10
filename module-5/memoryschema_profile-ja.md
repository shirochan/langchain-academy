# プロファイルスキーマ付きチャットボット

## 概要

[LangGraph Memory Store](https://langchain-ai.github.io/langgraph/reference/store/#langgraph.store.base.BaseStore)を長期メモリを保存・検索する方法として紹介しました。

`短期（スレッド内）`と`長期（スレッド間）`の両方のメモリを使用するシンプルなチャットボットを構築しました。

ユーザーがチャットしている間、長期の[意味的記憶](https://langchain-ai.github.io/langgraph/concepts/memory/#semantic-memory)（ユーザーに関する事実）を[「ホットパス」](https://langchain-ai.github.io/langgraph/concepts/memory/#writing-memories)で保存しました。

## 目標

チャットボットはメモリを文字列として保存していました。実際には、メモリに構造を持たせたいことがよくあります。

例えば、メモリは[単一の継続的に更新されるスキーマ](https://langchain-ai.github.io/langgraph/concepts/memory/#profile)にすることができます。

今回の場合、これを単一のユーザープロファイルにしたいと思います。

チャットボットを拡張して、意味的メモリを単一の[ユーザープロファイル](https://langchain-ai.github.io/langgraph/concepts/memory/#profile)に保存するようにします。

また、このスキーマを新しい情報で更新するためのライブラリ、[Trustcall](https://github.com/hinthornw/trustcall)も紹介します。

## ユーザープロファイルスキーマの定義

Pythonには[構造化データ](https://python.langchain.com/docs/concepts/structured_outputs/#schema-definition)のための多くの異なる型があります。TypedDict、辞書、JSON、[Pydantic](https://docs.pydantic.dev/latest/)などです。

まずは、TypedDictを使ってユーザープロファイルスキーマを定義してみましょう。

```python
from typing import TypedDict, List

class UserProfile(TypedDict):
    """型付けされたフィールドを持つユーザープロファイルスキーマ"""
    user_name: str  # ユーザーの好みの名前
    interests: List[str]  # ユーザーの興味のリスト
```

## スキーマをストアに保存する

[LangGraph Store](https://langchain-ai.github.io/langgraph/reference/store/#langgraph.store.base.BaseStore)は、`value`として任意のPython辞書を受け入れます。

```python
# TypedDictインスタンス
user_profile: UserProfile = {
    "user_name": "Lance",
    "interests": ["biking", "technology", "coffee"]
}
user_profile
```

[put](https://langchain-ai.github.io/langgraph/reference/store/#langgraph.store.base.BaseStore.put)メソッドを使用して、TypedDictをストアに保存します。

```python
import uuid
from langgraph.store.memory import InMemoryStore

# インメモリストアの初期化
in_memory_store = InMemoryStore()

# メモリを保存するための名前空間
user_id = "1"
namespace_for_memory = (user_id, "memory")

# 名前空間にキーと値としてメモリを保存
key = "user_profile"
value = user_profile
in_memory_store.put(namespace_for_memory, key, value)
```

[search](https://langchain-ai.github.io/langgraph/reference/store/#langgraph.store.base.BaseStore.search)を使用して、名前空間でストアからオブジェクトを取得します。

```python
# 検索
for m in in_memory_store.search(namespace_for_memory):
    print(m.dict())
```

また、[get](https://langchain-ai.github.io/langgraph/reference/store/#langgraph.store.base.BaseStore.get)を使用して、名前空間とキーで特定のオブジェクトを取得することもできます。

```python
# 名前空間とキーでメモリを取得
profile = in_memory_store.get(namespace_for_memory, "user_profile")
profile.value
```

## プロファイルスキーマ付きチャットボット

メモリのスキーマを指定し、ストアに保存する方法がわかりました。

では、この特定のスキーマでメモリを実際に*作成*するにはどうすればよいでしょうか？

チャットボットでは、[ユーザーチャットからメモリを作成したい](https://langchain-ai.github.io/langgraph/concepts/memory/#profile)と思います。

ここで[構造化出力](https://python.langchain.com/docs/concepts/structured_outputs/#recommended-usage)の概念が役立ちます。

LangChainの[チャットモデル](https://python.langchain.com/docs/concepts/chat_models/)インターフェースには、構造化出力を強制する[`with_structured_output`](https://python.langchain.com/docs/concepts/structured_outputs/#recommended-usage)メソッドがあります。

これは、出力がスキーマに準拠することを強制したい場合に役立ち、出力を解析してくれます。

作成した`UserProfile`スキーマを`with_structured_output`メソッドに渡してみましょう。

```python
from pydantic import BaseModel, Field

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

# モデルの初期化
model = ChatOpenAI(model="gpt-4o", temperature=0)

# スキーマをモデルにバインド
model_with_structure = model.with_structured_output(UserProfile)

# スキーマに一致する構造化出力を生成するためにモデルを呼び出す
structured_output = model_with_structure.invoke([HumanMessage("My name is Lance, I like to bike.")])
structured_output
```

次に、これをチャットボットで使用してみましょう。

これは`write_memory`関数に小さな変更を加えるだけです。

上記で定義した`model_with_structure`を使用して、スキーマに一致するプロファイルを生成します。

```python
from IPython.display import Image, display

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.store.base import BaseStore

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.runnables.config import RunnableConfig

# チャットボットの指示
MODEL_SYSTEM_MESSAGE = """You are a helpful assistant with memory that provides information about the user. 
If you have memory for this user, use it to personalize your responses.
Here is the memory (it may be empty): {memory}"""

# チャット履歴と既存のメモリから新しいメモリを作成
CREATE_MEMORY_INSTRUCTION = """Create or update a user profile memory based on the user's chat history. 
This will be saved for long-term memory. If there is an existing memory, simply update it. 
Here is the existing memory (it may be empty): {memory}"""

def call_model(state: MessagesState, config: RunnableConfig, store: BaseStore):

    """ストアからメモリを読み込み、それを使用してチャットボットの応答をパーソナライズします。"""
    
    # 設定からユーザーIDを取得
    user_id = config["configurable"]["user_id"]

    # ストアからメモリを取得
    namespace = ("memory", user_id)
    existing_memory = store.get(namespace, "user_memory")

    # システムプロンプト用にメモリをフォーマット
    if existing_memory and existing_memory.value:
        memory_dict = existing_memory.value
        formatted_memory = (
            f"Name: {memory_dict.get('user_name', 'Unknown')}\n"
            f"Interests: {', '.join(memory_dict.get('interests', []))}"
        )
    else:
        formatted_memory = None

    # システムプロンプトでメモリをフォーマット
    system_msg = MODEL_SYSTEM_MESSAGE.format(memory=formatted_memory)

    # メモリとチャット履歴を使用して応答
    response = model.invoke([SystemMessage(content=system_msg)]+state["messages"])

    return {"messages": response}

def write_memory(state: MessagesState, config: RunnableConfig, store: BaseStore):

    """チャット履歴を反映し、メモリをストアに保存します。"""
    
    # 設定からユーザーIDを取得
    user_id = config["configurable"]["user_id"]

    # ストアから既存のメモリを取得
    namespace = ("memory", user_id)
    existing_memory = store.get(namespace, "user_memory")

    # システムプロンプト用にメモリをフォーマット
    if existing_memory and existing_memory.value:
        memory_dict = existing_memory.value
        formatted_memory = (
            f"Name: {memory_dict.get('user_name', 'Unknown')}\n"
            f"Interests: {', '.join(memory_dict.get('interests', []))}"
        )
    else:
        formatted_memory = None
        
    # 指示で既存のメモリをフォーマット
    system_msg = CREATE_MEMORY_INSTRUCTION.format(memory=formatted_memory)

    # スキーマに一致する構造化出力を生成するためにモデルを呼び出す
    new_memory = model_with_structure.invoke([SystemMessage(content=system_msg)]+state['messages'])

    # 既存のユーザープロファイルメモリを上書き
    key = "user_memory"
    store.put(namespace, key, new_memory)

# グラフの定義
builder = StateGraph(MessagesState)
builder.add_node("call_model", call_model)
builder.add_node("write_memory", write_memory)
builder.add_edge(START, "call_model")
builder.add_edge("call_model", "write_memory")
builder.add_edge("write_memory", END)

# 長期（スレッド間）メモリ用のストア
across_thread_memory = InMemoryStore()

# 短期（スレッド内）メモリ用のチェックポインター
within_thread_memory = MemorySaver()

# チェックポインターとストアでグラフをコンパイル
graph = builder.compile(checkpointer=within_thread_memory, store=across_thread_memory)

# 表示
display(Image(graph.get_graph(xray=1).draw_mermaid_png()))
```

## チャットボットの使用例

```python
# 短期（スレッド内）メモリ用のスレッドIDを提供
# 長期（スレッド間）メモリ用のユーザーIDを提供
config = {"configurable": {"thread_id": "1", "user_id": "1"}}

# ユーザー入力
input_messages = [HumanMessage(content="Hi, my name is Lance and I like to bike around San Francisco and eat at bakeries.")]

# グラフを実行
for chunk in graph.stream({"messages": input_messages}, config, stream_mode="values"):
    chunk["messages"][-1].pretty_print()
```

ストア内のメモリを確認してみましょう。

メモリがスキーマに一致する辞書であることがわかります。

```python
# メモリを保存するための名前空間
user_id = "1"
namespace = ("memory", user_id)
existing_memory = across_thread_memory.get(namespace, "user_memory")
existing_memory.value
```

## 失敗する可能性のあるケース

[`with_structured_output`](https://python.langchain.com/docs/concepts/structured_outputs/#recommended-usage)は非常に便利ですが、より複雑なスキーマを扱う場合はどうなるでしょうか？

[ここに](https://github.com/hinthornw/trustcall?tab=readme-ov-file#complex-schema)より複雑なスキーマの例があります。以下でテストしてみましょう。

これは[Pydantic](https://docs.pydantic.dev/latest/)モデルで、ユーザーのコミュニケーションと信頼の好みを説明しています。

```python
from typing import List, Optional

class OutputFormat(BaseModel):
    preference: str
    sentence_preference_revealed: str

class TelegramPreferences(BaseModel):
    preferred_encoding: Optional[List[OutputFormat]] = None
    favorite_telegram_operators: Optional[List[OutputFormat]] = None
    preferred_telegram_paper: Optional[List[OutputFormat]] = None

class MorseCode(BaseModel):
    preferred_key_type: Optional[List[OutputFormat]] = None
    favorite_morse_abbreviations: Optional[List[OutputFormat]] = None
``` 