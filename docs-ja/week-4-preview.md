# 第04週 · smolagents Part 2 { #week-4-preview }

**目標：**検索の根拠を振り返り、複数のエージェントを連携させ、画像やスクリーンショットを根拠として使います。

**始める前に：**[第03週](week-3-learning-plan.md)を終えてください。第03週の作業は`First_agent_template`に残し、第04週は**別の`week04-exercises`フォルダー**を使います。教材はこのサイトで読み、Pythonファイルはコードエディターで作り、ターミナルで実行します。

## 学習の流れ { #planned-topics }

| トピック | 目標 |
| --- | --- |
| [14 · 第03週のRAGを確認する](week-4-retrieval.md) | 取得した文章が回答を裏付けるか確認します。RAGのコード作成は第03週で行います。 |
| [15 · マルチエージェントとBatman演習](week-4-batman.md) | 管理役とWeb調査役を作り、連携させます。 |
| [16 · 画像・ブラウザエージェント](week-4-vision-browser.md) | 画像と更新されたスクリーンショットを使うエージェントを作ります。 |
| [17 · 完了確認](week-4-completion.md) | コードを説明し、実行結果を確かめます。 |

**注：**すべてのトピックに取り組んでください。トピック15でエージェントをもう1体追加する課題は任意です。

## 1. ダウンロードして配布ファイルを確認する { #exercise-files }

[第04週の教材と補助ファイルをダウンロード](downloads/week04-smolagents-part2.zip){ .md-button .md-button--primary }

[Batman用ダウンロード](downloads/week4_batman_guided_student.zip)と[画像・ブラウザ用ダウンロード](downloads/week4_vision_browser_student.zip)も同じ内容です。**ZIPは1つだけダウンロードして展開してください。**

1. ZIPを保存します。通常は**ダウンロード**フォルダーに入ります。
2. **Windows：**右クリック → **すべて展開** → **展開**。**Mac：**FinderでZIPをダブルクリックします。
3. 展開された**`week04-exercises`**フォルダーを開きます。外側にもう1つフォルダーができた場合は、その中の`week04-exercises`を開いてください。`requirements.txt`と`week04_common.py`が同じ場所にあれば正しいフォルダーです。
4. フォルダーごと既存の**`agent-course`**へ移し、`First_agent_template`と並べます。標準の場所はWindowsでは`%USERPROFILE%\agent-course\week04-exercises`、Macでは`~/agent-course/week04-exercises`です。別の場所を使っている場合は、以降のコマンドのパスを自分の場所に合わせてください。

**すでに第04週を始めている場合：**作業のコピーを保存してから、最新のZIPを新しいフォルダーへ展開してください。この教材のコードと、そのZIPに入っている補助ファイルを一緒に使います。

**ZIPに入っているファイル — 既存のファイルを開いて使います。作り直す必要はありません。**

| 配布物 | 役割 |
| --- | --- |
| `README.md`、`NOTICE.md`、`HF-LICENSE.txt` | 使い方、出典・変更内容、HFのライセンスです。 |
| `requirements.txt` | インストールするパッケージの一覧です。 |
| `week04_common.py` | Groqに接続し、エージェントの結果をターミナルに表示します。 |
| `week04_search.py` | 調査回数の上限内でウェブを検索し、ページの短い抜粋を読みます。 |
| `week04_tools.py` | 貨物輸送時間の概算とHTMLレポートの作成を行います。 |
| `week04_browser.py` | ローカルページの操作とスクリーンショットの取得を行います。 |
| `prepare_visuals.py` | 練習用の会場図とウェブページを作成します。 |
| `lessons/en`、`lessons/ja` | 日英の教材と、出典を記したHFの図が入っています。 |

**これから追加するファイル：**手順に沿って`evidence.md`、`evidence-files`フォルダー、各`my_*.py`を作ります。環境準備で`.venv`と`assets`ができ、後の実行で`outputs`が作られます。

## 2. エディターを開いて環境を準備する { #activate-environment }

VS Codeの**ファイル → フォルダーを開く**で**`week04-exercises`**を選びます。ファイル一覧で`requirements.txt`と`week04_common.py`を確認してください。配布されたPythonファイルはそのまま残し、同じ場所に自分の`my_*.py`を作ります。

Python 3.11、既存のGroqキー、インストール・モデルへの問い合わせ・検索に使うインターネット接続、トピック16用のChromeが必要です。次のコマンドを**1行ずつ**実行してください。標準と異なる場所へ展開した場合は、実際のフォルダーのパスに変更します。

**Windows — コマンドプロンプト**（PowerShellではありません）：

```bat
cd /d "%USERPROFILE%\agent-course\week04-exercises"
py -3.11 -m venv .venv
.venv\Scripts\activate.bat
python --version
dir
python -m pip install -r requirements.txt
python prepare_visuals.py
```

**Mac — ターミナル：**

```bash
cd ~/agent-course/week04-exercises
python3.11 -m venv .venv
source .venv/bin/activate
python --version
ls
python -m pip install -r requirements.txt
python prepare_visuals.py
```

**`prepare_visuals.py`の役割：**LLMやネットワークを使わず、架空の会場図とローカルの練習ページを作ります。**`assets/venue.png`と`assets/venue.html`が生成されます。**これらを手作業で作る必要はありません。次のように表示されます。

```text
Created assets/venue.png and assets/venue.html (no LLM).
```

**先へ進む前に：**プロンプトに`(.venv)`が表示され、Pythonが3.11.xで、インストールが完了していることを確認します。ファイルマネージャーで`assets`内の2つのファイルを確認し、`assets/venue.png`を開いてください。インストールが失敗した場合は、そのエラーを解決してから次のプログラムを実行します。

このターミナルは開いたままにします。以降の**実行：`python filename.py`**は、環境を有効にした`week04-exercises`内のターミナルで行います。新しいターミナルを開いた場合は、上の`cd`と環境の有効化の行を再実行してください。`.venv`を作り直す必要はありません。**練習ページを編集した後は、元に戻したい場合を除き`prepare_visuals.py`を再実行しないでください。**生成した2つのファイルが上書きされます。

Seleniumは最初のブラウザ実行時にChrome対応のドライバーを取得することがあります。ドライバーやネットワークのエラーは、[トピック16のトラブル対処](week-4-vision-browser.md#credit)を確認してください。配布ヘルパーはキーを非表示入力で尋ねます。ローカルの`.env`と読み込み手順は下で説明します。キーをコードや記録用メモには保存しません。エージェントが使うタスク文、取得した文章、画像はGroqへ送信されます。

### ローカル設定：`.env`を作る

エディターで**`week04-exercises`内の`week04_common.py`と同じ場所**に**`.env`**を作ります。`.env.txt`ではなく`.env`で保存します。次の2行を貼り付け、キーの仮の文字列だけを自分のキーに置き換えてください。

```dotenv
GROQ_API_KEY=your_own_groq_api_key
GROQ_MODEL=qwen/qwen3.8-27b
```

このファイルは自分の端末だけに保存します。GitHub、記録用ファイル、スクリーンショットには含めません。モデルは[Groqの対応モデル一覧](https://console.groq.com/docs/models)で2026年11月4日に確認しました。プレビューモデルなので、変更時は一覧と自分のアカウントの権限を確認します。モデル名の先頭に`groq/`を追加しません。

**`.env`を作るだけではPythonに読み込まれません。**Batmanの4Aで`load_dotenv(Path(__file__).with_name(".env"), override=False)`を呼んでから設定を読みます。すでにターミナルに設定した値が優先されます。古い値が使われる場合はその設定を解除するか、新しいターミナルを開きます。確認のためにキーを表示しないでください。

配布された`week04_common.py`は`.env`を読みません。ターミナルの環境変数を調べ、なければ非表示入力でキーを尋ね、固定のモデル名を使います。この補助ファイルは変更しません。自分の`my_batman.py`の4Aだけでモデルの作成方法を更新し、キーがない場合の非表示入力を残し、`GROQ_MODEL`を読みます。トピック16の例は従来の補助ファイルを使うため、非表示入力と固定モデルのままです。`.env`を作っただけでは変わりません。

**ZIPの依存関係を入れた後**、有効化したターミナルで次を実行します。

```bash
python -m pip install "smolagents[litellm]==1.13.0" "ddgs==9.16.0" "python-dotenv>=1.0,<2"
python -m pip check
```

検索、`.env`の読み込み、LiteLLM連携が使えるようになり、smolagentsの教材用バージョンは維持します。新しいBatmanファイルでは古い`duckduckgo_search`や`DuckDuckGoSearchTool`を使いません。

GitHubをcloneした場合は、**リポジトリ直下**で`python -m pip install -r requirements.txt`を実行します。直下の一覧はWeek 4の依存関係と追加分を含みます。ZIP内の同名ファイルとは別です。ZIPはそのまま使い、更新した手順はこのオンライン教材で読んでください。ZIP内の教材は以前の版です。

## 3. 記録用ファイルを作る { #evidence-file }

**予想、回答、実行結果の短い抜粋を残すテキストファイル`evidence.md`を作ります。**Markdownは通常のテキストなので、コードエディターで編集できます。ZIPには含まれておらず、Pythonで実行するファイルでもありません。

1. エディターで**ファイル → 新しいテキストファイル**を選びます。
2. 下の見出しを貼り付けます。見出しは英語のままにし、各項目への回答やメモは日本語で書いて構いません。
3. **名前を付けて保存**で、**`week04-exercises`内の`requirements.txt`と同じ場所**に**`evidence.md`**として保存します。
4. **Ctrl + S**または**Command + S**で保存します。ファイル名が`evidence.md.txt`ではなく`evidence.md`になっていることを確認してください。
5. エディターのファイル一覧またはファイルマネージャーで**新しいフォルダー**を選び、`week04-exercises`内に**`evidence-files`**を作ります。比較に使うレポートやスクリーンショットのコピーを保存します。

```markdown title="evidence.md — create this text file"
# Week 4 evidence

## Topic 14 — Week 3 RAG review
- Evidence used: Week 3 run or provided example:
- Answers 1–5:

## Topic 15 — Batman team
- What each agent does and what evidence it returns:
- Build checks A–D: agent count, tools and managed-agent connection:
- One-location handoff: request, actions, observations, returned evidence:
- Full report: sources checked and one recalculated estimate:
- Code-reading answers, checked sources and limitations:
- Optional verifier: design, false-claim test and verdict (or not attempted):

## Topic 16 — Vision and browser
- My image predictions, supported facts and uncertainty:
- How each agent receives its image or screenshot:
- Initial image run and step-free-route comparison:
- Direct browser check: before.png versus after.png:
- Agent browser run: actions, screenshot names and supported answer:
- Edited-page run: exact change, prediction, archived results and comparison:

## Topic 17 — Review
- Status for each required checkpoint: complete or incomplete, with reason:
- Answers 1–5:
```

作業を進めながら、対応する見出しの下に回答や結果を追加します。ターミナルから短い抜粋をコピーし、エラーも記録してください。まず自分で問題に答え、その後で解答を開いて考え方を確認します。

## 4. 作成するファイルを確認する { #student-files }

| トピック | 作成するもの | 作成するタイミング |
| --- | --- | --- |
| 準備 | `evidence.md`と`evidence-files`フォルダー | 上の手順で今作ります。 |
| 14 | 新しいPythonファイルは不要 | 第03週の出力または教材の例を使って問題に答えます。 |
| 15 | `my_batman_tools.py` | ツールを直接確認する前に作ります。 |
| 15 | `my_batman.py` | 4A〜4Dに沿って2体のエージェントとタスクを追加します。 |
| 15・任意 | `my_batman_verified.py` | 検証役の追加に取り組むとき、動作しているチームのコピーを作ります。 |
| 16 | `my_vision.py` | B1〜B3に沿って画像を読み込み、エージェントとタスクを追加します。 |
| 16 | `my_browser_check.py` | ブラウザ操作を直接確認する前に作ります。 |
| 16 | `my_browser.py` | D1〜D3に沿ってブラウザエージェントを作ります。 |

**Pythonが作成するもの：**`.venv`は環境準備、`assets/venue.png`と`assets/venue.html`は`prepare_visuals.py`、`before.png`と`after.png`は`my_browser_check.py`、`outputs/batman-report.html`はレポートツール、`outputs/browser-*.png`はスクリーンショットのコールバックが作成します。該当する処理が成功するまでは、ファイルがなくても正常です。同じ名前の出力は再実行で上書きされることがあるため、各レッスンの手順で必要なコピーを残してください。

## 最初のエージェントを実行する前に { #for-now }

配布された補助ファイル、生成した会場図とページ、作成した`evidence.md`と`evidence-files`、有効化したターミナルを確認します。`my_*.py`は各レッスンで1つずつ作ります。配布された`README.md`にも準備の要点があります。

モデルのエラーが401ならキー、403/404ならモデルへのアクセス権を確認します。429では利用枠とトピック15の上限付き待機の説明を確認します。待機でクレジットは増えず、成功も保証されません。チーム全体を繰り返し再起動しないでください。ステップ上限後に最終回答が表示されても、ターミナルのツール呼び出しと観測結果を確認する必要があります。

**開始：**[14 · 第03週のRAGを確認する](week-4-retrieval.md)。
