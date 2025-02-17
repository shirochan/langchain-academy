# Agent

## Review

ルーターを構築しました。

* チャットモデルはユーザー入力に基づいてツール呼び出しを行うかどうかを判断します
* 条件付きエッジを使用して、ツールを呼び出すノードまたは終了するノードにルーティングします

## Goals

これを汎用的なエージェントアーキテクチャに拡張できます。

上記のルーターでは、モデルを呼び出し、ツールを呼び出すことを選択した場合、ユーザーに`ToolMessage`を返しました。

しかし、その`ToolMessage`をモデルに戻すとどうなるでしょうか？

モデルに(1)別のツールを呼び出すか、(2)直接応答するかを選択させることができます。

これが[ReAct](https://react-lm.github.io/)の背後にある考え方であり、汎用的なエージェントアーキテクチャです。

* `act` - モデルに特定のツールを呼び出させる
* `observe` - ツールの出力をモデルに戻す
* `reason` - モデルにツールの出力について推論させ、次に何をするか決定させる(例:別のツールを呼び出すか、直接応答するか)

この[汎用的なアーキテクチャ](https://blog.langchain.dev/planning-for-agents/)は、多くのタイプのツールに適用できます。

システムメッセージとノードをLLMとプロンプトで設定し、全体的な望ましいエージェントの振る舞いを指定します。


以前と同様に、`MessagesState`を使用し、ツールのリストを持つ`Tools`ノードを定義します。

`Assistant`ノードは、ツールをバインドしたモデルです。

`Assistant`と`Tools`ノードを持つグラフを作成します。

`tools_condition`エッジを追加し、`Assistant`がツールを呼び出すかどうかに基づいて`End`または`Tools`にルーティングします。

ここで新しいステップを1つ追加します:

`Tools`ノードを`Assistant`に戻して接続し、ループを形成します。

* `assistant`ノードが実行された後、`tools_condition`はモデルの出力がツール呼び出しかどうかをチェックします
* ツール呼び出しの場合、フローは`tools`ノードに向かいます
* `tools`ノードは`assistant`に戻ります
* このループは、モデルがツールを呼び出すことを決定する限り続きます
* モデルの応答がツール呼び出しでない場合、フローはENDに向かい、プロセスが終了します

## LangSmith

ここで、LangSmithを[トレース](https://docs.smith.langchain.com/concepts/tracing)のために使用します。

プロジェクト`langchain-academy`にログを記録します。

LangSmithでトレースを確認できます。
