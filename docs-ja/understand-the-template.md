# smolagentsとテンプレートを理解する { #understand-smolagents-and-the-template }

最初の応答に成功した後、ツールを追加する前に読みます。`app.py`を横に開いてください。読み終えたら、どの部品がテキストを生成し、どの部品が行動を実行し、独自の機能をどこに加えるのかを説明できるようにしましょう。

## 1. smolagentsとは？ { #1-what-is-smolagents }

**smolagentsはHugging Faceが開発する、エージェント構築用のPythonライブラリです。** ライブラリとは、自分のプログラムに取り込んで使える再利用可能なコードです。ここではモデルに次の行動を尋ね、実行し、結果を記録して回答に進む仕組みを提供します。`CodeAgent`は行動をPythonコードで表します。スターターと一致する[バージョン1.13.0の紹介](https://huggingface.co/docs/smolagents/v1.13.0/en/index)も参照できます。

ダミー演習では、メッセージを組み立て、LLMを呼び、天気関数を実行して結果を返しました。テンプレートではその流れをフレームワークに任せます。ただしモデルを選び、ツールを用意し、結果を確認するのは自分です。

Hugging Faceの**ライブラリ**と教材を使い続けながら、問い合わせには**GroqのAPI**を使います。この構成ではsmolagentsをインストールしても、SpaceのホスティングやHF推論クレジットの購入は必要ありません。

## 2. 各部品の役割 { #2-which-component-does-what }

このプロジェクトのエージェントとは、モデル・指示・使える行動・実行ループを組み合わせた全体を指します。

| 部品 | このテンプレートでの役割 | 実行場所 |
| --- | --- | --- |
| Qwenモデル | 提案するPythonの行動を含め、次の応答を生成する | Groq経由のリモート |
| Groq API | 認証済みの要求を受け、モデル出力を返す | Groqのサービス |
| `OpenAIServerModel` | smolagentsのメッセージを互換API用に変換する | 手元のPythonプロセス |
| `CodeAgent` | モデル要求、Python実行、観測結果をつなぐ | 手元のPythonプロセス |
| 登録されたツール | 時刻取得など、公開した機能を実行する | 呼び出しはローカル。一部は外部サービスに接続 |
| Gradio | ブラウザーのチャット画面を提供する | ローカルのウェブサーバーとブラウザー |

`OpenAIServerModel`の「OpenAI」は互換APIの接続クラス名です。接続先とキーはGroqなので、OpenAIアカウントは必要ありません。

時刻ツールはPCの時計にタイムゾーンを適用し、検索ツールは外部検索サービスに問い合わせます。どちらもPythonの機能ですが、情報の出所が違います。

## 3. メッセージから答えまで { #3-from-a-message-to-an-answer }

次の矢印は双方向の流れを示します。毎回、同じローカルエージェントがモデルに問い合わせます。

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


ブラウザーの入力がGradioからCodeAgentへ渡り、指示・課題・過去の観測をGroqに送ります。戻ったPythonコードをローカルで実行し、結果かエラーを観測として記録します。必要なら次の問い合わせに進み、`final_answer(...)`で完了するとブラウザーに結果が表示されます。

例えば、時刻ツールを登録すると、次のような行動が生成されます。

```python
current_time = get_current_time_in_timezone("Asia/Tokyo")
print(current_time)
```


**モデルがコードを生成し、ローカルの実行器が実行します。** 出力が**観測結果**になり、次の問い合わせに含まれます。モデルは続いて`final_answer(...)`を生成することがあります。同じブロックでツールを呼んで終了することもあり、必要なステップ数は一定ではありません。

これが、チャット1回で複数のAPI要求が起きる理由です。「時刻を調べました」という発言だけでは不十分で、実行された呼び出しと結果を確認します。

### CodeAgentが自動で行うこと { #what-codeagent-handles-automatically }

**CodeAgentは行動と観測のループを管理します。** 行動を提案するのはモデルで、生成Pythonをローカルで実行して記録するのはフレームワークです。

| 作業 | 担当 |
| --- | --- |
| ツール関数と入力の説明を書く | 自分 |
| `tools=[...]`に登録する | 自分 |
| 登録済みの名前と説明を指示に入れる | CodeAgent |
| ツールを使うか決め、Python引数を生成する | モデル |
| Pythonとツールを実行し、出力・エラーを記録する | CodeAgentのローカル実行器 |
| 続きが必要なら観測を次の要求に含める | CodeAgent |
| `final_answer(...)`を呼ぶコードを生成する | モデル |
| 実行を終え、最終結果を返す | CodeAgent |

「Asia/Tokyoの時刻ツールを使って」と頼むと、CodeAgentが課題と登録済みツールをモデルに渡し、提案された呼び出しを実行し、必要なら続けます。最終回答、ステップ上限、エラーのいずれかで止まります。登録と自動実行は、選択や回答の正しさを保証しません。

ダミー演習では行動を確認して固定の関数を自分で呼びました。ここではCodeAgentがループを処理します。`12 * 8`は組み込みのPython実行器で計算できますが、実際の検索には登録済みの検索ツールが必要です。「Thought」やテキスト中の関数名だけでは実行の証明になりません。

編集箇所は、実習の[ツールの接続と選択](first-agent-practical.md#how-does-the-agent-know-which-tools-it-can-use)と[新しいツールの例](first-agent-practical.md#6-optional-create-your-own-tool)で確認できます。

## 4. 配布テンプレートに含まれるもの { #4-what-does-the-downloaded-template-provide }

接続と画面を組み立て済みの出発点となるプログラムなので、簡単な質問にはすぐ応答できます。学生版では時刻と検索の登録を意図的に残しています。未完成の独自ツールは発展課題で、画像生成は除外しています。

| ファイル | 用途 | 学習での扱い |
| --- | --- | --- |
| `app.py` | ツール定義、Groq設定、エージェント作成、画面起動 | 主に編集するファイル |
| `Gradio_UI.py` | 入力を渡し、ステップ・回答・エラーを表示 | 流れを読む。課題のための編集は不要 |
| `prompts.yaml` | 指示文と応答書式のテンプレート | 基本のツール課題の後に読む |
| `tools/web_search.py` | DDGSをsmolagentsに接続し、DuckDuckGoを使う | `WebSearchTool`を実習で登録する |
| `tools/final_answer.py` | 完了を伝えるツール | 登録を保つ |
| `requirements.txt` | パッケージとバージョン制約 | 指定のコマンドでインストールする |
| `STUDENT_TASKS.md` | ツール課題と完了確認 | 実習と併用する |
| `.venv/` | 手元のPython環境 | 環境準備で作成。配布コードには含まれない |

モデルの重みとAPIキーは含まれません。テンプレートを入手しても、PCにLLMをダウンロードしたことにはなりません。

## 5. app.pyを実行順に読む { #5-read-apppy-in-execution-order }

### インポートと関数定義 { #imports-and-function-definitions }

`from smolagents import ...`でライブラリの部品を使えるようにします。`get_current_time_in_timezone`の定義は呼び出せるツールを作るだけで、起動時には時刻を取得しません。同様に`WebSearchTool`のインポートだけでは検索しません。

独自ツールの仮実装は、呼ぶと`NotImplementedError`になります。意図した動作なので、実装してから登録します。初期状態で起動するのは、この仮実装をエージェントに公開していないためです。

### main()と起動の条件 { #main-and-the-startup-guard }

ファイル末尾は次のようになっています。

```python
if __name__ == "__main__":
    main()
```


`python app.py`で`main()`が起動します。テストから`app`をインポートする場合は関数を定義するだけでチャットを起動しません。これによりツールを独立してテストできます。

### キーの入力 { #the-key-prompt }

`main()`は最初に環境変数`GROQ_API_KEY`を確認し、空なら`getpass(...)`で非表示入力を求めます。キーは認証用で、テキストの使用量を表す入力・出力トークンとは別です。

入力したキーは保存されません。環境変数を別途設定しない限り、再起動ごとに入力します。

### モデルへの接続 { #the-model-connection }

動作するスターターの設定です。説明用であり、置き換え用ブロックではありません。

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
| `model_id` | サービスに要求するモデルの正確な識別子 |
| `api_base` | リクエストの送信先 |
| `api_key` | 起動時に渡す認証情報 |
| `max_tokens` | 1回の生成の最大出力。短い演習用に512から始める。アカウント枠内に収める必要があり、1日の予算ではない |
| `client_kwargs` | 1試行のタイムアウト30秒、最大2回の自動再試行。一時障害や短い待ちに対応するが、長い制限では停止することもある |
| `temperature` | 出力のばらつきに関わる設定。正確さの指標ではない |
| `reasoning_effort` | ここではモデルの別の推論モードを無効にする、モデル固有の設定 |

初回はそのまま使ってください。モデルを変えると対応するオプションや応答形式が変わる場合があります。変更しても利用枠が自動で増えるわけではありません。

### 指示とエージェントの構築 { #instructions-and-agent-construction }

`app.py`の横の`prompts.yaml`を読み、`CodeAgent`を作ります。主な引数は次のとおりです。

```python
model=model,
tools=[final_answer],
max_steps=6,
prompt_templates=prompt_templates,
```


`model`は接続、`tools`は明示的に利用できる機能、`max_steps`は課題のループ反復上限、`prompt_templates`はやり取りの指示を指定します。`max_steps`は成功の保証でも、総API呼び出し回数の厳密な上限でもありません。[この版のエージェント参照](https://huggingface.co/docs/smolagents/v1.13.0/en/reference/agents)には、引数とPythonコード型・JSONツール呼び出し型の違いがあります。

計画や管理対象エージェントの情報など、いくつかの任意設定には`None`を渡しています。ツール実習で変える必要はありません。`verbosity_level=1`はログの詳しさです。

### 画面の起動 { #launching-the-interface }

`GradioUI(agent).launch(server_name="127.0.0.1")`がローカル画面を起動します。サーバーを起動しただけではLLMに回答を求めません。チャットを送ると`Gradio_UI.py`の`agent.run(...)`が呼ばれます。

URLがローカルでも、モデル要求はインターネットを通ります。Pythonプロセスを止めるとアプリが停止します。画面の再読み込みではPythonの変更は読み込まれないため、編集後は再起動します。

## 6. 関数をツールにするには？ { #6-how-does-a-function-become-a-tool }

関数を実装し、用途と入力を説明し、エージェントに登録する必要があります。

```python
@tool
def get_current_time_in_timezone(timezone: str) -> str:
```


`@tool`はPythonのデコレーターで、smolagentsが使える情報を関数に付けます。型ヒントは入力と戻り値の型、docstringは機能と引数を説明します。説明は選択と入力作成を助けますが、処理そのものを実装はしません。[この版のツールガイド](https://huggingface.co/docs/smolagents/v1.13.0/en/tutorials/tools)も参照できます。

既存の関数は`tools`に名前だけで登録し、呼び出しません。ここで呼ぶと起動時に結果を得てしまいます。一方、`WebSearchTool()`の括弧は、用意されたツールクラスのインスタンスを作るために必要です。

独自ツールでは本体を実装し、戻り値を確かめます。正確な説明でも誤った計算は直りません。**直接呼ぶ → 登録 → エージェントに依頼 → 実行記録を確認**の順で試します。[任意課題の手順](first-agent-practical.md#6-optional-create-your-own-tool)には、説明、テストファイル、登録、チャットの例があります。

## 7. final_answerが最初からある理由 { #7-why-final_answer-is-already-included }

`final_answer = FinalAnswerTool()`で、同名で登録するオブジェクトを作ります。`final_answer(96)`などの生成Pythonが終了を伝え、表示する結果を渡します。この関数自体が追加のLLMリクエストを送るわけではありません。

あいさつでも`python_interpreter`が見えるのは、検索などが不要でも、CodeAgentが`final_answer`を呼ぶ小さなPythonブロックを実行する場合があるためです。

明示的なツールが完了用のものだけでも、Python実行器で簡単な計算はできます。検索や時刻関数を登録すると、その機能が追加されます。

## 8. 実行記録を読み、限界を理解する { #8-read-the-trace-and-understand-the-limits }

| 表示 | 分かること |
| --- | --- |
| モデルの説明・「Thought」 | 生成された説明。行動の証明でも内部推論の完全な記述でもない |
| コード | モデルが提案した行動 |
| `python_interpreter` | フレームワークによる生成Pythonの実行 |
| 観測・実行出力 | 実行で返された情報。エラーも含む |
| 最終回答 | 報告された結果。観測と照合する必要がある |
| 入出力トークン数 | モデル要求のテキスト使用量。APIキーではない |

実行中のアプリではメッセージ間で履歴を保持します。後の問い合わせに前のステップが入り、使用量が増えることがあります。独立した実験をしたいときはアプリを再起動して記憶を新しくします。会話履歴はモデルの訓練ではありません。

応答前のエラーなら接続・権限・要求形式・利用枠、コード実行中なら生成引数・ツール実装・登録・実行権限を調べます。[トラブル対応表](run-your-first-agent.md#troubleshooting)で該当する層を確認してください。

## 9. 編集前の確認 { #9-before-you-start-editing }

採点用ではなく、理解の確認に使います。

- リモートモデルを選ぶ行と、ローカルツールを選ぶ行を見つける。
- 検索クラスのインポートだけでは検索が有効にならない理由を説明する。
- 入力から行動、表示結果まで1つの応答をたどる。
- 独自ツールの仮実装と、登録が必要な2つの機能を見つける。

**次へ：**[ツールを組み込み、テストする](first-agent-practical.md)。必須は時刻と検索で、独自ツールは任意です。
