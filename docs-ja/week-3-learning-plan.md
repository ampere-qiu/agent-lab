# 第03週 · 学習計画とダウンロード { #week-3-learning-plan }

今週は、**smolagentsと自分のGroqキー**を使い、小さなPythonエージェントをターミナルで動かします。題材は、アルフレッドのパーティー準備です。音楽の検索、メニューの選択、準備時間の計算、ケータリングやテーマを選ぶツールに取り組みます。

**時間の目安：3〜4時間。** smolagentsの概要、CodeAgent、アクションの表し方、ツールを扱います。[検索・取得を行うエージェントと、その先の内容は第04週に続きます](week-4-preview.md)。

## 学習目標 { #learning-objectives }

小さなエージェントプログラムを作成・実行し、アクションと観測結果を見分けられるようになります。Pythonコードと構造化されたツール呼び出しの違いを説明し、Pythonツールが使うデータを変更できることを目指します。

## 用意するもの { #what-you-need }

第2週で使った**`First_agent_template`フォルダー**、**Python 3.11の`.venv`**、コードエディター、**Groq APIキー**を使います。Groqへの問い合わせとウェブ検索にはインターネット接続が必要です。

**今週のプログラムはターミナルだけで動かし、結果もそこに表示します。** 第03週のためにGradioやブラウザのチャット画面を起動する必要はありません。この教材サイトでは手順を読みます。

## 今週の進め方 { #learning-sequence }

| レッスン | 取り組むこと | 時間の目安 |
| --- | --- | --- |
| [08 · smolagents入門](week-3-framework.md) | モデル、フレームワーク、ツールの役割を読む。 | 20〜25分 |
| [09 · CodeAgentを動かす](week-3-code-agent.md) | 音楽検索、メニュー選択、準備時間のプログラムを作って動かす。 | 50〜60分 |
| [10 · Pythonコードと構造化ツール呼び出し](week-3-action-formats.md) | 2種類のアクションを比べ、ToolCallingAgentを動かして実行記録を読む。 | 30〜40分 |
| [11 · 関数とクラスで作るツール](week-3-custom-tool.md) | 直接テストと2つのエージェントを作り、ツールのデータを変える。 | 50〜60分 |
| [12 · 完了確認](week-3-completion.md) | 保存したファイルと実行結果を示す。 | 15分 |

以下の準備、質問、サービスの利用制限への対応には、別途時間を見込んでください。

## 1. 補助ファイルをダウンロードして配置する { #exercise-files }

**何が入っていますか？** ZIPには**6つの補助ファイル**が入っています。Groqへの接続、用意済みのPythonツール、パッケージ一覧、手順書、原典のライセンスです。小さなエージェント本体は、レッスンのコードを使って自分で作ります。

[第03週の補助ファイルをダウンロード（.zip）](downloads/week03-smolagents.zip){ .md-button .md-button--primary download="week03-smolagents.zip" }

| ZIP内のファイル | 役割 |
| --- | --- |
| `week03_common.py` | Groqへの接続、エージェントの設定、結果・エラーの表示。 |
| `week03_tools.py` | メニュー、ケータリング、パーティーテーマのツール。 |
| `week03_search.py` | ウェブ検索ツール。 |
| `week03-requirements.txt` | 今週必要なPythonパッケージの一覧。 |
| `week03_README.md` | 環境準備と実行の手順書。 |
| `week03-HF-LICENSE.txt` | Hugging Faceの原典のライセンス。 |

1. 第2週のチャットアプリが動いていれば、そのターミナルで**Control + C**を押して停止します。
2. ダウンロードボタンを押します。通常、ZIPは**ダウンロード**フォルダーに保存されます。
3. **Windows：**ZIPを右クリック → **すべて展開** → **展開**。**Mac：**FinderでZIPをダブルクリックします。
4. 展開された**`week03-exercises`**フォルダーを開き、中の**6ファイル**をコピーします。
5. **既存の`First_agent_template`フォルダー**内、`app.py`と同じ場所に貼り付けます。`week03-exercises`フォルダーごとではなく、中のファイルだけをコピーしてください。以前の`week03...`ファイルを編集している場合は、同名ファイルを置き換える前に編集内容をバックアップします。

ファイル管理画面で、コピー先を開きます。

- **Windows — エクスプローラー：**アドレス欄に`%USERPROFILE%\agent-course\First_agent_template`を貼り付け、Enterを押します。
- **Mac — Finder：****移動 → フォルダへ移動**を選び、`~/agent-course/First_agent_template`を入力してReturnを押します。

これは第2週の標準の保存場所です。別の場所に保存した場合は、その既存フォルダーを使ってください。空の代替フォルダーを新しく作る必要はありません。

コピー後は、6ファイルが既存の`app.py`や`.venv`フォルダーと並びます。ZIPには補助処理とツールが入り、それらを使う`my_...py`プログラムの作り方はレッスンにあります。

## 2. エディターでプロジェクトを開く { #open-project }

コードエディターを開きます。VS Codeでは**ファイル → フォルダーを開く**から**`First_agent_template`**を選びます。ファイル一覧に`app.py`、`week03_common.py`、`week03_tools.py`、`week03_search.py`が並んでいることを確認してください。

レッスンで**ファイルを作成する**とあったら、**ファイル → 新しいテキストファイル**を選び、示されたPythonコード全体を貼り付けます。**ファイル → 名前を付けて保存**で、指定された名前でこのフォルダーに保存します。保存先は`app.py`と同じ場所です。`.venv`や`tools`の中には保存しません。

編集後はWindowsで**Ctrl + S**、Macで**Command + S**を押します。`my_playlist.py.txt`ではなく、`my_playlist.py`という名前にしてください。

## 3. ターミナルを開いて環境を有効にする { #activate-environment }

**Windows：**スタートで**コマンドプロンプト**を検索して開きます。Windows用のコマンドは、PowerShellではなく、このコマンドプロンプトのウィンドウで実行してください。

```bat
cd /d "%USERPROFILE%\agent-course\First_agent_template"
.venv\Scripts\activate.bat
python --version
dir
```

**Mac：****ターミナル**を開いて実行します。

```bash
cd ~/agent-course/First_agent_template
source .venv/bin/activate
python --version
ls
```

1行ずつ実行します。**`(.venv)`**が表示され、Pythonが**3.11.x**で、一覧に配布された`week03...`ファイルがあることを確認します。現在のフォルダーは`First_agent_template`です。

新しいターミナルを開いたら、`cd`と環境の有効化をやり直します。実習中はこのターミナルを開いたままにしましょう。この後のレッスンでは**実行：`python filename.py`**とだけ示します。WindowsでもMacでも、この環境を有効にした`First_agent_template`のターミナルで実行します。

## 4. 必要なパッケージを確認する { #packages }

**Windows・Mac共通で**、環境を有効にした同じターミナルで実行します。

```bash
python -m pip install -r week03-requirements.txt
```

一覧にあるのは`smolagents==1.13.0`、`openai>=1.0,<3`、`ddgs==9.16.0`だけです。Gradio、LangChain、BM25、GPU、ブラウザ自動操作用のパッケージは追加しません。第2週の環境にインストール済みなら、`Requirement already satisfied`と表示されます。

続いて、Groqを使わずに、配布されたメニューツールを確認します。

```bash
python -c "from week03_tools import suggest_menu; print(suggest_menu(occasion='formal'))"
```

表示される結果：

```text
3-course dinner with wine and dessert.
```

これは「ワインとデザート付きの3コースディナー」という意味です。フォルダー、読み込み、Pythonツールが動くことを確認しています。LLMへの問い合わせは行いません。

## 自分で作るファイル { #files }

| レッスン | 新しく作るファイル（すべてFirst_agent_template内） |
| --- | --- |
| 09 | `my_playlist.py`、`my_menu.py`、`my_timing.py` |
| 10 | `my_tool_calling.py` |
| 11 | `my_tool_check.py`、`my_catering.py`、`my_theme.py` |

各実習には、コード全体、ファイル名、短い実行コマンド、出力の確認点を示しています。環境の準備は上の手順を共通して使います。**読むだけ**と書かれた短いコードは、用意済みの関数や実行時の出力です。追加のプログラムとして作る必要はありません。

## 動かないとき { #local-adaptation }

| メッセージや症状 | 確認すること |
| --- | --- |
| フォルダーが存在しない | ファイル管理画面で実際の`First_agent_template`の場所を探し、その場所を指定します。 |
| `.venv`の有効化ファイルが見つからない | フォルダーが違う可能性があります。第2週で使ったプロジェクトと環境を使います。 |
| `can't open file` | 指定の`.py`ファイルを`app.py`と同じ場所に保存します。綴りと、`.py.txt`になっていないかを確認します。 |
| `No module named week03_common` | ZIPの中身を、新しいプログラムと同じ場所に置きます。下位フォルダーに入れないでください。 |
| `No module named smolagents`、`openai`、`ddgs` | `.venv`を有効にし、上のパッケージ導入コマンドを実行します。 |
| Groqキーを入力しても何も見えない | 入力は非表示です。キーを入力してEnterを押します。 |
| Groqへの問い合わせや検索が失敗する | 実際のエラーを教員に見せ、[第2週のトラブル対処](run-your-first-agent.md#troubleshooting)を確認します。 |

## 出典 { #sources }

レッスン、パーティーの例、出典を付した図は、[Hugging Face Agents Course Unit 2.1](https://huggingface.co/learn/agents-course/en/unit2/smolagents/introduction)を基に構成しています。[Apache 2.0ライセンス](licenses/huggingface-agents-course.txt)はダウンロードにも含まれます。

**次へ：**[08 · smolagents入門](week-3-framework.md)。
