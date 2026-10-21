# PCの環境を準備する { #prepare-your-computer }

第1週の基礎を読んだ後、ダミー演習に入る前に設定します。この段階で必要なのはPythonとGroqキーだけです。完全なテンプレートをダウンロードするのは、ダミー演習の3段階を終えて**から**です。

## 1. Python 3.11をインストールする { #1-install-python-311 }

### Windows { #windows }

**コマンドプロンプト**を開き、次を実行します。コマンドは1つずつ実行してください。

```bat
winget install --exact --id Python.Python.3.11
```


インストーラーの指示を確認し、コマンドプロンプトを閉じて開き直してから、バージョンを確認します。

```bat
py -3.11 --version
```


`winget`が使えない場合は、[Python 3.11.9のリリースページ](https://www.python.org/downloads/release/python-3119/)の**Files**から、x64 PC用の**Windows installer (64-bit)**をダウンロードします。実行して**Add python.exe to PATH**とPython launcherを有効にし、インストール後にコマンドプロンプトを開き直して`py -3.11 --version`を試します。このガイドのWindows用コマンドは、PowerShellではなく**コマンドプロンプト**で実行します。

### Mac { #mac }

**Terminal**を開きます。Homebrewが入っていれば、次を実行します。

```bash
brew install python@3.11
```


Homebrewがなければ、[公式のインストール手順](https://brew.sh)を最後の設定まで行ってから再試行します。

インストールを確認します。

```bash
python3.11 --version
```

**確認：**Python 3.11.xと表示されます。Macの`python3`が古い版を指していても構いません。以下では`python3.11`を使います。

## 2. ダミー演習用のフォルダーを作る { #2-create-a-folder-for-the-dummy-exercise }

自分のOS用のコマンドを、ターミナルで1つずつ実行します。

### Windows — コマンドプロンプト { #windows-command-prompt }

```bat
mkdir "%USERPROFILE%\agent-course\dummy-agent"
cd /d "%USERPROFILE%\agent-course\dummy-agent"
py -3.11 -m venv .venv
.venv\Scripts\activate.bat
python --version
```


### Mac — Terminal { #mac-terminal }

```bash
mkdir -p ~/agent-course/dummy-agent
cd ~/agent-course/dummy-agent
python3.11 -m venv .venv
source .venv/bin/activate
python --version
```


仮想環境は、この演習用のPythonライブラリを他の作業と分けておく仕組みです。`.venv`を作る操作で環境を用意し、有効にする操作で、そのターミナルから使う環境を選びます。ダミー演習と第2週のテンプレートでは、それぞれ専用の環境を使います。

フォルダーがすでにあれば、作り直さずそこへ移動します。仮想環境も作成は一度で十分です。

**確認：**ターミナルに`(.venv)`が付き、Python 3.11.xと表示されます。このウィンドウを開いたままにします。

## 3. モデル用クライアントを入れる { #3-install-the-model-client }

どちらのOSでも次を実行します。

```bash
python -m pip install "openai>=1.0,<3"
```


最後にエラーが出ず、通常の入力待ち表示に戻るまで待ちます。このライブラリは互換APIを通じてGroqに接続します。OpenAIアカウントは不要です。

## 4. Groq APIキーを作る { #4-create-your-groq-api-key }

自分のアカウントでGroq Consoleに登録・ログインします。無料プランには[利用制限](https://console.groq.com/docs/rate-limits)があります。

### A. キーの画面を開く { #a-open-the-key-page }

1. ブラウザーで[Groq Console](https://console.groq.com)にログインします。
2. ナビゲーションの**API Keys**を開くか、[API Keysの直接リンク](https://console.groq.com/keys)を使います。
3. **Create API Key**をクリックします。
4. 名前に`agents-course`など用途が分かる名前を入れます。有効期限を選べる場合は授業期間をカバーするものを選びます。
5. ダイアログの作成・送信ボタンで確定します。
6. 生成された秘密のキーをコピーし、起動時に取り出せるようパスワードマネージャーなどに保管します。他の学生と共有したり、このガイド、ソース、チャットに貼ったりしないでください。

`agents-course`はラベルにすぎません。実際に使うのは生成された秘密の値です。画面の表記は変わる場合があります。[公式クイックスタート](https://console.groq.com/docs/quickstart)にもキー作成へのリンクがあります。

**確認：**自分のGroqキーを用意できました。ただし、キーを作っただけではモデルを選択したことにも、リクエストの成功を確認したことにもなりません。

ダミースクリプトはターミナルの非表示入力でキーを求めます。完全なエージェントでも同じキーを使います。Pythonファイルには書かないでください。

## 5. ダミー演習へ進む { #5-continue-to-the-dummy-exercise }

必要なら[基礎と小テスト](unit-1-walkthrough.md)を終え、[ダミー演習の3段階](dummy-agent-local.md)に進みます。ここではまだ`app.py`、Gradio、完全なエージェントのZIPは必要ありません。

## 別の日にダミー演習を再開する { #restart-the-dummy-exercise-another-day }

Windowsの場合：

```bat
cd /d "%USERPROFILE%\agent-course\dummy-agent"
.venv\Scripts\activate.bat
```


Macの場合：

```bash
cd ~/agent-course/dummy-agent
source .venv/bin/activate
```


演習でファイルを作成した後、`python dummy_agent.py`で実行し、求められたらキーを入力します。結果はブラウザーのチャットではなくターミナルに出ます。
