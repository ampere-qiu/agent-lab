# 11 · 関数とクラスで作るツール { #week-3-custom-tool }

**目標：**ツールを定義する2つの方法を理解し、配布されたケータリング・テーマのツールを動かし、自分で1か所変更します。

**始める前に：**[第03週の準備](week-3-learning-plan.md#exercise-files)を終えてください。`First_agent_template`フォルダー、既存の`.venv`、Groqキーを使います。`my_tool_check.py`、`my_catering.py`、`my_theme.py`を`app.py`と同じ場所に作ります。

## モデルに伝えるツールの情報 { #your-task }

ツールには、名前、説明、入力の名前と型、出力の型があります。これらは、いつ、どのようにツールを使えばよいかをモデルに伝えます。実際の処理を行うのはPythonの実装です。

[![モデルの依頼、ツール実行、観測結果の流れを示すアニメーション](images/huggingface/Agent_ManimCE.gif)](images/huggingface/Agent_ManimCE.gif)

??? info "この図の説明を読む"

    ツールを使うときのやり取りを示すアニメーションです。モデルは、ツールの説明を基に「どのツールを、どの入力で使うか」を依頼します。実行側がその依頼に対応する処理を行い、結果を返します。返された結果が観測結果として次の判断に使われます。

    **モデルがツールの処理そのものを行うのではありません。** 今週は、Groq上のモデルが依頼し、PC上のPythonが実行し、CodeAgentが結果をモデルへ戻します。ツールの説明文と、実際に働くPythonコードを分けて考えましょう。

*図の出典：[Hugging Face Agents Course](https://huggingface.co/learn/agents-course/en/unit2/smolagents/tools)。画像を選ぶと拡大できます。*

## A. 配布されたケータリング関数を読む { #implement }

[![ケータリングを選ぶアルフレッド](images/huggingface/alfred-catering.jpg)](images/huggingface/alfred-catering.jpg)

??? info "この画像の説明を読む"

    アルフレッドがパーティーのケータリングを手配する場面です。これから扱う関数は、架空の業者と評価の一覧から最高評価の名前を返します。この画像は課題の題材を示すもので、実在の業者や検索結果を示すものではありません。

*画像の出典：[Hugging Face Agents Course](https://huggingface.co/learn/agents-course/en/unit2/smolagents/tools)。画像を選ぶと拡大できます。*

エディターで、ダウンロードに含まれる**`week03_tools.py`**を開き、`catering_service_tool`を探します。**次は、すでにそのファイルにあるコードです。元のファイルで読み、別の場所に重複して定義しないでください。**

```python
@tool
def catering_service_tool(query: str) -> str:
    """
    This tool returns the highest-rated catering service in Gotham City.

    Args:
        query: A search term for finding catering services.
    """
    # Example list of catering services and their ratings
    services = {
        "Gotham Catering Co.": 4.9,
        "Wayne Manor Catering": 4.8,
        "Gotham City Events": 4.7,
    }

    # Find the highest rated catering service (simulating search query filtering)
    best_service = max(services, key=services.get)

    return best_service
```

??? info "catering_service_toolのコード解説を読む"

    **固定のPythonデータから業者名を選ぶ、配布済みの関数です。**

    | コード | 意味 |
    | --- | --- |
    | `@tool` | 関数を、モデルが説明を読めるsmolagentsのツールにします。このデコレーターは配布ファイルの上部で読み込まれています。 |
    | `def catering_service_tool(query: str) -> str:` | 関数名を定義し、入力と出力が文字列であることを示します。`query`は受け取りますが、この例ではデータの絞り込みには使いません。 |
    | ドキュメント文字列と`Args:` | ツールの目的と入力をモデルに説明します。「ゴッサム・シティで最高評価の業者を返す」「queryは検索語」という説明で、この文章自体は検索を実行しません。 |
    | `services = {...}` | 架空の業者名と評価を、PC上の辞書に保存します。 |
    | `max(services, key=services.get)` | 評価を比べ、最大の評価を持つ業者名を選びます。`services.get`は、名前そのものではなく、その名前に対応する評価を比較するための指定です。 |
    | `return best_service` | 呼び出した側に業者名を返します。配布時のデータでは`Gotham Catering Co.`です。 |

    **この関数の中ではLLMを使いません。** 直接呼べば、PC上で普通のPythonとして動きます。エージェントから使う場合は、モデルがアクションを選び、Pythonが業者名を返し、それが観測結果になります。インターネット検索ではなく、4.9、4.8、4.7という固定の評価を比べています。

## B. ツールを直接テストするファイルを作る { #direct-tests }

**目標：**モデルを使う前に、Pythonツールだけを直接呼び出します。このテストにGroqキーやインターネット接続は必要ありません。

1. コードエディターで**`First_agent_template`**を開きます。
2. **ファイル → 新しいテキストファイル → 名前を付けて保存**で、**`my_tool_check.py`**を`app.py`、`week03_common.py`と同じ場所に保存します。
3. 下の**コード全体**を貼り付けます。
4. Windowsは**Ctrl + S**、Macは**Command + S**で保存します。拡張子は`.py`にし、`.txt`を付けないでください。

```python title="my_tool_check.py"
from week03_tools import suggest_menu, catering_service_tool, SuperheroPartyThemeTool

assert suggest_menu(occasion="formal") == "3-course dinner with wine and dessert."
assert catering_service_tool(query="catering") == "Gotham Catering Co."

theme_tool = SuperheroPartyThemeTool()
assert "Gotham Rogues' Ball" in theme_tool(category="villain masquerade")
assert "not found" in theme_tool(category="unknown")

print("PASS: menu, catering, theme, and unknown-category checks.")
```

??? info "my_tool_check.pyのコード解説を読む"

    **エージェントを作らず、Groqにも問い合わせずに、ツールを直接確認するファイルです。**

    | コード | 意味 |
    | --- | --- |
    | `from week03_tools import ...` | 配布された2つの関数と、テーマツールのクラスを読み込みます。 |
    | `assert suggest_menu(...) == ...` | `formal`でメニュー関数を呼び、戻り値が期待する文と完全に一致するかを調べます。 |
    | `assert catering_service_tool(...) == ...` | ケータリング関数を呼び、最高評価の業者名が期待どおりかを調べます。 |
    | `theme_tool = SuperheroPartyThemeTool()` | テーマツールのインスタンスを1つ作ります。次の行から呼び出せます。 |
    | `assert "Gotham Rogues' Ball" in theme_tool(...)` | `villain masquerade`（悪役の仮面舞踏会）で呼び、結果に期待するテーマ名が含まれるかを調べます。 |
    | `assert "not found" in theme_tool(category="unknown")` | 未対応のカテゴリなら、見つからないことを伝える文が返るかを調べます。 |
    | `print("PASS: ...")` | すべての確認に合格した後で成功を表示します。 |

    **アサーション（assertion）**は、満たすはずの条件を確かめるものです。条件が偽なら、Pythonは`PASS`を表示する前に`AssertionError`で止まります。`==`は完全一致、`in`は返された文章に期待する語句が含まれるかを確認します。ここでテストしているのはPythonツールで、モデルの回答ではありません。

**実行：**`python my_tool_check.py`。

表示される結果：

```text
PASS: menu, catering, theme, and unknown-category checks.
```

メニュー、ケータリング、テーマ、不明なカテゴリの確認に合格した、という意味です。アサーションが失敗したら、`week03_tools.py`のデータが配布時のままか確認します。まずローカルのツールを直しましょう。関数の誤りはLLMの回答では直りません。

## C. ケータリングのエージェントを作る { #register }

1. コードエディターで**`First_agent_template`**を開きます。
2. **ファイル → 新しいテキストファイル → 名前を付けて保存**で、**`my_catering.py`**を`app.py`、`week03_common.py`と同じ場所に保存します。
3. 下の**コード全体**を貼り付けます。
4. Windowsは**Ctrl + S**、Macは**Command + S**で保存します。拡張子は`.py`にします。

```python title="my_catering.py"
from smolagents import CodeAgent
from week03_common import build_model, agent_options, run_task
from week03_tools import catering_service_tool

model = build_model()
agent = CodeAgent(
    tools=[catering_service_tool],
    model=model,
    **agent_options(),
)

task = "Can you give me the name of the highest-rated catering service in Gotham City?"
raise SystemExit(run_task(agent, task))
```

??? info "my_catering.pyのコード解説を読む"

    **直接テストしたケータリング関数を、今度はモデルに使わせます。**

    | コード | 意味 |
    | --- | --- |
    | `from smolagents import CodeAgent` | モデルへの問い合わせ、Pythonアクション、観測結果をつなぐクラスを読み込みます。 |
    | `from week03_common import ...` | Groq接続、授業用設定、タスク実行の補助関数を読み込みます。 |
    | `from week03_tools import catering_service_tool` | 配布されたデコレーター付き関数を読み込みます。実装は`week03_tools.py`に残します。 |
    | `model = build_model()` | 自分のキーでGroq接続を準備します。まだタスクは実行しません。 |
    | `agent = CodeAgent(...)` | モデルとツールを持つローカルのエージェントを作ります。 |
    | `tools=[catering_service_tool]` | 関数を使えるように登録します。後で使うための登録なので、関数名の後ろに括弧を付けません。 |
    | `model=model` | 上で準備したモデル接続を渡します。 |
    | `**agent_options()` | Pythonアクション用の指示、4ステップの上限、ターミナルへの記録を設定します。 |
    | `task = "Can you ..."` | 「ゴッサム・シティで最も評価の高いケータリング業者の名前を教えて」という依頼です。 |
    | `raise SystemExit(run_task(agent, task))` | ループを開始し、結果を表示して、成功・エラーの状態で終了します。 |

    **処理を追うと：**Groqのモデルが`catering_service_tool(query="catering")`のような呼び出しを提案します。PC上のCodeAgentが関数を実行し、固定の評価から`Gotham Catering Co.`が返ります。モデルはその観測結果を回答に使います。実際の呼び出しと戻り値を実行記録で確認してください。

**実行：**`python my_catering.py`。

キーを求められたらGroqキーを入力します。入力は非表示です。実際の`catering_service_tool(...)`の呼び出し、返された`Gotham Catering Co.`、それを使った最終回答を探してください。

## D. 配布されたToolクラスを読む { #class-tool }

同じ**`week03_tools.py`**で`SuperheroPartyThemeTool`を探します。クラスも配布済みです。各項目と`forward(...)`を読み、コードは元のファイルに残します。

```python
class SuperheroPartyThemeTool(Tool):
    name = "superhero_party_theme_generator"
    description = """
    This tool suggests creative superhero-themed party ideas based on a category.
    It returns a unique party theme idea."""

    inputs = {
        "category": {
            "type": "string",
            "description": "The type of superhero party (e.g., 'classic heroes', 'villain masquerade', 'futuristic Gotham').",
        }
    }

    output_type = "string"

    def forward(self, category: str):
        themes = {
            "classic heroes": "Justice League Gala: Guests come dressed as their favorite DC heroes with themed cocktails like 'The Kryptonite Punch'.",
            "villain masquerade": "Gotham Rogues' Ball: A mysterious masquerade where guests dress as classic Batman villains.",
            "futuristic gotham": "Neo-Gotham Night: A cyberpunk-style party inspired by Batman Beyond, with neon decorations and futuristic gadgets."
        }

        return themes.get(category.lower(), "Themed party idea not found. Try 'classic heroes', 'villain masquerade', or 'futuristic Gotham'.")
```

??? info "SuperheroPartyThemeToolのコード解説を読む"

    **クラスでは、ツールの説明と、実際に働くPythonコードをひとまとめにします。**

    | コード | 意味 |
    | --- | --- |
    | `class SuperheroPartyThemeTool(Tool):` | smolagentsの`Tool`を基に、ツールクラスを定義します。`Tool`は配布ファイルで読み込まれています。 |
    | `name` | モデルが呼び出すときのツール名を`superhero_party_theme_generator`にします。 |
    | `description` | ヒーローを題材にしたパーティーテーマをカテゴリ別に提案する、という用途をモデルに伝えます。 |
    | `inputs` | 入力は`category`という文字列であることと、カテゴリの例を示します。 |
    | `output_type = "string"` | 戻り値が文字列であることをフレームワークに伝えます。 |
    | `def forward(self, category: str):` | ツールが呼ばれたときの処理です。`self`はそのインスタンスを指し、呼び出し側は`category`を渡します。 |
    | `themes = {...}` | 3つの架空のカテゴリと説明文を保存します。 |
    | `category.lower()` | 入力を小文字にし、辞書の小文字のキーに合わせます。 |
    | `themes.get(..., "Themed party idea not found. ...")` | カテゴリの説明を返します。キーがなければ、代わりの案内文を返します。 |

    `classic heroes`は定番ヒーローの祝宴、`villain masquerade`は悪役の仮面舞踏会、`futuristic Gotham`は近未来のゴッサムがテーマです。`villain masquerade`なら、Pythonが保存済みの**Gotham Rogues' Ball**の説明を返します。**別のLLMで新しい案を生成しているのではなく、PC上の固定文を取り出しています。** 未知のカテゴリには、見つからない旨と選べるカテゴリを返します。

    関数型では、`@tool`が関数名、ドキュメント文字列、型ヒントからツールの説明を作ります。このクラス型では、その説明項目を明示的に書き、処理を`forward(...)`に置きます。

## E. パーティーテーマのエージェントを作る { #run-agent }

1. コードエディターで**`First_agent_template`**を開きます。
2. **ファイル → 新しいテキストファイル → 名前を付けて保存**で、**`my_theme.py`**を`app.py`、`week03_common.py`と同じ場所に保存します。
3. 下の**コード全体**を貼り付けます。
4. Windowsは**Ctrl + S**、Macは**Command + S**で保存します。拡張子は`.py`にします。

```python title="my_theme.py"
from smolagents import CodeAgent
from week03_common import build_model, agent_options, run_task
from week03_tools import SuperheroPartyThemeTool

model = build_model()
party_theme_tool = SuperheroPartyThemeTool()
agent = CodeAgent(
    tools=[party_theme_tool],
    model=model,
    **agent_options(),
)

task = "What would be a good superhero party idea for a 'villain masquerade' theme?"
raise SystemExit(run_task(agent, task))
```

??? info "my_theme.pyのコード解説を読む"

    **配布されたツールクラスのインスタンスを作り、エージェントに渡すファイルです。**

    | コード | 意味 |
    | --- | --- |
    | `from smolagents import CodeAgent` | モデル・アクション・観測結果のループを管理するクラスを読み込みます。 |
    | `from week03_common import ...` | Groq接続、授業用設定、タスク実行の補助関数を読み込みます。 |
    | `from week03_tools import SuperheroPartyThemeTool` | 配布されたツールクラスを読み込みます。 |
    | `model = build_model()` | 自分のキーでGroq接続を準備します。 |
    | `party_theme_tool = SuperheroPartyThemeTool()` | ツールのインスタンスを作ります。括弧は生成のためのもので、まだテーマを依頼していません。 |
    | `agent = CodeAgent(...)` | 質問を扱うエージェントを作ります。 |
    | `tools=[party_theme_tool]` | インスタンスを登録します。モデルに見える名前は、クラスで宣言した`superhero_party_theme_generator`です。 |
    | `model=model` | Groqのモデル接続を渡します。 |
    | `**agent_options()` | Pythonアクション用の指示、ステップ上限、実行記録の表示を設定します。 |
    | `task = "What would ..."` | 「悪役の仮面舞踏会に合うパーティーのアイデアは？」という依頼です。 |
    | `raise SystemExit(run_task(agent, task))` | タスクを実行し、結果を表示して、返された状態で終了します。 |

    **処理を追うと：**Groq上のモデルがツールと`villain masquerade`という入力を選びます。CodeAgentがPC上で`superhero_party_theme_generator(category="villain masquerade")`を実行し、インスタンスの`forward(...)`が働きます。保存済みの説明文が観測結果となり、モデルが最終回答に使います。

**実行：**`python my_theme.py`。

実行記録で`superhero_party_theme_generator(category="villain masquerade")`を探します。返された説明は`Gotham Rogues' Ball`から始まるはずです。最終回答が、その観測結果と合っているかを比べてください。

## F. 1か所変更して、もう一度動かす { #challenge }

1. **`week03_tools.py`**の`services`辞書に、4.9より高い評価の架空の業者を追加します。`"name": rating,`という形を保ちます。
2. 保存し、どの業者名が返るかを予想します。
3. 同じターミナルで**`python my_catering.py`**を再実行し、実際のツールの結果と最終回答を読みます。
4. **`my_tool_check.py`**の以前のアサーションは、まだ`Gotham Catering Co.`を期待しています。その1か所の期待値を新しい最高評価の業者名に変更し、保存して**`python my_tool_check.py`**を再実行します。

テーマの辞書に小文字のカテゴリを追加し、**`my_theme.py`**の`task`でそのカテゴリを依頼しても構いません。両方のファイルを保存してから再実行します。変更しているのはPythonのデータと質問文で、モデルを学習し直しているわけではありません。

**確認ポイント：**直接テストの合格、ケータリングとテーマの呼び出し、自分の変更を反映したエージェントの結果を示してください。

## ツールでできるほかのこと { #default-toolbox }

ツールは利用者への入力要求、ウェブページの読み取り、最終回答の返却にも使えます。それぞれの機能をエージェントが使えるようにする必要があります。ウェブ検索ツールが返す短い抜粋と、ブラウザそのものの操作は別の機能です。

## 発展的な内容 { #integrations }

ツールを共有したり、別のシステムにつないだりすることもできます。今週の実習では扱いません。[第03週の完了確認](week-3-completion.md)に進んでください。続きの話題は[第04週の予告](week-4-preview.md)にあります。

## 出典 { #sources }

[Hugging Face Agents Course — Tools](https://huggingface.co/learn/agents-course/en/unit2/smolagents/tools)を基に構成しています。[Apache 2.0ライセンス](licenses/huggingface-agents-course.txt)に基づき利用しています。

**次へ：**[第03週の完了確認](week-3-completion.md)。
