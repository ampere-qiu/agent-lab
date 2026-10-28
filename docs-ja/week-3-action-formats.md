# 10 · Pythonコードと構造化ツール呼び出し { #week-3-action-formats }

**目標：**モデルがツールを依頼する2つの方法を理解します。**活動：**2つの検索例を読んで比較し、質問に答えます。その後、`my_tool_calling.py`を作って実行します。構造化呼び出しの記録を、ステップ09の`my_playlist.py`のPythonアクションと比べます。

## 同じ仕事を2つの形式で表す { #two-representations }

**このレッスンの問いは「モデルは、どのツールを動かすかをプログラムにどう伝えるのか」です。** ステップ09のCodeAgentでは、モデルがPythonを書きました。今回はToolCallingAgentも使い、ツール名と入力を構造化データで渡す方法を見ます。

読解の例では、アルフレッドがケータリング業者とパーティーのアイデアを検索します。どちらもツール名は`web_search`で、実際の検索関数が必要です。違うのは、モデルが依頼するアクションの書き方です。

**2つの例を読む → 質問に答えて解説付きの解答を開く → HFの図を読む → プログラムを動かす → 2つの実行記録を比べる**、という順番で進めます。最初の例は2件の検索を表し、後半のプログラムはステップ09と同じ音楽検索を使います。

### 1. Pythonアクション { #python-example }

CodeAgentは、次のようなPythonアクションを受け取れます。**生成されるアクションを読むための例で、そのまま保存・実行する完成プログラムではありません。**

```python
for query in [
    "Best catering services in Gotham City",
    "Party theme ideas for superheroes"
]:
    print(web_search(f"Search for: {query}"))
```

- リストには2つの検索内容が入っています。「ゴッサム・シティのおすすめケータリング業者」と「スーパーヒーロー向けのパーティーテーマ」です。
- `for`ループが、検索内容を1つずつ取り出します。
- `web_search(...)`が検索ツールを呼び出します。
- `print(...)`が返された結果を表示し、エージェントが読める記録に残します。

実行される順番に読んでみましょう。

1. 最初の繰り返しでは、`query`に`Best catering services in Gotham City`が入ります。
2. `f"Search for: {query}"`が、その値を文字列に埋め込み、`Search for: Best catering services in Gotham City`を作ります。先頭の`f`は書式付き文字列を示し、`{query}`が変数の値に置き換わります。
3. Pythonがその文字列で`web_search(...)`を呼びます。結果が返ると、`print(...)`が表示します。内側の関数呼び出しが先で、外側の`print`が後です。
4. 次に`Party theme ideas for superheroes`で同じ処理を繰り返します。これが2件目の検索です。

つまり、**1つのPythonアクションに、2回のツール呼び出しを含められます。** 検索ツールやインターネット接続が不要になるわけではありません。モデルがPythonを提案し、PC上のCodeAgentの実行エンジンが動かし、検索関数が検索サービスに接続します。表示された結果は、モデルに返す観測結果の一部になります。

### 2. 構造化されたツール呼び出し { #structured-example }

ToolCallingAgentは、構造化データでツールを依頼します。JSONは、項目名を付けて値を整理する形式です。同じ2件の検索を、次のように表せます。**読むだけにしてください。JSONファイルを作ったり、Pythonプログラムに貼り付けたりする必要はありません。**

```json
[
  {
    "name": "web_search",
    "arguments": {"query": "Best catering services in Gotham City"}
  },
  {
    "name": "web_search",
    "arguments": {"query": "Party theme ideas for superheroes"}
  }
]
```

最初の項目は、**「`web_search`に『ゴッサム・シティのおすすめケータリング業者』という検索語を渡して呼んで」**という意味です。

| 項目 | 読み方 |
| --- | --- |
| `name` | どのツールを動かすか。この例では`web_search`。 |
| `arguments` | ツールにどんな値を渡すか。 |
| `query` | この検索ツールが受け取る入力の名前。 |
| `"Best catering services in Gotham City"` | 検索語として渡す値。 |
| 2つ目の項目 | 同じツールへの、別の検索語による依頼。 |

このJSONに`for`ループはありません。2つの依頼を明示的に並べています。ToolCallingAgentが名前に対応する登録済みのPythonツールを探し、引数を渡します。検索するのはPythonツールで、JSONそのものが検索サービスに接続することはできません。

このリストは、**ツール名と引数を簡略化して示した例**です。APIの応答全体の形式ではありません。実際のプログラムではモデルとSDKが構造化メッセージを扱うので、このJSONを自分で書く必要はありません。

**PythonコードもJSONも、検索結果そのものではありません。** ツールを実行して初めて結果が返ります。

## 活動：2つの検索例を比べる { #comparison }

上の**例1のPythonの`for`ループ**と、**例2のJSONのリスト**を比べます。この質問では、ケータリングとパーティーテーマの検索例を使います。まず考えてから、**解答を表示**を押して理由をたどってください。

**1. 両方が使うツールと、2つの入力は何ですか？** Pythonの関数名と、JSONの`name`を探しましょう。

??? success "解答を表示"

    **ツールを探す：**Pythonは`web_search(...)`を呼び、JSONは`"web_search"`と指定しています。同じ検索機能を指します。

    **入力を探す：**1つ目はゴッサム・シティのケータリング業者、2つ目はスーパーヒーロー向けのパーティーテーマです。Pythonではリストの2つの文字列から取り出します。JSONでは、それぞれ`arguments`の中の`query`に入っています。

    **少し違う点：**Pythonは書式付き文字列で先頭に`Search for:`を付けます。JSONは検索内容を直接渡しています。探したい2つの内容は同じです。

    **解答例：**「どちらも`web_search`を使います。入力は、ゴッサム・シティのケータリング業者と、スーパーヒーロー向けのパーティーテーマを探す検索語です。」

**2. それぞれ、どこで2回の検索を表していますか？** Pythonではループに渡す値を、JSONでは依頼の項目を数えてみましょう。

??? success "解答を表示"

    **Python：**リストには2つの文字列があります。`for`はそれぞれの値について字下げされた処理を行うので、`web_search(...)`の行が2回実行されます。

    **JSON：**名前と引数を持つ依頼が2件並んでいます。ToolCallingAgentがその依頼を処理します。JSONデータ自身がループを動かすわけではありません。

    **解答例：**「Pythonは1つの命令をループで繰り返し、JSONは2件のツールの依頼を並べています。どちらの例も2回の検索を求めています。」これはこの例の回数で、各エージェントの呼び出し回数がいつも固定という意味ではありません。

**3. アクションを選ぶのは誰で、実行するのは誰ですか？** Groq上のモデルと、PC上のプログラムを分けて考えましょう。

??? success "解答を表示"

    **選ぶ：**Groq上のモデルがタスクと使えるツールの説明を読み、ツールと入力を提案します。CodeAgentではPythonで、ToolCallingAgentでは構造化された呼び出しで表します。

    **実行する：**PC上のCodeAgentの実行エンジンがPythonを動かすか、ToolCallingAgentが指定されたツールに引数を渡して呼び出します。Pythonの検索ツールが検索サービスに接続します。

    **返す：**フレームワークがツールの結果を観測結果として記録し、ループを続けるときにモデルへ返します。

    **解答例：**「モデルが何をするかを提案します。自分のPC上のPythonがツールを動かします。フレームワークがアクションと返された観測結果をつなぎます。」

**4. このコードは検索結果ですか？ まだ何が必要ですか？** 検索する指示と、実際に返されたページや抜粋を区別しましょう。

??? success "解答を表示"

    **どちらにも検索結果は含まれていません。** これから行う操作が書かれています。ケータリングを探す検索語は入力であり、業者が見つかった証拠ではありません。

    **次に必要なこと：**登録されたPythonツールが実行され、結果かエラーを返すことです。その戻り値が観測結果になります。モデルは成功した結果を回答に使ったり、次の操作を選んだりできます。

    **解答例：**「これは結果ではなく依頼です。検索が成功したと言うには、実際に返されたタイトル、URL、抜粋を確認する必要があります。」

## コードとJSONのアクションを図で見る { #comparison-figure }

[![PythonアクションとJSONツール呼び出しの比較](images/huggingface/code_vs_json_actions.png)](images/huggingface/code_vs_json_actions.png)

??? info "この図の説明を読む"

    **課題は、同じスマートフォンを最も安く買える国を探すことです。** 対象は米国、日本、ドイツ、インド。図の上部には、為替・税率、商品価格、送料、最終価格を調べたり計算したりするAPIが示されています。

    **左側はText/JSONによるアクションです。** たとえばドイツの為替・税率を調べ、返された値を受け取ってから、商品価格の取得や換算を依頼します。`Action`が依頼、`Environment`が実行側の返す値、`Response`が最後の回答です。他の国についても同じ処理を行います。

    **右側はコードによるアクションです。** `countries`に対象国を入れ、`for country in countries`で各国の処理を繰り返します。結果を`final_prices`に保存し、`min(..., key=final_prices.get)`で最も安い国を選びます。変数、繰り返し、Pythonの関数で複数の操作をまとめられます。

    図のメッセージは**「コードなら、一連の操作を1つのアクションにまとめられる場合がある」**ということです。ツール自体の実行が不要になるわけではありません。JSONを使うエージェントにも複数段階のループはあります。図の価格や結論は説明用で、現在の価格情報ではありません。

*図の出典：[Hugging Face Agents Course](https://huggingface.co/learn/agents-course/en/unit2/smolagents/tool_calling_agents)。画像を選ぶと拡大できます。*

この図の課題はパーティー検索とは別で、**為替、税、送料を含めて、同じスマートフォンを最も安く買える国を探すこと**です。上部の依頼を読んでから、左右を比べましょう。

- **左 — Text/JSON：**為替を調べるなどの操作を依頼し、その結果を受け取ってから次の操作を依頼します。繰り返す手順の一部は省略されています。
- **右 — Code：**`for`で各国の計算を繰り返し、合計を`final_prices`に保存します。`min(..., key=final_prices.get)`で合計が最小の国を選びます。
- **共通点：**必要なデータを返すツールが要ります。コードなら複数の操作を1つのアクションにまとめられますが、どんな仕事でもモデルへの問い合わせが少なくなるとは限りません。図の価格は説明用で、現在の価格ではありません。

**やってみよう：**繰り返す部分と、最も安い国を選ぶ部分を指してください。右側では、なぜ1つのコードブロックで表せるのでしょうか？

??? success "解答を表示"

    **繰り返しを探す：**`for country in countries`が、米国、日本、ドイツ、インドについて同じ計算を繰り返します。

    **1か国分を追う：**為替と税率を調べ、商品の価格を取得し、通貨換算と税の計算をします。送料を取得して最終価格を求め、その国の名前をキーにして`final_prices`に保存します。

    **比較を探す：**`min(final_prices, key=final_prices.get)`が保存された合計を比べ、最小の国名を返します。続く辞書の参照で、その国の金額を取り出します。

    **解答例：**「コードのアクションでは、ループでツール呼び出しを繰り返し、変数に結果を残せます。同じPythonブロック内で結果の比較までできます。左側は個々の操作を別々の依頼として表しています。どちらも実際にツールを動かす必要があります。」

## ループの流れ { #tool-calling-loop }

**アクションの形式を変えても、ループは必要です。** どちらのプログラムも次の流れで動きます。

1. 利用者がエージェントにタスクを渡す。
2. モデルがアクションを依頼する。
3. プログラムが実行する。
4. 結果またはエラーが観測結果になる。
5. モデルが観測結果を使い、次のアクションを選ぶか、回答して終了する。

## 構造化ツール呼び出しのプログラム { #hf-agent-example }

ここからは、ステップ09の音楽検索を構造化呼び出しで動かします。**タスク、Groq接続、検索ツールは同じ**なので、アクションの形式の違いに注目できます。次のプログラムは、検索ツールを持つToolCallingAgentを作ります。`build_model()`がGroq接続を準備し、`tools=[...]`が検索ツールを登録し、`agent_options(action_format="tool")`が構造化呼び出し用の設定を渡します。

## my_tool_calling.pyを作る { #groq-example }

先に[第03週の準備](week-3-learning-plan.md#exercise-files)を終えてください。同じプロジェクトフォルダー、既存の環境、Groqキーを使います。

1. コードエディターで**`First_agent_template`**を開きます。
2. **ファイル → 新しいテキストファイル → 名前を付けて保存**で、**`my_tool_calling.py`**を`app.py`、`week03_common.py`と同じ場所に保存します。
3. 下の**コード全体**を貼り付けます。
4. Windowsは**Ctrl + S**、Macは**Command + S**で保存します。指定どおりの`.py`ファイル名を使い、`.txt`を付けないでください。

**このファイルの役割 — `my_tool_calling.py`:** my_playlist.pyと同じ音楽検索を、ToolCallingAgentで動かします。Groq上のモデルがツール名と引数で検索を依頼し、Pythonが検索を実行して結果と回答を表示します。ターミナルの記録を使い、構造化呼び出しとCodeAgentのPythonアクションを比べます。

```python title="my_tool_calling.py"
from smolagents import ToolCallingAgent
from week03_common import build_model, agent_options, run_task
from week03_search import WebSearchTool

model = build_model()
agent = ToolCallingAgent(
    tools=[WebSearchTool()],
    model=model,
    **agent_options(action_format="tool"),
)

task = "Search for the best music recommendations for a party at the Wayne's mansion."
raise SystemExit(run_task(agent, task))
```

??? info "my_tool_calling.pyのコード解説を読む"

    `my_playlist.py`と同じGroq接続、検索ツール、パーティーの音楽を探す依頼を使います。

    | コード | 意味 |
    | --- | --- |
    | `from smolagents import ToolCallingAgent` | 構造化されたツールの依頼を扱うエージェントを読み込みます。 |
    | `build_model()`と`WebSearchTool()` | ステップ09と同じモデル接続と検索ツールのインスタンスを準備します。 |
    | `agent = ToolCallingAgent(...)` | モデルの構造化された依頼から、ツール名と引数を読み取るエージェントを作ります。 |
    | `tools=[WebSearchTool()]`と`model=model` | 検索ツールと、準備したGroq接続を渡します。 |
    | `**agent_options(action_format="tool")` | Pythonアクション用の指示ではなく、構造化呼び出し用の設定を渡します。 |
    | `task = "Search ..."` | 同じパーティーに合う音楽のおすすめを依頼します。 |
    | `raise SystemExit(run_task(agent, task))` | ループを実行し、結果を表示して、成功・エラーの状態で終了します。 |

    アクションを選ぶのは引き続きモデルで、検索するPythonツールはPC上で動き、結果は観測結果として戻ります。変わるのは**モデルがアクションを依頼する形式**です。

**実行：**`python my_tool_calling.py`。

Groqキーを求められたら入力してEnterを押します。入力は非表示です。出力は同じターミナルで読みます。ブラウザの画面は開きません。`task`は、ウェイン邸のパーティーに合う音楽を検索する依頼です。

## 出力で確認すること { #execution-log }

構造化呼び出しの実行記録には、たとえば次のように表示されます。

```text
Calling tool: 'web_search' with arguments:
{'query': "best music recommendations for a party at Wayne's mansion"}
```

これは、`web_search`というツールに、表示された`query`を渡すことを示します。ツール名、入力、返された検索結果、最終回答を探してください。引用されたURLが、検索結果にもあるかを確認します。呼び出しを示す表示だけでは、検索が成功した証拠にはなりません。実行が失敗したら、実際のエラーを記録し、[トラブル対処](run-your-first-agent.md#troubleshooting)に沿って確認してから再試行します。検索の失敗を成功した結果として扱わないでください。

## どのファイルを使うのか { #local-setup }

ステップ09の`my_playlist.py`はCodeAgentとPythonアクションを使います。`my_tool_calling.py`はToolCallingAgentと構造化呼び出しを使います。どちらも`First_agent_template`に保存する別々のターミナル用プログラムです。第2週の`app.py`を編集する必要はありません。

**活動：2つの実行を比べる。** `my_tool_calling.py`のターミナル出力を残し、ステップ09の`my_playlist.py`の記録と並べます。前の記録がなければ、`python my_playlist.py`を再実行します。

**それぞれの実行**について、次の4点に当たる実際の出力を短く抜き出してください。

| 探すもの | 抜き出す内容 |
| --- | --- |
| アクション | 生成されたPython、または構造化されたツール名と引数。 |
| 入力 | `query`に渡された検索語。 |
| 観測結果 | 返されたタイトル、URL、抜粋。失敗した場合は実際のエラー。 |
| 最終回答 | 結果を使った1文。成功した結果がなければ、その制約を記録する。 |

そのうえで、**プログラム間で何が変わり、何が同じか**を答えてください。

??? success "解答を表示"

    **まず最初のプログラム：**`my_playlist.py`で、`web_search(...)`を呼ぶなどの、モデルが生成したPythonを探します。CodeAgentがそのPythonを実行します。変数名や検索語は読解の例と違うことがあります。

    **次のプログラムのアクション：**`my_tool_calling.py`では、`Calling tool: 'web_search'`と`query`の引数を探します。これは構造化されたツールの依頼を示します。ToolCallingAgentが同じPythonの検索実装を呼びます。

    **実際に起きたことを確認：**どちらの記録でも、呼び出し後に返されたデータを探します。最終回答のURLと、検索ツールが実際に返したURLを照合します。上に示した2行の出力例は依頼だけです。返された検索結果や最終回答はないので、それだけでは検索の成功を判断できません。

    **比較の解答例：**「音楽検索のCodeAgentでは、モデルがPythonを書いて検索を依頼しました。ToolCallingAgentでは、ツール名と引数を渡しました。どちらもGroqのモデルがアクションを選び、PC上の同じPython検索ツールが実行しました。結果が観測結果になり、回答に使われます。」

    この比較に、**自分の実行で使われた検索語と、実際に返された情報源**を加えます。失敗した実行はエラーと不足している証拠を記録し、成功した結果を作り上げないでください。検索結果や表現は実行ごとに変わります。比べる中心は、アクションの形式と実行の流れです。

## 確認ポイント { #activity }

**ToolCallingAgentはPythonツールの代わりになりますか？ なぜフレームワークが必要なのでしょうか？** 自分の言葉で答えてください。

??? success "解答を表示"

    「ToolCallingAgentは、モデルがアクションを依頼する形式を変えます。実際の仕事には、登録されたPythonツールが引き続き必要です。モデルがツールと入力を選び、フレームワークが呼び出して結果やエラーを記録し、観測結果を次の処理に使います。CodeAgentも同じようなループを管理しますが、Pythonアクションを受け取ります。」

    自分の記録で**依頼、実行結果、それを使った回答**を指し示し、Groq上とPC上の役割を説明できれば、この確認ポイントを達成しています。

## 出典 { #sources }

[Hugging Face Agents Course — Writing actions as code snippets or JSON blobs](https://huggingface.co/learn/agents-course/en/unit2/smolagents/tool_calling_agents)を基に構成しています。[Apache 2.0ライセンス](licenses/huggingface-agents-course.txt)に基づき利用しています。

**次へ：**[11 · 関数とクラスで作るツール](week-3-custom-tool.md)。
