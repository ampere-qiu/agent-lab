# 最初のエージェント：テンプレートの入手と実行 { #download-and-run-the-first-agent-template }

<div class="template-download" markdown>

<p class="template-download__label">ステップ04 · スターターファイル</p>

**完全なエージェントのテンプレートをダウンロード**

Pythonファイル、ツール、手順、必要なライブラリの一覧を1つのZIPにまとめています。ダミー演習の3段階を終えた後に使います。

[テンプレートをダウンロード (.zip)](downloads/groq-agent-starter.zip){ .md-button .md-button--primary .template-download__button download="groq-agent-starter.zip" }

**次に：** ZIPを展開し、[下のステップ3](#3-download-the-groq-starter)へ進みます。APIキーは含まれていません。起動時に自分のGroqキーを入力します。

</div>

> **なぜローカル環境？** 確認した環境では、元の教材のSpace複製が使えませんでした。CPU Basicは無効、ZeroGPUはPROが必要で、カスタムハードウェアは有料でした。APIトークンを作ってもホスティングの条件は変わりません。このガイドではローカルアプリとGroqを使い、このサイトの説明、時刻・検索の実習、元の小テスト2回で学びます。[コースの紹介](index.md)も参照してください。

**このページを使うタイミング：** 先に[ダミー演習の3段階](dummy-agent-local.md)を終えます。ここからは完全なテンプレートで、モデル・行動・観測のループをCodeAgentに任せます。既存のGroqキーを再利用し、テンプレート用には別の仮想環境を作ります。Pythonとアカウントの準備が済んでいればステップ3から始め、ステップ6でも同じキーを使えます。ダミー演習の環境から移る前に`deactivate`を実行し、以下の手順で別の環境を作成・有効化してください。

WindowsまたはMacで、Hugging Face Agents CourseのスターターをGroq用に調整したアプリを動かします。

初めてのPythonプロジェクトなら[始める前に](before-you-start.md)を読んでください。コマンドは自分のOSのものだけを使います。両OS共通の手順は全員が行います。

PC上でアプリとツールが動き、リモートの大規模言語モデル（LLM）が応答を生成します。インターネット接続が必要です。既存モデルを使う実習で、モデルの学習ではありません。

この版のチャットにHugging Faceトークンは不要です。モデルAPIはGroqが提供します。手順はこのサイトで学び、HFの小テスト2回だけを残しています。最終テスト、認定、画像生成は含めません。

## 1. Groqアカウントを作る { #1-create-your-groq-account }

1. [Groq Console](https://console.groq.com)を開きます。
2. 自分のアカウントで登録またはログインし、求められた確認を完了します。
3. この実習は**Free**プランを使います。有料へのアップグレードは環境構築の条件ではありません。
4. キーの作成方法は下のステップ6にあります。

無料プランにはリクエスト数とトークン数の上限があります。複数ステップのエージェントは1メッセージで複数回モデルを呼ぶことがあります。アカウントのLimitsを確認してください。キーを増やしても組織の利用枠は増えません。[Groqの利用上限](https://console.groq.com/docs/rate-limits)を参照してください。

## 2. Python 3.11をインストールする { #2-install-python-311 }

Pythonがアプリを実行します。3.11が既にあれば再インストールは不要です。ZIPを使う手順ではGitも不要です。

### Windows { #windows }

**コマンドプロンプト**を開き、コマンドを1つずつ実行します。

```bat
winget install --exact --id Python.Python.3.11
```

インストーラーの案内に従い、コマンドプロンプトを閉じて開き直してから確認します。

```bat
py -3.11 --version
```

`winget`が使えなければ、[Python 3.11.9のリリースページ](https://www.python.org/downloads/release/python-3119/)の**Files**から、x64 PC向けの**Windows installer (64-bit)**を入手します。実行時に**Add python.exe to PATH**とPython launcherを有効にしてください。インストール後にコマンドプロンプトを開き直して`py -3.11 --version`を再実行します。PowerShellではなく**コマンドプロンプト**を使います。

### Mac { #mac }

**ターミナル**を開き、Homebrewがあれば実行します。

```bash
brew install python@3.11
```

Homebrewがなければ[インストール手順](https://brew.sh)と最後の設定手順に従ってから再実行します。

インストールを確認します。

```bash
python3.11 --version
```

**確認：** Python 3.11.xが出ます。Macの`python3`が古い版を指していても構いません。以下では`python3.11`を使います。

## 3. Groqスターターをダウンロードする { #3-download-the-groq-starter }

[テンプレートをダウンロード (.zip)](downloads/groq-agent-starter.zip){ .md-button .md-button--primary .template-download__button download="groq-agent-starter.zip" }

1. 上のダウンロードボタンを押します。ページ上部で入手済みなら同じZIPを使います。
2. Macではダブルクリック、Windowsでは右クリックして**すべて展開（Extract All）**を選びます。
3. `app.py`、`Gradio_UI.py`、`requirements.txt`、`prompts.yaml`、`tools`が入った`First_agent_template`フォルダーを見つけます。課題を説明した`STUDENT_TASKS.md`もあります。
4. ホーム／ユーザーフォルダーに`agent-course`を作り、その中へ移します。同名のフォルダーが既にあれば、置き換える前にバックアップします。
5. ターミナルを開いてプロジェクトに移動します。

**Windows — コマンドプロンプト**

```bat
cd /d "%USERPROFILE%\agent-course\First_agent_template"
```

**Mac — ターミナル**

```bash
cd ~/agent-course/First_agent_template
```

未展開のZIP内では作業しません。同名のフォルダーが二重になった場合は、`app.py`のある内側を使います。

**確認：** Windowsで`dir`、Macで`ls`を実行し、`app.py`と`requirements.txt`を確認します。ZIPに含まれるのはコードだけで、仮想環境や誰かのAPIキーは含まれません。

## 4. 仮想環境を作る { #4-create-a-virtual-environment }

このプロジェクトのライブラリを、ほかのPythonプロジェクトから分離します。

### Windows { #windows_1 }

```bat
py -3.11 -m venv .venv
.venv\Scripts\activate.bat
python --version
```

### Mac { #mac_1 }

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python --version
```

**確認：** 表示が`(.venv)`で始まり、Pythonの版が3.11.xです。このターミナルを使い続けます。

## 5. ライブラリをインストールする { #5-install-the-libraries }

どちらのOSでも同じです。

```bash
python -m pip install -r requirements.txt
```

インストールが終わって入力待ちに戻るまで待ちます。ダウンロードの進捗表示は正常です。

**確認：** 最後に`ERROR`が出ていません。`Successfully installed`や`Requirement already satisfied`が表示されることがあります。処理中に次のコマンドを入力しないでください。

Groq用ZIPの`requirements.txt`を使います。`openai`クライアントはGroqの互換APIへの接続に使っており、OpenAIアカウントは不要です。

## 6. 自分のGroq APIキーを作る { #6-create-your-groq-api-key }

### A. キーのページを開く { #a-open-the-key-page }

1. [Groq Console](https://console.groq.com)にログインします。
2. **API Keys**または[直接リンク](https://console.groq.com/keys)を開きます。
3. **Create API Key**をクリックします。
4. `agents-course`など用途が分かる名前を入力します。有効期限を選べる場合は授業期間をカバーするものにします。
5. ダイアログの作成・送信ボタンで確定します。
6. 生成された秘密キーをコピーしてパスワードマネージャーに保管します。ほかの学生と共有せず、ガイド、コード、チャットに貼り付けないでください。

`agents-course`はラベルです。生成された秘密の文字列が実際のキーです。画面の表記は変わることがあります。[公式クイックスタート](https://console.groq.com/docs/quickstart)にも作成へのリンクがあります。

**確認：** 自分のキーを用意できました。キーの作成だけではモデルを選んだことにも、リクエスト成功の確認にもなりません。

### B. アプリでの使い方 { #b-understand-how-the-app-uses-it }

ステップ8で`python app.py`を実行するとキーが求められます。Hugging Faceのログインや`whoami`は別サービスの確認で、Groqへのアクセス確認にはなりません。

貼り付け中のキーは表示されず、起動中のアプリのメモリーに保持されます。アプリはキーを保存しません。別途`GROQ_API_KEY`を設定していなければ、再起動のたびに入力します。

### C. モデルの選択は設定済み { #c-model-selection-is-already-configured }

付属の`app.py`には次の設定があります。

```python
model_id="qwen/qwen3.8-27b",
api_base="https://api.groq.com/openai/v1",
```

モデルとGroqの接続先を指定しています。`reasoning_effort="none"`も設定し、推論の前置きを付けずにコード形式の応答を返すようにしています。最初のテストでは変更しません。キー入力の処理を、コードに直書きしたキーに置き換えないでください。

### D. 実際の応答で確認する { #d-verification-happens-with-a-real-response }

キーを作ってもユーザー名が表示される方式ではありません。ステップ9のモデル応答が成功して初めて、そのリクエストについてキー、アカウントのアクセス、接続先、モデルが動いたと確認できます。チャット画面が開くだけでは確認できません。

キーを公開してしまった、または紛失した場合は、[Groq API Keys](https://console.groq.com/keys)で管理・失効し、必要なら新しく作り、そのキーでアプリを再起動します。

## 7. ローカルだけで使う設定を確認する { #7-confirm-local-only-sharing }

スターターの`Gradio_UI.py`は既に`share=False`で、アドレスも`127.0.0.1`です。編集は不要です。

古いコピーを確認する場合は、`demo.launch`に`share=False`が含まれるか確認します。公開リンクを作ると、ほかの人が起動中のアプリのGroq認証情報を使ってリクエストを送れるようになります。

## 8. エージェントを起動する { #8-start-the-agent }

```bash
python app.py
```

最初にターミナルに次が出ます。

```text
Paste your Groq API key (hidden):
```

キーを貼り付けてEnter／Returnを押します。文字が見えないのが正常です。その後、次が表示されます。

```text
Using Groq: qwen/qwen3.8-27b
```

これは設定されたモデル名で、まだGroqがキーを受理した証拠ではありません。キー入力が出ない場合は環境の`GROQ_API_KEY`を使っています。その変数を表示して共有しないでください。

ローカルの`app.py`がモデルを設定し、画面を起動します。次のような表示を待ちます。

```text
Running on local URL: http://127.0.0.1:7860
```

表示された正確なアドレスをブラウザーで開き、ターミナルを動かしたままにします。

アドレスはチャットではなくブラウザーのアドレス欄に入れます。別のポートが表示されたらそれを使います。アプリの実行中に通常の入力待ちへ戻らないのは正常です。

## 9. LLMへの接続をテストする { #9-test-the-connection-to-the-llm }

次の文をチャットへ送ります。コードや比較用プロンプトは英語版と同じです。

> What is 12 multiplied by 8?

**96**を含む最終応答を確認します。生成されたPythonや`python_interpreter`のステップが表示される場合もあります。

リクエストはブラウザーからローカルアプリ、次にリモートLLMへ進みます。アプリが生成コードを実行して結果を表示します。モデルはGroqが提供する`qwen/qwen3.8-27b`です。提供状況は変わることがあります。

ページが開けば画面の動作を、モデルの応答が返ればリモート接続も確認できます。スターターのツールは限定されており、最初からWeb検索できるとは限りません。

## 10. トークンの利用量を理解する { #10-understand-token-usage }

| 用語 | 意味 |
| --- | --- |
| アクセストークン／APIキー | 繰り返し使う認証情報 |
| 入力トークン | 指示や会話履歴など、モデルへ送るテキストの単位 |
| 出力トークン | モデルが生成するテキストの単位 |

起動中は同じキーを使い続けます。停止・再起動後は、`GROQ_API_KEY`がなければ再入力します。入力・出力のトークン数はモデル利用量であり、認証情報ではありません。

## 11. 停止と再起動 { #11-stop-and-restart }

停止するにはターミナルを選び、**Control + C**を押します。

別の日に再開するときは新しいターミナルで実行します。

### Windows { #windows_2 }

```bat
cd /d "%USERPROFILE%\agent-course\First_agent_template"
.venv\Scripts\activate.bat
python app.py
```

### Mac { #mac_2 }

```bash
cd ~/agent-course/First_agent_template
source .venv/bin/activate
python app.py
```

ライブラリの再インストールは不要です。求められたらGroqキーを入力し、表示されたローカルURLを開きます。

## トラブルシューティング { #troubleshooting }

### モデル接続の問題 { #model-connection-problems }

| 問題 | 対応 |
| --- | --- |
| Pythonの版が違う | ステップ4のPython 3.11環境を有効にする |
| `app.py`や`requirements.txt`が見つからない | 展開した`First_agent_template`へ移動する |
| `ModuleNotFoundError: openai` | `.venv`を有効にし、ステップ5を再実行する |
| Groqキーを入力していない | 再起動し、非表示の入力欄に貼り付ける |
| 400／`tool_use_failed`／「Tool choice is none」 | 最新スターターの`app.py`と`prompts.yaml`を使い、古いプロセスを止めて再起動する。現在はGPT-OSSではなくQwenを使い、Pythonテキストを明示的に要求している。再発時は[Groqのツール呼び出し](https://console.groq.com/docs/tool-use/local-tool-calling)と最新ZIPのモデルIDを確認する。この実習はPythonテキストを想定するため、ネイティブツールを安易に有効にしない |
| 401／無効なAPIキー | ラベルやHFトークンではなく、Groqキーの全体を使う。有効期限・失効も確認する |
| 403／アクセス拒否 | アカウント・プロジェクトのモデル権限や組織の制限を確認する |
| 429／Request too large | ターミナルの上限名を読む。出力なら`app.py`の`max_tokens`を下げる（現スターターは512）、保存して再起動。入力なら再起動で履歴を消すかプロンプトを短くする。大きすぎるリクエストは待つだけでは直らない |
| 429／利用上限に到達 | 指定された再試行時間を待つ。無料枠はリクエスト数とトークン数の両方に適用される。連続送信を避ける |
| 404／モデルが使えない | `model_id`と[対応モデル](https://console.groq.com/docs/models)を照合し、コンソールの権限を確認する。IDは完全一致が必要 |
| HF router 402／クレジット不足 | 古いHF接続のアプリが動いている。停止してGroqスターターを使う。この版にHFクレジット購入は不要 |
| 古い`NoneType`トークン数エラー | 最新ZIPの`Gradio_UI.py`を使っているか確認する |
| ページは開くがチャットは失敗 | ターミナルのモデルエラーを読む。ページ表示だけではAPIを確認できない |
| 接続エラー／タイムアウト | ネットとGroqの稼働状況を確認して1回再試行する。現スターターは各試行30秒、最大2回の自動再試行。待機中に何度もメッセージを送らない |
| ブラウザーで接続できない | アプリを動かしたまま、表示されたローカルURLを使う |
| ポートが使用中 | 以前のアプリを停止してから起動する |

相談するときはOS、コマンド、最後のエラー行を共有し、認証情報は除いてください。

### 編集時によくある間違い { #common-editing-mistakes }

| 表示・症状 | 確認すること |
| --- | --- |
| `IndentationError` | 元のファイルやバックアップと比較し、先頭の空白を戻す |
| `SyntaxError` | カンマ、引用符、角括弧、丸括弧の欠落を確認する |
| ツール追加後の`NameError` | 関数名、エージェントより前の定義、保存を確認する |
| `app.py.txt`になっている | コードエディターで`app.py`として保存する |
| 編集が反映されない | 保存、停止、再起動、ブラウザー再読み込みを行う |
| `>>>`が出ている | `exit()`で通常のコマンド画面に戻ってから実行する |

**完了確認：** アプリを起動してLLM応答を受け取り、モデルの実行場所を説明し、アプリを停止できます。

## 動作確認の状況 { #validation-status }

2026年10月12日、別のMacのテストフォルダーに新しいPython 3.11環境を作り、依存関係のインストール、Groqでのダミー3段階、ブラウザーチャット、時刻取得、検索アダプター更新後の単独の実検索が成功しました。その後の組み合わせテストは最終応答まで進みましたが、検索結果が空だったため検索の証拠確認は未達でした。以前の2,096出力トークン設定があるアカウントに拒否されたため、現在は1応答512トークンと2回の自動再試行を使います。確認済みの設定ですが、全アカウントでの成功を保証しません。Windowsでのインストール、アカウント作成、PythonがないPCへの新規導入は未検証です。検索は不安定で、モデルの上限も適用されます。各確認項目で自分の環境を検証してください。一部の依存関係は固定バージョンではありません。

**次へ：** [smolagentsとテンプレートを理解](understand-the-template.md)し、[ツールを実装・登録](first-agent-practical.md)します。
