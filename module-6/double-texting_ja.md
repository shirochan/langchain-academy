# ダブルテキスト

[ダブルテキスト](https://langchain-ai.github.io/langgraph/concepts/double_texting/)のシームレスな処理は、特にチャットアプリケーションにおいて、実際の使用シナリオを処理する上で重要です。

ユーザーは、前回の実行が完了する前に複数のメッセージを連続して送信することができ、これを適切に処理することを確保したいと考えています。

## 拒否

シンプルなアプローチとして、現在の実行が完了するまで新しい実行を[拒否](https://langchain-ai.github.io/langgraph/cloud/how-tos/reject_concurrent/)する方法があります。

## エンキュー

現在の実行が完了するまで、新しい実行を[エンキュー](https://langchain-ai.github.io/langgraph/cloud/how-tos/enqueue_concurrent/https://langchain-ai.github.io/langgraph/cloud/how-tos/enqueue_concurrent/)することができます。

## 中断

[中断](https://langchain-ai.github.io/langgraph/cloud/how-tos/interrupt_concurrent/)を使用して、現在の実行を中断し、その時点までに行われたすべての作業を保存することができます。 