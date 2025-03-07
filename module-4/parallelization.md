# Parallel node execution

## Review

モジュール3では、「human-in-the loop 」について詳しく説明し、3つの一般的な使用例を示した：

(1) `Approval` - エージェントを中断し、ユーザに状態を提示し、ユーザにアクションを許可する。

(2) `デバッグ` - グラフを巻き戻して、問題を再現したり回避したりすることができる。

(3) `編集` - 状態を修正することができる。

## Goals

このモジュールでは、「ヒューマン・イン・ザ・ループ（Human-in-the-Loop）」と、モジュール2で説明した「メモリ（Memory）」の概念を基礎とする。

マルチエージェントワークフローに飛び込み、このコースのすべてのモジュールを結びつけるマルチエージェント研究アシスタントを構築します。

このマルチエージェントリサーチアシスタントを構築するために、まずLangGraphの可制御性のトピックをいくつか議論します。

まずは[並列化](https://langchain-ai.github.io/langgraph/how-tos/branching/#how-to-create-branches-for-parallel-node-execution)から。

## Fan out and fan in

各ステップで状態を上書きする単純な線形グラフを作ってみよう。

予想通り、状態を上書きする。

では、`b`と`c`を並行して走らせてみよう。

そして`d`を実行する。

`a` から `b` と `c` にfan-outし、次に `d` にfan-inすれば簡単にできる。

状態の更新は各ステップの最後に適用される。

実行してみよう。

**We see an error**! 
これは、`b`と`c`の両方が同じステップで同じステートキー/チャンネルに書き込んでいるためである。

fan outを使用する場合、同じチャネル/キーに書き込む場合は、リデューサを使用していることを確認する必要があります。

モジュール 2 で触れたように、`operator.add` は Python の組み込み演算子モジュールの関数です。

`operator.add`をリストに適用すると、リストの連結が行われる。

ここで、`b`と`c`が並行して行った更新をステートに追加していることがわかる。

## Waiting for nodes to finish

ここで、平行パスの一方が他方よりステップ数が多い場合を考えてみよう。

この場合、`b`、`b2`、`c`はすべて同じステップの一部である。

グラフはこれら全てが完了するのを待ってから、ステップ `d` に進む。

## Setting the order of state updates

しかし、各ステップにおいて、私たちは状態の更新の順番をコントロールすることはできません！

簡単に言えば、グラフのトポロジーに基づいてLangGraphが決定的に決定する順番であり、**私たちはコントロールできない**のだ。

上の例では、`c`が`b2`の前に追加されている。

しかし、カスタムReducerを使ってこれをカスタマイズすることもできます。

ここで、リデューサは更新された状態の値をソートします！

sorting_reducer` の例では、すべての値をグローバルにソートしています。次のこともできます： 

1. 並列ステップの間に、状態の別のフィールドに出力を書き込む
2. 並列ステップの後に 「sink 」ノードを使用して、これらの出力を結合して並べ替える。
3. 結合後、一時フィールドをクリアする。

詳細は[docs](https://langchain-ai.github.io/langgraph/how-tos/branching/#stable-sorting)を参照。

## Working with LLMs

現実的な例を挙げてみよう！

2つの外部ソース（WikipediaとWeb-Seach）からコンテキストを収集し、LLMに質問に答えさせたい。

いろいろなウェブ検索ツールを試してみてください。[Tavily](https://tavily.com/)は検討すべき素晴らしいオプションの1つですが、`TAVILY_API_KEY`が設定されていることを確認してください。

## Using with LangGraph API

--

**⚠️免責事項**

*現在、Studioの実行にはMacが必要です。Macを使用していない場合は、このステップを飛ばしてください。

*また、このノートブックをCoLabで実行している場合は、このステップを飛ばしてください。

--

module-4/studio/parallelization.py`は`module-4/studio/langgraph.json`に設定されています。

![Screenshot 2024-08-29 at 3.05.13 PM.png](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/66dbb10f43c3d4df239e0278_parallelization-1.png)

StudioからローカルデプロイのURLを取得してみましょう。