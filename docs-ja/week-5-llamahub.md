# 19 · 連携パッケージを探して使う { #week-5-llamahub }

**目標：**モデル、埋め込み、保存先をつなぐパッケージの役割を理解します。[準備](week-5-learning-plan.md#environment)で有効にしたターミナルを使ってください。

[![分類と連携パッケージが並ぶHFのLlamaHubカタログ](images/huggingface-week05/llama-hub.png)](images/huggingface-week05/llama-hub.png){ .course-figure-link }

??? info "この図の説明を読む"

    LlamaHubは、用意されている連携機能のカタログです。分類からモデル接続、文書の読み込み、データベース、ツールなどを探せます。全部をインストールする必要はありません。今週はGroqでモデルに接続し、Hugging Faceの埋め込みをPCで計算し、Chromaで検索用の情報を保存します。下の表で、パッケージ名とPythonでの読み込み方を対応させましょう。

*HFの図を変更せず使用しています。[原典のレッスン](https://huggingface.co/learn/agents-course/en/unit2/llama-index/llama-hub) · [図を拡大する](images/huggingface-week05/llama-hub.png)。*

## 1. LlamaHubで用意されているもの { #integrations }

[LlamaHub](https://llamahub.ai/)では、行いたい仕事に合わせて連携機能を探せます。パッケージをインストールするとコードがPCに入り、Pythonの`import`でプログラムから使えるようになります。パッケージ名と`import`の名前は似ていますが、完全には同じではありません。

| 役割 | requirements内のパッケージ | 今週使うimport先 |
| --- | --- | --- |
| 基本の部品とツール | `llama-index-core` | `llama_index.core` |
| 授業用のGroq接続 | `llama-index-llms-groq` | `llama_index.llms.groq` |
| PCで動くHugging Face埋め込み | `llama-index-embeddings-huggingface` | `llama_index.embeddings.huggingface` |
| Chromaへのベクトル保存 | `llama-index-vector-stores-chroma` | `llama_index.vector_stores.chroma` |
| ワークフローの作図 | `llama-index-utils-workflow` | `llama_index.utils.workflow` |

これらは準備でまとめてインストール済みです。第4週の環境へ追加する必要はありません。動作には入力も必要です。GroqにはキーとモデルID、埋め込みにはモデルファイル、保存にはローカルのフォルダーを使います。

## 2. モデルへの問い合わせを1回試す { #connection-test }

**`week05-exercises`に`my_llm.py`を作成します。**設定を読み、下のあいさつをGroqへ送り、応答をターミナルに表示するプログラムです。LLMとGroqのトークンを使います。人物像のファイルは読み込まず、検索もしません。

```python title="my_llm.py"
from week05_common import get_llm, run

async def main():
    llm = get_llm()
    response = await llm.acomplete("Hello, how are you?")
    print(response.text)

if __name__ == "__main__":
    run(main)
```

??? info "コードの説明を読む"

    `get_llm()`が`.env`を読み、設定したGroq接続を返します。`acomplete`は非同期の文章生成メソッドで、`await`が応答を待ちます。配布ヘルパーの`run(main)`が`asyncio.run(main())`を呼ぶため、通常のターミナルから実行できます。末尾のmainガードにより、ほかのファイルから読み込んだだけでは問い合わせが発生しません。

**保存して実行：**`python my_llm.py`。

短いあいさつが返れば接続を確認できます。文面は毎回同じとは限りません。失敗したら、`.env`、有効な環境、通信、モデルの利用権限を確認します。APIキーは表示しないでください。ヘルパーは失敗した実行を未完了として表示します。エラーの種類を`evidence.md`の19の欄へ記録してください。

**確認：**このプログラムは人物像のファイルを使いましたか？実際にモデルへの問い合わせを行った行はどこですか？

??? success "答え"

    人物像のファイルは読みません。問い合わせは`await llm.acomplete(...)`で行います。接続用のオブジェクトを作るだけでは、文章生成は実行されません。

*原典・演習の出典：[HF Unit 2.2 — llama-hub](https://huggingface.co/learn/agents-course/en/unit2/llama-index/llama-hub)。Apache-2.0。`NOTICE.md`と`HF-LICENSE.txt`を参照してください。*

## ここで確認 { #checkpoint }

| 残しておく新しいファイル | 確認する結果 |
| --- | --- |
| `my_llm.py` | エラーが出ず、短いあいさつが表示される。 |

次の演習でもこのファイルを残します。失敗した場合は、モデルを使う演習へ進む前に[準備のトラブル対処](week-5-learning-plan.md#troubleshooting)を使ってください。成功したあいさつ、または実際の失敗をメモの19の欄に残します。

**次へ：**[20 · コンポーネントとRAG](week-5-components.md)。
