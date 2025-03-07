# Sub-graphs

## Review

我々は、このコースのすべてのモジュールを結びつけるマルチエージェント研究アシスタントを構築している。

LangGraphの可制御性の重要なトピックの1つである並列化について説明した。

## Goals

[部分グラフをカバーする](https://langchain-ai.github.io/langgraph/how-tos/subgraph/#simple-example)。

## State

サブグラフ(sub-graph)によって、グラフの異なる部分に異なる状態を作成し、管理することができます。

これは、マルチエージェントシステムで、各エージェントがそれぞれの状態を持つような場合に特に便利です。

おもちゃの例を見てみよう：

* ログを受け取るシステムがある。
* ログを受け取るシステムがある。
* この2つのオペレーションを2つの異なるサブグラフで実行したい。

最も重要なことは、グラフがどのように通信を行うかということだ！

要するに、通信は**オーバーラップするキー**で行われる： 

* サブグラフは親から`docs`にアクセスできる。
* 親はサブグラフから`summary/failure_report`にアクセスできる。

！[subgraph.png](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/66dbb1abf89f2d847ee6f1ff_sub-graph1.png)

## Input

グラフに入力するログのスキーマを定義しよう。

[トレース](https://docs.smith.langchain.com/concepts/tracing)には[LnagSmith](https://docs.smith.langchain.com/)を使うことにする。

## Sub graphs

以下は、`FailureAnalysisState`を使った故障解析のサブグラフである。

ここでは `QuestionSummarizationState` を使用する質問要約サブグラフを示します。

## Adding sub graphs to our parent graph

さて、これですべてをまとめることができる。

`EntryGraphState`で親グラフを作成する。

そしてサブグラフをノードとして追加する！

```
entry_builder.add_node(「question_summarization」, qs_builder.compile())
entry_builder.add_node(「failure_analysis」, fa_builder.compile())
```

しかし、`cleaned_logs` は各サブグラフに入力として *入る* だけなのに、なぜリデューサーがあるのでしょうか? 変更されません。

```
cleaned_logs: Annotated[List[Log], add] # これは両方のサブグラフで USED BY になります
```

これは、サブグラフの出力状態に、変更されていない場合でも **すべてのキー** が含まれるためです。

サブグラフは並列で実行されます。

並列サブグラフは同じキーを返すため、各サブグラフからの入力値を結合するには、`operator.add` のようなリデューサーが必要です。

ただし、前に説明した別の概念を使用することで、これを回避できます。

各サブグラフの出力状態スキーマを作成し、出力として公開する異なるキーが出力状態スキーマに含まれるようにするだけです。

実際には、各サブグラフが `cleaned_logs` を出力する必要はありません。

## LangSmith

Let's look at the LangSmith trace:

https://smith.langchain.com/public/f8f86f61-1b30-48cf-b055-3734dfceadf2/r