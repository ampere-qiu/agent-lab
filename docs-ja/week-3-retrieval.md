# 12 · Agentic RAGシステムを作る（任意） { #week-3-retrieval }

!!! note "第3週では任意です"

    このレッスンは今週は任意で、来週あらためて扱います。今は飛ばして、ツールの後に[13 · 完了確認](week-3-completion.md)へ進んで構いません。予習や練習ができるよう、第3週に残しています。

**目標：**エージェントに検索できるノート集を渡し、何を取得したかを追い、回答がそのノートに基づくかを確認します。**活動：**読解、ウェブ検索、LLMを使わない検索テスト、ローカルのRAGエージェント、自分のノートの追加に取り組みます。

先に[11 · 関数とクラスで作るツール](week-3-custom-tool.md)を終えてください。新しいファイルはすべて**`First_agent_template`内の`app.py`と同じ場所**に作ります。同じ有効化済みの環境とGroqキーを使い、保存したファイルをターミナルで実行します。

## ツールのレッスンから何が変わる？ { #retrieval-concept }

メニューやテーマのツールは、Pythonのデータから決まった文章を選んで返しました。今度は、文章の集まりから必要な箇所を探して返す**検索・取得ツール（retrieval tool）**をエージェントに渡します。

**RAG**は**Retrieval-Augmented Generation（検索拡張生成）**の略です。関係する資料を探し、その文章をモデルに渡して回答に使います。**Agentic RAG**では、モデルが検索語を選び、結果を読んで、必要ならもう一度検索できます。

**質問 → モデルが検索を選ぶ → Pythonが文章を取得 → 観測結果 → モデルが回答、または再検索。**

| 部分 | 役割 | 動く場所 |
| --- | --- | --- |
| モデル | 検索語を選び、返された文章を使って回答する。 | Groq |
| 検索・取得ツール | 配布されたノートを検索し、文章と出典ラベルを返す。 | 自分のPC |
| CodeAgent | 依頼されたアクションを実行し、ループをつなぐ。 | 自分のPC |

ノート自体はローカルのPythonファイルにありますが、エージェントの実行では取得した文章が観測結果としてGroqに送られます。後で行う直接テストはGroqに接続しません。検索・取得でモデルを学習し直したり、永続的な記憶を自動作成したりするわけではありません。

## 検索・取得用ファイルの準備 { #setup }

現在の[第03週のダウンロード](week-3-learning-plan.md#exercise-files)には、**`week03_retriever.py`**を含む**7つの補助ファイル**が入っています。以前の6ファイル版を使っている場合は、現在のZIPをダウンロードし、**`week03_retriever.py`**と**`week03-requirements.txt`**を`app.py`と同じ場所にコピーします。編集済みの`week03_tools.py`と、自分の`my_...py`は残してください。

更新されたパッケージ一覧をまだ導入していない場合は、既存の有効化済みターミナルで次を一度実行します。

```bash
python -m pip install -r week03-requirements.txt
```

検索・取得用の`langchain-community`、`langchain-text-splitters`、`rank-bm25`を追加します。`smolagents==1.13.0`とGroq接続は引き続き使います。別のAPIキー、埋め込みモデル、ベクトルデータベースは不要です。モジュールが見つからない場合は、実行に使う`.venv`に更新版の一覧を導入したか確認します。非推奨の警告とテストの失敗は別なので、実際の結果を確認してください。

## A. ウェブから情報を取得する { #web-retrieval }

まず、すでに使った検索ツールから始めます。豪華なスーパーヒーローパーティーの**飾り付け、催し物、ケータリング**を探す依頼です。モデルは各話題を検索し、結果を組み合わせて計画にできます。

コードエディターで**`my_rag_search.py`**を作り、下のコード全体を貼り付け、`app.py`と同じ場所に保存します。

**このファイルの役割 — `my_rag_search.py`:** 飾り付け、催し物、ケータリングのアイデアをウェブで集め、取得した情報からパーティーの計画を作るエージェントを動かします。Groqが検索を選んで計画を書き、Pythonツールが抜粋とURLを取得します。どの情報源が提案を裏付けるかを、ターミナルの出力で確認します。

```python title="my_rag_search.py"
from smolagents import CodeAgent
from week03_common import build_model, agent_options, run_task
from week03_search import WebSearchTool

model = build_model()
search_tool = WebSearchTool()
agent = CodeAgent(
    tools=[search_tool],
    model=model,
    **agent_options(),
)

task = "Search for luxury superhero-themed party ideas, including decorations, entertainment, and catering."
task += " Use web_search and print its results. Cite only URLs returned by the tool."
raise SystemExit(run_task(agent, task))
```

??? info "my_rag_search.pyのコード解説を読む"

    | コード | 役割 |
    | --- | --- |
    | 読み込みの行 | CodeAgent、配布されたGroqの補助関数、検索ツールのクラスを読み込みます。 |
    | `model = build_model()` | Groq接続を準備します。必要ならキーを尋ねます。 |
    | `search_tool = WebSearchTool()` | 検索ツールのインスタンスを作ります。まだ検索はしません。 |
    | `tools=[search_tool]` | そのインスタンスをCodeAgentに登録します。 |
    | `model=model`と`**agent_options()` | Groq接続と、授業用のPythonアクション設定を渡します。 |
    | `task = ...` | パーティーの3つの話題についてアイデアを探す依頼です。 |
    | `task += ...` | 取得結果を表示し、そのURLを引用するよう指示を追加します。`+=`は既存の文字列に文章を足します。 |
    | `raise SystemExit(run_task(agent, task))` | タスクを実行して結果を表示し、成功・エラーの状態で終了します。 |

    検索語を選ぶのはモデルです。PC上のPythonが検索サービスに接続し、返された抜粋がモデルの観測結果になります。これまでの検索と同じ仕組みを、複数の話題から回答の材料を集めるために使います。

**実行：**`python my_rag_search.py`。

**活動：**検索の呼び出し、返された抜粋とURL、その結果に基づく計画の一部を探します。実際の検索は1回でしたか、複数回でしたか？

??? success "解答を表示"

    モデルが生成した`web_search(...)`の呼び出しと、その後に実際に返されたデータを探します。そこからURLを1つ選び、回答がその抜粋の内容を使っているか確認します。モデルの文章だけに登場するURLは、取得した証拠にはなりません。

    **解答例：**「モデルが検索語を選び、検索ツールが抜粋とURLを返しました。エージェントはその情報を使い、計画の一部を提案しました。」自分の実際の検索語、情報源、それが裏付ける提案を付け加えましょう。

    実行記録の呼び出し回数を数えます。複数回の検索ができても、その実行では1回だけかもしれません。起きていない検索を報告しないでください。サービスが失敗したら成功した情報源の代わりにエラーを記録します。提案されたアイデアだけでは、実在の業者がそのサービスを提供する証拠にはなりません。

## B. ローカルの知識ベースを読む { #hf-retrieval-code }

配布された**`week03_retriever.py`**を開きます。次は、そのファイル内のコード全体です。**別のコピーを作らず、元のファイルで読んでください。** 5つの短いノートは架空のパーティー資料で、それぞれ出典ラベルが付いています。

```python
"""HF PartyPlanningRetrieverTool and five example documents (Apache-2.0).
Source: https://huggingface.co/learn/agents-course/en/unit2/smolagents/retrieval_agents
Changes: accurate BM25 description and returned source metadata.
"""
from langchain_community.docstore.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.retrievers import BM25Retriever
from smolagents import Tool


class PartyPlanningRetrieverTool(Tool):
    name = "party_planning_retriever"
    description = "Uses BM25 keyword search to retrieve relevant party planning ideas for Alfred’s superhero-themed party at Wayne Manor."
    inputs = {
        "query": {
            "type": "string",
            "description": "The query to perform. This should be a query related to party planning or superhero themes.",
        }
    }
    output_type = "string"

    def __init__(self, docs, **kwargs):
        super().__init__(**kwargs)
        self.retriever = BM25Retriever.from_documents(
            docs, k=5  # Retrieve the top 5 documents
        )

    def forward(self, query: str) -> str:
        assert isinstance(query, str), "Your search query must be a string"

        docs = self.retriever.invoke(
            query,
        )
        return "\nRetrieved ideas:\n" + "".join(
            [
                f"\n\n===== Idea {str(i)} =====\n" + doc.page_content
                + f"\nSource: {doc.metadata['source']}"
                for i, doc in enumerate(docs)
            ]
        )

# Simulate a knowledge base about party planning
party_ideas = [
    {"text": "A superhero-themed masquerade ball with luxury decor, including gold accents and velvet curtains.", "source": "Party Ideas 1"},
    {"text": "Hire a professional DJ who can play themed music for superheroes like Batman and Wonder Woman.", "source": "Entertainment Ideas"},
    {"text": "For catering, serve dishes named after superheroes, like 'The Hulk's Green Smoothie' and 'Iron Man's Power Steak.'", "source": "Catering Ideas"},
    {"text": "Decorate with iconic superhero logos and projections of Gotham and other superhero cities around the venue.", "source": "Decoration Ideas"},
    {"text": "Interactive experiences with VR where guests can engage in superhero simulations or compete in themed games.", "source": "Entertainment Ideas"}
]

source_docs = [
    Document(page_content=doc["text"], metadata={"source": doc["source"]})
    for doc in party_ideas
]

# Split the documents into smaller chunks for more efficient search
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    add_start_index=True,
    strip_whitespace=True,
    separators=["\n\n", "\n", ".", " ", ""],
)
docs_processed = text_splitter.split_documents(source_docs)

# Create the retriever tool
party_planning_retriever = PartyPlanningRetrieverTool(docs_processed)
```

??? info "week03_retriever.pyのコード解説を読む"

    次の順番で読みましょう。

    | 部分 | 意味 |
    | --- | --- |
    | `party_ideas` | 豪華な装飾、DJ、ヒーロー風の料理、ロゴの投影、VR体験という5つのノートです。各項目は`text`と`source`を持ちます。 |
    | `Document(...)` | 本文を包み、出典を`metadata`に残します。 |
    | `RecursiveCharacterTextSplitter(...)` | 分割が必要なら、500文字を目安の上限として、50文字重ねた断片を作ります。この短いノートでは5つの断片のままです。`add_start_index`は各断片の開始位置を記録します。 |
    | `PartyPlanningRetrieverTool(Tool)` | ステップ11と同じツールクラスです。名前、説明、`inputs`、`output_type`がモデルにインターフェースを伝えます。 |
    | `__init__(self, docs, **kwargs)` | 文書を受け取ってインスタンスを準備します。`super().__init__(**kwargs)`は基になるToolの初期化です。 |
    | `BM25Retriever.from_documents(docs, k=5)` | PC上に単語ベースの索引を作り、検索ごとに最大5件の順位付き結果を求めます。 |
    | `forward(self, query)` | 検索語が文字列か確認し、検索して結果を文章として返します。ツール自体はLLMに問い合わせません。 |
    | `enumerate(docs)` | 今回の結果の順に、0から番号を付けます。`Idea 0`は順位であり、固定の文書IDではありません。 |
    | `Source: ...` | 各文章に保存済みの出典ラベルを付け、回答の根拠を確かめられるようにします。 |
    | `party_planning_retriever = ...` | 処理済みの文書からインスタンスを作ります。このモジュールの読み込みで、ローカルに準備されます。 |

    **BM25は一致する単語を使って文章を順位付けします。** 埋め込みモデルではありません。この単純な標準の単語分割では、綴り、大文字・小文字、句読点、同義語が一致の度合いに影響します。

    **重要な制約：**`k=5`で5件を求め、元のノートも5つなので、弱い一致や無関係な文章を含め、全部が返ることがあります。このツールにはスコアのしきい値や、自動の「該当なし」はありません。先頭は最も高い順位ですが、返ったすべての文章が役立つわけではありません。

`Source:`の値は配布ノートのラベルで、ウェブアドレスではありません。催し物に関する2つのノートは同じラベルを持つので、**ラベルと本文の両方**で、何が根拠になっているかを確かめます。

## C. LLMなしで検索・取得をテストする { #direct-tests }

**`my_retrieval_check.py`**を`app.py`と同じ場所に作り、コード全体を貼り付けて保存します。

**このファイルの役割 — `my_retrieval_check.py`:** エージェントを作らず、ローカルの知識ベース検索ツールをテストします。velvetで期待するノートが先頭になること、出典ラベルが残ること、存在しない検索語でも文書が返ることを確認します。取得したノートと、合格時のPASSを表示します。LLMとGroqキーは使いません。

```python title="my_retrieval_check.py"
from week03_retriever import party_ideas, docs_processed, party_planning_retriever

matches = party_planning_retriever.retriever.invoke("velvet")
assert "velvet curtains" in matches[0].page_content
assert matches[0].metadata["source"] == "Party Ideas 1"
assert len(docs_processed) == len(party_ideas)

result = party_planning_retriever(query="velvet")
assert "Source: Party Ideas 1" in result
print(result)

unrelated = party_planning_retriever.retriever.invoke("zyxwvu")
assert len(unrelated) == min(5, len(docs_processed))
assert all("zyxwvu" not in doc.page_content.lower() for doc in unrelated)

print("PASS: retrieval ranks a matching note, preserves sources, and exposes the no-match limitation.")
```

??? info "my_retrieval_check.pyのコード解説を読む"

    | コード | 意味 |
    | --- | --- |
    | 読み込みの行 | ノート、処理済みの断片、準備したツールを読み込みます。 |
    | `.retriever.invoke("velvet")` | 直接検索し、本文とメタデータを調べられるDocumentを返します。 |
    | 最初の2つの`assert` | 先頭の結果に`velvet curtains`があり、出典も期待どおりかを確認します。 |
    | `len(docs_processed) == len(party_ideas)` | これらの短いノートが、1つずつの断片のままかを確認します。 |
    | `party_planning_retriever(query="velvet")` | エージェントが使うツールのインターフェースを呼びます。出典付きの整形された文章が返ります。 |
    | `zyxwvu`の確認 | どのノートにも検索語がないのに、順位付きの結果が返ることを示します。`min(5, ...)`により、6つ目の短いノートを追加した後も確認できます。 |
    | `all(...)` | 返された全ての文書が条件を満たすことを求めます。 |
    | 最後の`print` | 全アサーションに合格したときだけ成功を表示します。 |

    エージェントやGroqのモデルは作りません。APIキーや通信なしで、ローカルの検索を確かめています。アサーションが失敗したら、モデルに使わせる前に、ローカルのデータや検索の設定を直します。

**実行：**`python my_retrieval_check.py`。

返されたノートを読みます。先頭の結果に`velvet curtains`と`Source: Party Ideas 1`があり、最後に次が表示されるはずです。

```text
PASS: retrieval ranks a matching note, preserves sources, and exposes the no-match limitation.
```

「一致するノートの順位、出典の保持、該当語がなくても返る制約を確認した」という意味です。

**活動：**`zyxwvu`はどのノートにもないのに、なぜテストは合格するのでしょうか？ 「5件返った」は「5件とも有用」という意味ですか？

??? success "解答を表示"

    `velvet`では、一致するノートが先頭に来て、出典も残ることを確認しています。`zyxwvu`では別の動作を確認しています。一致する単語がなくても、BM25は最大5件の順位付き結果を返します。このツールはスコアがゼロの結果を除外しません。

    **解答例：**「返された文書は候補であり、関連性の証明ではありません。直接テストは制約を示しており、エージェントは本文が回答を裏付けるか確認する必要があります。」未知の語を見つけたからではなく、この動作を期待するテストなので合格します。

## D. CodeAgentにノートを使わせる { #agent-retrieval }

**`my_rag.py`**を`app.py`と同じ場所に作り、コード全体を貼り付けて保存します。

**このファイルの役割 — `my_rag.py`:** week03_retriever.pyのローカルノートを使い、パーティー準備の質問に答えるエージェントを動かします。Pythonが本文と出典ラベルを取得し、Groq上のモデルがその文章を使って回答します。ターミナルの取得結果と最終回答で、根拠、答えのない質問、追加したノートの反映を確認できます。

```python title="my_rag.py"
from smolagents import CodeAgent
from week03_common import build_model, agent_options, run_task
from week03_retriever import party_planning_retriever

model = build_model()
agent = CodeAgent(
    tools=[party_planning_retriever],
    model=model,
    **agent_options(),
)

task = "Find ideas for a luxury superhero-themed party, including entertainment, catering, and decoration options."
task += " Use party_planning_retriever and print its results."
task += " Answer briefly from the returned notes and cite their Source labels."
task += " If the notes do not support an answer, say so."
raise SystemExit(run_task(agent, task))
```

??? info "my_rag.pyのコード解説を読む"

    | コード | 意味 |
    | --- | --- |
    | `from week03_retriever import party_planning_retriever` | 直接テストしたツールと、ローカルの索引を読み込みます。 |
    | `build_model()` | これまでと同じGroq接続を準備します。 |
    | `tools=[party_planning_retriever]` | 既存のインスタンスを登録します。準備中に呼び出すのではないので、括弧は付けません。 |
    | `CodeAgent(...)` | Pythonアクション、ツールの結果、モデルへの問い合わせをつなぎます。 |
    | `task = ...` | 催し物、料理、飾り付けについて、豪華なヒーローパーティーの案を依頼します。 |
    | 3つの`task += ...` | ノートを取得・表示し、返された出典を使い、根拠がなければそう答えるよう求めます。指示に従ったかは実行記録で確認します。 |
    | `run_task(...)` | モデル・アクション・観測結果のループを開始し、最終結果を表示します。 |

    **1回の実行を追うと：**モデルが`party_planning_retriever(query=...)`を提案し、ローカルのPythonが文章を取得します。本文とラベルが観測結果になり、モデルがそれを使って回答します。直接テストと違い、この実行にはGroqとインターネット接続が必要です。

**実行：**`python my_rag.py`。

**活動：**回答の提案を1つ選び、実際の検索呼び出し、それを裏付ける文章、返された`Source:`を探します。この3つを書き留めてください。

??? success "解答を表示"

    たとえばDJの提案なら、`Hire a professional DJ`で始まる取得済みの本文と、`Source: Entertainment Ideas`が根拠になります。豪華な飾り付けなら、金の装飾とベルベットのカーテンの文章と、`Source: Party Ideas 1`が対応します。

    **解答の型：**「エージェントは［実際の検索語］でツールを呼び、［観測した文章］と［そのSource］が返りました。最終回答はこの文章を使い、［裏付けられる案］を提案しました。」自分の実行から埋めてください。上の例だけでは、自分のエージェントが呼び出した証拠にはなりません。

    ラベルだけでなく本文も確認します。出典名だけでは、価格、予約の確定、実在業者の空き状況など、本文にない詳細を裏付けられません。

## E. 範囲を絞った質問と、根拠のない質問 { #query-experiments }

**`my_rag.py`**の最初の`task = ...`だけを、`task = "Find the idea mentioning velvet curtains."`に変えます。ベルベットのカーテンに触れた案を探す依頼です。後ろの3つの追加指示は残します。保存し、**`python my_rag.py`**を再実行します。

次に最初の文を`task = "Do these notes contain the word zyxwvu?"`に変え、保存して同じファイルを実行します。ノートに`zyxwvu`という語があるかを尋ねています。両方の実行記録を残してください。

**活動：**最初の回答の根拠は何ですか？ 2つ目では、ノートが返っても、どう答えるべきでしょうか？

??? success "解答を表示"

    **範囲を絞った質問：**実際に返された`velvet curtains`を含む文章と、`Party Ideas 1`のラベルを探します。その文章が回答の根拠です。

    **根拠のない質問：**配布ノートに`zyxwvu`はありません。5件返っても、回答は「返されたノート内にはその語が見つからない」と伝えるべきです。文章が返っただけでは、質問に答えられるとは限りません。

    モデルが検索語を選ぶので、実際の検索内容を見ます。Pythonツールが正常に動いても、モデルが一致する文章を作り上げたら、この確認には合格しません。

## F. 自分の知識を追加する { #challenge }

1. **`week03_retriever.py`**を開き、`party_ideas`を探します。
2. 閉じる`]`の前に6つ目の辞書を追加し、同じ`"text"`と`"source"`を使います。たとえば`"text": "Create a planetarium ceiling for the party."`（会場の天井をプラネタリウム風にする）と、`"source": "Student Decoration Idea"`です。項目の間のカンマを忘れないでください。
3. 保存します。**`my_rag.py`**の最初の文を`task = "Find the planetarium decoration idea."`にし、追加指示は残して保存し、**`python my_rag.py`**を実行します。
4. ツール出力と回答で、新しい本文と出典を確認します。**`python my_retrieval_check.py`**も再実行します。元のベルベットのノートは、その検索では引き続き先頭になるはずです。

**活動：**モデルを学習し直しましたか？ 6つあるノートのうち、検索結果に出ないものがあるのはなぜですか？

??? success "解答を表示"

    変えたのは**知識ベース**で、モデルの重みではありません。プログラムを起動し直すと編集したノートを読み、新しいローカル索引を作ります。`planetarium`の検索では追加したノートが上位になるはずなので、実際の出力と出典を確認します。

    短いノートが6つあり、`k=5`なので、1回の取得は最大5件です。少なくとも1件は含まれません。直接テストは元の`velvet`を使うので、新しいノートとエージェントの回答も別に確認する必要があります。

## 大きなシステムで検索を改善するには { #limitations-and-next-steps }

| 方法 | 簡単な説明 |
| --- | --- |
| 質問の言い換え | 検索に向いた語句へ書き換える。 |
| 質問の分解 | 複数の話題を、小さな検索に分ける。 |
| 検索語の展開 | 複数の言い回しで探す。 |
| 再ランキング | クロスエンコーダーなどの別の方法で、最初の結果を再評価する。 |
| 複数段階の検索 | 最初の結果を見て、次に何を探すか決める。 |
| 情報源の統合 | ノートとウェブなど、複数の情報源を組み合わせる。 |
| 結果の検証 | 本文が質問に関係し、回答を裏付けるか確かめる。 |

これらは設計の選択肢であり、BM25を使うだけで自動的に備わる機能ではありません。上の2つのプログラムは、それぞれ1種類の検索ツールを登録しています。1つのエージェントがウェブとノートを自動で選ぶ例ではありません。実行履歴はその実行中に役立ちますが、永続的な記憶には別の設計が必要です。

**活動：**料理と催し物の両方を尋ねられ、広い質問ではよい結果が出ない場合、エージェントはどうできますか？

??? success "解答を表示"

    `catering`と`entertainment`などの2つの検索に分け、それぞれの観測結果を確認し、根拠のある文章を組み合わせられます。これは質問の分解で、複数段階の検索にもなり得ます。別の言葉を使えば言い換えや検索語の展開です。小さな実習で実際に行ったかどうかは、実行記録を見て判断してください。

**確認ポイント：**直接テストの合格、実際の取得呼び出し、出典に基づく回答、根拠のない質問への結果、自分が追加したノートを示します。モデルが選ぶことと、ローカルのPythonが実行することを説明してください。

## 出典と次のステップ { #sources }

[Hugging Face Agents Course — Building Agentic RAG Systems](https://huggingface.co/learn/agents-course/en/unit2/smolagents/retrieval_agents)を基に、[Apache 2.0ライセンス](licenses/huggingface-agents-course.txt)に従って構成しています。パーティーのノート、検索ツールのクラス、分割設定はそのレッスンに由来します。返す文章には、ノートの出典ラベルを含めています。

補足資料として[原典のノートブック](https://huggingface.co/agents-course/notebooks/blob/main/unit2/smolagents/retrieval_agents.ipynb)と、[より大きなAgentic RAGのレシピ](https://huggingface.co/learn/cookbook/agent_rag)があります。[HF Quick Quiz 2](https://huggingface.co/learn/agents-course/en/unit2/smolagents/quiz2)は任意です。

**次へ：**[13 · 完了確認](week-3-completion.md)。
