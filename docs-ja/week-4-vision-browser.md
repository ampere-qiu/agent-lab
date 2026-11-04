# 16 · 画像・ブラウザエージェント { #week-4-vision-browser }

**目標：**画像を読むエージェントと、スクリーンショットを使ってウェブページを確認するエージェントを作ります。

**始める前に：**[第04週の準備](week-4-preview.md#exercise-files)と、[記録用の`evidence.md`、`evidence-files`の作成](week-4-preview.md#evidence-file)を終えてください。同じ`week04-exercises`内の、有効化したターミナルを使います。ブラウザの実習にはChromeが必要です。

| ファイルなど | 状態と使い方 |
| --- | --- |
| `week04_common.py`、`week04_browser.py`、`prepare_visuals.py` | ZIPに入っています。指定されたときに既存のファイルを開きます。 |
| `assets/venue.png`、`assets/venue.html` | 準備で配布の`prepare_visuals.py`を実行すると生成されます。ない場合はAの前に実行します。 |
| `my_vision.py`、`my_browser_check.py`、`my_browser.py` | 配布されません。下の手順で別々に作ります。 |
| `before.png`、`after.png` | ブラウザの直接操作テストで生成されます。成功するまではありません。 |
| `outputs/browser-*.png` | ブラウザエージェントのコールバックが生成します。実行するまではありません。 |
| `evidence.md`、`evidence-files` | 準備で自分で作成しました。同じメモとフォルダーに結果を残します。 |

エージェントの回答はターミナルで読みます。会場図と保存したスクリーンショットは画像ビューアーで確認します。ブラウザ演習では別のChromeウィンドウが開きます。

## いつ、どこで実行するか { #where-and-when }

**Pythonはコードエディターに書いて保存し、コマンドはターミナルで実行します。**Windowsは**コマンドプロンプト**、Macは**ターミナル**を使い、第04週の環境を有効にしてください。現在のフォルダーは、`requirements.txt`、補助ファイル、自分の`my_*.py`がある**`week04-exercises`**です。プロンプトに**`(.venv)`**があるか確認します。新しいターミナルを開いた場合は、[第04週のフォルダー移動と有効化](week-4-preview.md#activate-environment)を先に行ってください。

各**実行**欄のコマンドだけを入力し、**Enter**を押します。Pythonの`>>>`、教材のウェブページ、Chromeの開発者コンソールには入力しません。処理が終わり、ターミナルの入力待ちに戻ってから次のコマンドへ進みます。

| 段階 | 実行するタイミング | コマンド |
| --- | --- | --- |
| Aの前 | 会場のファイルがない場合のみ。ページを編集する前に行います。 | `python prepare_visuals.py` |
| B・最初の画像 | B1〜B3を`my_vision.py`に追加して保存し、予想を書いた後。 | `python my_vision.py` |
| B・質問の変更 | 最初の回答を残し、タスクの質問を変えて同じファイルを保存した後。 | `python my_vision.py` |
| C・ブラウザの直接確認 | `my_browser_check.py`を作成して保存した後。Dの前に成功させます。 | `python my_browser_check.py` |
| D・ブラウザエージェント | Cが成功し、D1〜D3を`my_browser.py`に追加・保存した後。 | `python my_browser.py` |
| D・ページの変更 | 元のスクリーンショットを保存し、`assets/venue.html`を編集・保存し、予想を書いた後。 | `python my_browser.py` |

すべて**同じ、有効化済みの`week04-exercises`のターミナル**で実行します。AはPythonを動かさず画像を観察します。`my_vision.py`はB1〜B3、`my_browser.py`はD1〜D3を終えてから実行してください。CとDではプログラムがChromeを開いて操作するため、HTMLを先に手動で開く必要はありません。

架空の会場図を使います。画像には部屋の名前があり、ブラウザのページはクリック後に追加の利用案内を表示します。検索結果や取得したページの文章と、実際に描画された画面を見て操作することは区別してください。

## 画像が観測としてループに入る仕組み { #vision-memory }

画像と言語を扱うモデルは、文章だけでなくピクセルも受け取ります。最初に`images=[image]`を渡すと、タスクの入力に画像が付きます。ブラウザでは操作後に初めて重要な情報が現れることがあるため、その変化を判断するには新しいスクリーンショットが必要です。

[![CodeAgentの最初の画像入力と操作後のスクリーンショット観測を示すHFの図](images/huggingface-week04/vision-memory.png)](images/huggingface-week04/vision-memory.png){ .course-figure-link }

??? info "この図の説明を読む"

    最初の画像は、依頼と一緒に**TaskStep**へ渡されます。その後、モデルがアクションを選び、PCが実行します。ブラウザの操作後に撮った画像は**ActionStep**の観測となり、次のモデル問い合わせへ送られます。最初の画像を与えることと、操作後の新しい画面を観測させることを分けて読んでください。

    図の記録名には古い表記もあります。この演習のコードでは、画像を入れる場所は`ActionStep.observations_images`、履歴は`agent.memory.steps`です。PNGをディスクへ保存するだけではモデルに画像は届きません。コールバックが観測へ追加し、その画像を受けたモデルが次の判断をします。図をクリックすると拡大できます。

[元の大きさで開く](images/huggingface-week04/vision-memory.png)

*元の図を変更せず使用：[HF Vision and Browser Agents](https://huggingface.co/learn/agents-course/en/unit2/smolagents/vision_agents)。タスクの画像から、その後のアクションのスクリーンショットへ流れをたどってください。*

図で、タスク入力から操作後の観測へ画像がどう渡るかを確認します。コールバックが撮影し、次の行動を決めるのはモデルです。使うコードでは`ActionStep.observations_images`に画像を付け、`agent.memory.steps`に履歴を保存します。

**コードを書く前に：**最初の画像を使うループとブラウザのループを1つずつ描き、新しい画像が入る場所を示してください。コールバックがPNGを保存するだけで、観測に付けなかった場合を予想します。後のブラウザ実行では、操作、画像、その後の回答を対応させます。

??? success "考え方を確認する"

    ファイルを保存することとモデルへ画像を届けることは別です。後の問い合わせで送る観測に画像を含める必要があります。それがなければ、モデルは古い画面や推測に基づいて答える可能性があります。

別の例として、任意の[HFブラウザ実演動画](https://www.youtube.com/watch?v=rObJel7-OLc)も見られます。操作の直後で止め、次のスクリーンショットを探してください。以下の実習はダウンロード内の会場図を使います。

## A. 画像を見て予想する { #predict }

エクスプローラー／Finderで**`week04-exercises` → `assets` → `venue.png`**を開きます。**準備で生成プログラムを実行すれば存在する画像**です。空の同名ファイルを作らないでください。ない場合は上の準備リンクへ戻ります。

モデルを呼ぶ前に、`evidence.md`の**Topic 16 → Image predictions**に次の回答を書いてください。

**1. 画像から直接分かることを3つ、この画像では答えられない質問を1つ挙げてください。**

??? success "画像の解答1 — 見える事実と不足する情報"

    例として、左上にENTRANCE（入口）、右上にSTAGE（舞台）、左下にBUFFET（ビュッフェ）があります。右下にはEXIT（出口）があります。今その出口が開いているかは分かりません。実際に見えるものを3つ選び、本当に不足している情報を1つ挙げます。

**2. 出口は開いていますか？**

??? success "画像の解答2 — 出口の利用状況"

    EXITのラベルはありますが、現在の開閉状況は示されていません。「出口の表示がある」は裏付けられても、「今利用できる」とは判断できません。

**3. 色の付いた四角形だけで、利用可能なバリアフリー経路を確認できますか？**

??? success "画像の解答3 — アクセシビリティ"

    できません。色や位置だけでは、段差、通路、扉の幅、現在の利用状況は分かりません。見える配置と、別の根拠が必要な情報を分けます。

予想を保存します。会場図を作る配布プログラムはLLMを使いませんが、次のプログラムでは使います。

## B. 画像エージェントを作る { #initial-image }

コードエディターの**新しいテキストファイル → 名前を付けて保存**で、**`week04-exercises`内の`week04_common.py`と同じ場所**に**`my_vision.py`**を作ります。配布ファイルではありません。**Ctrl + S**または**Command + S**で、拡張子を`.py`にして保存します。既存のファイルを置き換える場合は、先にコピーを残してください。

同じファイルへ**B1 → B2 → B3**の順に追加し、各段階で保存します。実行するのはB3の後です。

**このファイルの役割 — `my_vision.py`：**Groq上の画像対応モデルを使い、生成された会場図を読みます。独自の検索・ブラウザツールは登録しません。ターミナルの回答を、開いた画像と比較します。

### B1. 入力画像を読み込む { #b1-load-the-input }

最初にこのブロックを貼り付け、`assets/venue.png`を画像として開きます。

```python title="my_vision.py"
from pathlib import Path
from PIL import Image
from smolagents import CodeAgent
from week04_common import build_model, agent_options, run_task

root = Path(__file__).resolve().parent
image = Image.open(root / "assets/venue.png").convert("RGB")
```

??? info "B1の説明 — 画像オブジェクト"

    `root`は保存したスクリプト自身のフォルダーを示します。Pillowが生成済みのPNGを読み、色の形式を変えます。この段階ではエージェントを作らず、Groqへ画像も送りません。ファイル名の文字列だけでは画像入力になりません。

### B2. 画像エージェントを作る { #b2-create-the-image-agent }

B1の下に追加します。`tools=[]`と、トピック15のWeb調査役のツール一覧を比較してください。検索ツールがなくても、このエージェントには何ができるでしょうか？`evidence.md`に回答を書きます。

```python title="my_vision.py"

agent = CodeAgent(
    tools=[],
    model=build_model(),
    **agent_options(max_steps=3),
)
```

??? info "B2の説明 — 画像エージェントの作成"

    ここで新しい`CodeAgent`を作ります。`tools=[]`は独自の検索・ブラウザツールを登録しない指定です。組み込みの最終回答ツールは使えます。`model=build_model()`でGroqにつなぎ、`max_steps=3`でアクションの上限を指定します。画像は検索ツールではなく、次の段階で入力として渡します。

### B3. 画像とタスクを渡す { #b3-give-your-agent-the-pixels-and-a-task }

最後のブロックを追加し、同じファイルを保存します。実行前に、確認できそうなラベル1つと、分からない情報1つを予想してください。

```python title="my_vision.py"

run_task(agent,
    "Inspect this fictional venue plan. Name the labeled areas and their relative positions. Separate visible facts from assumptions. Can the image prove whether the exit is currently open? State uncertainty.",
    images=[image],
)
```

??? info "B3の説明 — パスではなく画像を送る"

    `run_task`で実行が始まります。`images=[image]`が実際の画像をタスクへ付けます。質問文にファイルパスを書くだけでは画像を添付できません。モデルが正しく読めたと決めつけず、自分の予想と回答を比較してください。

**確認：**どの段階でエージェントを作り、どの段階で画像を渡しますか？検索ツールがないのはなぜですか？

??? success "作成の解答 — 画像エージェント"

    **B2で作り、B3で画像を付けて実行します。**B3で渡した画像はウェブ検索なしで説明できます。B1は入力を読み込むだけです。独自ツールが空でも、LLMを使わないという意味ではありません。

**いつ：**B1〜B3をすべて追加・保存し、確認問題と画像の予想を書いた後です。**どこで：**現在のフォルダーが**`week04-exercises`**になっている、有効化済みのターミナルです。

**実行：**

```bash
python my_vision.py
```

必要ならGroqキーを入力し、最終結果が表示されて入力待ちに戻るまで待ちます。**確認すること：**ラベルや位置の説明を実際の画像と比べてください。裏付けられる記述と、不確か／裏付けのない記述を`evidence.md`に1つずつ残します。このプログラムは文章を表示し、新しい画像は生成しません。

**別の質問を試す：**元のタスク文と回答をメモに残します。既存の**`my_vision.py`**の下にある`run_task(...)`全体だけを、次のブロックに置き換えてください。上のインポート、画像の読み込み、エージェント作成は変えず、同じファイルへ保存します。

**変更の役割：**同じ画像と同じGroqエージェントに、段差のない経路について質問します。結果はターミナルに表示されます。

```python title="Replace only the run_task call in existing my_vision.py"
run_task(agent,
    "Describe a step-free route from ENTRANCE to BUFFET. Separate visible layout from missing accessibility information.",
    images=[image],
)
```

??? info "変更の説明を読む"

    変わるのはタスクの文章だけです。`images=[image]`で同じ画像を送り、同じ種類のエージェントとモデルを使います。同じ根拠に別の質問をした結果を比べられます。

**いつ：**最初のタスクと結果を`evidence.md`に残し、上のタスク呼び出しだけを変更して**`my_vision.py`を再保存した後**です。**どこで：**同じ**`week04-exercises`**の有効化済みターミナルです。

**再実行：**

```bash
python my_vision.py
```

結果を待ち、変更した質問と実際の回答を同じ`evidence.md`に記します。

**4. この画像だけで、段差のない経路を確認できますか？どの情報が不足していますか？**

??? success "画像の解答4 — 質問を変えた結果"

    できません。相対的な配置は分かっても、スロープ、段差、幅、通路の状態は確認できません。位置関係を説明し、足りないアクセシビリティ情報を示します。次のブラウザでは文章の利用案内が加わりますが、それも新しい観測であり、現地の経路を独立に確認したことにはなりません。

**確認：**2つの質問と回答の比較、回答1〜4を`evidence.md`に残します。`my_vision.py`は保存したまま使い、別の画像用プログラムは作りません。

## C. LLMなしでブラウザ操作を確認する { #browser-check }

1. エディターで**`week04-exercises`**を開き、`requirements.txt`と`week04_common.py`を確認します。
2. **ファイル → 新しいテキストファイル → 名前を付けて保存**で、同じ場所に**`my_browser_check.py`**を作ります。**ZIPには入っていません。ここで作成します。**
3. 次のコード全体を貼り付けます。
4. **Ctrl + S**または**Command + S**で保存します。`.py.txt`ではなく`.py`とし、`.venv`、`lessons`、`assets`の中には保存しません。

**このファイルの役割 — `my_browser_check.py`：**別のChromeでローカルの会場ページを開き、詳細ボタンを押し、`before.png`と`after.png`を保存します。Seleniumを使い、LLMは使いません。2つの画像を開いて、観測の変化を確認します。

```python title="my_browser_check.py"
from week04_browser import BrowserSession

browser = BrowserSession()
try:
    print(browser.tools[0]())
    browser.driver.save_screenshot("before.png")
    print(browser.tools[1]())
    browser.driver.save_screenshot("after.png")
    print("Compare before.png and after.png")
finally:
    browser.close()
```

??? info "コードの説明を読む"

    | コード | 意味 |
    | --- | --- |
    | `BrowserSession()` | 配布の補助クラスで別のChromeセッションを開始します。対応ドライバーを取得することがあります。LLMは使いません。 |
    | `browser.tools[0]()` | `open_venue`を直接呼び、生成済みのローカルHTMLを開きます。 |
    | 最初の`save_screenshot` | ターミナルの現在のフォルダーへ`before.png`を生成します。 |
    | `browser.tools[1]()` | `show_access_details`を呼び、ページのボタンをクリックします。 |
    | 2つ目の`save_screenshot` | クリック後の`after.png`を生成します。 |
    | `finally: browser.close()` | 途中で失敗してもChromeを閉じます。 |

    Chromeがすぐ閉じても、後で保存したPNGを確認できます。モデルを加える前に、ページと操作ツールが動くか調べるテストです。成功という文字列だけでなく、画像を確認してください。

**いつ：**`my_browser_check.py`にコード全体を貼り付けて保存し、`assets/venue.html`があることを確認した後です。**Dの作成・実行の前にこのテストを成功させます。** **どこで：**有効化済みの**`week04-exercises`**のターミナルです。

**実行：**

```bash
python my_browser_check.py
```

プログラムがChromeを開き、クリックし、撮影して自動で閉じます。ターミナルが入力待ちに戻るまで待ってください。Chromeやドライバーのエラーは、エージェントを動かす前に解決します。

**確認すること：**Chromeが閉じたら、エクスプローラー／Finderで`week04-exercises`直下の**`before.png`**と**`after.png`**を開きます。プログラムが生成する画像で、自分で作ったりダウンロードしたりしません。ない場合はエラーを確認します。再実行すると同名の画像は置き換わります。

**1. クリック後に何が変わりましたか？**

??? success "ブラウザの解答1 — 観測の変化"

    `before.png`には利用案内の段落がなく、`after.png`には「The east exit is closed for maintenance（東側の出口は整備のため閉鎖）」と「Use the north entrance for accessible entry（利用しやすい入口として北側を使用）」が表示されるはずです。自分の画像にその文字があるか確認してください。見えていなければ成功とはしません。

**2. この直接テストから何が分かり、何は分かりませんか？**

??? success "ブラウザの解答2 — 直接テストの範囲"

    ローカルページの読み込み、クリック、画像の変化を確認できます。モデルは使わないため、モデルがクリックを選んだことや、画像を受け取って理解したことは示せません。

`evidence.md`に両方の画像名、変わった文章、回答1〜2を記します。確認用にPNGを残し、画像の代わりにHTMLソースを貼らないでください。

## D. ブラウザエージェントを作る { #browser-loop }

**`week04-exercises`内のほかのプログラムと同じ場所**に**`my_browser.py`**を作ります。配布ファイルではありません。同じファイルへD1、D2、D3の順に追加し、保存します。古い版を置き換える場合は、先に作業のコピーを残してください。

このエージェントはローカルページを開き、詳細ボタンを押し、新しいスクリーンショットから質問に答えます。コールバックが各ブラウザ操作と、次にモデルが受け取る画像をつなぎます。

**このファイルの役割 — `my_browser.py`：**Groqがローカルページで行う操作を選び、操作後の画像を受け取ります。SeleniumがChromeを操作し、観測画像を`outputs/browser-*.png`に保存します。ターミナル、画像の順番、最終回答を確認します。

### D1. 必要な機能を読み込む { #d1-import-the-parts }

```python title="my_browser.py"
from smolagents import CodeAgent
from week04_common import build_model, agent_options, run_task
from week04_browser import BrowserSession
```

??? info "D1の説明 — ツールとスクリーンショット"

    `BrowserSession`が操作ツールと撮影コールバックを用意します。インポートだけではモデルを使うエージェントは作られません。次のブロックで`CodeAgent`を作ります。

### D2. ブラウザエージェントを定義する { #d2-define-the-browser-agent }

D1の下にこの関数を追加します。ブラウザツールと撮影コールバックを持つエージェントを作る関数で、D3から呼びます。

```python title="my_browser.py"

def build_browser_agent(model, browser):
    return CodeAgent(
        tools=browser.tools,
        model=model,
        step_callbacks=[browser.capture],
        **agent_options(max_steps=6),
    )
```

??? info "D2の説明 — 操作後の画像を受け取る"

    `tools=browser.tools`が開く・クリックする操作を登録します。`step_callbacks=[browser.capture]`は各ステップ後に画像を撮影して観測へ付けます。コールバックはPNGを`outputs`へ保存し、`ActionStep.observations_images`と現在のURLを設定し、古い画像を履歴から外します。保存だけではモデルに画像は届きません。コールバックは観測を用意し、操作を選ぶのはエージェントです。

### D3. ブラウザを開いてタスクを追加する { #d3-open-the-browser-and-add-the-task }

最後のブロックを追加します。`try`の内側を表示どおり字下げし、`finally`は`try`と同じ位置にします。正常終了やエラーの後にChromeを閉じるための処理です。実行前に保存してください。

```python title="my_browser.py"

browser = BrowserSession()
try:
    agent = build_browser_agent(build_model(), browser)
    run_task(agent, """Use open_venue first, then inspect its screenshot.
In a separate action step call show_access_details. Inspect the NEW screenshot
before answering: which exit is closed and which entrance is recommended?
Describe the visual evidence and explain what the original venue plan alone
could not establish. Do not combine both tool calls in one action step.
""")
finally:
    browser.close()
```

??? info "D3の説明 — 作成・実行・終了処理"

    セッションがChromeを起動します。`build_browser_agent`でそのセッションを使う新しいエージェントを作り、`run_task`で判断を始めます。タスクは開く操作の後に別ステップのクリックを求め、2つの画面を比較できるようにします。`finally`は成功時も失敗時もChromeを閉じます。番号付きのPNGは実行時に生成されます。`browser-*.png`は複数のファイルを表す書き方で、`*`を含む名前のファイルを自分で作る指示ではありません。

**確認：**B2のエージェントと比べてください。操作と新しい観測をつなぐ2つの設定は何ですか？コールバックがなかったらどうなりますか？

??? success "作成の解答 — ブラウザエージェント"

    `tools=browser.tools`で操作を使え、`step_callbacks=[browser.capture]`で操作後の新しい画像を受け取れます。コールバックがなければ、このプログラムの観測ループでは新しい画面をモデルへ渡せません。「クリックした」という文字だけでは、何が表示されたか分かりません。

**いつ：**Cが成功し、D1〜D3をすべて`my_browser.py`に追加・保存し、確認問題に答えた後です。**どこで：**有効化済みの**`week04-exercises`**のターミナルです。

**実行：**

```bash
python my_browser.py
```

必要ならGroqキーを入力します。プログラムがChromeを操作し、最終結果とターミナルの入力待ちが戻るまで待ちます。**確認すること：**`open_venue`と`show_access_details`が別々に呼ばれたか調べ、**`week04-exercises/outputs`**の番号付きPNGを開いて操作と照合してください。他のステップ後も撮影するため、画像が2枚より多い場合があります。枚数を決めつけず、実際のファイル名を使います。

**1. 閉鎖されている出口と推奨される入口はどれですか？何が根拠ですか？**

??? success "エージェントの解答1 — 最初の根拠"

    クリック後の画面に、東側の出口が閉鎖中で、北側の入口を使うよう表示されます。最初の会場図だけでは分からなかった情報です。「Clicked」というツールの文字だけでなく、クリック後に返された画像が根拠になっているか確認します。

**2. 両方のツールが1つのアクションステップで実行されたらどうなりますか？**

??? success "エージェントの解答2 — 異なる画面を比べる"

    ステップ末尾の撮影では、最後の画面だけが残る場合があります。その場合は最終状態しか得られなかったと記します。D3のタスクが全部コピーされ、別ステップでの実行を求めているか確認してください。前後比較には各操作後の画像が必要です。

**3. コールバックの担当は何ですか？**

??? success "エージェントの解答3 — 観測と判断"

    操作を選ぶのはエージェント／モデルです。コールバックは現在の画面を撮影し、次のモデル呼び出し用にステップへ追加します。クリックを選んだり、正しい読み取りを保証したりはしません。`images=[image]`は最初のタスク画像、コールバックは操作後の新しい観測です。

### 最初の結果を残してページを変更する { #browser-comparison }

**次の実行前に、生成された結果を残してください。**

1. 準備で作った**`evidence-files`**を開き、ファイルマネージャーの**新しいフォルダー**で中に**`browser-baseline`**を作ります。自分で作る保存先であり、Pythonが生成するフォルダーではありません。
2. 実際の`outputs/browser-*.png`をそこへコピーします。`evidence.md`には最初の操作と回答の抜粋、対応する画像名を記します。
3. エディターで**生成済みの`assets/venue.html`**を開きます。新しいHTMLや教材のページではなく、このファイルの利用案内の段落から次の文章を探してください。

```text
The east exit is closed for maintenance. Use the north entrance for accessible entry.
```

4. この2文だけを次の架空のテスト情報へ置き換えます。HTMLタグとボタンは変えません。

```text
The west exit is closed for maintenance. Use the south entrance for accessible entry.
```

5. `assets/venue.html`を保存し、`evidence.md`に新しい回答を予想します。**`prepare_visuals.py`は再実行しません。**元の文章に戻ってしまいます。
6. **1〜5を終えてから**、**同じ`week04-exercises`の有効化済みターミナル**で**`python my_browser.py`**を再実行します。新しいChromeセッションで保存済みのページが開きます。最終結果と入力待ちが戻ってから7へ進みます。ページの変化に答えが追随するか確認するため、`my_browser.py`は変更しません。
7. `evidence-files`内に**`browser-revised`**を作り、新しい`outputs/browser-*.png`をコピーします。番号はセッションごとに最初へ戻るため元の出力が上書きされることがあります。2つの保存先を比較に使います。

**4. 新しい回答は変更後のスクリーンショットに合っていますか？**

??? success "エージェントの解答4 — ページ変更後の比較"

    保存した編集後の実行では、表示される案内が**西側の出口**と**南側の入口**を示すはずです。保存済みの東／北の画像と比べてください。西／南の画面に対して東／北と答えたら裏付けがありません。保存したか、正しいページを開いたか、新しい画像がエージェントに届いたかを調べ、実際の結果を残します。

**5. 回答がページと一致しても、何が不確かなままですか？**

??? success "エージェントの解答5 — 残る限界"

    画像はこの架空のページに何と書かれているかを裏付けるもので、現地の経路を独立して確かめたことにはなりません。実際の利用条件は分からず、モデルが読み間違えることもあります。

**確認：**3つのPythonファイル、`evidence.md`、直接確認の`before.png`と`after.png`、変更前後の画像フォルダーを保存します。`assets/venue.html`には編集を残し、変えた2文も記録してください。記録した後で元の文章に戻しても構いませんが、比較結果は消さないでください。

## トラブル対処と出典 { #credit }

会場図やページがない場合は、**現在のフォルダーを`week04-exercises`にした有効化済みターミナル**で、配布の**`python prepare_visuals.py`**を実行してからAへ戻ります。既存の画像とページを置き換えるため、残したいHTMLの編集は先に記録してください。ChromeのエラーではインストールとSelenium Managerによる対応ドライバーの取得を確認します。学内ネットワークの制限などは教員への相談が必要なこともあります。画像リクエストやモデル制限のエラーでは利用権限を確認し、最新の画像だけを渡します。画像がモデルへ届いていない文章だけの回答では、画像実習の成功とは言えません。

| 問題 | 確認すること |
| --- | --- |
| `my_*.py`で`No such file` | 手順どおりに指定ファイルを作り、保存場所と`.py`拡張子を確認します。 |
| `week04_...`のインポートエラー | 展開先と配布ファイル、`requirements.txt`をインストールした環境を使っているか確認します。 |
| `before.png`／`after.png`がない | 直接テストが成功していないか、違うフォルダーで実行しています。エラーと現在のフォルダーを調べます。 |
| `outputs`がない | レポートや撮影の成功前は存在しない場合があります。空の代わりを作らないでください。 |
| 変更後も元の文章が出る | 別のコピーではなく、保存した`assets/venue.html`を確認します。生成プログラムを再実行していないか、新しい画像かも調べます。 |

**出典：**最初の画像入力とスクリーンショット観測の仕組みは[HF Vision and Browser Agents](https://huggingface.co/learn/agents-course/en/unit2/smolagents/vision_agents)を参考にしています。Apache-2.0。会場の素材と操作範囲を限定したSeleniumツールはこの教材用です。画像リクエストが拒否された場合は、[Groqの画像入力ガイド](https://console.groq.com/docs/vision)と自分のモデル利用権限を確認してください。

**次：**[17 · 完了確認](week-4-completion.md)。
