# 始める前に { #before-you-start }

このガイドでは、環境準備を最初から説明します。後半の実習では、Python関数、引数、戻り値を見分けることを前提とします。復習する場合は、[Pythonの関数定義の解説](https://docs.python.org/3.11/tutorial/controlflow.html#defining-functions)で引数と戻り値も確認してください。エージェントを作った経験は必要ありません。

## 必要なもの { #what-you-need }

- Windows PCまたはMac、ブラウザー、インターネット接続。
- Pythonとコードエディターをインストールできる権限。管理されたPCでは承認済みのソフトウェア配布窓口を使い、制限がある場合はインストールが許可されたPCを使います。
- モデルへの問い合わせ用の自分のGroqアカウント。実習にHFトークン、最終テスト、認定証は不要です。
- プレーンテキストを編集できるコードエディター。普段のものがあればそのまま使えます。[Visual Studio Code](https://code.visualstudio.com/docs/setup/setup-overview)を入れる場合は、File → Open Folderで演習フォルダーを開きます。

アプリがローカルでも、外部サービスには接続します。正しくインストールできていても、モデルの提供状況、アクセス権、利用枠で失敗することがあります。その段階のエラーは、必ずしもコードの間違いではありません。

## どのウィンドウを使うか { #know-which-window-to-use }

| ウィンドウ | 入力・操作するもの |
| --- | --- |
| MacのTerminal／WindowsのCommand Prompt | `python app.py`などのコマンド |
| コードエディター | `app.py`などのファイルの編集 |
| ブラウザー | アカウント設定、このガイド、小テスト、起動したエージェントとのチャット |

ターミナル用コマンドをエージェントのチャットに貼らないでください。キーもチャットやPythonソースに貼らないでください。

### コマンド用ウィンドウを開く { #open-a-command-window }

**Mac：**Command + Spaceを押し、`Terminal`と入力してReturnを押します。

**Windows：**スタートを開き、`Command Prompt`を検索して起動します。このガイドではPowerShellではなくコマンドプロンプトを使います。

コード枠の中身だけをコピーするか、コピーボタンを使ってください。外側のバッククォート3つ、質問例、実行結果はコピーしません。コマンドは1つずつ実行し、通常の入力待ち表示に戻ってから次に進みます。

`(.venv)`は入力待ち表示の一部で、コマンドではありません。`>>>`はPythonの対話画面です。`exit()`と入力してEnter／Returnを押すと、通常のコマンド画面に戻れます。

## ダウンロードしたプロジェクトを見つける { #find-your-downloaded-project }

ダミー演習では`agent-course/dummy-agent`で作業し、そこに`dummy_agent.py`を作ります。その後、スターターをダウンロードしたら、次の別フォルダーを使います。

```text
agent-course/
└── First_agent_template/
    ├── app.py
    ├── Gradio_UI.py
    ├── prompts.yaml
    ├── requirements.txt
    ├── tools/
    └── .venv/              (created during setup; may be hidden)
```


`.venv/`は環境準備で作られ、非表示の場合があります。他のファイルが入っていても構いません。編集するのはプロジェクトのファイルで、`.venv`内のファイルではありません。

**Mac：**Finderで「移動 → フォルダへ移動」を選び、`~/agent-course/First_agent_template`を入力してReturnを押します。

**Windows：**エクスプローラーのアドレス欄に`%USERPROFILE%\agent-course\First_agent_template`を入力してEnterを押します。

エディターの**File → Open Folder**などでそのフォルダーを開き、ファイル一覧から編集対象を選びます。ファイル管理画面で`.py`をダブルクリックすると、編集画面ではなくプログラムが起動する場合があります。

## 編集箇所を見失わずに保存する { #edit-a-file-without-losing-your-place }

1. 指定されたファイルをエディターで開きます。
2. 検索（MacはCommand + F、WindowsはControl + F）で、ガイドにある文字列を正確に探します。
3. 指定の行・ブロックだけを置き換えます。行頭の空白、カンマ、周囲の括弧を保ちます。
4. Command + S／Control + Sで保存します。拡張子は`app.py`のままにし、`app.py.txt`にしないでください。
5. ターミナルに戻り、動作中ならControl + Cで停止してから起動し直します。
6. アプリのブラウザーページを再読み込みします。

Pythonの編集にワープロソフトは使わないでください。インデントはPythonの構造の一部です。コード例の空白を保ちます。

## 困ったときは { #if-you-get-stuck }

最初に失敗したところで止まり、後のコマンドを続けて実行しないでください。手順番号とコマンドを控え、認証情報を除いたターミナルのエラーを[トラブル対応](run-your-first-agent.md#troubleshooting)と照合します。再試行前に、作業フォルダー、有効な環境、コマンドの綴りを確認します。

アプリの実行中はターミナルが使用中のままになります。これは正常です。同じ画面で別のコマンドを実行するには、Control + Cでアプリを停止します。MacでもCommandではなくControlキーです。

**第1週の次のステップ：**[エージェントの基礎](unit-1-walkthrough.md)を読み、[環境を準備](prepare-your-computer.md)します。
