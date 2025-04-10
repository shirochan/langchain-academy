# メモリ機能付きチャットボット

## 概要

[メモリ](https://pmc.ncbi.nlm.nih.gov/articles/PMC10410470/)は、人々が情報を保存、検索、利用して現在と未来を理解することを可能にする認知機能です。

AIアプリケーションでは、[様々な長期記憶タイプ](https://langchain-ai.github.io/langgraph/concepts/memory/#memory)を使用することができます。

## 目標

ここでは、[LangGraph Memory Store](https://langchain-ai.github.io/langgraph/reference/store/#langgraph.store.base.BaseStore)を長期記憶を保存・検索する方法として紹介します。

`短期（スレッド内）`と`長期（スレッド間）`の両方のメモリを使用するチャットボットを構築します。

長期の[意味的記憶](https://langchain-ai.github.io/langgraph/concepts/memory/#semantic-memory)に焦点を当て、ユーザーに関する事実を記憶します。

これらの長期記憶は、ユーザーに関する事実を記憶できるパーソナライズされたチャットボットを作成するために使用されます。

ユーザーがチャットしている間、メモリは[「ホットパス」](https://langchain-ai.github.io/langgraph/concepts/memory/#writing-memories)で保存されます。

## LangGraph Storeの概要

[LangGraph Memory Store](https://langchain-ai.github.io/langgraph/reference/store/#langgraph.store.base.BaseStore)は、LangGraphでスレッド間で情報を保存・検索する方法を提供します。

これは永続的な`キー値`ストアのための[オープンソースのベースクラス](https://blog.langchain.dev/launching-long-term-memory-support-in-langgraph/)です。

## メモリの保存と検索

Storeにオブジェクト（例：メモリ）を保存する際、以下を提供します：

- オブジェクトの`namespace`（ディレクトリに似たタプル）
- オブジェクトの`key`（ファイル名に似たもの）
- オブジェクトの`value`（ファイルの内容に似たもの）

[put](https://langchain-ai.github.io/langgraph/reference/store/#langgraph.store.base.BaseStore.put)メソッドを使用して、`namespace`と`key`でオブジェクトをストアに保存します。

## 短期メモリと長期メモリの実装

`短期メモリ`には、[チェックポインター](https://langchain-ai.github.io/langgraph/concepts/persistence/#checkpointer-libraries)を使用します。

モジュール2と[概念ドキュメント](https://langchain-ai.github.io/langgraph/concepts/persistence/)でチェックポインターについて詳しく説明していますが、要約すると：

* グラフの状態を各ステップでスレッドに書き込みます。
* チャット履歴をスレッドに永続化します。
* グラフをスレッド内の任意のステップで中断および再開できるようにします。

そして、`長期メモリ`には、上記で紹介した[LangGraph Store](https://langchain-ai.github.io/langgraph/reference/store/#langgraph.store.base.BaseStore)を使用します。

## チャットボットの実装

チャットモデルを初期化します：

```python
# チャットモデル
from langchain_openai import ChatOpenAI

# LLMの初期化
model = ChatOpenAI(model="gpt-4o", temperature=0)
```

チャット履歴はチェックポインターを使用して短期メモリに保存されます。

チャットボットはチャット履歴を反映し、[LangGraph Store](https://langchain-ai.github.io/langgraph/reference/store/#langgraph.store.base.BaseStore)にメモリを作成して保存します。

このメモリは将来のチャットセッションでアクセスでき、チャットボットの応答をパーソナライズするために使用されます。

## メモリの保存と検索の実装

チャットボットと対話する際、2つのものを提供します：

1. `短期（スレッド内）メモリ`: チャット履歴を永続化するための`スレッドID`
2. `長期（スレッド間）メモリ`: ユーザーに長期メモリを名前空間化するための`ユーザーID`

これらの機能が実際にどのように連携するかを見てみましょう。

## 長期メモリ付きチャットボット

2種類のメモリを持つチャットボットを作成します：

1. `短期（スレッド内）メモリ`: チャットボットは会話履歴を保持し、チャットセッションでの中断を許可できます。
2. `長期（スレッド間）メモリ`: チャットボットは特定のユーザーに関する情報を*すべてのチャットセッションで*記憶できます。

## メモリの保存と検索の実装例

チャットボットとの対話例を見てみましょう：

```
================================ Human Message =================================

Hi, my name is Lance
================================== Ai Message ==================================

Hello, Lance! It's nice to meet you. How can I assist you today?
================================ Human Message =================================

I like to bike around San Francisco
================================== Ai Message ==================================

That sounds like a great way to explore the city, Lance! San Francisco has some beautiful routes and views. Do you have a favorite trail or area you like to bike in?
```

この会話は、スレッドID "1" を使用して短期メモリに保存されました。

次に、ストアにメモリが保存されたか確認してみましょう。以下のコードで、ユーザーID "1" のメモリを取得します：

```python
# メモリを保存するための名前空間
user_id = "1"
namespace = ("memory", user_id)
existing_memory = across_thread_memory.get(namespace, "user_memory")
```

保存されたメモリの内容は以下の通りです：

```json
{
  'value': {
    'memory': "**Updated User Information:**\n- User's name is Lance.\n- Likes to bike around San Francisco."
  },
  'key': 'user_memory',
  'namespace': ['memory', '1'],
  'created_at': '2024-11-05T00:12:17.383918+00:00',
  'updated_at': '2024-11-05T00:12:25.469528+00:00'
}
```

次に、同じユーザーIDで新しいスレッドを開始してみましょう。チャットボットはユーザーのプロファイルを覚えていて、それを使って応答をパーソナライズするはずです：

```
================================ Human Message =================================

Hi! Where would you recommend that I go biking?
================================== Ai Message ==================================

Hi Lance! Since you enjoy biking around San Francisco, there are some fantastic routes you might love. Here are a few recommendations:

1. **Golden Gate Park**: This is a classic choice with plenty of trails and beautiful scenery. You can explore the park's many attractions, like the Conservatory of Flowers and the Japanese Tea Garden.

2. **The Embarcadero**: A ride along the Embarcadero offers stunning views of the Bay Bridge and the waterfront. It's a great way to experience the city's vibrant atmosphere.

3. **Marin Headlands**: If you're up for a bit of a challenge, biking across the Golden Gate Bridge to the Marin Headlands offers breathtaking views of the city and the Pacific Ocean.

4. **Presidio**: This area has a network of trails with varying difficulty levels, and you can enjoy views of the Golden Gate Bridge and the bay.

5. **Twin Peaks**: For a more challenging ride, head up to Twin Peaks. The climb is worth it for the panoramic views of the city.

Let me know if you want more details on any of these routes!
```

さらに会話を続けると：

```
================================ Human Message =================================

Great, are there any bakeries nearby that I can check out? I like a croissant after biking.
================================== Ai Message ==================================

Absolutely, Lance! Here are a few bakeries in San Francisco where you can enjoy a delicious croissant after your ride:

1. **Tartine Bakery**: Located in the Mission District, Tartine is famous for its pastries, and their croissants are a must-try.

2. **Arsicault Bakery**: This bakery in the Richmond District has been praised for its buttery, flaky croissants. It's a bit of a detour, but worth it!

3. **b. Patisserie**: Situated in Lower Pacific Heights, b. Patisserie offers a variety of pastries, and their croissants are particularly popular.

4. **Le Marais Bakery**: With locations in the Marina and Castro, Le Marais offers a charming French bakery experience with excellent croissants.

5. **Neighbor Bakehouse**: Located in the Dogpatch, this bakery is known for its creative pastries, including some fantastic croissants.

These spots should provide a delightful treat after your biking adventures. Enjoy your ride and your croissant!
```

このように、チャットボットは短期メモリと長期メモリを組み合わせて使用し、ユーザーとの会話を自然に続け、パーソナライズされた応答を提供することができます。 