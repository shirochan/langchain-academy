# Multiple Schemas

## Review 

LangGraph の state schemaとreducersについて説明しました。

通常、すべてのグラフノードは単一のスキーマとやり取りします。

また、この単一のスキーマには、グラフの入力と出力のキー/チャネルが含まれます。

## Goals

しかし、これについてより詳細な制御が必要なケースがあります：

* 内部ノードは、グラフの入力/出力で*不要な*情報を渡すことがあります。

* グラフに異なる入力/出力スキーマを使用することもできます。例えば、出力には、関連する出力キーが 1 つだけ含まれる場合があります。

複数のスキーマを使用してグラフをカスタマイズする方法をいくつか説明します。

## Private State

まず、ノード間の[プライベート状態](https://langchain-ai.github.io/langgraph/how-tos/pass_private_state/)を渡すケースについて説明します。

これは、グラフの中間的な実行ロジックの一部として必要な場合に役立つが、グラフ全体の入力や出力全体には関係ありません。

`OverallState`と`PrivateState`を定義してみましょう。

`node_2`は入力として`PrivateState`を使用しますが、`OverallState`に書き込みます。

[コードブロックは原文のまま]

`baz`は`PrivateState`にのみ含まれます。

`node_2`は入力として`PrivateState`を使用しますが、`OverallState`に書き込みます。

したがって、`baz`は`OverallState`に含まれていないため、グラフの出力から除外されることがわかります。

## Input / Output Schema

デフォルトでは、`StateGraph`は単一のスキーマを受け取り、すべてのノードはそのスキーマと通信することが期待されます。

しかし、[グラフに明示的な入力および出力スキーマを定義する](https://langchain-ai.github.io/langgraph/how-tos/input_output_schema/?h=input+outp)ことも可能です。

このような場合、多くのケースで、グラフの操作に関連する*すべての*キーを含む「内部」スキーマを定義します。

しかし、特定の`input`および`output`スキーマを使用して入力と出力を制限します。

まず、単一のスキーマでグラフを実行してみましょう。

[コードブロックは原文のまま]

`OverallState`のすべてのキーが呼び出しの出力に含まれていることに注意してください。

では、グラフで特定の`input`および`output`スキーマを使用してみましょう。

ここで、`input`/`output`スキーマはグラフの入力および出力で許可されるキーに*フィルタリング*を実行します。

また、型ヒント `state: InputState` を使用して、各ノードの入力スキーマを指定できます。

これは、グラフが複数のスキーマを使用している場合に重要です。

たとえば、以下の型ヒントを使用して、`answer_node` の出力が `OutputState` にフィルタリングされることを示します。

[コードブロックは原文のまま]

`output`スキーマが出力を`answer`キーのみに制限していることがわかります。
