# 09 · CodeAgentを動かす { #week-3-code-agent }

**目標：**CodeAgentが質問を受け、モデルが提案したPythonを実行し、その結果を使う流れを見ます。音楽検索、メニュー選択、準備時間の計算という3つの小さなプログラムを作ります。

**始める前に：**[第03週の準備](week-3-learning-plan.md#exercise-files)を終えてください。プロジェクト内に`.venv`、`app.py`、`week03_common.py`、`week03_search.py`、`week03_tools.py`が必要です。

新しいファイルはすべて、**`First_agent_template`内の`app.py`と同じ場所**に保存します。Pythonは**コードエディター**に書き、保存したファイルをターミナルで実行します。

[![パーティーを計画するアルフレッド](images/huggingface/alfred-party.jpg)](images/huggingface/alfred-party.jpg)

??? info "この画像の説明を読む"

    パーティーの準備をするアルフレッドのイラストです。このレッスンでは、音楽を探す、メニューを決める、準備時間を計算するという仕事をプログラムに依頼します。この画像は題材を紹介するもので、実行結果や操作画面ではありません。

*画像の出典：[Hugging Face Agents Course](https://huggingface.co/learn/agents-course/en/unit2/smolagents/code_agents)。画像を選ぶと拡大できます。*

## エージェントの動く流れ { #actions }

CodeAgentは、Pythonの変数、繰り返し、計算、登録されたツールを使えます。基本の流れは次のとおりです。

1. タスクと、使えるツールの説明をGroq上のモデルに送る。
2. モデルが提案したPythonアクションを受け取る。
3. そのPythonを自分のPCで実行する。
4. 返された値やエラーを記録する。これが**観測結果（observation）**。
5. 観測結果をモデルに送り、次のアクションを選ぶか、回答して終了する。

[![CodeAgentの実行ループ](images/huggingface/codeagent_docs.png)](images/huggingface/codeagent_docs.png)

??? info "この図の説明を読む"

    **`CodeAgent.run()`の内部で何が起こるか**を表した図です。左側の3つの要素は、実行記録の`logs`、モデル接続の`model`、使えるツールの`tools`です。

    右側を上からたどります。まず依頼を`TaskStep`として記録します。記録からモデルに送るメッセージを作り、モデルが返した文章からコードを取り出します。コードを実行すると、必要なツールが呼ばれます。返された値やエラーを`ActionStep`に記録し、次の問い合わせに使います。

    モデルが`final_answer(...)`を呼ぶコードを出し、それが実行されると、`run()`が最終結果を返します。今週の設定にはステップ数の上限もあるため、成功するまで無限に続くわけではありません。図の`images`や`observation_images`は画像も扱える仕組みを示していますが、今週の実習はテキスト中心です。

    **役割を分けて読むことが大切です。** モデルが次のコードを提案し、PC上の実行エンジンが動かし、CodeAgentが記録と次の問い合わせを管理します。

*図の出典：[Hugging Face Agents Course](https://huggingface.co/learn/agents-course/en/unit2/smolagents/code_agents)。画像を選ぶと拡大できます。*

## A. 音楽検索のプログラムを作る { #run-and-inspect }

**目標：**モデルにウェブ検索ツールを使わせ、音楽の候補を探します。

[![プレイリストを選ぶアルフレッド](images/huggingface/alfred-playlist.jpg)](images/huggingface/alfred-playlist.jpg)

??? info "この画像の説明を読む"

    アルフレッドがパーティーの音楽を選ぶ場面です。これから作るプログラムも、ウェイン邸のパーティーに合う音楽を検索します。画像の内容をモデルに読み取らせる実習ではなく、文章の依頼と検索ツールを使う実習です。

*画像の出典：[Hugging Face Agents Course](https://huggingface.co/learn/agents-course/en/unit2/smolagents/code_agents)。画像を選ぶと拡大できます。*

1. コードエディターで**`First_agent_template`**を開きます。
2. **ファイル → 新しいテキストファイル**を選び、**名前を付けて保存**で**`my_playlist.py`**として保存します。場所は`app.py`、`week03_common.py`と同じです。
3. 下の**コード全体**をそのファイルに貼り付けます。
4. Windowsは**Ctrl + S**、Macは**Command + S**で保存します。拡張子は`.py`です。`.py.txt`にしないでください。

```python title="my_playlist.py"
from smolagents import CodeAgent
from week03_common import build_model, agent_options, run_task
from week03_search import WebSearchTool


model = build_model()
agent = CodeAgent(
    tools=[WebSearchTool()],
    model=model,
    **agent_options(),
)

task = "Search for the best music recommendations for a party at the Wayne's mansion."
raise SystemExit(run_task(agent, task))
```

??? info "my_playlist.pyのコード解説を読む"

    **検索ツールを持つエージェントを作り、依頼を渡すファイルです。** 上から順に見ていきます。

    | コード | 意味 |
    | --- | --- |
    | `from smolagents import CodeAgent` | モデルへの問い合わせ、Pythonアクション、観測結果をつなぐクラスを読み込みます。 |
    | `from week03_common import ...` | Groq接続、授業用の設定、タスクの実行・表示を行う3つの補助関数を読み込みます。 |
    | `from week03_search import WebSearchTool` | 配布された検索ツールのクラスを読み込みます。 |
    | `model = build_model()` | Groqへの接続を準備します。必要ならキーを尋ねます。まだタスクは実行しません。 |
    | `agent = CodeAgent(...)` | PC上にエージェントを作ります。 |
    | `tools=[WebSearchTool()]` | 検索ツールのインスタンスを作り、このエージェントに登録します。この括弧はツールを作るためのもので、ここで検索するわけではありません。 |
    | `model=model` | 上で準備したGroq接続をエージェントに渡します。 |
    | `**agent_options()` | Pythonアクション用の指示、4ステップの上限、ターミナルへの記録などを渡します。`**`は辞書の内容を名前付き引数として展開する書き方です。 |
    | `task = "Search ..."` | 「ウェイン邸のパーティーに合う音楽のおすすめを検索して」という依頼を文字列として保存します。この行だけではモデルへの問い合わせも検索も始まりません。 |
    | `raise SystemExit(run_task(agent, task))` | タスクを実行して結果を表示します。補助関数が成功・エラーの状態を返し、`SystemExit`がその状態でプログラムを終了します。 |

    **実行すると：**Groqのモデルが依頼を読み、`web_search(...)`などの呼び出しを提案します。CodeAgentがPC上で実行し、検索ツールが検索サービスに接続します。返された抜粋が観測結果になり、モデルが回答に使います。複数のステップに進む場合もあります。

    **役割分担：**アクションの選択と回答文の作成はGroq上のモデル、検索結果の取得はローカルのPythonツール、ループの管理はCodeAgentです。

**実行：**`python my_playlist.py`。キーを求められたらGroqキーを入力します。

出力はターミナルで読みます。

**確認すること：**`web_search(query=...)`の呼び出し、返されたタイトル・URL・抜粋、最終回答を探します。生成されたアクションは、たとえば次のようになります。**これはターミナル出力の例です。別のファイルを作ったり、自分のプログラムに貼り付けたりしないでください。**

```python
results = web_search(query="best music for a Batman party")
print(results)
```

検索語や回答の表現は変わることがあります。引用されたURLが、実際の検索結果にもあるかを確認してください。検索が失敗する、または結果がない場合は教員に相談するか、[トラブル対処](run-your-first-agent.md#troubleshooting)を確認します。モデルの記憶だけで出した回答は、検索した証拠にはなりません。

## B. メニューを選ぶプログラムを作る { #menu }

**目標：**配布されたPython関数に渡す入力を、エージェントが選ぶ様子を見ます。

[![メニューを準備するアルフレッド](images/huggingface/alfred-menu.jpg)](images/huggingface/alfred-menu.jpg)

??? info "この画像の説明を読む"

    アルフレッドがパーティーのメニューを考える場面です。ここでは、モデルが依頼から`formal`などの種類を選び、Python関数が対応するメニュー文を返します。画像から料理を認識したり、実際のレストランを探したりする課題ではありません。

*画像の出典：[Hugging Face Agents Course](https://huggingface.co/learn/agents-course/en/unit2/smolagents/code_agents)。画像を選ぶと拡大できます。*

まず、エディターで**既存の`week03_tools.py`**を開き、`suggest_menu`を探します。関数は配布済みです。次のコードは読むためのもので、定義は元のファイルに残します。

```python
@tool
def suggest_menu(occasion: str) -> str:
    """
    Suggests a menu based on the occasion.
    Args:
        occasion (str): The type of occasion for the party. Allowed values are:
                        - "casual": Menu for casual party.
                        - "formal": Menu for formal party.
                        - "superhero": Menu for superhero party.
                        - "custom": Custom menu.
    """
    if occasion == "casual":
        return "Pizza, snacks, and drinks."
    elif occasion == "formal":
        return "3-course dinner with wine and dessert."
    elif occasion == "superhero":
        return "Buffet with high-energy and healthy food."
    else:
        return "Custom menu for the butler."
```

関数は、用意された4つのメニュー文のどれかを返します。`occasion`を選ぶのはモデルで、対応する文字列を返すのはPythonです。メニューは説明用の架空の例で、最新のレストラン情報ではありません。たとえば`formal`には「ワインとデザート付きの3コースディナー」が対応します。

この関数を使う別のプログラムを作ります。

1. コードエディターで**`First_agent_template`**を開きます。
2. **ファイル → 新しいテキストファイル → 名前を付けて保存**で、**`my_menu.py`**を`app.py`、`week03_common.py`と同じ場所に保存します。
3. 下の**コード全体**を貼り付けます。
4. Windowsは**Ctrl + S**、Macは**Command + S**で保存します。拡張子は`.py`にします。

```python title="my_menu.py"
from smolagents import CodeAgent
from week03_common import build_model, agent_options, run_task
from week03_tools import suggest_menu


model = build_model()
agent = CodeAgent(
    tools=[suggest_menu],
    model=model,
    **agent_options(),
)

task = 'Prepare a formal menu for the party.'
raise SystemExit(run_task(agent, task))
```

??? info "my_menu.pyのコード解説を読む"

    **検索ツールの代わりに、メニューを選ぶ関数を使うファイルです。**

    | コード | 意味 |
    | --- | --- |
    | `from smolagents import CodeAgent` | エージェントのループを管理するクラスを読み込みます。 |
    | `from week03_common import ...` | Groq接続、授業用設定、タスク実行の補助関数を読み込みます。 |
    | `from week03_tools import suggest_menu` | 上で読んだ関数を既存のファイルから読み込みます。このファイルで再定義する必要はありません。 |
    | `model = build_model()` | 自分のキーを使うGroq接続を準備します。 |
    | `agent = CodeAgent(...)` | モデルとツールを持つローカルのエージェントを作ります。 |
    | `tools=[suggest_menu]` | 関数を名前で登録します。括弧がないのは、今呼び出すのではなく、後で使えるようにするためです。 |
    | `model=model` | 使うモデル接続を渡します。 |
    | `**agent_options()` | Pythonアクション用の指示、ステップ上限、表示設定を渡します。 |
    | `task = 'Prepare a formal menu for the party.'` | 「パーティーのフォーマルなメニューを用意して」という依頼です。次の実験ではこの文を変えられます。 |
    | `raise SystemExit(run_task(agent, task))` | モデル・アクション・観測結果のループを開始し、結果を表示して、成功・エラーの状態で終了します。 |

    **正常な実行例：**モデルが「formal」を読み取り、`suggest_menu(occasion="formal")`を提案します。Pythonが関数を実行し、`3-course dinner with wine and dessert.`を返します。モデルはその観測結果を回答に使います。

    **メニューはどこから来る？** `week03_tools.py`内の固定の文字列です。モデルは入力を選んで結果を伝え、関数がメニューを返します。実行記録で呼び出しが本当に起きたか確認してください。

**実行：**`python my_menu.py`。

出力はターミナルで読みます。

**確認すること：**`suggest_menu(occasion="formal")`と、その後の`3-course dinner with wine and dessert.`を探します。最終回答はこの結果を使っているはずです。

**変更してみる：****`my_menu.py`**の`task`を`Prepare a superhero menu for the party.`（スーパーヒーロー向けのメニューを用意して）に変えます。保存し、同じターミナルで`python my_menu.py`を再実行します。関数の結果は`Buffet with high-energy and healthy food.`（エネルギー補給と健康に配慮したビュッフェ）になるはずです。

## C. 準備の終了時刻を計算する { #limits-and-recovery }

**目標：**許可されたPythonモジュール`datetime`をエージェントに使わせます。作業時間は30 + 60 + 45 + 45分です。1人が順番に作業するので、合計は**180分、つまり3時間**です。

1. コードエディターで**`First_agent_template`**を開きます。
2. **ファイル → 新しいテキストファイル → 名前を付けて保存**で、**`my_timing.py`**を`app.py`、`week03_common.py`と同じ場所に保存します。
3. 下の**コード全体**を貼り付けます。
4. Windowsは**Ctrl + S**、Macは**Command + S**で保存します。拡張子は`.py`にします。

```python title="my_timing.py"
from smolagents import CodeAgent
from week03_common import build_model, agent_options, run_task


model = build_model()
agent = CodeAgent(
    tools=[],
    model=model,
    additional_authorized_imports=["datetime"],
    **agent_options(),
)

task = """Alfred needs to prepare for the party. Here are the tasks:
1. Prepare the drinks - 30 minutes
2. Decorate the mansion - 60 minutes
3. Set up the menu - 45 minutes
4. Prepare the music and playlist - 45 minutes

If we start right now, at what time will the party be ready?
Assume one person completes the tasks in order. Use datetime for the current local
PC time, add the total duration, and print both times before answering."""
raise SystemExit(run_task(agent, task))
```

??? info "my_timing.pyのコード解説を読む"

    **Pythonで終了時刻を計算するように依頼するファイルです。**

    | コード | 意味 |
    | --- | --- |
    | `from smolagents import CodeAgent` | Pythonアクションとモデルへの問い合わせをつなぐクラスを読み込みます。 |
    | `from week03_common import ...` | Groq接続、授業用設定、タスク実行の補助関数を読み込みます。 |
    | `model = build_model()` | Groq上のモデルへの接続を準備します。 |
    | `agent = CodeAgent(...)` | 時刻の質問を扱うエージェントを作ります。 |
    | `tools=[]` | 独自ツールや検索ツールは登録しません。許可されたPythonの操作と、smolagents標準の`final_answer`は使えます。 |
    | `model=model` | 準備したGroq接続を渡します。 |
    | `additional_authorized_imports=["datetime"]` | モデルが生成するコードに、日時や時間差を扱う`datetime`の読み込みを許可します。許可するだけで、この行で計算するわけではありません。 |
    | `**agent_options()` | Pythonアクション用の指示、4ステップの上限、実行記録の表示を設定します。 |
    | `task = """..."""` | 複数行の依頼を1つの文字列にします。三重引用符は、作業一覧と指示を改行したまま書くためのものです。 |
    | `raise SystemExit(run_task(agent, task))` | エージェントを実行し、結果を表示して、成功・エラーの状態で終了します。 |

    **依頼の内容：**飲み物30分、飾り付け60分、メニュー準備45分、音楽準備45分。今から1人で順番に作業すると何時に終わるか、PCの現在時刻と合計時間を使って求め、開始・終了時刻を表示するよう頼んでいます。30 + 60 + 45 + 45 = **180分**です。

    **実行すると：**Groq上のモデルが、たとえば`datetime.datetime.now()`でPCの現在時刻を読み、`datetime.timedelta(minutes=180)`を足すPythonを提案します。CodeAgentがローカルで実行し、開始・終了時刻が観測結果になります。モデルはその結果を回答に使います。

    **「今」はどこから来る？** PCの時計とローカルのタイムゾーン設定です。後で実行すれば終了時刻も変わります。実際に生成されたコードと表示された時刻を確認してください。

**実行：**`python my_timing.py`。

出力はターミナルで読みます。

**確認すること：**生成されたPythonがPCの現在時刻を取得し、3時間を加えているかを確認します。開始時刻、所要時間、終了時刻を探してください。回答はPCの時計によって変わります。

## 実行記録を読む { #read-the-record }

| 記録 | 意味 |
| --- | --- |
| モデルの文章／`Thought` | これから行うことの説明として生成された文章。実行した証拠ではありません。 |
| Pythonアクション | モデルが提案したコード。 |
| 観測結果（Observation） | 実際に返された結果またはエラー。 |
| 最終回答 | エージェントが伝える回答。観測結果と照らし合わせます。 |

**確認ポイント：**メニューと時刻のプログラムから、それぞれ**アクション → 観測結果 → 最終回答**を1組示します。音楽検索についても、実際にどうなったかを記録してください。

## 出典 { #sources }

レッスンと例は、[Hugging Face Agents Course — Building Agents That Use Code](https://huggingface.co/learn/agents-course/en/unit2/smolagents/code_agents)を基に構成しています。[Apache 2.0ライセンス](licenses/huggingface-agents-course.txt)に基づき利用しています。

**次へ：**[ステップ10 — Pythonコードと構造化ツール呼び出し](week-3-action-formats.md)。
