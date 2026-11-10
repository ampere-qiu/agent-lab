# 22 · エージェントにツールを選ばせる { #week-5-agents }

**目標：**ツールを直接呼ぶ場合と、モデルが行動を選ぶ場合の違いを確認します。[小テスト1](week-5-quiz-1.md)を終え、同じ有効な`week05-exercises`のターミナルを使ってください。

## 1. エージェントの方式を選ぶ { #agent-types }

HFは、構造化されたツール呼び出しを使う**関数呼び出し型**、文章形式の推論・アクションを解釈する**ReAct型**、専用の動作を定義する**独自エージェント**を紹介しています。ここでは授業用モデルで関数呼び出し型を使います。`AgentWorkflow.from_tools_or_functions`は、モデルのメタデータに応じて対応する方式を選びます。

[![HFのエージェントの方式：関数呼び出し、ReAct、独自の高度な構成](images/huggingface-week05/agents.png)](images/huggingface-week05/agents.png){ .course-figure-link }

??? info "この図の説明を読む"

    3つのカードは、判断のループを作る方式の違いです。関数呼び出し型は、モデルから構造化されたツール名と入力を受け取ります。ReAct型は文章のアクション形式を解釈し、独自型は専用の動作を定めます。モデルがその形式に従えることも必要です。この演習の「2 times 2」では、モデルが`multiply`と`a=2, b=2`を選び、Pythonが`4`を計算し、モデルが答えます。実行記録で順に確かめましょう。

*HFの図を変更せず使用しています。[原典のレッスン](https://huggingface.co/learn/agents-course/en/unit2/llama-index/agents) · [図を拡大する](images/huggingface-week05/agents.png)。*

エージェントもツールや入力を間違えることがあります。ヘルパーが表示する**REQUEST**は依頼、**TOOL**は実際の呼び出し、**RETURN**は戻り値、**ANSWER**は最終回答です。回答だけで判断せず、この観測結果を確認します。モデル内部の非公開の思考過程を表示する課題ではありません。

## 2. 計算ツール1つから始める { #arithmetic }

**`my_agent.py`を作成します。**掛け算の関数を渡し、HFの「2 times 2」という質問で、呼び出しと回答を表示します。Groqが行動を選び、Pythonが計算します。Groqのトークンを使い、結果はターミナルに出ます。

```python title="my_agent.py"
from llama_index.core.agent.workflow import AgentWorkflow
from week05_common import get_llm, run, show_agent


def multiply(a: int, b: int) -> int:
    """Multiply two integers and return the result."""
    return a * b


async def main():
    agent = AgentWorkflow.from_tools_or_functions(
        tools_or_functions=[multiply], llm=get_llm(),
        system_prompt="Use the multiply tool for multiplication. State its returned result.",
        timeout=180,
    )
    await show_agent(agent, "What is 2 times 2? Use the tool.")

if __name__ == "__main__":
    run(main)
```

??? info "エージェントの説明を読む"

    関数の引数・型・docstringからツールの窓口を作ります。`AgentWorkflow.from_tools_or_functions`はツール、モデル、指示をまとめます。`show_agent`が開始し、完了したツール呼び出しを表示します。反復回数とタイムアウトが実行を制限します。mainガードがあるので、ほかのプログラムから`multiply`を読み込んでも、この依頼は実行されません。

**実行：**`python my_agent.py`。

`multiply`に`a=2`、`b=2`が渡り、戻り値が`4`で、回答も一致することを確認します。ツール呼び出しがなければ、答えが`4`でもツール利用は未確認です。前の`weather.call(...)`と比べ、どちらの場合に誰が操作を選んだか説明してください。

## 3. Contextで会話を覚える { #memory }

**`my_memory.py`を作成します。**「My name is Bob.」と伝え、同じContextで名前を聞き、その後、新しいContextでも同じ質問をします。3つのメッセージを入力とし、比較結果はターミナルに出ます。3回ともGroqのトークンを使います。

```python title="my_memory.py"
from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.core.workflow import Context
from my_agent import multiply
from week05_common import get_llm, run, show_agent

async def main():
    agent = AgentWorkflow.from_tools_or_functions(
        tools_or_functions=[multiply], llm=get_llm(), timeout=180,
        system_prompt="Answer briefly. Remember only information present in this conversation.",
    )
    ctx = Context(agent)
    await show_agent(agent, "My name is Bob.", ctx=ctx)
    await show_agent(agent, "What was my name again?", ctx=ctx)
    print("NOW A FRESH CONTEXT:")
    await show_agent(agent, "What was my name again?", ctx=Context(agent))

if __name__ == "__main__":
    run(main)
```

??? info "会話の記憶の説明を読む"

    `Context(agent)`は実行履歴の情報を持ちます。同じ`ctx`を渡すことで最初の2つの会話をつなぎます。配布ヘルパーの`show_agent`は、以前の会話を次の実行へ明示的に渡します。新しいContextには先ほどの名前は渡りません。同じモデルオブジェクトを使うだけでは、履歴は共有されません。プログラムを再起動した後まで記憶を保存する例でもありません。

**予測：**先ほどの名前を使えるのはどの質問でしょうか？**実行：**`python my_memory.py`を1回実行します。

3つの回答を確認してください。

1. 最初はBobという名前を受け取る。あいさつの文面は変わっても構いません。
2. 同じContextはBobを覚えている。
3. 新しいContextは名前が分からないと答える。

**`UnserializableKeyWarning`が出る場合：**フレームワークは記憶用オブジェクトを自動で保存形式に変換できません。ヘルパーが次の実行へそのオブジェクトを渡すので、上の回答で確認します。2番目がBobを忘れる場合は、`python week05_common.py`で**2026-11-10.2**を確認してください。違う場合は現在のZIPのヘルパーだけを入れ直し、この演習を再実行します。ほかの作業は残してください。

??? info "最終回答の表示方法を読む"

    モデルが`<think>`のタグや、`</think>`前後で重複する文章を返すことがあります。ヘルパーはタグ付きの思考部分を表示せず、最終回答の文章を表示します。表示を整える処理なので、回答の根拠は引き続きツールと出典で確認します。

3つの結果を`evidence.md`の22の欄に記録します。プログラムを起動し直すと例はリセットされます。配布されたBobのメッセージは変えずに使ってください。

## 4. エージェントにRAGツールを渡す { #rag-agent }

[![HFのAgentic RAG図：検索、外部API、Web検索、直接回答などの選択肢](images/huggingface-week05/agentic-rag.png)](images/huggingface-week05/agentic-rag.png){ .course-figure-link }

??? info "この図の説明を読む"

    エージェントには複数の行動候補があり、文書検索もその1つです。ツールを選び、結果を読んで、どう答えるか決めます。この演習で使えるのは`personas`と`multiply`です。図のWeb検索や外部APIは、より広い構成の例です。人物像の質問には`personas`、掛け算には`multiply`を使うか、選択と戻り値で確認します。

*HFの図を変更せず使用しています。[原典のレッスン](https://huggingface.co/learn/agents-course/en/unit2/llama-index/agents) · [図を拡大する](images/huggingface-week05/agentic-rag.png)。*

**`my_rag_agent.py`を作成します。**掛け算と人物像の検索ツールを渡し、説明文の検索と根拠の返答を依頼します。クエリエンジンもエージェントもGroqを使うため、ツール1回でモデルを複数回呼ぶ場合があります。ターミナルの実行記録と最終回答を読みます。

```python title="my_rag_agent.py"
from llama_index.core.agent.workflow import AgentWorkflow
from my_agent import multiply
from week05_common import get_llm, run, show_agent
from week05_rag import persona_tool

async def main():
    llm = get_llm()
    agent = AgentWorkflow.from_tools_or_functions(
        tools_or_functions=[multiply, persona_tool(llm)], llm=llm, timeout=180,
        system_prompt=("Use personas for questions about profiles and multiply for arithmetic. "
                       "Quote only original EXCERPT text, cite its SOURCE filename, and distinguish it from GENERATED ANSWER text. "
                       "Search results cover only retrieved passages. Say no match was found in those passages; do not claim all profiles were checked. Do not invent names or contact details."),
    )
    await show_agent(agent, "Find the persona interested in Cincinnati art. Use personas and quote its description.")

if __name__ == "__main__":
    run(main)
```

??? info "エージェントによるRAGの説明を読む"

    決められたクエリエンジンは毎回同じ検索・回答の経路を進みます。このエージェントはツールと`personas`への質問を選べます。クエリエンジンの回答を観測結果として受け、さらに回答を作る場合があります。どちらにも根拠のない追加がないか調べます。`return_direct=False`により、ツールの戻り値を即座に最終回答とせず、エージェントが使えます。

**実行：**`python my_rag_agent.py`。

次の順に確認します。

1. `TOOL: personas`と、返された**SOURCE**、**EXCERPT**を探す。
2. `data`内の出典ファイルを開き、本文と抜粋を照合する。
3. 最終回答の引用が元の本文に一致し、ファイル名を示しているか確認する。

**GENERATED ANSWER**はモデルの要約です。呼び出し、元の文章、出典表示のどれかが足りなければ、不足を記録します。

**`my_rag_agent.py`で選択を比較します。**`main`の中の`await show_agent(...)`を探してください。末尾の`run(main)`はそのままにし、依頼の1行全体を次へ置き換えます。先頭の空白4個を残します。

```text
    await show_agent(agent, "What is 2 times 2? Use multiply.")
```

保存し、`python my_rag_agent.py`を1回実行します。人物像の検索ではなく、`TOOL: multiply`と`RETURN: 4`を確認してください。記録を`evidence.md`へ残したら、次の元の行へ戻して保存します。

```text
    await show_agent(agent, "Find the persona interested in Cincinnati art. Use personas and quote its description.")
```

??? info "任意：別の関心について検索する"

    **利用可能な範囲で行うHFとの比較です。**元の依頼を`evidence.md`へ控え、同じ`main`内で次の1行を使ってください。

    ```text
        await show_agent(agent, "Search the database for 'science fiction' and return some persona descriptions. Use only the source excerpts. If they contain no match, say no match was found in the retrieved passages; do not claim to have checked every profile.")
    ```

    `python my_rag_agent.py`を1回実行します。ツールが取り出すのは10ファイルのうち最大2つの文章です。どちらにもSFへの関心が書かれていなければ、「この検索結果には一致なし」と言えます。「データベース内の誰もSFを好まない」は、残りを全部確認していないため言い過ぎです。回答がどちらの主張か記録し、上に示した元の依頼へ戻します。

## 5. 2体のエージェントをつなぐ { #team }

HFは次に計算役と情報検索役を作ります。それぞれに専用のツールと指示があります。`AgentWorkflow`の**最初に受け取る役（root agent）**が依頼を受け、**受け渡し（handoff）**で別の役へ移ります。図だけでなく実行記録で確認してください。

**`my_agent_team.py`を作成します。**計算役から始め、`info_lookup`が担当する人物像の調査を依頼します。既存のインデックス、共有するGroq接続、モデルのトークンを使います。最終回答だけでなく、受け渡しと検索をターミナルで確認します。

```python title="my_agent_team.py"
from llama_index.core.agent.workflow import AgentWorkflow, FunctionAgent
from my_agent import multiply
from week05_common import get_llm, run, show_agent
from week05_rag import persona_tool

async def main():
    llm = get_llm()
    calculator = FunctionAgent(
        name="calculator", description="Multiplies integers.",
        system_prompt="Use multiply for math. Hand persona research to info_lookup.",
        tools=[multiply], llm=llm, can_handoff_to=["info_lookup"],
    )
    researcher = FunctionAgent(
        name="info_lookup", description="Searches ten persona descriptions.",
        system_prompt="Use personas. Quote only original EXCERPT text and cite its SOURCE filename. GENERATED ANSWER is not a source quotation. Limit missing-match claims to the retrieved passages. Mark missing information.",
        tools=[persona_tool(llm)], llm=llm, can_handoff_to=["calculator"],
    )
    team = AgentWorkflow(agents=[calculator, researcher], root_agent="calculator", timeout=180)
    await show_agent(team, "Find the Cincinnati art historian. Hand this task to info_lookup, which must query personas.")

if __name__ == "__main__":
    run(main)
```

??? info "チームの説明を読む"

    2つの`FunctionAgent`は名前、ツール、指示が異なります。`can_handoff_to`が渡せる相手を定め、`root_agent="calculator"`が最初の役を選びます。同じモデル接続を使っても別の役です。記録では受け渡しの後に`personas`が出るはずです。HFの単純な計算問題は計算役だけで処理できますが、ここでは調査を依頼して接続を確かめます。

**実行：**`python my_agent_team.py`。`info_lookup`への受け渡し、その役の`personas`呼び出し、元の文章、それに沿う回答を探します。実際の受け渡しと結果を22の欄へ記録してください。

**確認メモ：**計算、Bobの比較、RAGツールの選択、受け渡しの記録を残します。1つのモデル接続を共有する2体が、なぜ別々のエージェントなのか説明してください。

*原典・演習の出典：[HF Unit 2.2 — agents](https://huggingface.co/learn/agents-course/en/unit2/llama-index/agents)。Apache-2.0。`NOTICE.md`と`HF-LICENSE.txt`を参照してください。*

## ここで確認 { #checkpoint }

| 残しておく新しいファイル | 確認する結果 |
| --- | --- |
| `my_agent.py` | 実際に`multiply(2,2)`が動き、`4`を返した。 |
| `my_memory.py` | 共有するContextはBobを覚え、新しいContextには名前の根拠がない。 |
| `my_rag_agent.py` | 人物像の呼び出し、元の抜粋、出典付きの引用か、根拠がないという記録。比較後は元の依頼へ戻す。 |
| `my_agent_team.py` | 実際に`info_lookup`へ渡り、その後`personas`を呼ぶ。 |

`my_agent.py`は、ほかの例が掛け算関数を読み込むので残してください。実行記録はメモの22の欄に保存します。

**次へ：**[23 · ワークフロー](week-5-workflows.md)。
