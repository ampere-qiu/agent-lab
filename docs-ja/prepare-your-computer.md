# PCの準備 { #prepare-your-computer }

レッスンとダミー演習の前に、この手順を行います。この段階で必要なのはPythonとGroqキーだけです。完全なテンプレートは、ダミー演習の3段階を終えた**後**にダウンロードします。

## 1. Python 3.11をインストールする { #1-install-python-311 }

### Windows { #windows }

**コマンドプロンプト**を開き、コマンドを1つずつ実行します。

```bat
winget install --exact --id Python.Python.3.11
```

インストーラーの案内に従い、コマンドプロンプトを閉じて開き直してから確認します。

```bat
py -3.11 --version
```

`winget`が使えない場合は[Python 3.11.9のリリースページ](https://www.python.org/downloads/release/python-3119/)の**Files**から、x64 PC向けの**Windows installer (64-bit)**をダウンロードします。実行時に**Add python.exe to PATH**とPython launcherを有効にしてください。インストール後にコマンドプロンプトを開き直し、`py -3.11 --version`を再実行します。このガイドではPowerShellではなく**コマンドプロンプト**を使います。

### Mac { #mac }

**ターミナル**を開きます。Homebrewがあれば次を実行します。

```bash
brew install python@3.11
```

Homebrewがなければ[インストール手順](https://brew.sh)と最後の設定手順に従い、その後再実行してください。

インストールを確認します。

```bash
python3.11 --version
```

**確認：** Python 3.11.xが表示されます。Macの`python3`が古い版を指していても問題ありません。以下では`python3.11`を使います。

## 2. ダミー演習用のフォルダーを作る { #2-create-a-folder-for-the-dummy-exercise }

ターミナルを開き、自分のOSに合うコマンドを1つずつ実行します。

### Windows — コマンドプロンプト { #windows-command-prompt }

```bat
mkdir "%USERPROFILE%\agent-course\dummy-agent"
cd /d "%USERPROFILE%\agent-course\dummy-agent"
py -3.11 -m venv .venv
.venv\Scripts\activate.bat
python --version
```

### Mac — ターミナル { #mac-terminal }

```bash
mkdir -p ~/agent-course/dummy-agent
cd ~/agent-course/dummy-agent
python3.11 -m venv .venv
source .venv/bin/activate
python --version
```

フォルダーが既にあれば、作り直さずにその中へ移動します。仮想環境は一度作れば十分です。

**確認：** `(.venv)`とPython 3.11.xが表示されます。この画面を開いたままにします。

## 3. モデル接続用のクライアントを入れる { #3-install-the-model-client }

どちらのOSでも同じです。

```bash
python -m pip install "openai>=1.0,<3"
```

最後にエラーが出ず、通常の入力待ちに戻るまで待ちます。このライブラリはGroqの互換APIへの接続に使います。OpenAIアカウントは不要です。

## 4. 自分のGroq APIキーを作る { #4-create-your-groq-api-key }

自分のアカウントでGroq Consoleに登録またはログインします。無料プランにも[利用上限](https://console.groq.com/docs/rate-limits)があります。

### A. キーのページを開く { #a-open-the-key-page }

1. ブラウザーで[Groq Console](https://console.groq.com)にログインします。
2. メニューの**API Keys**、または[API Keysの直接リンク](https://console.groq.com/keys)を開きます。
3. **Create API Key**をクリックします。
4. `agents-course`など、用途が分かる名前を入力します。有効期限を選べる場合は授業期間をカバーする期限にします。
5. ダイアログの作成・送信ボタンで確定します。
6. 生成された秘密キーをコピーし、起動時に取り出せるようパスワードマネージャーに保管します。学生同士で共有せず、このガイド、コード、チャットにも貼り付けないでください。

`agents-course`はラベルにすぎません。生成された秘密の文字列が実際のキーです。画面の表記が変わる場合があります。[公式クイックスタート](https://console.groq.com/docs/quickstart)にもキー作成へのリンクがあります。

**確認：** 自分のGroqキーを用意できました。キーの作成だけでは、モデルの選択やモデルへのリクエスト成功は確認できません。

ダミーのスクリプトは、ターミナルの非表示入力でキーを求めます。後の完全なエージェントでも同じキーを使います。Pythonファイルには書かないでください。

## 5. レッスンに進む { #5-continue-to-the-lessons }

[基礎レッスンと小テスト](unit-1-walkthrough.md)、次に[ダミー演習の3段階](dummy-agent-local.md)へ進みます。今は`app.py`、Gradio、完全なZIPは**不要**です。

## 別の日にダミー演習を再開する { #restart-the-dummy-exercise-another-day }

Windows：

```bat
cd /d "%USERPROFILE%\agent-course\dummy-agent"
.venv\Scripts\activate.bat
```

Mac：

```bash
cd ~/agent-course/dummy-agent
source .venv/bin/activate
```

演習でファイルを作った後は`python dummy_agent.py`を実行し、求められたらキーを貼り付けます。結果はブラウザーのチャットではなくターミナルに表示されます。
