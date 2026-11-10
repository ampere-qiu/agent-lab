# 第05週 · LlamaIndex { #week-5-plan }

**目標：**文書を検索し、ツールを使い、明確な手順で仕事を受け渡すアシスタントを作ります。

先に[第4週](week-4-completion.md)を終えてください。今週は**HF Unit 2.2と同じ順序**で学びます。以前の作業を残し、新しい**`week05-exercises`**フォルダー、Python 3.11、エディター、ターミナルを使います。ノートブックやGPUは不要です。英語版と日本語版は、同じコードと演習を使います。

## 学習の順番 { #route }

| 順番 | レッスン | 行うこと |
| --- | --- | --- |
| 準備 | このページ | 専用の環境を作り、人物像の説明文10件を取得する。 |
| 18 | [入門](week-5-introduction.md) | コンポーネント、ツール、エージェント、ワークフローを区別する。 |
| 19 | [LlamaHub](week-5-llamahub.md) | パッケージとimportを対応させ、モデル接続を試す。 |
| 20 | [コンポーネント](week-5-components.md) | 読み込み、分割、埋め込み、保存、検索、質問と根拠の確認。 |
| 21 | [ツール](week-5-tools.md) | 関数ツール、検索ツール、ローカルのツールの集まりを作る。 |
| 確認 | [小テスト1](week-5-quiz-1.md) | エージェントを作る前に、部品とツールを説明する。 |
| 22 | [エージェント](week-5-agents.md) | 計算、Bobの記憶、人物像の検索、仕事の受け渡し。 |
| 23 | [ワークフロー](week-5-workflows.md) | イベントとステップ、制限付きループ、作図、状態の共有。 |
| 確認 | [小テスト2](week-5-quiz-2.md) | 判断、イベント、記憶、共有状態を説明する。 |
| 振り返り | [まとめと完了確認](week-5-completion.md) | 作成ファイルを示し、実際の結果を説明する。 |

人物像の検索、練習用の天気、計算、Bobの会話、ワークフローは[HFの単元](https://huggingface.co/learn/agents-course/en/unit2/llama-index/introduction)に沿っています。保存したPythonファイルとしてPCで実行します。これまでの授業用Groq接続を使うので、新しいモデル提供元のアカウントは不要です。

## 1. ZIPを展開してフォルダーを開く { #download }

[第5週の英語・日本語スターターをダウンロード](downloads/week05-llamaindex.zip){ .md-button .md-button--primary }

1. ZIPを保存します。Windowsは右クリックして**すべて展開**、MacはFinderでダブルクリックします。
2. 展開先で、`requirements.txt`と`week05_common.py`が入っているフォルダーを探します。Macでは通常、展開された`week05-exercises`自体です。Windowsではその外にもう1つフォルダーがある場合があります。ファイルが入ったほうを**`agent-course`**内の以前の演習フォルダーの隣へ移し、名前を**`week05-exercises`**にします。
3. VS Codeの**ファイル → フォルダーを開く**で`week05-exercises`を開きます。`requirements.txt`、`prepare_personas.py`、`week05_common.py`、`week05_rag.py`が同じ場所にあることを確認します。
4. 配布ヘルパーは残します。**`my_*.py`はZIPに入っていません。**各レッスンのコードを使い、ヘルパーの隣に自分で作成します。Web版、または`lessons/en`と`lessons/ja`のMarkdownを読んで進めてください。

| 配布ファイル | 用途 |
| --- | --- |
| `requirements.txt` | smolagentsとは分けた第5週用のパッケージ。 |
| `prepare_personas.py` | LLMを使わず、公開された人物像10件を取得する。 |
| `week05_common.py` | 設定を読み、Groqへ接続し、ツールの結果を表示する。 |
| `week05_rag.py` | 後の演習で保存済みのインデックスを再利用する。 |
| `README.md`、`NOTICE.md`、`HF-LICENSE.txt` | 準備の要約、出典、ライセンス。 |
| `lessons/en`、`lessons/ja` | 英語版と日本語版のレッスン。 |
| `images/huggingface-week05` | 元のHFの図。クリックすると拡大できる。 |

## 2. 専用の環境を作って有効にする { #environment }

対応するWindows／Macで**64ビットのPython 3.11**を使います。パッケージとモデル用の空き容量を確認してください。Macでの検証では環境だけで約1.6 GB使い、PCによって変わります。ローカル埋め込み用の大きなパッケージも含みます。インストール、人物像の取得、最初のモデル取得、Groqへの問い合わせには通信が必要です。取得後の検索や通常のワークフローはPCで動きます。有効にしたターミナルをそのまま使ってください。

### ターミナルを選び、Pythonを確認する { #choose-the-terminal-and-check-python }

**WindowsのVS Code：**［ターミナル → 新しいターミナル］を開きます。入力欄が`PS`で始まる場合はPowerShellです。ターミナルの**＋の横の矢印 → Command Prompt**を選び、コマンドプロンプトを開いてください。以後も使う場合は、**Ctrl + Shift + P → Terminal: Select Default Profile → Command Prompt**を選び、新しいターミナルを開きます。日本語表示では「ターミナル：既定のプロファイルの選択」を探します。下のコマンドはコマンドプロンプト用です。[VS Codeの説明](https://code.visualstudio.com/docs/terminal/profiles)も参照できます。

環境を作る前に確認します。

- **Windowsのコマンドプロンプト：**`py -3.11 --version`。
- **Macのターミナル：**`python3.11 --version`。

`Python 3.11.x`と出たら先へ進みます。コマンドがない、または3.11が見つからない場合は、先に下を開いてください。

??? help "Python 3.11が見つからない場合"

    **Windows 10／11：**[python.org](https://www.python.org/downloads/windows/)から**Python install manager**をインストールします。VS Codeを閉じて開き直し、新しいコマンドプロンプトで次を1行ずつ実行します。

    ```bat
    pymanager install 3.11
    py -3.11 --version
    ```

    `pymanager`は古い`py`ランチャーとの競合を避けるために使います。まだコマンドが見つからない場合は[PythonのWindows向け対処](https://docs.python.org/3/using/windows.html#troubleshooting)を参照するか、実行したコマンドとエラーを教員へ伝えてください。

    **Mac：**Homebrewが入っていれば、次を実行します。

    ```bash
    brew install python@3.11
    python3.11 --version
    ```

    `brew`がない場合は[brew.sh](https://brew.sh/)の手順で導入し、インストーラーの**Next steps**にあるターミナルの設定も行ってから、上の2行を実行します。[HomebrewのPython 3.11のページ](https://formulae.brew.sh/formula/python@3.11)で対応OSを確認できます。管理対象や非対応のPCでは、先へ進む前に教員へ相談してください。

### 第5週のパッケージをインストールする { #install-the-week-5-packages }

**Windows — コマンドプロンプト：**1行ずつ実行します。

```bat
cd /d "%USERPROFILE%\agent-course\week05-exercises"
py -3.11 -m venv .venv
.venv\Scripts\activate.bat
python --version
python -m pip install -r requirements.txt
python -m pip check
python week05_common.py
python prepare_personas.py
```

**Mac — ターミナル：**1行ずつ実行します。

```bash
cd ~/agent-course/week05-exercises
python3.11 -m venv .venv
source .venv/bin/activate
python --version
python -m pip install -r requirements.txt
python -m pip check
python week05_common.py
python prepare_personas.py
```

保存場所が異なる場合は、自分のフォルダーのパスへ置き換えてください。`(.venv)`、Python `3.11.x`、`No broken requirements found.`、**`Week 5 starter version: 2026-11-10.2`**、**`Saved 10 persona files in data/ (no LLM, no Groq tokens).`**を確認します。順に「環境が有効」「依存関係の不整合なし」「ヘルパーの版」「10件の保存完了」という意味です。版の確認はモデルを呼びません。取得時は`dataset-source.json`も生成します。`data/persona_0.txt`を開くと、シンシナティの美術史家の説明があるはずです。これは人物像の説明で、実在する人を特定した情報ではありません。不完全な説明も、推測で補わず使います。

`prepare_personas.py`はHFのノートブックと同じ[人物像データ](https://huggingface.co/datasets/dvilasuero/finepersonas-v0.1-tiny)の先頭10件を取得します。通常の取得先が失敗したり文章を省略したりする場合は、元のデータファイル約35 MBを取得・検証し、同じ10件の全文だけを保存します。HFのトークンは不要です。空でない`data`を上書きしません。保存完了まで待ち、止まった場合は表示された原因に沿って対処してください。最初の埋め込みでは`BAAI/bge-small-en-v1.5`をこのフォルダーの`.cache/huggingface`へ取得します。その後は完全なキャッシュをPCから読み、HFへ確認しません。CPUで動き、Groqのトークンは使いません。

新しいターミナルでは、フォルダー移動と有効化の行だけを繰り返します。毎回環境を作り直す必要はありません。

## 3. 自分のPC用の設定を作る { #settings }

**第4週のキーを再利用する場合：**`GROQ_API_KEY`の値だけを新しいファイルへコピーします。`.env`全体をコピーした場合は、`GROQ_MODEL`を下の行へ置き換えてください。第4週の`groq/`のような接頭辞は、今週のモデルIDには付けません。第4週のファイルは残します。

エディターで`week05-exercises`の直下、`week05_common.py`の隣に**`.env`**を作ります。`.env.txt`ではなく`.env`として保存し、次を貼ってキーの仮の値を置き換えます。

```dotenv
GROQ_API_KEY=your_own_groq_api_key
GROQ_MODEL=qwen/qwen3.8-27b
```

ヘルパーは`load_dotenv`を呼んでから設定を読みます。ファイルを作るだけではPythonは読み込みません。ターミナルに既にある環境変数が優先されます。以前このターミナルに`GROQ_MODEL`を設定した場合は、Windowsのコマンドプロンプトで`set GROQ_MODEL=`、Macで`unset GROQ_MODEL`として消してから再実行します。キーはPCに残し、`.env`をGitHub、スクリーンショット、提出メモへ含めないでください。

モデルは[Groqのモデル一覧](https://console.groq.com/docs/models)で2026-11-09に確認しています。プレビューモデルなので、失敗時は現在の提供状況と権限を確認してください。上のモデルIDを使います。ヘルパーは先頭の`groq/`を取り除けますが、古いモデル名まで更新するわけではありません。この演習では依頼と検索した公開文章をGroqへ送ります。

モデルを使うプログラムは1つずつ実行します。エージェントの反復は最大6回で、APIの自動再試行はありません。検索ツール1回で複数のモデル呼び出しが起きる場合があります。**429**が返ったら止め、アカウントの制限・クレジット・再試行間隔を確認します。待つことで短い制限期間がリセットされる場合はありますが、クレジットは増えず、成功も保証されません。

## 4. 結果を記録するメモを作る { #evidence }

同じフォルダーに**`evidence.md`**を作り、下の見出しを貼って保存します。各レッスンの後に短い出力と自分の説明を追記します。Pythonプログラムではありません。見出しは英語のまま使い、説明は日本語で構いません。

```markdown title="evidence.md"
# Week 5 evidence
## 18 — Components, tools, agents, workflows
## 19 — Integration and model connection
## 20 — Ingestion, retrieval, answer, sources, evaluation
## 21 — Function tool, query tool, ToolSpec and utility tools
## Quiz 1
## 22 — Tool calls, Bob memory, RAG and handoff
## 23 — Events, loop, flow diagram and shared counter
## Quiz 2
## Completion — complete/incomplete and limitations
```

以後のファイルは、**ファイル → 新しいテキストファイル → 名前を付けて保存**で、指定どおりの`.py`名をヘルパーの隣に付けます。ブロックを順に貼り、**Ctrl + S**／**Command + S**で保存します。`.venv`や`lessons`内には入れません。

**1つずつ作って実行します。**先に全部作る必要はありません。各ページ末尾の一覧でファイルと結果を確認し、後からimportする以前のファイルも残します。全体では必須の小さなプログラム17個と、任意の評価用1個があります。準備の段階で全部を理解・作成する必要はありません。

**準備の確認：**配布ヘルパー、`.venv`、`.env`、`evidence.md`、`dataset-source.json`、`data/persona_0.txt`〜`data/persona_9.txt`がそろっていますか？まだ`my_*.py`は不要です。最初の1つはLlamaHubのレッスンで作ります。

**開始：**[18 · LlamaIndex入門](week-5-introduction.md)。

## 必要なときのヘルプ { #help }

コマンドが止まった場合は、該当する説明を開いてから先へ進みます。

### 初回のメッセージを読む { #first-run-messages }

??? help "インストールとモデル読み込みのメッセージ"

    | 表示・段階 | 行うこと |
    | --- | --- |
    | `Collecting`、`Downloading`、`Installing`が続く | インストール中です。入力待ちに戻るまで次の行を実行せず待ちます。 |
    | `No broken requirements found.` | 依存関係の確認に通りました。データ取得へ進みます。 |
    | `Downloading ten public persona records...` | 10件の取得中です。`Saved 10 persona files...`まで待ちます。代替元の表示だけでは保存完了ではありません。 |
    | `No complete model cache...`、`Loading weights` | 最初の完全なモデル取得には通信が必要です。以後の`Loaded the cached CPU embedding model locally`はHFへ接続せず読めた意味です。各演習の完了出力を待ちます。 |
    | モデル取得時に`HF_TOKEN`を勧める警告 | この公開モデルにトークンは不要です。完全なキャッシュがあれば次からローカルで読みます。 |
    | pipの`huggingface-hub ... does not provide the extra 'inference'` | 埋め込み用の接続パッケージが、現在のHubにはない古い任意機能名を要求しています。この警告だけでは検証時のローカル埋め込みは失敗しませんでした。終了後に`No broken requirements found.`と演習の結果を確認し、指定バージョンを維持します。 |
    | PyTorchのmacOSではredirects非対応という表示 | 検証時は、この表示があっても完了しました。続く期待結果で判断します。 |
    | `Run incomplete`、エラーの詳細、0以外の終了値 | 未完了です。下の対処表を使い、完了とは記録しません。 |

### 途中で止まった場合 { #troubleshooting }

??? help "エラーに合う次の操作を探す"

    | 表示・状態 | 次の操作 |
    | --- | --- |
    | `python: can't open file` | ターミナルの場所、ヘルパーの隣に保存したファイル名、`.py.txt`になっていないかを確認します。 |
    | 版が違う・表示されない | 現在の第5週ZIPから`week05_common.py`だけを入れ直し、`python week05_common.py`を実行します。`.env`、データ、自作プログラムは残します。 |
    | `ModuleNotFoundError` | 上の手順で今週の`.venv`を有効にし、`python -m pip install -r requirements.txt`を再実行します。第4週へは入れません。 |
    | データ取得が止まる | HTTP 503はサーバー側の失敗なので後で試します。通信のタイムアウトなら接続を確認します。チェックサムの不一致は、元のファイルが不完全か変化した意味です。これらの失敗時は人物像を保存しません。表示を教員へ伝えます。 |
    | `persona_*.txt`が不足 | `python prepare_personas.py`を実行します。不完全な`data`を上書きできない場合は`data-backup`へ名前を変えて残し、再取得します。 |
    | 埋め込みモデルを読み終えない | 通信と空き容量を確認して同じプログラムを再実行します。繰り返し失敗する場合はプログラムを閉じ、`.cache/huggingface`を`.cache/huggingface-backup`へ変え、安定した接続で再取得します。データとコードは残します。取得にGroqのトークンは使いません。 |
    | 索引がない・不完全 | 10件の取得後に`python my_ingest.py`を実行します。途中のDBがある場合は利用中のプログラムを閉じ、`alfred_chroma_db`をバックアップ名へ変えてから作り直します。 |
    | `NameError`、`TypeError`、`ValueError` | 表示されたファイル名と行番号で、名前、引用符、字下げを教材の該当箇所と比べます。 |
    | Groq 401 | ローカルの`.env`のキーを確認します。表示や提出はしません。 |
    | Groq 403／404 | 今週のモデルIDと利用権限を確認します。第4週の設定をコピーした場合は手順3でモデル行を置き換えます。 |
    | Groq 413 | 小さいデータと短い依頼を使います。待っても大きな入力は小さくなりません。 |
    | Groq 429 | 停止して[手順3](#settings)の制限についての説明を確認します。 |
    | `flow.html`が真っ白 | [レッスン23の作図の確認](week-5-workflows.md#draw)へ進みます。現在のヘルパーは図のライブラリをHTMLに含めるため、閲覧に通信は不要です。 |

    今の確認項目を直してから、それに依存するプログラムへ進みます。相談時はファイル名、コマンド、エラーの種類を記録し、`.env`やキーは含めないでください。
