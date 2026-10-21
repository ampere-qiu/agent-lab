# ダミーエージェント：3段階でループを作る { #dummy-agent-build-the-loop-in-three-stages }

[HFのDummy Agentレッスン](https://huggingface.co/learn/agents-course/en/unit1/dummy-agent-library)にある手動ループの考え方を、ローカル用に構成した実習です。必要なコードはすべて下にあります。原典は任意の参考資料で、モデル接続をGroqに置き換えています。

問い合わせを送り、提案された行動を確認し、自分で関数を実行して結果を返します。仕組みを学ぶための例で、汎用の自律エージェントではありません。完全なテンプレートは後で扱います。

## 天気の情報はどこから来る？ { #where-weather-comes-from }

| 段階 | 実際に起こること | 天気の情報 |
| --- | --- | --- |
| ステップ1 | モデルが一般的な質問に答える | 天気の問い合わせも関数呼び出しもない |
| ステップ2 | モデルが行動の提案をテキストで書く | 関数はまだ実行されていない。天気を出力しても未検証 |
| ステップ3 | Pythonが`get_weather("London")`を実行する | 関数が固定のデモデータ「晴れ、18°C」を返す |

**ステップ3**で、**同じ`dummy_agent.py`ファイル**に`get_weather`を追加します。その`return`行に`sunny, 18 degrees Celsius`と書いてあります。演習用に決めた値で、観測値や実際の天気予報ではありません。Pythonがその戻り値をモデルに渡し、モデルが最終応答に使います。

古いスクリプトのプロンプトに「invent an example weather result」（天気の例を作って）とあれば、それはテキストだけのシミュレーションです。その版ではモデルが天気を作り、Pythonの天気関数は実行しません。以下の3段階は新しいファイルにまとめて使い、別の古いスクリプトの末尾には追加しないでください。

## ファイルを準備する { #prepare-the-file }

[基本設定](prepare-your-computer.md)を済ませ、`agent-course/dummy-agent`の仮想環境を有効にします。エディターでそのフォルダーに`dummy_agent.py`を作り、以下のブロックをこの1つのファイルに順に追加して、段階ごとに保存します。ステップ1のコードを貼って保存してから、次のコマンドで実行します。

```bash
python dummy_agent.py
```


出力はブラウザーチャットではなくターミナルに表示されます。再実行するたびに、ファイルに追加済みのリクエストがすべて繰り返され、Groqの利用枠を使います。上限に達したら、何度も再実行せずサービスの再試行間隔に従います。

## ステップ1. LLMに簡単な問い合わせを送る { #step-1-make-a-simple-llm-call }

新しいファイルに次を入れます。

```python
from getpass import getpass
from openai import OpenAI

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=getpass("Paste your Groq API key (hidden): ").strip(),
)
MODEL = "qwen/qwen3.8-27b"

reply = client.chat.completions.create(
    model=MODEL,
    reasoning_effort="none",
    messages=[{"role": "user", "content": "Name the capital city of France."}],
    max_tokens=150,
)
print("STEP 1 — model response:")
print(reply.choices[0].message.content)
```


保存して実行し、非表示の入力欄にキーを貼ってEnter／Returnを押します。コード中の英語の入力案内は「Groq APIキーを貼り付けてください（非表示）」という意味です。

**動作の説明：**`messages`がユーザーの質問を渡し、クライアントがGroqに送ります。`choices[0].message.content`で最初の回答を取り出します。ここでは天気の関数もエージェント用フレームワークも使っていません。

**確認：**フランスの首都がParisであるという応答が返ります。これはモデル接続のテストです。トレースバックが出た場合は接続やリクエストの問題なので、[トラブル対応](run-your-first-agent.md#troubleshooting)を確認してから先へ進みます。

## ステップ2. 提案された行動を確認する { #step-2-inspect-a-proposed-action }

ステップ1の下に追加します。

```python
SYSTEM_PROMPT = """You are demonstrating a text-based action loop.
The available capability is get_weather(location: str).
Describe an action as plain text, not a native API function call.
Use these labels in order:
Action: get_weather(location="city name")
Observation: the result supplied by the Python program
Final Answer: a brief answer using that result
Do not claim that an observation came from a real function unless supplied.
"""
weather_messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "Use get_weather to check the weather in London."},
]

proposal = client.chat.completions.create(
    model=MODEL,
    reasoning_effort="none",
    messages=weather_messages,
    max_tokens=250,
)
print("STEP 2A — without a stop marker:")
print(proposal.choices[0].message.content)

stopped_reply = client.chat.completions.create(
    model=MODEL,
    reasoning_effort="none",
    messages=weather_messages,
    max_tokens=250,
    stop=["Observation:"],
)
proposed_action = stopped_reply.choices[0].message.content or ""
print("STEP 2B — stop before the observation:")
print(proposed_action)
```


保存して再実行します。キーをもう一度入力し、2つの出力を比較してください。プロンプトは、`get_weather`を使う行動をテキストで示し、観測結果がまだないのに実際の関数の結果だと主張しないよう指示しています。

**動作の説明：**systemメッセージで機能を説明しても、関数は実行されません。停止マーカーなしでは、モデルが結果を作る、結果がないと伝える、そのまま終了するなどの可能性があります。文面は毎回同じとは限りません。`stop`は、指定したマーカーに達したときに生成を止め、その先をプログラムからのフィードバック用に残します。

**確認：**ステップ2Bに、Londonを入力とする`get_weather`の行動が提案されているか確認します。関数の結果を得たという主張は含まれないはずです。別の行動や都市なら、プロンプトを直してから続けます。停止マーカーだけで全指示への従順さが保証されるわけではありません。

## ステップ3. 関数を実行し、観測結果を返す { #step-3-execute-the-function-and-return-its-observation }

ステップ2の下に追加します。

```python
def get_weather(location: str) -> str:
    """Return fixed demonstration data, not a live weather forecast."""
    return f"Demo weather for {location}: sunny, 18 degrees Celsius."

# Read Step 2B first. This teaching script handles only the London example.
confirmation = input("Does Step 2B request get_weather for London? Type yes: ")
if confirmation.strip().lower() != "yes":
    raise SystemExit("Check the proposed action and prompt before running the function.")

observation = get_weather("London")
print("STEP 3 — actual Python function result:")
print(observation)

follow_up = weather_messages + [
    {"role": "assistant", "content": proposed_action},
    {
        "role": "user",
        "content": (
            "Observation from the Python function: " + observation
            + "\nNow give a final answer. Clearly label this as demo data."
        ),
    },
]
final_reply = client.chat.completions.create(
    model=MODEL,
    reasoning_effort="none",
    messages=follow_up,
    max_tokens=250,
)
print("STEP 3 — model answer using the observation:")
print(final_reply.choices[0].message.content)
```


**ステップ3を実行する：**`dummy_agent.py`を保存し、仮想環境を有効にした同じターミナルで`python dummy_agent.py`をもう一度実行します。先に前の段階も実行されます。キーを入力し、**STEP 2B**の出力がLondonの`get_weather`を求めていることを読んでから、`yes`と入力します。続いてステップ3の関数の結果、モデルの最終応答の順に表示されます。それ以外では「行動とプロンプトを確認してから関数を実行してください」として終了します。

**動作の説明：**人が提案を確かめ、Pythonが関数を呼び、その戻り値が次のモデルリクエストに加わります。答えの出所をたどれるよう、関数は「晴れ、摂氏18度」という固定データを返します。実際の天気APIには接続しません。最終応答でもデモデータと明示するよう指示しています。

確認を挟むのは意図的です。この小さなスクリプトは任意の行動を解析したり、自動で関数を選んだりしません。生成されたテキストを`eval`や`exec`に貼らないでください。次の実習ではCodeAgentが実行ループを担います。

**確認：**最終的なモデル応答より先に、関数の結果がターミナルに出ます。最終応答が晴れ・18度という値を反映し、デモだと分かることを確認します。観測と矛盾する場合は、検証済みの答えとして扱わず、最後のリクエストとプロンプトを調べます。

## この演習で学んだこと { #what-you-have-learned }

| 部分 | 確認できる根拠 |
| --- | --- |
| モデルへの問い合わせ | 最初の回答がGroqから返る |
| 行動の提案 | モデルが関数名と入力を示す |
| 実行 | Pythonスクリプトが実際に`get_weather`を呼ぶ |
| 観測結果 | 戻り値の文字列が次のリクエストに入る |
| 最終応答 | モデルが与えられた結果を使う |

天気関数はダミーの例です。完全なエージェントでは、**実際のタイムゾーン別時刻取得とウェブ検索**を使います。

**第1週の締めくくり：**[第1週の完了確認](week-1-learning-plan.md#week-1-completion)を行います。今週はここで終了できます。

**来週：**[第2週の計画](week-2-learning-plan.md)に沿って、[テンプレートのダウンロードと起動](run-your-first-agent.md)から始めます。
