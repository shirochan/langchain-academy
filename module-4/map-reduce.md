# Map-reduce

## Review
私たちは、このコースのすべてのモジュールを結びつけるマルチエージェント研究アシスタントを構築しています。

このマルチ・エージェント・アシスタントを構築するために、LangGraphの可制御性のトピックをいくつか紹介してきた。

先ほど、並列化と部分グラフについて説明しました。

## Goals

今回は[map reduce](https://langchain-ai.github.io/langgraph/how-tos/map-reduce/)を取り上げる。

[トレース](https://docs.smith.langchain.com/concepts/tracing)には[LnagSmith](https://docs.smith.langchain.com/)を使うことにする。

## Problem

Map-reduceオペレーションは、効率的なタスク分解と並列処理に不可欠である。

Map-Reduceには2つのフェーズがある：

(1) `Map` - タスクを小さなサブタスクに分割し、各サブタスクを並列処理する。

(2) `Reduce` - 完了した並列化された全てのサブタスクの結果を集約する。

次の2つのことを行うシステムを設計しよう：

(1) `Map` - トピックに関するジョークのセットを作成する。

(2) `Reduce` - リストから最適なジョークを選ぶ。

ジョブの生成と選択にはLLMを使う。

## State

### Parallelizing joke generation

グラフのエントリーポイントを定義しよう：

* ユーザーの入力トピックを受け取る
* そこからジョーク・トピックのリストを生成する。
* 各ジョークトピックを上記のジョーク生成ノードに送る。

私たちの状態には `jokes` キーがあり、並列化されたジョーク生成からのジョークを蓄積します。

ジョークの題材を作る。

ここにマジックがある。[送信](https://langchain-ai.github.io/langgraph/concepts/low_level/#send)を使って、各テーマにジョークを作るのだ。

これは非常に便利である！これは非常に便利です！任意の数の被験者に対して、ジョーク生成を自動的に並列化することができます。

* `generate_joke`: グラフのノード名
* `{「subject」: s`}: 送信する状態

`send` は `generate_joke` に任意の状態を渡すことができます。OverallState`に合わせる必要はない。

この場合、 `generate_joke` は自身の内部状態を使用しているので、 `Send` を使って内部状態を設定することができる。

### Joke generation (map)

ここで、ジョークを生成するノード `generate_joke` を定義します！

`OverallState`の`jokes`に書き戻します！

このキーには、リストを結合するリデューサがあります。

### Best joke selection (reduce)

ここで、最高のジョークを選ぶためにロジックを加える。

## Compile

## Studio
--

**⚠️免責事項**

*現在、Studioの実行にはMacが必要です。Macを使用していない場合は、このステップを飛ばしてください。

*また、このノートブックをCoLabで実行している場合は、このステップを飛ばしてください。

--

module-4/studio/langgraph.json`に設定された`module-4/studio/map_reduce.py`を使用しています。

![Screenshot 2024-08-28 at 3.17.53 PM.png](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/66dbb0c0ed88a12e822811e2_map-reduce1.png)