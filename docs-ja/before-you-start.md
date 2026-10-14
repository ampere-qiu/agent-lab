# 始める前に { #before-you-start }

このガイドは環境構築を最初から説明します。後半の実習では、Pythonの関数、引数、戻り値が分かることを想定しています。復習には[Pythonの関数定義ガイド](https://docs.python.org/3.11/tutorial/controlflow.html#defining-functions)を使い、引数と戻り値も確認してください。エージェントを作った経験は不要です。

## 必要なもの { #what-you-need }

- Windows PCまたはMac、ブラウザー、インターネット接続。
- Pythonとコードエディターをインストールする権限。管理されたPCでは承認済みのソフトウェア配布窓口を使い、制限がある場合はインストール権限のあるPCを使ってください。
- モデル呼び出し用の、自分のGroqアカウント。この実習にHFトークン、最終テスト、認定証は不要です。
- プレーンテキストを編集できるコードエディター。普段のものがあれば使えます。[Visual Studio Code](https://code.visualstudio.com/docs/setup/setup-overview)をインストールする場合は、File → Open Folderで演習フォルダーを開きます。

ローカルアプリでも外部サービスに接続します。インストールが正しくても、モデルの提供状況、権限、利用上限で失敗することがあります。その段階のエラーが必ずしもコードの間違いとは限りません。

## どの画面で操作するか { #know-which-window-to-use }

| 画面 | 入力・操作する内容 |
| --- | --- |
| Macのターミナル／Windowsのコマンドプロンプト | `python app.py`などのコマンド |
| コードエディター | `app.py`などのファイルの編集 |
| ブラウザー | アカウント設定、このガイド、小テスト、エージェントのチャット |

ターミナルのコマンドをエージェントのチャットに貼り付けないでください。キーやトークンをチャットやPythonのソースファイルに貼り付けないでください。

### コマンドを入力する画面を開く { #open-a-command-window }

**Mac：** Command + Spaceを押し、`Terminal`と入力してReturnを押します。

**Windows：** スタートで`Command Prompt`を検索して開きます。このガイドではPowerShellではなくコマンドプロンプトを使います。

コードブロックの中の文字だけをコピーするか、コピーボタンを使ってください。囲みのバッククォート3個、入力例のプロンプト、実行結果はコピーしません。コマンドは1つずつ実行し、入力待ちの表示に戻ってから次へ進みます。

`(.venv)`は入力待ちの表示の一部で、コマンドではありません。`>>>`はPythonの対話モードです。`exit()`を入力してEnter／Returnを押すと通常のコマンド画面に戻ります。

## ダウンロードしたプロジェクトを見つける { #find-your-downloaded-project }

ダミー演習では`agent-course/dummy-agent`で作業し、その中に`dummy_agent.py`を作ります。その後、完全なスターターをダウンロードしたら、別のフォルダーを使います。

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

ほかのファイルがある場合もあります。編集するのはプロジェクトのファイルで、`.venv`内のファイルではありません。

**Mac：** Finderで「移動 → フォルダへ移動」を選び、`~/agent-course/First_agent_template`を入力してReturnを押します。

**Windows：** エクスプローラーのアドレス欄に`%USERPROFILE%\agent-course\First_agent_template`を入力してEnterを押します。

エディターの**File → Open Folder**などでフォルダーを開き、ファイル一覧から対象を選んでください。ファイル管理画面で`.py`をダブルクリックすると、編集画面ではなくプログラムが実行される場合があります。

## ファイルを正しく編集する { #edit-a-file-without-losing-your-place }

1. 指定されたファイルをエディターで開きます。
2. 検索（MacはCommand + F、WindowsはControl + F）で、ガイドに示された文字を探します。
3. 指定した行やブロックだけを置き換えます。先頭の空白、カンマ、周囲の括弧を維持します。
4. Command + SまたはControl + Sで保存します。拡張子は`app.py`のままで、`app.py.txt`にしません。
5. ターミナルに戻り、実行中ならControl + Cで停止してから再起動します。
6. アプリのブラウザーページを再読み込みします。

Pythonの編集にワープロは使わないでください。インデントはPythonの構造の一部です。例に示した空白を保ってください。

## 困ったとき { #if-you-get-stuck }

最初に失敗した手順で止まり、後続のコマンドを実行しないでください。手順番号と実行コマンドを控えます。認証情報を除いてターミナルのエラーをコピーし、[トラブルシューティング](run-your-first-agent.md#troubleshooting)と照合してください。現在のフォルダー、仮想環境、正確なコマンドを確認してから再試行します。

アプリの実行中はターミナルが入力待ちに戻らないのが正常です。別のコマンドを実行するときは、先にControl + Cで停止します。MacでもCommandではなくControlです。

**次へ：** [PCの準備](prepare-your-computer.md)。
