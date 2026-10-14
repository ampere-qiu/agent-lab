# smolagentsとテンプレートを理解する { #understand-smolagents-and-the-template }

最初の応答が成功した後、ツールを追加する前に読みます。ガイドの横に`app.py`を開いてください。どの部品が文章を生成し、どの部品が行動を実行し、自分の機能をどこに追加するか説明できるようになるのが目標です。

## 1. smolagentsとは？ { #1-what-is-smolagents }

**smolagentsはHugging Faceが開発した、エージェントを作るためのPythonライブラリです。** ライブラリとは、プログラムに読み込んで再利用するコードです。ここでは、モデルに次の行動を尋ね、実行し、結果を記録し、答えに向けて続ける仕組みを提供します。`CodeAgent`は行動をPythonコードで表します。スターターと同じ[バージョン1.13.0の説明](https://huggingface.co/docs/smolagents/v1.13.0/en/index)を参照できます。

ダミー演習では自分でメッセージを組み立て、LLMを呼び、天気関数を実行して結果を戻しました。テンプレートでは、この順序をフレームワークが管理します。モデルの選択、ツールの提供、結果の確認は引き続き自分で行います。

Hugging Faceの**ライブラリ**と教材を使いながら、モデルへのリクエストには**Groq API**を使います。この構成では、smolagentsを入れるためにSpaceをホストしたり、HF推論クレジットを買ったりする必要はありません。

## 2. 各部品の役割 { #2-which-component-does-what }

このプロジェクトの*エージェント*は、モデル、指示、利用可能な行動、実行ループを組み合わせた全体です。

| 部品 | テンプレート内の役割 | 実行場所 |
| --- | --- | --- |
| Qwenモデル | 次の応答と、行動としてのPythonを生成する | Groq経由のリモート環境 |
| Groq API | 認証されたリクエストを受け、モデルの出力を返す | Groqのサービス |
| `OpenAIServerModel` | smolagentsのメッセージを互換APIの形式に変換する | 自分のPythonプロセス |
| `CodeAgent` | モデル呼び出し、Python実行、観測を管理する | 自分のPythonプロセス |
| 登録したツール | 時刻取得など、提供した機能を実行する | ローカルから呼ぶ。外部サービスに接続するものもある |
| Gradio | ブラウザーのチャット画面を提供する | ローカルWebサーバーとブラウザー |

`OpenAIServerModel`の「OpenAI」はAPI互換の接続クラスの名前です。このテンプレートの接続先とキーはGroqです。OpenAIアカウントは不要です。

時刻ツールはPCの時計とタイムゾーンを使います。検索ツールは外部の検索サービスにリクエストします。どちらもPythonの機能ですが、情報の取得元が異なります。

## 3. メッセージから答えまで { #3-from-a-message-to-an-answer }

矢印は往復の流れを示します。各モデル呼び出しは同じローカルエージェントが行います。図の英語は、上の部品名と対応しています。

```text
Browser chat
    ↓ user message
Gradio → CodeAgent on your computer
              ↓ instructions + task + earlier observations
         Groq → Qwen model
              ↓ model response containing Python code
         Local Python execution
              ↓ result or error recorded as an observation
         CodeAgent → another model request if needed
              ↓ final_answer(...) completes the task
Browser displays the result
```

例えば時刻ツールを登録した後、行動に次のコードが含まれることがあります。

```python
current_time = get_current_time_in_timezone("Asia/Tokyo")
print(current_time)
```

**モデルがコードを生成し、ローカルの実行機構が実行します。** 出力は**観測（observation）**となり、次のリクエストにも含められます。その後モデルが`final_answer(...)`を生成して終了する場合も、1ブロック内でツールを呼び終了する場合もあります。全課題でステップ数が同じとは限りません。

そのため1チャットメッセージでもAPIを複数回使うことがあります。また「時刻を確認しました」という文章だけでは証拠になりません。実行された呼び出しと結果を確認します。

## 4. テンプレートに含まれるもの { #4-what-does-the-downloaded-template-provide }

モデル接続と画面を組み立て済みの開始用プログラムです。簡単な質問にはすぐ答えられます。学生版では、必須の時刻・Web検索ツールを意図的に未登録にしています。未完成の自作ツールは任意の発展課題で、画像生成は含めません。

| ファイル | 役割 | 自分が行うこと |
| --- | --- | --- |
| `app.py` | ツール定義、Groq設定、エージェント作成、画面起動 | 実習で編集する主なファイル |
| `Gradio_UI.py` | チャットをエージェントへ渡し、ステップ・答え・エラーを表示 | 流れを読む。課題のための編集は不要 |
| `prompts.yaml` | 指示と応答形式のテンプレート | 基本ツール課題の後で確認 |
| `tools/web_search.py` | DDGSをsmolagentsのツールに変換し、DuckDuckGoを使う | 実習で`WebSearchTool`を登録 |
| `tools/final_answer.py` | スターターの最終応答ツール | 登録を維持 |
| `requirements.txt` | Pythonパッケージと版の条件 | 指定コマンドでインストール |
| `STUDENT_TASKS.md` | ツール課題と完了条件 | 実習ガイドと併用 |
| `.venv/` | ローカルのPython環境 | 設定時に作成。ダウンロードには含まれない |

モデルの重みやAPIキーは含まれません。テンプレートをダウンロードしても、PCにLLM本体が入るわけではありません。

## 5. app.pyを実行順に読む { #5-read-apppy-in-execution-order }

### インポートと関数定義 { #imports-and-function-definitions }

`from smolagents import ...`でライブラリの部品が使えるようになります。`get_current_time_in_timezone`の定義は呼び出せるツールを作りますが、起動時に時刻を取得するわけではありません。`WebSearchTool`のインポートも検索の実行ではありません。

自作ツールの仮実装は、呼ぶと`NotImplementedError`になります。登録前に実装するための意図的な仕組みです。初期状態でアプリが動くのは、エージェントに公開していないためです。

### main()と起動ガード { #main-and-the-startup-guard }

ファイルの末尾に次があります。

```python
if __name__ == "__main__":
    main()
```

`python app.py`なら`main()`が呼ばれます。テスト用スクリプトで`app`をインポートした場合は、関数を定義するだけでチャットを起動しません。これでツールを単独テストできます。

### キーの入力 { #the-key-prompt }

`main()`は最初に環境変数`GROQ_API_KEY`を確認します。空なら`getpass(...)`が表示しない入力欄でキーを求めます。キーはAPIリクエストの認証用で、利用量を表す入力・出力の*トークン*とは異なります。

入力したキーをアプリは保存しません。環境変数を別途設定していなければ、再起動時に再入力します。

### モデルの接続 { #the-model-connection }

動作するスターターの設定を説明用に示します。置き換え用のブロックではありません。

```python
model = OpenAIServerModel(
    model_id="qwen/qwen3.8-27b",
    api_base="https://api.groq.com/openai/v1",
    api_key=api_key,
    client_kwargs={"timeout": 30, "max_retries": 2},
    max_tokens=512,
    temperature=0.5,
    reasoning_effort="none",
)
```

| 設定 | 意味 |
| --- | --- |
| `model_id` | サービスに要求するモデルの正確なID |
| `api_base` | リクエストの送信先 |
| `api_key` | 起動時に渡す認証情報 |
| `max_tokens` | 1応答の最大出力。短い演習は512から始める。アカウント上限内に収める必要があり、1日分の利用予算ではない |
| `client_kwargs` | 各通信試行は30秒でタイムアウト。一時的な失敗や短い上限待ちには最大2回自動再試行する。長い制限では停止することがある |
| `temperature` | 出力のばらつきに関係するサンプリング設定。正確さの尺度ではない |
| `reasoning_effort` | モデル固有のオプション。ここでは独立した推論モードを無効にしている |

最初の実習では維持してください。モデルを変えると対応オプションや応答形式が変わることがあります。利用枠が自動的に増えることもありません。

### 指示とエージェントの作成 { #instructions-and-agent-construction }

`app.py`の隣の`prompts.yaml`を読み、`CodeAgent`を作ります。主な引数は次です。

```python
model=model,
tools=[final_answer],
max_steps=6,
prompt_templates=prompt_templates,
```

`model`は接続、`tools`は明示的に提供する機能です。`max_steps`は1課題の行動ループの反復上限で、成功の保証でも、API呼び出し総数の厳密な上限でもありません。`prompt_templates`は対話の指示です。[版を指定したエージェント資料](https://huggingface.co/docs/smolagents/v1.13.0/en/reference/agents)には、これらとPythonコード型・JSONツール呼び出し型の違いが説明されています。

計画や管理対象エージェントの情報など、一部の任意設定には`None`を渡しています。ツール課題では変更不要です。`verbosity_level=1`はログの詳しさを調整します。

### 画面の起動 { #launching-the-interface }

`GradioUI(agent).launch(server_name="127.0.0.1")`がローカル画面を起動します。起動だけではLLM応答を要求しません。チャット送信によって`Gradio_UI.py`の`agent.run(...)`が動きます。

URLはローカルでもモデルリクエストはネットを通ります。Pythonプロセスを停止するとアプリも止まります。ブラウザーの再読み込みだけでは編集したPythonは反映されないので、コードを変えたら再起動します。

## 6. 関数をツールにするには？ { #6-how-does-a-function-become-a-tool }

関数が存在し、入力と目的を説明し、エージェントに登録する必要があります。

```python
@tool
def get_current_time_in_timezone(timezone: str) -> str:
```

`@tool`はPythonのデコレーターです。smolagentsが利用できる情報を関数に付けます。型ヒントは引数と戻り値の型、docstringは機能と引数を説明します。モデルが関数を選ぶ助けになりますが、動作そのものを実装するものではありません。[この版のツールガイド](https://huggingface.co/docs/smolagents/v1.13.0/en/tutorials/tools)を参照できます。

既存の関数を登録するときは、呼び出さず名前を`tools`に追加します。呼ぶと、機能の登録ではなく、その場で結果を作ってしまいます。`WebSearchTool()`はツールクラスのインスタンスを作るため、異なる書き方です。

任意の自作ツールでは、関数の本体を書き、戻り値も検証します。正しい説明だけでは誤った計算は直りません。**直接呼び出す → 登録する → エージェントへ依頼する → 実行履歴を確認する**の順でテストします。

## 7. final_answerが最初からある理由 { #7-why-final_answer-is-already-included }

`final_answer = FinalAnswerTool()`で、その名前で登録するオブジェクトを作ります。生成Pythonの`final_answer(96)`などは終了を知らせ、表示する結果を渡します。この関数自体が追加のLLMリクエストを送るわけではありません。

検索や外部取得が不要な挨拶でも、小さなPythonブロックで`final_answer`を呼ぶため、`python_interpreter`が表示される場合があります。

初期状態で明示的なツールが最終応答だけでも、Python実行機構による簡単な計算はできます。検索や時刻関数を登録すると、その機能が追加されます。

## 8. 実行履歴と限界を読む { #8-read-the-trace-and-understand-the-limits }

| 表示 | 分かること |
| --- | --- |
| モデルの説明／Thought | 生成された説明。実行の証拠や内部推論の完全な記録ではない |
| Code | モデルが提案した行動 |
| `python_interpreter` | フレームワークによるPythonの実行 |
| Observation／実行出力 | 実行から返った情報。エラーも含む |
| Final answer | 報告された結果。観測との照合が必要 |
| 入力・出力トークン数 | モデルへのテキスト利用量。APIキーではない |

起動中のアプリはメッセージ間の履歴を保持します。後のリクエストには以前のステップが含まれ、利用量が増えます。独立した実験をしたいときはアプリを再起動し、エージェントの記憶を新しくします。会話履歴はモデルの学習ではありません。

モデル応答前のエラーは接続、アクセス、形式、利用上限を疑います。コード実行中のエラーは引数、ツール本体、登録、実行権限を確認します。対応する層の[トラブルシューティング](run-your-first-agent.md#troubleshooting)を参照してください。

## 9. 編集前の確認 { #9-before-you-start-editing }

追加の採点付きテストではなく、理解の確認です。

- リモートモデルを選ぶ行と、ローカルツールを選ぶ行を見つける。
- 検索クラスのインポートだけでは検索が使えない理由を説明する。
- チャット入力から行動、表示結果まで1つの応答を追う。
- 任意の自作ツールの仮実装と、登録する必須の2機能を見つける。

**次へ：** [ツールの実装・登録とテスト](first-agent-practical.md)。必須は時刻とWeb検索で、自作ツールは任意です。
