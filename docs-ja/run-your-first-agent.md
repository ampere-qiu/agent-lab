# 最初のエージェントのテンプレートを入手して動かす { #download-and-run-the-first-agent-template }

[ダミー演習の3段階](dummy-agent-local.md)を終えたら、第2週を始めます。このページで完全なテンプレートを入手し、専用の環境を準備して起動します。ダミー演習で手動で組み立てたモデル・行動・観測のループを、今度はCodeAgentが管理します。

[基本設定](prepare-your-computer.md)で用意したPython 3.11とGroqキーを引き続き使います。アプリとツールはPC、モデルはGroq側で動くので、インターネット接続は必要です。

自分のOSのコマンドだけを使ってください。ターミナル、フォルダー、編集については[始める前に](before-you-start.md)を参照します。

## 1. Groq APIキーを用意する { #1-create-your-groq-account }

[基本設定](prepare-your-computer.md#4-create-your-groq-api-key)で作った同じキーを、ステップ8の起動時に非表示の入力欄へ貼れるよう準備します。別のアカウントやキーは必要ありません。

まだ作っていない場合は、リンク先の設定を先に済ませます。

## 2. インストール済みのPythonを使う { #2-install-python-311 }

基本設定のPython 3.11を使います。ステップ4で新しい環境のバージョンを確認します。未導入なら[Pythonの設定](prepare-your-computer.md#1-install-python-311)を先に行います。

ダミー演習が動いているなら**Control + C**で止めます。入力待ち表示に`(.venv)`があれば、`deactivate`を実行してからテンプレートのフォルダーへ移ります。

## 3. テンプレートをダウンロードする { #3-download-the-groq-starter }

<div class="template-download" markdown>

<p class="template-download__label">エージェントの完全なテンプレート</p>

`app.py`、画面、ツール、手順、必要なライブラリ一覧が1つのZIPに入っています。「Groqスターター」と「エージェントテンプレート」は同じものです。APIキーと仮想環境は含まれません。

[テンプレートをダウンロード（.zip）](downloads/groq-agent-starter.zip){ .md-button .md-button--primary .template-download__button download="groq-agent-starter.zip" }

</div>

1. 上の**テンプレートをダウンロード（.zip）**をクリックします。
2. Macではダブルクリック、Windowsでは右クリックから「すべて展開」でZIPを展開します。
3. `app.py`、`Gradio_UI.py`、`requirements.txt`、`prompts.yaml`、`tools`が入った`First_agent_template`フォルダーを見つけます。課題一覧の`STUDENT_TASKS.md`も入っています。
4. 基本設定で作った`agent-course`へ移します。同名のフォルダーがある場合は、置き換える前にバックアップを取ります。
5. ターミナルを開いてプロジェクトへ移動します。

**Windows — コマンドプロンプト**

```bat
cd /d "%USERPROFILE%\agent-course\First_agent_template"
```


**Mac — Terminal**

```bash
cd ~/agent-course/First_agent_template
```


未展開のZIP内で作業しないでください。同名フォルダーが二重になっていれば、`app.py`が入った内側を使います。

**確認：**Windowsは`dir`、Macは`ls`で、`app.py`と`requirements.txt`があることを確認します。

## 4. 仮想環境を作る { #4-create-a-virtual-environment }

ダミー演習とライブラリを分けるため、`First_agent_template`内に新しい環境を作ります。ステップ3で移動した後、一度だけ実行します。

### Windows { #windows }

```bat
py -3.11 -m venv .venv
.venv\Scripts\activate.bat
python --version
```


### Mac { #mac }

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python --version
```


**確認：**入力待ち表示に`(.venv)`が付き、Python 3.11.xと出ます。同じターミナルを使い続けます。

## 5. ライブラリをインストールする { #5-install-the-libraries }

どちらのOSでも次を実行します。

```bash
python -m pip install -r requirements.txt
```


インストールが終わり、入力待ちに戻るまで待ちます。ダウンロードの進行表示は正常です。

**確認：**最後に`ERROR`が出ていないことを確認します。`Successfully installed`や`Requirement already satisfied`は正常です。処理中に次のコマンドを入力しないでください。

Groq ZIPに入った`requirements.txt`を使います。`openai`クライアントも含まれますが、ここでは互換API経由でGroqにつなぐためのもので、OpenAIアカウントは不要です。

## 6. 配布されたモデル設定を保つ { #6-create-your-groq-api-key }

`app.py`にはすでにGroq接続の設定があります。

```python
model_id="qwen/qwen3.8-27b",
api_base="https://api.groq.com/openai/v1",
```


コードエージェント用に`reasoning_effort="none"`も設定しています。初回は変えずに使います。APIキーはソースに書かず、起動時に入力します。

## 7. ローカルだけで公開される設定を確認する { #7-confirm-local-only-sharing }

スターターの`Gradio_UI.py`はすでに`share=False`で、`127.0.0.1`にバインドします。編集は不要です。

古いコピーを使う場合は`demo.launch`に`share=False`があるか確認します。公開リンクを有効にすると、他の人が実行中アプリのGroq認証情報を使ってリクエストを送れる状態になります。

## 8. エージェントを起動する { #8-start-the-agent }

```bash
python app.py
```


ターミナルで最初に次のようにキーを求められます。

```text
Paste your Groq API key (hidden):
```


キーを貼ってEnter／Returnを押します。貼っている間、何も表示されないのは正常です。その後、次のように表示されます。

```text
Using Groq: qwen/qwen3.8-27b
```


入力したキーは実行中のメモリーだけに保持され、保存されません。別途`GROQ_API_KEY`を設定していれば、その値を使い、入力を求めません。キーを表示・共有しないでください。

次のような起動表示を待ちます。

```text
Running on local URL: http://127.0.0.1:7860
```


表示された正確なアドレスをブラウザーで開き、ターミナルは動かしたままにします。

アドレスの入力先はブラウザーのアドレス欄です。チャットではありません。違うポートが表示されたら、そのポートを使います。アプリの実行中に通常の入力待ちに戻らないのは正常です。

## 9. LLMへの接続をテストする { #9-test-the-connection-to-the-llm }

次の英語のテスト質問を送ります（12×8はいくつか、という意味です）。

> What is 12 multiplied by 8?

最終回答に**96**が含まれることを確認します。生成されたPythonや`python_interpreter`のステップも表示される場合があります。

**確認：**モデルが生成した答えが返れば、このリクエストについてキー、アカウント権限、接続先、モデルが動作したと分かります。チャット画面が開いただけでは画面の確認しかできません。失敗したら下の表を使います。

時刻と検索の実装は配布済みですが、最初に登録されているのは`final_answer`だけです。[ツール実習](first-agent-practical.md)で2つをテストして登録します。それまでは、エージェントは配布済みの`web_search`を使えません。モデルの知識から回答したりURLを出したりすることはありますが、検索の証拠にはなりません。

## 10. 使用量の制限を確認する { #10-understand-token-usage }

1回のチャットで複数回のモデルリクエストが発生することがあります。[Groqの利用制限](https://console.groq.com/docs/rate-limits)を確認し、短時間に送信を繰り返さないでください。APIキーは認証用、入力・出力トークンはテキストの使用量です。出力上限と設定は[モデル接続の解説](understand-the-template.md#the-model-connection)を参照します。

## 11. 停止と再起動 { #11-stop-and-restart }

止めるには、ターミナルを選んで**Control + C**を押します。

別の日に再開する場合、新しいターミナルで実行します。

### Windows { #windows_1 }

```bat
cd /d "%USERPROFILE%\agent-course\First_agent_template"
.venv\Scripts\activate.bat
python app.py
```


### Mac { #mac_1 }

```bash
cd ~/agent-course/First_agent_template
source .venv/bin/activate
python app.py
```


ライブラリの再インストールは不要です。求められたらGroqキーを入力し、表示されたローカルURLを開きます。

## トラブル対応 { #troubleshooting }

### モデル接続の問題 { #model-connection-problems }

| 問題 | 次に確認すること |
| --- | --- |
| Pythonの版が違う | ステップ4のPython 3.11環境を有効にする。 |
| `app.py`や`requirements.txt`がない | 展開した`First_agent_template`へ移動する。 |
| `ModuleNotFoundError: openai` | `.venv`を有効にしてステップ5をやり直す。 |
| Groqキーを入力していない | 再起動し、非表示の入力欄に貼る。 |
| 400／`tool_use_failed`／「Tool choice is none」 | 現行スターターの`app.py`と`prompts.yaml`を使い、古いプロセスを停止して再起動する。更新版はGPT-OSSではなくQwenを選び、Pythonテキストを明示的に求める。続く場合は[Groqのツール呼び出し仕様](https://console.groq.com/docs/tool-use/local-tool-calling)と配布版のモデルIDを確認する。この演習はPythonテキストを期待するため、むやみにネイティブツールを有効にしない。 |
| 401／キーが無効 | ラベルやHFトークンではなくGroqキー全体を使う。有効期限や失効を確認する。 |
| 403／アクセス拒否 | アカウント・プロジェクトのモデル権限と組織の制限を確認する。 |
| 429／Request too large | ターミナルで制限の種類を読む。出力なら`app.py`の`max_tokens`を下げて保存・再起動（現行版は512）。入力なら再起動して履歴を消すか質問を短くする。大きすぎる要求は待つだけでは直らない。 |
| 429／利用枠を使い切った | 指定された再試行間隔に従う。無料枠はリクエスト数とトークンの両方に適用される。連続送信を避ける。 |
| 404／モデルが利用できない | `model_id`を[対応モデル一覧](https://console.groq.com/docs/models)と照合し、権限を確認する。IDは完全一致が必要。 |
| HF router 402／no credits | 古いHF接続のアプリが動いている。停止しGroqスターターを使う。この版のためにHFクレジットを買う必要はない。 |
| 古い`NoneType`のトークン数エラー | ZIP内の更新済み`Gradio_UI.py`を使っているか確認する。 |
| 画面は開くが応答しない | ターミナルのモデルエラーを読む。画面だけではAPIアクセスは分からない。 |
| 接続エラー・タイムアウト | インターネットとGroqの稼働状況を確認し、一度再試行する。現行版は1試行30秒、最大2回の自動再試行。待機中に何度も送らない。 |
| ブラウザーから接続できない | アプリを起動したまま、表示されたURLを使う。 |
| ポートが使用中 | 古いアプリのプロセスを停止してから起動する。 |

質問するときはOS、コマンド、エラー末尾を伝えます。認証情報は除いてください。

### 編集でよくある間違い { #common-editing-mistakes }

| 表示・症状 | 確認すること |
| --- | --- |
| `IndentationError` | 編集部分の行頭の空白を、元ファイルやバックアップと比較して戻す。 |
| `SyntaxError` | カンマ、引用符、角括弧、丸括弧の不足を調べる。 |
| ツール追加後の`NameError` | 名前の綴り、エージェントより上での定義、保存を確認する。 |
| `app.py.txt`になっている | コードエディターで`app.py`として保存し、`.txt`を付けない。 |
| 編集が反映されない | 保存し、アプリを停止・再起動して、画面も再読み込みする。 |
| ターミナルが`>>>` | `exit()`で通常のコマンド入力に戻る。 |

**完了確認：**起動し、LLMの応答を得て、モデルの実行場所を説明し、アプリを止められることを確認します。

**次へ：**[smolagentsとテンプレートの仕組み](understand-the-template.md)を読み、[ツールを組み込みます](first-agent-practical.md)。
