# 21 · 部品をツールとして公開する { #week-5-tools }

**目標：**作成済みの関数やクエリエンジンに、分かりやすいツール用の窓口を付けます。先に[コンポーネントの演習](week-5-components.md#query)を終えてください。

[![HFの4種類のツール：FunctionTool、クエリエンジン、ToolSpec、補助ツール](images/huggingface-week05/tools.png)](images/huggingface-week05/tools.png){ .course-figure-link }

??? info "この図の説明を読む"

    各カードは、機能をエージェントから使える形にする方法です。`FunctionTool`はPython関数、`QueryEngineTool`は文書の検索と回答、`ToolSpec`は関連ツールの集まりを扱います。補助ツールは、大きな結果の読み込みや検索を助けます。図の2枚目は「Search Engine」という表記ですが、この演習のコードは`QueryEngineTool`を使います。まず天気と人物像のツールを自分で直接呼び、後の演習で選択をエージェントに任せます。ツールを作っただけでは、エージェントは増えません。

*HFの図を変更せず使用しています。[原典のレッスン](https://huggingface.co/learn/agents-course/en/unit2/llama-index/tools) · [図を拡大する](images/huggingface-week05/tools.png)。*

## 1. FunctionTool：Python関数を公開する { #function-tool }

**`my_tools.py`を作成します。**HFの天気の例を使い、固定の「晴れ」という文字列、ツール名、説明、入力の形式を表示します。**練習用のデータで、実際の天気予報ではありません。**LLMやGroqのトークンは使いません。エージェントに渡す前に、ターミナルの出力を読みましょう。

```python title="my_tools.py"
from llama_index.core.tools import FunctionTool


def get_weather(location: str) -> str:
    """Return a fixed classroom weather example, not live weather."""
    print(f"Getting demo weather for {location}")
    return f"The weather in {location} is sunny (demo data)"


weather = FunctionTool.from_defaults(
    get_weather, name="my_weather_tool",
    description="Return fixed demo weather for a location. Not a live forecast.",
)

if __name__ == "__main__":
    print(weather.call("New York"))
    print("NAME:", weather.metadata.name)
    print("DESCRIPTION:", weather.metadata.description)
    print("INPUT SCHEMA:", weather.metadata.fn_schema.model_json_schema())
```

??? info "関数ツールの説明を読む"

    `FunctionTool.from_defaults`が関数をツールとして包みます。型注釈が入力を示し、名前と説明がモデルに用途を伝えます。`weather.call`は関数を直接実行します。mainガードがあるので、後で`get_weather`を読み込んでも確認用の呼び出しは実行されません。ツール自体はエージェントなしでも使えます。

**実行：**`python my_tools.py`。

New Yorkの練習用メッセージ、ツール名、`location`という文字列入力のスキーマを確認します。同じファイルのmainガード内にある次の1行だけを探します。

```text
    print(weather.call("New York"))
```

この行へ置き換えます。

```text
    print(weather.call("Tokyo"))
```

先頭の空白4個を残し、保存して`python my_tools.py`を再実行してください。なぜTokyoでも晴れなのでしょうか？結果を記録したらNew Yorkの行へ戻し、保存します。`get_weather`とツールの定義はそのままにします。

??? success "答え"

    関数が常に同じ形式の文章を返すためです。天気サービスには接続していません。自然な文が表示されても、実際に調べた証拠にはなりません。

## 2. QueryEngineTool：文書検索を公開する { #query-tool }

**`my_query_tool.py`を作成します。**人物像のクエリエンジンに名前を付けたツールを作り、直接呼んで結果を表示します。保存済みのインデックスと下の質問を使い、Groqが回答を作ります。まだエージェントはツールを選びません。

```python title="my_query_tool.py"
from week05_common import get_llm, run
from week05_rag import persona_tool

async def main():
    tool = persona_tool(get_llm())
    print("TOOL:", tool.metadata.name, tool.metadata.description)
    result = await tool.acall("Describe the persona interested in Cincinnati art. Do not invent a real name.")
    print("RETURN:", result)

if __name__ == "__main__":
    run(main)
```

??? info "検索ツールの説明を読む"

    `week05_rag.py`の`persona_tool`を開いてください。クエリエンジン、名前`personas`、用途の説明、`return_direct=False`を指定した`QueryEngineTool`を作っています。説明にはデータと検索範囲の限界も含まれます。クエリエンジンは最大2つの断片を使い、`acall`が非同期で呼び出します。配布ヘルパーは元の出典を**SOURCE**と**EXCERPT**として付け、モデルが書いた**GENERATED ANSWER**とは分けて返します。元の文章と要約の違いを確認できます。後でエージェントに渡すと、最終回答を作るために別のモデル問い合わせが発生することがあります。

**実行：**`python my_query_tool.py`。`my_query.py`の結果と比べてください。`SOURCE: persona_0.txt`を探し、**EXCERPT**を`data`内の同じファイルと照合します。**GENERATED ANSWER**は生成文なので、元の文章として引用しません。抜粋が省略されていたら元のファイルを開きます。直接呼び出したことは、エージェントが選んだ証拠にはなりません。

## 3. ToolSpec：関連するツールをまとめる { #tool-spec }

HFではコミュニティの`GmailToolSpec`を紹介しています。Gmail接続には別の設定とアカウント権限が必要です。ここでは同じ「ツールをまとめる仕組み」を、ローカルの天気・計算で学びます。メールアカウントへは接続しません。

**`my_toolspec.py`を作成します。**2つのPython関数をツールのリストにまとめ、名前と説明を表示してから両方を直接呼びます。LLM、通信、Groqのトークンは使いません。

```python title="my_toolspec.py"
from llama_index.core.tools.tool_spec.base import BaseToolSpec
from my_tools import get_weather

class ClassroomToolSpec(BaseToolSpec):
    spec_functions = ["weather", "multiply"]

    def weather(self, location: str) -> str:
        """Return fixed classroom weather, not a live forecast."""
        return get_weather(location)

    def multiply(self, a: int, b: int) -> int:
        """Multiply two integers."""
        return a * b

tools = ClassroomToolSpec().to_tool_list()
for tool in tools:
    print(tool.metadata.name, "=>", tool.metadata.description)
print(tools[0].call("New York"))
print(tools[1].call(a=2, b=2))
```

??? info "ツールの集まりの説明を読む"

    `spec_functions`に公開するメソッド名を指定し、`to_tool_list()`で個々のツールを作ります。`ToolSpec`は機能の集まりです。エージェントへ渡す前にリストを確認できます。各メソッドのdocstringが用途の説明になります。

**実行：**`python my_toolspec.py`。2つのツールの説明、練習用の天気、`4`を確認します。ツールを追加してもエージェントが増えない理由を記録してください。

### MCPのツール { #mcp }

HFは次にMCPの`ToolSpec`を紹介します。**MCP**は別のサーバーのツールを公開するための通信規約です。クライアントのインストールだけではサーバーは作られず、接続先のサーバーが動いている必要があります。返されるものは呼び出せるツールのリストです。今週は読み物として扱い、外部サーバーや個人アカウントの接続は必須にしません。GmailとMCPの例は[HFのツールのレッスン](https://huggingface.co/learn/agents-course/en/unit2/llama-index/tools)を参照してください。

## 4. 補助ツール：大きな結果から必要な部分を取り出す { #utility-tools }

ツールが、必要以上に長い結果を返すことがあります。HFは次の2つの方法を紹介しています。

| 方法 | 行うこと |
| --- | --- |
| 必要なときに読み込むローダー | 呼び出されたときにデータを読み込み、インデックスを作り、質問へ答える。 |
| 読み込み用と検索用のツールの組 | 1つのツールで大きな結果を保存・索引化し、もう1つで必要な情報を検索する。 |

大きな結果の全文を繰り返し渡さず、必要な部分を扱いやすくなります。一方、埋め込み、保存、モデル呼び出しが増える場合があります。取り出した情報の正しさは別に確認します。人物像の小さな検索ツールでも、元の抜粋があると根拠を確かめやすいことが分かります。

**確認：**サービスが長い記録を100件返し、質問はそのうち1件についてです。読み込み用と検索用を分けると何が変わり、何を確認する必要がありますか？

??? success "答え"

    大きな結果を索引化し、必要な部分を検索できるようになります。選ばれた記録が回答を支えるか、大事な情報が落ちていないか、どのモデル呼び出しや保存処理を使ったかは確認が必要です。

**確認メモ：**`evidence.md`の21の欄で、関数の直接呼び出し、検索ツールの直接呼び出し、ツールの集まりを区別してください。これだけではエージェントによる選択はまだ示していません。

*原典・演習の出典：[HF Unit 2.2 — tools](https://huggingface.co/learn/agents-course/en/unit2/llama-index/tools)。Apache-2.0。`NOTICE.md`と`HF-LICENSE.txt`を参照してください。*

## ここで確認 { #checkpoint }

| 残しておく新しいファイル | 確認する結果 |
| --- | --- |
| `my_tools.py` | 練習用の天気、名前・説明、`location`の入力形式。比較後はNew Yorkへ戻す。 |
| `my_query_tool.py` | 元のSOURCE／EXCERPTと、生成されたGENERATED ANSWERが分かれている。 |
| `my_toolspec.py` | 2つのツールの説明と、直接呼び出した結果。 |

前のコンポーネントのファイルと、今回の3つを残してください。配布ヘルパーを編集する必要はありません。ツールの集まりがエージェントではない理由をメモの21の欄に書きます。

**次へ：**[小テスト1](week-5-quiz-1.md)。
