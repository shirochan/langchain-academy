# メモリエージェントの実装

## メモリの更新と取得

会話の更新と新しいメモリの作成を行います：

```python
# 会話の更新
updated_conversation = [
    AIMessage(content="それは素晴らしいですね。その後何をされましたか？"), 
    HumanMessage(content="Tartineに行ってクロワッサンを食べました。"),                       
    AIMessage(content="他に何か気になることはありますか？"),
    HumanMessage(content="日本に戻ることを考えていて、この冬に帰る予定です！"),
]

# システムメッセージの更新
system_msg = """以下の会話に基づいて既存のメモリを更新し、新しいメモリを作成してください："""

# 既存のメモリを保存（ID、キー（ツール名）、値を持つ）
tool_name = "Memory"
existing_memories = [(str(i), tool_name, memory.model_dump()) for i, memory in enumerate(result["responses"])] if result["responses"] else None
```

## メモリ抽出の実行

更新された会話と既存のメモリを使用してメモリ抽出を実行します：

```python
# 更新された会話と既存のメモリを使用して抽出を実行
result = trustcall_extractor_see_all_tool_calls.invoke({
    "messages": updated_conversation, 
    "existing": existing_memories
})
```

## メタデータの確認

ツール呼び出しのメタデータを確認します：

```python
# メタデータにはツール呼び出しが含まれています
for m in result["response_metadata"]: 
    print(m)
```

## グラフの定義

メモリを保存するかどうかの二択を行うシンプルなルーター`route_message`を追加します。
メモリコレクションの更新は、以前と同様に`write_memory`ノードの`Trustcall`によって処理されます。

## メモリの更新と取得の実装

メモリの更新と取得を実装するために、以下のコードを使用します：

```python
# メモリの更新と取得
def update_and_retrieve_memory(conversation, existing_memories):
    # メモリ抽出の実行
    result = trustcall_extractor_see_all_tool_calls.invoke({
        "messages": conversation, 
        "existing": existing_memories
    })
    
    # メモリの保存
    tool_name = "Memory"
    memories = [(str(i), tool_name, memory.model_dump()) for i, memory in enumerate(result["responses"])] if result["responses"] else None
    
    return memories
```

## メモリの使用例

メモリの更新と取得の使用例を示します：

```python
# 会話の更新
updated_conversation = [
    AIMessage(content="それは素晴らしいですね。その後何をされましたか？"), 
    HumanMessage(content="Tartineに行ってクロワッサンを食べました。"),                       
    AIMessage(content="他に何か気になることはありますか？"),
    HumanMessage(content="日本に戻ることを考えていて、この冬に帰る予定です！"),
]

# 既存のメモリを取得
existing_memories = [(str(i), "Memory", memory.model_dump()) for i, memory in enumerate(result["responses"])] if result["responses"] else None

# メモリの更新と取得
updated_memories = update_and_retrieve_memory(updated_conversation, existing_memories)
```

## メモリの検証

更新されたメモリが正しく保存されているか確認します：

```python
# メモリの検証
for memory in updated_memories:
    print(f"Memory ID: {memory[0]}")
    print(f"Tool Name: {memory[1]}")
    print(f"Memory Value: {memory[2]}")
    print("---")
``` 