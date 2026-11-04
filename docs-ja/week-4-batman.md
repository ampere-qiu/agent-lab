# 15 · マルチエージェントシステム { #week-4-batman }

*参考：[Hugging Face Multi-Agent Systems](https://huggingface.co/learn/agents-course/en/unit2/smolagents/multi_agent_systems)。矢印をたどり、下へ渡る依頼と、上へ返る根拠を確認してください。*

**目標：**エージェントの役割と委任を理解し、Batman調査チームを作ります。

まず**Part Aでエージェントの連携**を学び、**Part BでBatmanチーム**を作ります。3体目の追加は任意です。

## Part A · マルチエージェントの仕組み { #multi-agent-concepts }

[![HFの管理役・コードツール・Webエージェントの構成図](images/huggingface-week04/multi-agent-architecture.png)](images/huggingface-week04/multi-agent-architecture.png){ .course-figure-link }

??? info "この図の説明を読む"

    管理役がタスクを受け、必要な作業をコードツールやWeb調査役へ渡す構成です。管理役から下向きの矢印は依頼、調査役から戻る矢印は調査結果を表します。Web調査役は自分で検索やページ閲覧を選ぶループを持ちます。コードツールの呼び出しは、それ自体がもう1体のエージェントになるわけではありません。結果が管理役へ戻るとき、出典や不確かな点も一緒に渡す必要があります。図をクリックすると拡大できます。

*Hugging Faceの図を変更せず使用しています。[元の大きさで開く](images/huggingface-week04/multi-agent-architecture.png)。*

### 1. マルチエージェントとは？ { #why-teams }

**エージェント**は、モデルが判断するループ、指示、ツール、自分の実行履歴を持ちます。**マルチエージェントシステム**は、このようなエージェントを2体以上つなぎ、作業を分担して結果を受け渡す仕組みです。**役割（role）**は担当する仕事、**受け渡し（handoff）**はエージェント間で渡す依頼と情報です。

1体のCodeAgentでも検索、ページ閲覧、計算、レポート作成はできます。履歴が1つなので、動きを追いやすい利点があります。ただし、長い調査では検索の抜粋、ページ本文、計算結果、レポートの判断が同じ履歴にたまります。不要な詳細に注意を取られ、同じ検索を繰り返したり、後で必要な出典を見失ったりすることがあります。

管理役と専門役に分けると、調査側に独自の「モデル → アクション → 観測」のループができます。管理役が目標を渡し、専門役が検索語や読むページを選び、短い報告を返します。管理役はその報告を使って続きを進めます。決められたPython処理を実行して値を返す関数ツールとは、この点が異なります。

2体で同じモデル接続とキーを共有しても、履歴や使えるツールは別々です。また、2体いるからといって並列実行になるとは限りません。この演習では管理役が専門役の返答を待ちます。受け渡しで管理役の履歴を整理できる一方、大事な根拠が失われる可能性もあります。問い合わせと連携が増えると、時間や費用が増えることもあります。チームのほうが良いと決めつけず、実際の記録で評価してください。

[![管理役と専門役の別々のループ、依頼と根拠の矢印、エージェント数に含めないツールを示す図](images/week04/multi-agent-concept.svg)](images/week04/multi-agent-concept.svg){ .course-figure-link }

??? info "この図の説明を読む"

    左の**1 · MANAGER**が全体を管理する役、右の**2 · SPECIALIST**が特定の仕事を担当する役です。それぞれに「Model → action → observation」という独立したループがあります。上の右向きの矢印**Request**は依頼、下の左向きの矢印**Evidence**は返された根拠です。専門役の下の**TOOLS**は検索やページ閲覧などの処理で、追加のエージェントには数えません。この図のエージェントは**合計2体**です。

*教材の図：別々のループを持つ**2体のエージェント**です。ツールは追加のエージェントではありません。[図を拡大する](images/week04/multi-agent-concept.svg)。*

### 例に進む前の確認 { #concept-check }

**1. 管理役が1体の調査役に委任し、計算ツールも呼びます。エージェントは何体ですか？**

??? success "確認1 — ループを数える"

    管理役と調査役の**2体**です。計算ツールは定められた処理を行うもので、3体目のモデル判断ループではありません。

**2. 2体で1つのモデル接続を共有すると、同じエージェントになりますか？**

??? success "確認2 — 接続とエージェントの違い"

    なりません。別々のエージェントとして、それぞれの履歴、指示、使えるツールを持ちます。役割ごとに別のモデルを用意する必要はありません。

**3. 管理役と専門役の図があれば、並列実行や回答の検証ができていると言えますか？**

??? success "確認3 — 実行を調べる"

    言えません。この演習では管理役が専門役を待ちます。実際の委任と返された出典を確認してください。図やエージェントの追加だけでは正しさを保証できません。

## Part B · メイン演習：Batman調査チーム { #batman-exercise }

**課題：**Web調査役と管理役を作り、地点の調査、出典の確認、レポートの作成を連携して行わせます。

アルフレッドは、代わりのバットモービルが見つかりそうな場所の候補を必要としています。**Batmanの撮影地3か所とスーパーカーメーカーの工場1か所**を調べ、その用途と座標の根拠を残してください。架空のゴッサムまでの貨物航空輸送時間を授業用の式で概算し、出典付きの表と色分けした座標図を作ります。

最初に調査ツールを確認します。その後、専門役と管理役を作ってつなぎ、1件の撮影情報を確認してから4地点へ進みます。各確認問題に答え、結果を`evidence.md`に残してください。

**始める前に：**[第04週の準備](week-4-preview.md#exercise-files)と、[記録用の`evidence.md`、`evidence-files`の作成](week-4-preview.md#evidence-file)を終えます。この演習の回答と結果は、メモの**Topic 15**に記入します。

| ファイル | 配布・作成・生成の区別 |
| --- | --- |
| `week04_common.py`、`week04_search.py`、`week04_tools.py` | ZIPに入っています。指定されたときに既存のファイルを開きます。作り直す必要はありません。 |
| `my_batman_tools.py`、`my_batman.py` | 手順3、4に沿って`week04-exercises`内に作ります。 |
| `my_batman_verified.py` | 配布されません。任意課題に取り組むときだけ、動作しているチームのコピーを作ります。 |
| `evidence.md` | 準備で作成したファイルです。回答とターミナルの抜粋を保存します。 |
| `outputs/batman-report.html` | レポートツールが成功したときに生成されます。空のHTMLファイルを自分で作らないでください。 |

すべて、環境を有効にした同じ`week04-exercises`のターミナルで実行します。調査やモデルの記録はターミナルで読み、生成したレポートだけをブラウザで開きます。

### 必須の2体と任意の追加を確認する { #team-roles }

[![必須のBatmanチーム2体と、任意の検証役を加えた3体の役割・ツール・接続を示す図](images/week04/batman-agent-roles.svg)](images/week04/batman-agent-roles.svg){ .course-figure-link }

??? info "この図の説明を読む"

    **1 · MANAGER**が管理役で、調査を依頼し、出典と不足情報を保ちながら`cargo_time`と`save_report`を使います。最終レポートと地図を書くのはこの役だけです。左下の**2 · WEB SPECIALIST**が調査役で、撮影地3か所と工場1か所の候補、用途と座標の出典を調べます。この**管理役＋Web調査役の2体が必須**です。

    右下の点線の枠**3 · VERIFIER · OPTIONAL**が任意の検証役です。追加すると**合計3体**になります。引用されたページを独立して読み、`pass`、`fail`、`uncertain`と根拠を返します。点線は追加した場合の依頼と判定の受け渡しです。調査役と検証役はどちらも管理役へ直接報告します。ツールは各枠の中に書かれており、エージェントの人数には含めません。

*教材の図：**必須は管理役＋Web調査役の2体**、**任意で検証役を加えると合計3体**です。[図を拡大する](images/week04/batman-agent-roles.svg)。*

Web調査役が調べ、管理役が全体の調整、計算、保存を行います。任意課題では、調査結果1件を独立して確認し判定する検証役を加えます。検証役は調査役の別名ではなく、別のエージェントです。検索・ページ閲覧・計算・レポートの各ツールは、人数を増やすものではありません。

**コードを書く前に：**専門役が「Wollaton Hallは良い候補です」としか返さなかったら、管理役は何を確かめられるでしょうか？地図の作成と出典の確認には、どの情報が必要ですか？

??? success "考え方を確認する"

    裏付けるページ、座標とその出典、撮影地か工場かという区分、不確かな点が足りません。説得力のある要約だけでは調査記録として使えません。専門役の自信だけから、管理役が不足した根拠を復元することはできません。

### 2. 各エージェントの役割を理解する { #plan }

下の表で担当を確認します。コードを書く前に、2つの役割を自分の言葉で`evidence.md`のTopic 15に説明してください。

| 部分 | 渡すもの・担当すること |
| --- | --- |
| Web調査役 | `WebSearchTool(budget=budget)`と`PageExcerptTool(budget=budget)`、呼び出し名`web_specialist`、調査の役割を伝える説明文。 |
| 管理役 | `cargo_time`と`save_report`。`managed_agents=[specialist]`で調査役へ委任できます。 |
| 受け渡し | 裏付けのある地点と用途、確認できた場合の座標、用途の出典URL、座標の出典URL、根拠と不確かな点。 |
| 小さなテスト | `ONE_LOCATION_TASK`が建物1件の情報と出典を求めます。レポートは保存しません。 |
| 全体のタスク | `TASK`が異なる撮影地3か所と工場1か所、計算、表・座標図の保存を求めます。 |

レポートの1行に必要な項目は`location`、`kind`（`filming`または`factory`）、`latitude`、`longitude`、`source_url`、`coordinate_source_url`、`evidence`です。撮影情報の出典だけでは、座標を確認できない場合もあります。不足している根拠は不足として示し、計算用の座標を推測で作らないでください。

```text
Given task → manager → web_specialist(task="a research goal")
                           ↓ web_search → visit_webpage
                     sourced report → manager
                           ↓ cargo_time → save_report (full task only)
                     outputs/batman-report.html
```

**1. 調査役に検索・ページ閲覧ツールを持たせ、管理役に計算・レポートツールを持たせるのはなぜですか？**

??? success "解答1 — それぞれの担当"

    調査役は自分のループで根拠を集めます。管理役はその調査を依頼し、返された座標で計算して保存します。管理役が直接検索できないため、委任の動きが分かりやすくなります。

**2. 専門役が返答に出典URLと不確かな点を含めるべきなのはなぜですか？**

??? success "解答2 — 使える根拠"

    自分と管理役が、各主張と座標の裏付けを確認するためです。根拠のない結論では計算や点検を支えられません。足りない項目は解決するまで不足として残します。

### 3. ツールと概算式を確認する { #tool-check }

**目標：**エージェントに使わせる前に、LLMなしでツールを試します。

1. エディターで**`week04-exercises`**を開き、`requirements.txt`と`week04_common.py`を確認します。
2. **ファイル → 新しいテキストファイル → 名前を付けて保存**で、同じ場所に**`my_batman_tools.py`**を作ります。**ZIPには入っていないので、ここで作成してください。**
3. 下のコード全体を貼り付け、Windowsは**Ctrl + S**、Macは**Command + S**で保存します。
4. 拡張子が`.py`で、`.py.txt`ではないことを確認します。`.venv`、`lessons`、`assets`の中には保存しません。

まずコード内の検索語とURLを使い、それぞれの戻り値を読みます。ページを取得できない場合はエラーを記録し、自分のブラウザでも出典を確認してください。

**このファイルの役割 — `my_batman_tools.py`：**ウェブ検索、1ページの読み込み、固定座標による計算ツールの確認を行います。LLMは使いません。ターミナルの出力と出典ページを調べます。

```python title="my_batman_tools.py"
from week04_search import WebSearchTool, PageExcerptTool
from week04_tools import cargo_time

print("Same-coordinate classroom estimate:", cargo_time(40.7128, -74.0060))
print(WebSearchTool()("Batman Wollaton Hall filming official"))
print(PageExcerptTool()("https://wollatonhall.org.uk/hall-and-museum/history/", focus="Wayne Manor Batman"))
```

??? info "コードの説明を読む"

    | コード | 意味 |
    | --- | --- |
    | `from ... import ...` | 配布された上限付きの検索・ページ閲覧クラスと計算ツールを読み込みます。 |
    | `cargo_time(40.7128, -74.0060)` | ゴッサムと同じ座標を直接計算します。モデルは使いません。 |
    | `WebSearchTool()("...")` | ツールを作って検索語を渡し、検索サービスから抜粋とURLを取得します。 |
    | `PageExcerptTool()("...", focus="...")` | 最大1,600文字の関連するページ抜粋を取得します。Chromeを操作する処理ではありません。 |

    検索結果は出典を探す手掛かりです。ブラウザで出典を開き、抜粋が主張を裏付けるか確認してください。出力上限は維持します。抜粋はページの一部なので、確認できない点はメモに残します。

**実行：**`python my_batman_tools.py`。**確認すること：**同じ座標の概算が`1.0`になり、検索にURLが返り、ページ閲覧では文章か明確なエラーが返ることです。`evidence.md`に検索結果のURLを1つと、主張を裏付けるか判断できる文章を残します。取得を拒否された場合は失敗として記録し、別の信頼できる出典を確認します。

配布された`week04_tools.py`を開き、`cargo_time`を探します。次へ進む前に関数を読んでください。自分のプログラムではこの関数をインポートします。式は`round(distance_km * 1.1 / 750 + 1, 2)`です。架空のゴッサム`(40.7128, -74.0060)`からの大圏距離に10%を加え、750 km/hで割り、固定の1時間を加えています。**授業用の貨物航空輸送の概算**で、実際の運航予定ではありません。緯度と経度を受け取って時間を返す関数であり、座標の検索や撮影地の確認はしません。

**計算の確認：**同じ座標でもゼロではなく`1.0`になるのはなぜですか？速度の仮定を下げたら時間は増えますか、減りますか？仮定した値と、出典が必要な値を分けて説明してください。

??? success "概算を確認する"

    距離がゼロでも固定の1時間が残ります。速度を下げると距離÷速度が大きくなります。座標は出典で裏付ける入力で、速度、距離の割増、固定時間は授業用の仮定です。計算が正しくても、撮影地という主張が正しいとは限りません。

### 4. エージェントを1体ずつ作る { #build-team }

**目標：**Web調査役と管理役を作り、管理役が調査を委任できるようにつなぎます。

1. エディターで**`week04-exercises`**を開き、`requirements.txt`と`week04_common.py`を確認します。
2. **ファイル → 新しいテキストファイル → 名前を付けて保存**で、同じ場所に**`my_batman.py`**を作ります。このファイルはZIPにはありません。
3. **同じファイル**に**4A → 4B → 4C → 4D**の順で追加します。各ブロックは前の内容の下へ貼り付け、既存部分を置き換えたりインポートを重複させたりしません。字下げは表示どおりに保ちます。
4. 各段階で**Ctrl + S**または**Command + S**で保存します。拡張子は`.py`です。**4Dが終わるまでは実行しません。**それ以前はオブジェクトの作成だけで、実行するタスクがまだありません。
5. 古い`my_batman.py`がある場合は結果を保存してから内容を一度消し、手順どおりに作り直します。古い完成コードの下に追加しないでください。

**このファイルの役割 — `my_batman.py`：**自分で作る2体のエージェントを、Groqとウェブ調査ツールで動かします。管理役が調査を頼み、その結果を使ってローカルの計算・レポートツールを呼びます。最初の小さなタスクはターミナルに受け渡しを表示し、後の全体タスクでは`outputs/batman-report.html`を生成できます。

#### 4A. インポートとモデル接続を用意する { #4a-start-the-file-imports-and-model }

最初に次のブロックを貼り付けます。インポートだけではエージェントは作られません。

```python title="my_batman.py"
from smolagents import CodeAgent
from week04_common import build_model, agent_options, run_task
from week04_search import WebSearchTool, PageExcerptTool, ResearchBudget
from week04_tools import cargo_time, save_report

model = build_model(max_tokens=800)
```

??? info "4Aの説明 — 接続を共有する"

    `CodeAgent`はこの後2回使うクラスです。ほかのインポートは接続・検索・計算・レポート用の補助機能を読み込みます。`build_model(max_tokens=800)`は出力の上限を小さくしたGroq接続を準備し、ファイル実行時に必要ならキーを求めます。ここでは検索もエージェントの作成もしません。接続を共有しても履歴は別です。

**確認A：**この時点でエージェントを何体作りましたか？

??? success "解答A"

    **0体です。**クラスのインポートやモデル接続の準備は、`CodeAgent(...)`の呼び出しではありません。

#### 4B. Web調査役を作る { #4b-create-the-web-specialist }

`model = build_model(max_tokens=800)`の下に追加します。これが**最初のエージェント**です。次へ進む前に、名前、役割の説明、モデル、ツールを自分のファイルで示してください。

```python title="my_batman.py"

budget = ResearchBudget(max_searches=1, max_pages=2)
specialist = CodeAgent(
    tools=[WebSearchTool(budget=budget), PageExcerptTool(budget=budget)],
    model=model,
    name="web_specialist",
    description="Researches ONE named place per call. Visit sources and return a concise claim, URL and quote. Seek coordinates only when explicitly requested. Respect tool limits; stop after sufficient evidence or mark gaps. Return at most 500 characters.",
    **agent_options(max_steps=4, compact=True),
)
budget.bind(specialist)
```

??? info "4Bの説明 — 専門役を作る"

    | 設定 | 意味 |
    | --- | --- |
    | `specialist = CodeAgent(...)` | 別個のエージェントを作り、変数`specialist`に保持します。 |
    | `budget = ResearchBudget(max_searches=1, max_pages=2)` | 1タスクにつき検索1回、ページ取得2回までとします。失敗や拒否も数え、同じURLの再試行は拒否します。 |
    | `tools=[WebSearchTool(budget=budget), PageExcerptTool(budget=budget)]` | 2つのツールで同じ回数制限を共有します。検索は最大2件の短い結果、ページ閲覧は最大1,600文字の関連する抜粋を返します。 |
    | `model=model` | 4Aのモデル接続を渡します。 |
    | `name="web_specialist"` | 管理役が呼ぶ名前です。Pythonの変数名とは役割が異なります。 |
    | `description=...` | いつ委任し、どの根拠を返すかを管理役に伝えます。 |
    | `**agent_options(max_steps=4, compact=True)` | 専門役を最大4アクションステップ、各表示を最大1,800文字に制限します。 |
    | `budget.bind(specialist)` | 回数制限をこの専門役のタスクに結び付けます。新しい委任では履歴とカウンターがリセットされます。同じタスク内で呼び出しを増やしても上限は超えられません。 |

**確認B：**この専門役は、登録されたツールとして`save_report`を使えますか？

??? success "解答B"

    **使えません。**登録した独自ツールは検索とページ閲覧です。レポートツールは管理役へ渡します。

#### 4C. 管理役を作ってチームをつなぐ { #4c-create-the-manager-and-connect-the-team }

次のブロックを追加します。これが**2体目のエージェント**です。作成済みの専門役をつなぐ行を探してください。同じモデルを使うだけでは連携しません。

```python title="my_batman.py"

manager = CodeAgent(
    tools=[cargo_time, save_report],
    model=model,
    managed_agents=[specialist],
    **agent_options(max_steps=3, compact=True),
)
manager.visualize()
```

??? info "4Cの説明 — 管理役と接続"

    `manager = CodeAgent(...)`は独自の履歴を持つ別のエージェントを作ります。`cargo_time`と`save_report`は、ここでは呼ばずに関数名を登録します。`managed_agents=[specialist]`で専門役へ委任できるようになります。`visualize()`は構成を表示しますが、委任が実行された証拠ではありません。管理役は専門役の返答を待つため、この例は並列実行ではありません。

**確認C：**実行前に、コードからチームの構成を描いてください。検索するのは誰、保存するのは誰でしょうか？どの行を消すと委任できなくなりますか？

??? success "解答C"

    管理役には`cargo_time`、`save_report`とWeb調査役があり、Web調査役には`web_search`と`visit_webpage`があります。組み込みの`final_answer`も表示されることがあります。`managed_agents=[specialist]`を消すと、専門役への接続がなくなります。

#### 4D. 2体を作った後でタスクを追加する { #4d-add-the-tasks-only-after-both-agents-exist }

同じファイルの末尾へ追加します。最初は撮影情報1件を確認する`ONE_LOCATION_TASK`を使います。`TASK`には、手順6で使う4地点の依頼が入っています。

```python title="my_batman.py"

TASK = """Alfred needs three Batman filming locations and one supercar factory.
Use at most FOUR separate web_specialist calls, ONE named candidate per call:
Wollaton Hall, Knebworth House, Mentmore Towers, and Lamborghini Sant'Agata Bolognese.
Use ONE delegation per manager action step; do not combine delegations in a loop.
These are candidates to VERIFY, not facts to assume. For each, request a supported
filming/factory claim, coordinates, source_url, coordinate_source_url and a short
evidence quote. Ask the specialist to use focused page excerpts, at most one search
and three page attempts, and return one compact record under 500 characters.
Preserve each record before the next delegation. Do not request all four places
in one specialist call. Do not repeat a failed delegation or invent missing data.
If four supported rows are unavailable, report the gaps without saving a complete report.
Otherwise calculate all four cargo estimates and call save_report in ONE Python
action using the compact rows; do not print the whole JSON again. Then finish with
the report path, sources and assumptions. Keep responses and printed output short.
"""

ONE_LOCATION_TASK = """Delegate ONCE to web_specialist: check ONLY whether
Wollaton Hall was used as Wayne Manor in a Batman film. First read
https://wollatonhall.org.uk/hall-and-museum/history/ with focus="Wayne Manor Batman".
If blocked or insufficient, use at most one search and one alternate page.
Stop as soon as a relevant page supports the claim. Do NOT research coordinates,
transport, opening times or other places. Return the claim, source URL, one short
quote and uncertainty in at most 500 characters. If unsupported, mark it missing.
The manager should preserve that evidence and finish. No calculation or report.
"""

run_task(manager, ONE_LOCATION_TASK)
```

??? info "4Dの説明 — 準備と実行を分ける"

    三重引用符で、複数行のタスクを1つの文字列として保存します。`TASK`を定義しただけでは実行しません。`run_task(manager, ONE_LOCATION_TASK)`で、小さな依頼を使う管理役のループが始まります。管理役は別に作った専門役を呼べます。専門役も独自のループを実行して、根拠を返します。

**確認D：**どの行からモデルの判断が始まりますか？構成図だけで専門役が呼ばれたと分かりますか？

??? success "解答D"

    `run_task(manager, ONE_LOCATION_TASK)`でタスクが始まります。図は設定の確認です。実際の委任は`web_specialist(task=...)`の呼び出しで確認します。

**実行前に：**インポートと接続、専門役の作成、管理役の作成、2つのタスク、1つの`run_task`呼び出しがあることを確認します。2体を作るコードとつなぐ行をペアに説明するか、`evidence.md`に記してから保存してください。

### 5. 撮影情報を1件確認する { #small-handoff }

**最初は撮影情報だけを確認します。**座標の調査は手順6で行います。返された引用を出典と照合してください。

| 上限 | 最初の実行 |
| --- | --- |
| 管理役のアクションステップ | 3 |
| 専門役のアクションステップ | 委任1回につき4 |
| 検索回数 | 委任1回につき1回、短い結果は最大2件 |
| ページ取得回数 | 委任1回につき2回。失敗も数え、同じURLは再試行しません。 |
| ページ抜粋／表示する観測結果 | 最大1,600／1,800文字 |
| モデルの出力 | 1応答につき800トークン。入力トークンの上限ではありません。 |

これは上限であり、必ずその回数になるわけではありません。ステップ上限に達すると、フレームワークが最終回答のためにもう1回モデルへ問い合わせることがあります。取得の拒否や調査回数の上限に達したら、再試行を増やすのではなく、不足情報を短く伝える結果にします。

4A〜4Dを保存したら、最終行が**`run_task(manager, ONE_LOCATION_TASK)`**になっているか確認します。

**実行：**`python my_batman.py`。必要ならGroqキーを入力します。最初に構成が表示され、その後、管理役からWollaton Hallの依頼が専門役へ渡るはずです。

**確認すること：**自分の実行から短い抜粋をコピーし、`evidence.md`の**Topic 15 → One-location handoff**に残してください。

| 段階 | 自分の実行で探すもの |
| --- | --- |
| 管理役のアクション | 実行された`web_specialist(task=...)`。 |
| 専門役のアクション | ページ閲覧と、必要な場合の検索。最初の出典で確認できれば検索は不要です。 |
| 観測結果 | 返された文章、または明確な取得失敗。 |
| 専門役の報告 | 撮影情報、出典URL、短い引用、不確かな点。ここでは座標を求めません。 |
| 管理役の回答 | 出典と限界が保たれているか。 |

**1. 管理役が`web_search`を直接呼ぶことと同じですか？**

??? success "解答1 — 2つのループ"

    違います。管理役は独自のループを持つ`web_specialist`を呼び、専門役は複数のツール操作をしてから返答できます。`web_search`は、その専門役のループ内にあるツール操作です。

**2. このテストで`outputs/batman-report.html`は生成されるべきですか？**

??? success "解答2 — 小さなテストの出力"

    いいえ。1地点のタスクは計算とレポート作成を求めていません。結果はターミナルに表示されます。レポートは次の全体タスクで作るため、空のHTMLを自分で作らないでください。

**3. 委任が起こらない、ページ取得が失敗する、ステップ上限に達する場合はどうしますか？**

??? success "解答3 — 未完了の実行"

    失敗内容を記録し、未完了とします。最終回答だけでは十分ではありません。4つの作成段階、2体を作るコード、`managed_agents`、ツールの直接確認を見直します。上限は保ち、繰り返し再実行せず、[調査上限の対処](#research-limits)で次の確認点を調べてください。

### 6. 4地点を調べてレポートを確認する { #full-run }

全体のタスクは**撮影地3か所と工場1か所**です。ただし、**専門役には1回の委任で1地点だけ**を依頼します。各呼び出しでは専門役の履歴が新しくなり、前の地点のページ本文が蓄積しません。管理役は返された短い記録だけを保持します。

既存の**`my_batman.py`**で次の変更を行い、保存します。

1. `ResearchBudget(max_searches=1, max_pages=2)`を**`ResearchBudget(max_searches=1, max_pages=3)`**に変更します。用途の出典、座標の出典、必要なら代わりの出典1つを確認する余地を作ります。
2. 専門役の`agent_options(max_steps=4, compact=True)`を**`agent_options(max_steps=5, compact=True)`**に変更します。
3. 管理役の`agent_options(max_steps=3, compact=True)`を**`agent_options(max_steps=6, compact=True)`**に変更します。
4. 最終行を`run_task(manager, ONE_LOCATION_TASK)`から**`run_task(manager, TASK)`**へ変更します。

抜粋、表示、モデル出力の上限はそのままにします。完成させるために上限を上げないでください。タスクは最大4回の短い委任、その後のまとめた計算と保存、最終回答を求めます。予算内で主張や座標を確認できなかった場合は、その不足を明示します。

**確認すること：**管理役の各アクションステップで、`web_specialist(task=...)`が1地点だけを指定しているか見ます。専門役のステップ番号はタスクごとに最初へ戻ります。管理役は返された根拠付きの記録を保持し、前の結果を再調査させないようにします。4件を1つのアクションで表示すると最後が切り詰められることがあるため、委任は別々のステップで行います。

**実行：**`python my_batman.py`。ターミナルを確認します。`save_report`が成功すると、`week04-exercises`内に**`outputs/batman-report.html`**が作られます。エクスプローラー／Finderで`week04-exercises` → `outputs`を開き、`batman-report.html`をダブルクリックしてブラウザで読みます。ファイルがない場合は、ターミナルの`save_report`呼び出しとエラーを探してください。

生成されたHTMLを、ファイルマネージャーで既存の**`evidence-files`**に**`batman-report.html`**という名前のままコピーします。新しいプログラムではなく、出力の控えです。出典と実行記録も`evidence.md`に残します。保存ツールは時間を再計算し、表と座標図を描きますが、入力形式やURLの形を確認するだけで、ページが主張を裏付けるかは検証しません。ファイルができても、すべての出典と座標を確認してください。

[![HFのBatman調査例の出力地図](images/huggingface-week04/batman-output-map.png)](images/huggingface-week04/batman-output-map.png){ .course-figure-link }

??? info "この図の説明を読む"

    HFの調査例で得られた地図です。マーカーの位置、色、名称、地点間の違いに注目してください。見やすい地図でも、各地点の撮影・工場という区分と座標に出典が必要です。この画像を自分の調査結果として提出するのではなく、表示の読み方を比較する参考にします。自分のレポートは地理的な背景地図を使わない簡略な経度・緯度の図なので、見た目は異なります。

[元の大きさで開く](images/huggingface-week04/batman-output-map.png)

*元の出力例を変更せず使用：[Hugging Face Multi-Agent Systems](https://huggingface.co/learn/agents-course/en/unit2/smolagents/multi_agent_systems)。位置、色、ラベル、根拠を考える参考です。自分の調査の解答例ではありません。*

**最終チェックと別エージェントの違い：**smolagentsでは、回答を受理する前にPythonの`final_answer_checks`を実行できます。出力の欠落やデータの不整合を拒否できますが、このコールバックが自動で3体目のエージェントになるわけではありません。ここでは自分で出典と地図を確認します。任意課題では、別のエージェントに1件の調査記録を確認させます。それぞれのチェックが何を根拠に判断できるか比べてください。

自分の出力は、地理的な背景を持たない簡略な経度・緯度の座標図です。凡例では概算5時間未満が紫、5時間以上が赤です。整った図でも、座標の誤り、マーカーの重なり、裏付けのない撮影情報が含まれることがあります。

**地図の確認：**マーカーを1つ選び、表の行と2つの出典を確認して時間を再計算します。経度の符号を間違えると反対側へ移るでしょうか？色は概算と一致していますか？簡略な地図と輸送の仮定について、限界を1つずつ記してください。

??? success "地図の解答1 — 位置と経度の符号"

    マーカー名を表と両方の出典に照合します。経度の符号を反転すると、経度0の線を挟んで横方向の位置が反転します。西側の地点が大きく東へ移ることがあります。もっともらしい位置だけでは、座標の裏付けになりません。

??? success "地図の解答2 — 時間と色"

    出典で確認した座標で`round(distance_km * 1.1 / 750 + 1, 2)`を計算します。凡例どおり、5時間未満は紫、5時間以上は赤です。色が違う、座標に根拠がない場合は修正が必要です。

??? success "地図の解答3 — 限界と最終チェック"

    座標図には地理的な背景がなく、マーカーが重なることもあります。輸送概算には実際の経路、運航予定、荷役などを含めていません。Pythonのチェックはファイルやデータの条件を調べ、検証役はモデルとツールのループで出典を確認します。どちらも適切な根拠がなければ、主張の正しさを証明できません。

### 7. 作ったチームを確認して説明する { #audit }

**結果の確認：**レポートとターミナルの出力を使い、次の回答を`evidence.md`に書きます。

**1. すべての行の用途と座標に根拠がありますか？**撮影地3か所と工場1か所について、各行の両方の出典を開きます。裏付けのある例を1つと、見つかった不足点を書いてください。

??? success "解答1 — 根拠を確認する"

    主張の出典は撮影・工場という用途を、座標の出典は計算に使った地点を裏付ける必要があります。URLが開くことや数字がもっともらしいことだけでは不十分です。不足を記録し、裏付けのない4行を完了としないでください。

**2. モデルの判断と、配布されたPythonツールの処理はどこで分かれますか？**

??? success "解答2 — モデルとツールの担当"

    Groqがアクションとレポートの判断を生成し、PC上のPythonが検索・ページ取得・計算・描画を実行します。`cargo_time`は入力された座標から計算し、座標の発見や検証はしません。`save_report`は渡された行を表示し、引用先が主張を裏付けるかは確かめません。

**3. 1体のエージェントは、このチームより必ず劣りますか？**

??? success "解答3 — チームの利点と負担"

    いいえ。小さな仕事では1体のほうが単純な場合もあります。チームは役割と履歴を分ける一方、問い合わせ、連携、情報欠落が増える可能性があります。人数ではなく、根拠のある結果で評価します。

**確認：**2つの必須Pythonファイル、1地点と全体タスクの実行記録、確認した出典、概算1件の再計算、問題への回答を保存してください。全体タスクが成功した場合はレポートとそのコピーも残します。失敗した場合はエラーと未完了の確認項目を記します。

### サービスがリクエストを拒否した場合 { #research-limits }

- **ページの403：**サイトが取得を拒否しています。試行回数に数えるため、許された別の出典を使うか、取得不可と記します。同じURLを再試行しません。
- **Research limit reached：**調査回数の上限です。得られた根拠と不足項目を返します。上限に達したことは、主張が誤りだという証明ではありません。
- **Groqの413／request too large：**実行を止めます。補助ファイルが最新のZIPと一致し、`ONE_LOCATION_TASK`を使っているか確認してから、新しい小さな実行を始めます。待つだけでは、大きくなった履歴は小さくなりません。
- **Groqの429：**実行を止め、サービスが示す待機時間を守ってから新しい実行を始めます。トークンとリクエストの上限はアカウントで共有されます。今回の制限は使用量を減らすもので、利用枠を保証するものではありません。

[Groqのレート制限の説明](https://console.groq.com/docs/rate-limits)も確認できます。文字数の上限とトークン数は同じではありません。拒否を避けようとして、ページ全体をタスクに貼り付けたりステップ上限を増やしたりしないでください。

### 8. 任意課題：検証役のエージェントを加える { #optional-verifier }

Batman調査の結果1件を独立して確認する、3体目のエージェントを追加します。2体の演習を終えてから、次の手順でコピーを作ってください。

1. 保存済みの動作する**`my_batman.py`**をエディターで開きます。
2. **名前を付けて保存**で、同じ`week04-exercises`内に**`my_batman_verified.py`**としてコピーします。`my_batman.py`は2体版として残します。
3. 両方のファイルがあることと、現在編集しているのが**`my_batman_verified.py`**であることを確認します。このファイルはZIPには入っていません。
4. コピー内の`specialist = CodeAgent(...)`の**後**、`manager = CodeAgent(...)`の**前**に、検証役を自分で作ります。両方の専門役を管理役へ登録し、同じモデル接続を使います。変更はこのコピー内で行います。
5. コピーの`TASK`を、自分で書いた**1行分の調査と検証の依頼**に変えます。既存レポートの1件を再確認する候補として使い、両方への委任と根拠付きの判定を求めます。**新しいレポートは保存しません。**各専門役は4ステップ、各自の検索1回・ページ2回の上限、管理役は4ステップにします。最終行が新しい`TASK`を使うことを確認し、保存します。困ったら下のヒントを使ってください。

**このファイルの役割 — `my_batman_verified.py`：**既存のチームに、候補1件を確認する独立したループを追加します。実際の調査ツールを使い、2つの受け渡しと判定をターミナルに表示します。既存のレポートと比較し、そのファイルは上書きしません。4件すべてを確認するなら、6ステップの全体タスクに8回の委任を詰め込まず、1件ずつ新しい実行に分ける必要があります。

追加する前に、次を決めてください。

1. 独自の名前、説明、狭く定めた検証の担当を決めます。必要なツールと、出典を自分で読み直す理由を考えます。
2. 各行の判定を`pass`、`fail`、`uncertain`とし、確認したURL、裏付けた／否定した主張、修正点または不足情報を返す形式を決めます。信頼できる判定には何が必要でしょうか？
3. いつ検証役を呼び、各判定を管理役がどう扱うか決めます。レポートを書けるのは誰で、裏付けのない行を止めるのは誰ですか？
4. 新しい`CodeAgent`を作り、管理役の`managed_agents`にWeb調査役と**並べて**登録します。管理役が記録を受け入れる前に、出典付きの1件を検証役へ渡すようタスクを変更します。
5. 図に管理役と異なる2体の専門役があることを確認し、実行記録では両方が実際に呼ばれることを確認します。

**誤りを入れるテスト：**同じ任意ファイルで、通常の最終呼び出しを`evidence.md`に控えます。一時的に最終行を`run_task(manager, "YOUR FALSE-CLAIM TEST REQUEST")`へ変え、自分のテスト依頼を書きます。たとえば「Wollaton Hall is a supercar factory（Wollaton Hallはスーパーカー工場）」という意図的な誤りと、[公式の歴史ページ](https://wollatonhall.org.uk/hall-and-museum/history/)を渡し、保存せず判定するよう頼みます。予想を書き、検証役がページを読んで否定または根拠不足と判断するか調べます。メモには意図的なテストの誤りと明記し、調査結果として扱わないでください。

**任意の実行：**保存して`python my_batman_verified.py`で誤りのテストを行います。その後`run_task(manager, TASK)`へ戻して保存し、1件の調査・検証を実行します。両方の結果を`evidence.md`の**Topic 15 → Optional verifier**に記します。誤りを見つけたか、独自に確認した出典を返したか、それとも調査役の文章を繰り返しただけか、既存レポートと比較してください。増えたモデル呼び出しと残った不確かさも記します。

??? tip "ヒント1 — 別のエージェントを作る"

    検証役独自の`name`、`description`、`CodeAgent`を用意します。既存の専門役を別の変数へ代入するだけでは、新しいループにはなりません。

??? tip "ヒント2 — 新しい役をつなぐ"

    コピーの管理役に`managed_agents=[specialist, verifier]`を使います。検証役専用の`ResearchBudget(max_searches=1, max_pages=2)`、上限付きの検索・ページツール、最大4ステップを与え、その予算を検証役へ`bind`します。調査役とカウンターを共有せず、レポートツールも与えません。1回につき1件を確認して、短い判定を返します。

??? tip "ヒント3 — 実際の検証を依頼する"

    登録だけでは実行されません。管理役が出典付きの1件を渡して判定を求めるようタスクを変更します。`fail`や`uncertain`の扱いを定め、この任意課題では新しいレポートを保存しません。

??? success "検証役の解答1 — 名前・担当・ツール"

    用途と座標を独立して確認する役が適切です。独自の名前と検索・ページ閲覧ツールを持たせ、調査役の自信ではなく引用先を調べさせます。

??? success "検証役の解答2 — 役に立つ判定"

    各主張についてpass／fail／uncertain、確認したURL、根拠、修正点または不足項目を返します。実際に確認した出典がなければ、単に別の主張を増やすだけです。

??? success "検証役の解答3 — いつ記録を受け入れるか"

    調査後、記録を受け入れる前に検証役を呼びます。根拠付きの判定か、不確かな理由を返し、予算を使い切った後に修正のループを続けません。このテストは既存レポートを変更しません。後で検証済みのレポートを作る場合も、書くのは管理役です。

??? success "検証役の解答4 — 構成と実行"

    図には管理役と異なる2体の専門役が必要です。そのうえで、実行記録に両方の呼び出しがあるか確認します。図だけでは実行した証拠になりません。

??? success "検証役の解答5 — 意図的な誤り"

    建物の撮影・歴史ページは、スーパーカー工場という主張を裏付けません。ページを読んだ検証役は否定するか、裏付けなし／不確かと判定するはずです。見逃したら実際の結果を残します。その後、通常の1件のタスクに戻して判定を比べます。エージェントを増やしても、有効な修正を保証するわけではありません。

??? success "任意課題で示すこと"

    図に3体目があるだけでは不十分です。追加した役、2つ目の委任、ページの観測、根拠付きの判定を示してください。検証役も誤ることがあるため、出典は自分でも確かめます。

### コードを振り返る { #reference }

**4Bで専門役、4Cで管理役**を作りました。ファイル内でそれぞれを作る場所と、`managed_agents=[specialist]`でつなぐ場所を探してください。手順6では短い抜粋と新しい専門役の履歴を保ったまま、全体タスクへ切り替えました。任意の検証役を加えた版と比較できるよう、2体版も残します。

**出典：**題材、階層構成、概算式、元の図は[HF Multi-Agent Systems](https://huggingface.co/learn/agents-course/en/unit2/smolagents/multi_agent_systems)を基にしています。Apache-2.0。調査にはGroqを使い、レポートは簡略な座標図で表示します。

**次：**[16 · 画像・ブラウザエージェント](week-4-vision-browser.md)。説明、受け渡しの結果、出典と地図の確認を[完了確認](week-4-completion.md)まで残してください。
