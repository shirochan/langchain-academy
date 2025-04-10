# コレクションスキーマを持つチャットボット

## 概要

このノートブックでは、コレクションスキーマを使用してメモリを保存するチャットボットの実装方法を説明します。

## 目標

- コレクションにメモリを保存する方法を学ぶ
- コレクションスキーマの更新方法を理解する
- Trustcallを使用してコレクションを更新する方法を学ぶ

## 実装

### メモリクラスの定義

```python
from pydantic import BaseModel, Field

class Memory(BaseModel):
    content: str = Field(description="メモリの主要な内容。例：ユーザーがフランス語を学ぶことに興味があると表明しました。")
```

### メモリの保存

```python
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# モデルの初期化
model = ChatOpenAI(model="gpt-4", temperature=0)

# メモリの作成
memory = Memory(content="ユーザーはフランス語を学ぶことに興味があると表明しました。")

# メモリの保存
store.put(("memories", "user_id"), "memory_id", memory.model_dump())
```

### メモリの検索

```python
# メモリの検索
memories = store.search(("memories", "user_id"))
for memory in memories:
    print(memory.value)
```

### Trustcallを使用したコレクションの更新

```python
from trustcall import create_extractor

# エクストラクターの作成
trustcall_extractor = create_extractor(
    model,
    tools=[Memory],
    tool_choice="Memory",
    enable_inserts=True,
)

# 会話の更新
updated_conversation = [
    AIMessage(content="それは素晴らしいですね。その後何かされましたか？"),
    HumanMessage(content="Tartineに行ってクロワッサンを食べました。"),
    AIMessage(content="他に何か気になることはありますか？"),
    HumanMessage(content="日本に戻ることを考えていて、この冬に帰国する予定です！"),
]

# システムメッセージの更新
system_msg = """以下の会話に基づいて既存のメモリを更新し、新しいメモリを作成してください："""

# 既存のメモリを保存
tool_name = "Memory"
existing_memories = [(str(i), tool_name, memory.model_dump()) for i, memory in enumerate(result["responses"])] if result["responses"] else None

# エクストラクターの呼び出し
result = trustcall_extractor.invoke({
    "messages": updated_conversation,
    "existing": existing_memories
})
```

### チャットボットの実装

```python
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.store.memory import InMemoryStore
from langgraph.checkpoint.memory import MemorySaver

# モデルの初期化
model = ChatOpenAI(model="gpt-4", temperature=0)

# チャットボットの指示
MODEL_SYSTEM_MESSAGE = """あなたは親切なチャットボットです。ユーザーのコンパニオンとなるように設計されています。

長期的なメモリを持っており、時間の経過とともにユーザーについて学んだ情報を追跡します。

現在のメモリ（この会話から更新されたメモリを含む場合があります）：

{memory}"""

# Trustcallの指示
TRUSTCALL_INSTRUCTION = """以下のやり取りについて振り返ってください。

提供されたツールを使用して、ユーザーについて必要なメモリを保持してください。

並列ツール呼び出しを使用して、更新と挿入を同時に処理してください："""

def call_model(state: MessagesState, config: RunnableConfig, store: BaseStore):
    """ストアからメモリを読み込み、それらを使用してチャットボットの応答をパーソナライズします。"""
    
    # 設定からユーザーIDを取得
    user_id = config["configurable"]["user_id"]

    # ストアからメモリを取得
    namespace = ("memories", user_id)
    memories = store.search(namespace)

    # システムプロンプト用にメモリをフォーマット
    info = "\n".join(f"- {mem.value['content']}" for mem in memories)
    system_msg = MODEL_SYSTEM_MESSAGE.format(memory=info)

    # メモリとチャット履歴を使用して応答
    response = model.invoke([SystemMessage(content=system_msg)]+state["messages"])

    return {"messages": response}

def write_memory(state: MessagesState, config: RunnableConfig, store: BaseStore):
    """チャット履歴を振り返り、メモリコレクションを更新します。"""
    
    # 設定からユーザーIDを取得
    user_id = config["configurable"]["user_id"]

    # メモリの名前空間を定義
    namespace = ("memories", user_id)

    # コンテキスト用に最新のメモリを取得
    existing_items = store.search(namespace)

    # Trustcallエクストラクター用に既存のメモリをフォーマット
    tool_name = "Memory"
    existing_memories = ([(existing_item.key, tool_name, existing_item.value)
                          for existing_item in existing_items]
                          if existing_items
                          else None
                        )

    # チャット履歴と指示をマージ
    updated_messages=list(merge_message_runs(messages=[SystemMessage(content=TRUSTCALL_INSTRUCTION)] + state["messages"]))

    # エクストラクターを呼び出し
    result = trustcall_extractor.invoke({"messages": updated_messages, 
                                        "existing": existing_memories})

    # Trustcallからのメモリをストアに保存
    for r, rmeta in zip(result["responses"], result["response_metadata"]):
        store.put(namespace,
                  rmeta.get("json_doc_id", str(uuid.uuid4())),
                  r.model_dump(mode="json"),
            )

# グラフの定義
builder = StateGraph(MessagesState)
builder.add_node("call_model", call_model)
builder.add_node("write_memory", write_memory)
builder.add_edge(START, "call_model")
builder.add_edge("call_model", "write_memory")
builder.add_edge("write_memory", END)

# 長期的（スレッド間）メモリ用のストア
across_thread_memory = InMemoryStore()

# 短期的（スレッド内）メモリ用のチェックポインター
within_thread_memory = MemorySaver()

# チェックポインターとストアでグラフをコンパイル
graph = builder.compile(checkpointer=within_thread_memory, store=across_thread_memory)
```

## 使用例

### 会話の開始

```python
# 短期的（スレッド内）メモリ用のスレッドIDを提供
# 長期的（スレッド間）メモリ用のユーザーIDを提供
config = {"configurable": {"thread_id": "1", "user_id": "1"}}

# ユーザー入力
input_messages = [HumanMessage(content="こんにちは、私の名前はランスです")]

# グラフの実行
for chunk in graph.stream({"messages": input_messages}, config, stream_mode="values"):
    chunk["messages"][-1].pretty_print()
```

### メモリの確認

```python
# メモリを保存する名前空間
user_id = "1"
namespace = ("memories", user_id)
memories = across_thread_memory.search(namespace)
for m in memories:
    print(m.dict())
```

### 新しいスレッドでの会話の継続

```python
# 短期的（スレッド内）メモリ用のスレッドIDを提供
# 長期的（スレッド間）メモリ用のユーザーIDを提供
config = {"configurable": {"thread_id": "2", "user_id": "1"}}

# ユーザー入力
input_messages = [HumanMessage(content="どのベーカリーをお勧めしますか？")]

# グラフの実行
for chunk in graph.stream({"messages": input_messages}, config, stream_mode="values"):
    chunk["messages"][-1].pretty_print()
``` 