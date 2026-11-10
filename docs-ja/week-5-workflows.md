# 23 · イベントで処理をつなぐ { #week-5-workflows }

**目標：**処理の間を情報がどう移動するかを決め、エージェントのチームにもつなげます。HFと同じ順番で進めます。各プログラムは、既存のヘルパーと同じ場所に別々のファイルとして作ってください。

[![HFのワークフロー図：StartEventから各処理と型のあるイベントを通り、run_queryとStopEventへ進む](images/huggingface-week05/workflows.png)](images/huggingface-week05/workflows.png){ .course-figure-link }

??? info "この図の説明を読む"

    青い四角は仕事をするステップ、色の付いた楕円はデータを運ぶイベントです。たとえば`StartEvent → parse_query → QueryEvent → run_query → StopEvent`とたどれます。ステップが仕事を終えると、種類の決まったメッセージを渡し、その種類を受け取れる次のステップが動きます。メッセージには次の処理が必要とする結果も入ります。図は大きな構成例ですが、演習では1ステップから始め、`ProcessingEvent`などの型で接続を表します。

*HFの図を変更せず使用しています。[原典のレッスン](https://huggingface.co/learn/agents-course/en/unit2/llama-index/workflows) · [図を拡大する](images/huggingface-week05/workflows.png)。*

## 1. 1ステップのワークフロー { #one-step }

ワークフローは`StartEvent`で始まります。対応するステップが受け取り、別のイベントを返します。`StopEvent`は実行を終え、結果を運びます。`@step`がメソッドを登録し、型注釈が受け取るイベントと返すイベントを示します。

**`my_workflow.py`を作成します。**開始イベントを入力に、1つのステップで「Hello, world!」をターミナルへ表示します。LLM、通信、Groqのトークンは使いません。

```python title="my_workflow.py"
from llama_index.core.workflow import StartEvent, StopEvent, Workflow, step
from week05_common import run

class MyWorkflow(Workflow):
    @step
    async def my_step(self, ev: StartEvent) -> StopEvent:
        return StopEvent(result="Hello, world!")

async def main():
    print(await MyWorkflow(timeout=10, verbose=False).run())

if __name__ == "__main__":
    run(main)
```

??? info "開始と終了の説明を読む"

    `StartEvent`という型で、開始と`my_step`がつながります。`StopEvent(result=...)`を返すと終了します。`await ...run()`の戻り値を`print`で表示します。`run(main)`が通常のPythonファイルから実行できる入口を用意するため、ノートブック専用の最上位`await`は不要です。

**実行：**`python my_workflow.py`。`Hello, world!`というあいさつを確認します。どこでLLMを使いましたか？

??? success "答え"

    どこでも使っていません。ワークフローは通常のPython処理も整理できます。イベント駆動であるだけでは、AIエージェントとは限りません。

## 2. 2つのステップをつなぐ { #two-steps }

**1つのメッセージを追います。**`StartEvent → step_one → ProcessingEvent → step_two → StopEvent`。`step_one`が「Step 1 complete」をメッセージへ書き、`step_two`が読み取って「Finished processing:」を付けます。ファイルで次に書かれたメソッドが動くのではなく、イベントの型で接続が決まります。

**`my_workflow_steps.py`を作成します。**最初のステップが文字列を独自の`ProcessingEvent`へ入れ、次のステップが読み取って完了結果を表示します。入力は開始イベントで、データはイベントを通して渡されます。LLM、通信、Groqのトークンは使いません。

```python title="my_workflow_steps.py"
from llama_index.core.workflow import Event, StartEvent, StopEvent, Workflow, step
from week05_common import run

class ProcessingEvent(Event):
    intermediate_result: str

class MultiStepWorkflow(Workflow):
    @step
    async def step_one(self, ev: StartEvent) -> ProcessingEvent:
        return ProcessingEvent(intermediate_result="Step 1 complete")

    @step
    async def step_two(self, ev: ProcessingEvent) -> StopEvent:
        return StopEvent(result=f"Finished processing: {ev.intermediate_result}")

async def main():
    print(await MultiStepWorkflow(timeout=10, verbose=False).run())

if __name__ == "__main__":
    run(main)
```

??? info "イベントの受け渡しの説明を読む"

    最初のステップが返す`ProcessingEvent`は、`step_two`の入力の型に一致します。`intermediate_result`が渡すデータです。接続を決めるのはイベントの型であり、ステップ名やファイル内の順番ではありません。

**実行：**`python my_workflow_steps.py`。`Finished processing: Step 1 complete`という「ステップ1を処理し終えた」結果を確認します。

同じファイルの`step_one`内にあるreturnの行を、次の行へ置き換えます。先頭の空白8個を残してください。

```text
        return ProcessingEvent(intermediate_result="Step 1 changed by the student")
```

保存して`python my_workflow_steps.py`を再実行します。結果が`Finished processing: Step 1 changed by the student`に変わることを確認します。`step_two`を編集していないのに変わる理由を説明してください。記録後は、次の元の行へ戻して保存します。

```text
        return ProcessingEvent(intermediate_result="Step 1 complete")
```

## 3. 分岐と繰り返し { #loop }

HFは、同じステップへ戻る場合と先へ進む場合がある例を示しています。ここでは両方を予測・確認できるよう、必ず1回だけ繰り返します。タイムアウトも実行の上限です。無制限に繰り返す形には変えません。

**`my_workflow_loop.py`を作成します。**最初に`LoopEvent`を返して同じステップへ戻り、次に`ProcessingEvent`で2番目のステップへ進みます。入力は開始イベントで、試行回数をイベントで運びます。分岐の記録と最終結果を表示し、LLMや通信は使いません。

```python title="my_workflow_loop.py"
from llama_index.core.workflow import Event, StartEvent, StopEvent, Workflow, step
from week05_common import run

class LoopEvent(Event):
    attempt: int

class ProcessingEvent(Event):
    intermediate_result: str

class LoopWorkflow(Workflow):
    @step
    async def step_one(self, ev: StartEvent | LoopEvent) -> ProcessingEvent | LoopEvent:
        attempt = ev.attempt if isinstance(ev, LoopEvent) else 0
        if attempt < 1:
            print("Try again once")
            return LoopEvent(attempt=attempt + 1)
        print("Continue to step two")
        return ProcessingEvent(intermediate_result="First step complete")

    @step
    async def step_two(self, ev: ProcessingEvent) -> StopEvent:
        return StopEvent(result=f"Finished processing: {ev.intermediate_result}")

async def main():
    print(await LoopWorkflow(timeout=10, verbose=False).run())

if __name__ == "__main__":
    run(main)
```

??? info "繰り返しの説明を読む"

    `StartEvent | LoopEvent`は、どちらのイベントも受け取れるという型の指定です。最初の試行回数は0です。`LoopEvent(attempt=1)`を返すと同じステップへ戻り、その値で2回目の繰り返しを防ぎます。`ProcessingEvent`を返すと別の分岐で`step_two`へ進みます。このループは、APIの回数制限を再試行する機能ではありません。

**出力を予測してから実行：**`python my_workflow_loop.py`。

```text
Try again once
Continue to step two
Finished processing: First step complete
```

表示は順に「1回だけ再試行」「ステップ2へ進む」「処理完了」です。どのイベントで繰り返し、どのイベントで先へ進んだかを記録してください。

## 4. 進める経路を図にする { #draw }

[![HFの作図例：step_oneへ戻るLoopEventと、step_twoからStopEventへ進む経路](images/huggingface-week05/workflow-draw.png)](images/huggingface-week05/workflow-draw.png){ .course-figure-link }

??? info "この図の説明を読む"

    `StartEvent`から矢印をたどると`step_one`へ進みます。`LoopEvent`は同じステップへ戻し、`ProcessingEvent`は`step_two`へ進め、最後に`StopEvent`を返します。`_done`はフレームワーク内部の終了処理です。この演習は最初にループし、次に先へ進みます。図は可能な経路を示し、ターミナルは実際に通った経路を示します。自分が作る図は配置が違っても構いません。

*HFの図を変更せず使用しています。[原典のレッスン](https://huggingface.co/learn/agents-course/en/unit2/llama-index/workflows) · [図を拡大する](images/huggingface-week05/workflow-draw.png)。*

**`my_workflow_draw.py`を作成します。**前のファイルのワークフロークラスを調べ、プログラムと同じ場所に`flow.html`を保存します。ワークフローの実行やLLMの利用は行いません。結果はブラウザで開ける図です。

```python title="my_workflow_draw.py"
from my_workflow_loop import LoopWorkflow
from week05_common import ROOT, save_diagram

if __name__ == "__main__":
    save_diagram(LoopWorkflow, ROOT / "flow.html")
    print("Saved flow.html. Open it yourself in your browser.")
```

??? info "作図の説明を読む"

    `save_diagram`はHFの`draw_all_possible_flows`を使い、登録されたステップとイベントの接続をHTMLにします。配布ヘルパーはブラウザを自動起動しません。`LoopWorkflow`のファイルにはmainガードがあるため、読み込むだけでは`main`は動きません。図だけでは、ある実行がどの経路を通ったかまでは分かりません。

**実行：**`python my_workflow_draw.py`。`Saved flow.html. Open it yourself in your browser.`という保存完了の表示を待ちます。ブラウザは自動で開きません。エクスプローラー／Finderで`week05-exercises/flow.html`をダブルクリックしてください。配置が落ち着くと全体が収まります。見切れる場合は図の下の**Fit diagram**で全体を表示します。何もない場所をドラッグして移動し、スクロールやピンチで拡大・縮小できます。繰り返しと終了の経路を探し、必要ならスクリーンショットを残します。実際の3行の出力とも比べてください。図のライブラリはHTMLに含まれるので、閲覧時の通信は不要です。

??? help "ファイルがない、または図が真っ白になる場合"

    `python week05_common.py`で**2026-11-10.2**を確認します。違う場合は現在のZIPからそのヘルパーだけを更新し、`python my_workflow_draw.py`を再実行します。`Saved flow.html...`を待ち、新しく保存したファイルを開いてください。HFの図と配置が違うだけなら問題ありません。

    `No module named pyvis`なら、今週の`.venv`を有効にして`python -m pip install -r requirements.txt`を実行します。`python -m pip show pyvis`で確認でき、指定バージョンは**0.3.2**です。まだ真っ白なら別のブラウザを試し、ファイル名とエラーを教員へ伝えてください。

## 5. Contextで状態を共有する { #state }

**`Context`は、この実行で共有するメモ帳だと考えてください。**イベントは対応するステップへメッセージを運び、Contextは後のステップが名前で読み出せる情報を保管します。ここでは`query`という名前で質問を保存し、後で読みます。実行中のメモリ内の状態であり、保存ファイルではありません。

**`my_workflow_state.py`を作成します。**HFの「フランスの首都は何か」という質問を保存し、次のステップと実行後に同じ文字列を読みます。保存した質問と完了メッセージを表示します。質問への回答、LLMへの接続、Groqのトークン消費は行いません。

```python title="my_workflow_state.py"
from llama_index.core.workflow import Context, Event, StartEvent, StopEvent, Workflow, step
from week05_common import run

class ProcessingEvent(Event):
    intermediate_result: str

class StateWorkflow(Workflow):
    @step
    async def step_one(self, ctx: Context, ev: StartEvent) -> ProcessingEvent:
        await ctx.store.set("query", "What is the capital of France?")
        return ProcessingEvent(intermediate_result="Step 1 complete")

    @step
    async def step_two(self, ctx: Context, ev: ProcessingEvent) -> StopEvent:
        query = await ctx.store.get("query")
        print("STORED QUERY:", query)
        return StopEvent(result=f"Finished processing: {ev.intermediate_result}")

async def main():
    workflow = StateWorkflow(timeout=10, verbose=False)
    ctx = Context(workflow)
    print(await workflow.run(ctx=ctx))
    print("STATE AFTER RUN:", await ctx.store.get("query"))

if __name__ == "__main__":
    run(main)
```

??? info "共有状態の説明を読む"

    `ctx.store.set`で名前付きの値を書き、`ctx.store.get`で読みます。両方のステップと終了後の読み出しに、同じ実行のContextを使います。処理の経路は引き続き`ProcessingEvent`が決め、Contextはその流れと並行して共有情報を持ちます。

**実行：**`python my_workflow_state.py`。`What is the capital of France?`という質問が2回出ることを確認します。答えがParisだと調べた処理はありますか？

??? success "答え"

    ありません。質問を保存して読み出すだけです。調査やモデルによる回答処理は含まれません。質問を表示できたことと、質問に答えられたことは別です。

## 6. チームを動かし、計算回数を数える { #agent-workflow }

最後にHFは、掛け算役、足し算役、最初に受け取る役、共有状態を使うチームへ戻ります。ワークフローと、前の演習のモデルによる判断をつなげます。

**`my_team_workflow.py`を作成します。**HFの足し算の質問を、まず掛け算役に渡します。足し算役へ受け渡し、その役が`add`を呼ぶはずです。計算ツールが共有カウンターを更新します。Groqのトークンを使い、実行記録、最終回答、計算の呼び出し回数を表示します。

```python title="my_team_workflow.py"
from llama_index.core.agent.workflow import AgentWorkflow, FunctionAgent
from llama_index.core.workflow import Context
from week05_common import get_llm, run, show_agent

async def add(ctx: Context, a: int, b: int) -> int:
    """Add two integers and count this arithmetic call."""
    state = await ctx.store.get("state")
    state["num_fn_calls"] += 1
    await ctx.store.set("state", state)
    return a + b

async def multiply(ctx: Context, a: int, b: int) -> int:
    """Multiply two integers and count this arithmetic call."""
    state = await ctx.store.get("state")
    state["num_fn_calls"] += 1
    await ctx.store.set("state", state)
    return a * b

async def main():
    llm = get_llm()
    multiplier = FunctionAgent(
        name="multiply_agent", description="Multiplies two integers.", tools=[multiply], llm=llm,
        can_handoff_to=["add_agent"],
        system_prompt="Use multiply for multiplication. Hand all addition requests to add_agent.",
    )
    adder = FunctionAgent(
        name="add_agent", description="Adds two integers.", tools=[add], llm=llm,
        can_handoff_to=["multiply_agent"],
        system_prompt="Use add for addition. Return the result from the tool.",
    )
    workflow = AgentWorkflow(
        agents=[multiplier, adder], root_agent="multiply_agent", timeout=180,
        initial_state={"num_fn_calls": 0},
        state_prompt="Current state: {state}. User message: {msg}",
    )
    ctx = Context(workflow)
    await show_agent(workflow, "Can you add 5 and 3? Hand off to add_agent and use add.", ctx=ctx)
    state = await ctx.store.get("state")
    print("ARITHMETIC CALLS:", state["num_fn_calls"])

if __name__ == "__main__":
    run(main)
```

??? info "チームの状態の説明を読む"

    `initial_state`は回数0の辞書を用意します。計算ツールは`ctx`を受け、カウンターを増やして保存し直します。Contextはフレームワークが渡すもので、モデルが数値として入力するものではありません。`state_prompt`は状態とユーザーの依頼をモデルへ伝えます。増えるのは計算関数の実行回数だけで、モデル呼び出し、受け渡し、トークンの数ではありません。この例の受け渡しは順番に行います。同時に状態を更新する場合は、別の調整が必要です。

**実行：**`python my_team_workflow.py`を1回実行します。

`add_agent`への受け渡し、`5`と`3`での`add`呼び出し、戻り値`8`、それに合う最終回答、`ARITHMETIC CALLS: 1`を別々に確認してください。回数が1より大きい場合は、計算の繰り返しを記録で調べます。回数だけでは、どのツールが動き、回答が正しいかは分かりません。

**比較：**このページのどのプログラムはGroqなしで動き、どれがモデルに経路を選ばせますか？メモの23の欄に、イベントで次のステップが決まる場合と、エージェントがツールを選ぶ場合の違いを図にしてください。

*原典・演習の出典：[HF Unit 2.2 — workflows](https://huggingface.co/learn/agents-course/en/unit2/llama-index/workflows)。Apache-2.0。`NOTICE.md`と`HF-LICENSE.txt`を参照してください。*

## ここで確認 { #checkpoint }

| 残しておく新しいファイル | 確認する結果 |
| --- | --- |
| `my_workflow.py` | あいさつが出る。LLMは使わない。 |
| `my_workflow_steps.py` | イベントのデータがステップ2へ届く。比較後は元の行に戻す。 |
| `my_workflow_loop.py` | 完了前にちょうど1回繰り返す。 |
| `my_workflow_draw.py` | 自動起動せず`flow.html`を保存する。読み込み元の`my_workflow_loop.py`も残す。 |
| `my_workflow_state.py` | 保存した同じ質問が実行中と終了後に出る。 |
| `my_team_workflow.py` | 受け渡し、`add(5,3)`、結果`8`、実行記録と一致する計算回数。 |

6つのうちGroqが必要なのは最後のプログラムだけです。前のファイルも残し、メモの23の欄へ結果を保存してください。図だけに頼らず、実際の出力とイベントの経路を並べます。

**次へ：**[小テスト2](week-5-quiz-2.md)。
