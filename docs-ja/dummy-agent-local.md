# ダミーエージェント：ループを3段階で作る { #dummy-agent-build-the-loop-in-three-stages }

[HFのDummy Agentレッスン](https://huggingface.co/learn/agents-course/en/unit1/dummy-agent-library)の手動ループを、ローカル演習に調整しています。必要なコードはすべて下にあります。元のページは任意の参考資料で、モデル接続にはGroqを使います。

リクエストを送り、提案された行動を確認し、自分で関数を実行して結果を戻します。学習用の例であり、汎用の自律エージェントではありません。完全なテンプレートは後で使います。

## ファイルの準備 { #prepare-the-file }

[基本設定](prepare-your-computer.md)を終え、`agent-course/dummy-agent`の仮想環境を有効にします。そのフォルダーにエディターで`dummy_agent.py`を作ります。以下のブロックを順に追加し、各段階で保存してください。実行コマンドは次のとおりです。

```bash
python dummy_agent.py
```

結果はブラウザーのチャットではなくターミナルに表示されます。再実行すると、ファイルにあるリクエストが繰り返され、Groqの利用枠を消費します。上限に達した場合は連続で実行せず、サービスが示す再試行時間を待ってください。

## ステップ1. 単純なLLM呼び出し { #step-1-make-a-simple-llm-call }

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

保存して実行します。非表示のキー入力欄にキーを貼り付け、Enter／Returnを押します。

**動作：** `messages`がユーザーの依頼を渡し、クライアントがGroqへ送信します。`choices[0].message.content`は最初の応答を読み取ります。天気の関数も、エージェントのフレームワークもまだ動いていません。

**確認：** パリと答える応答を受け取ります。モデル接続の確認です。トレースバックが出たら接続またはリクエストの問題なので、[トラブルシューティング](run-your-first-agent.md#troubleshooting)を確認してから進みます。

## ステップ2. 行動の提案を確認する { #step-2-inspect-a-proposed-action }

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

保存して再実行し、キーをもう一度入力します。2つの出力を比べてください。

**動作：** systemメッセージは機能を説明するだけで、実行しません。停止マーカーがない場合、モデルは結果を作り上げることも、結果がないと説明することも、そのまま止まることもあります。毎回同じ表現にはなりません。`stop`は指定したマーカーに達すると生成を止め、プログラムから結果を渡す位置を確保します。

**確認：** ステップ2Bに、Londonを入力とする`get_weather`の提案があることを確認します。関数の結果を得たという主張が含まれていないことも確認してください。別の行動や都市なら、プロンプトを直してから進みます。停止マーカーだけでは、すべての指示に従うことは保証できません。

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

**動作：** 提案を確認した後、Pythonが関数を呼び、戻り値を次のモデルへのリクエストに加えます。答えの由来を追えるよう、関数は固定のデモデータを返します。天気APIには接続しません。

確認の入力は意図的なものです。この小さなスクリプトは任意のモデルの行動を解析したり、関数を自動選択したりしません。生成された文章を`eval`や`exec`に貼り付けないでください。次の実習ではCodeAgentが実行ループを担当します。

**確認：** 最終応答より先に関数の結果がターミナルに出ます。応答は晴れ・18度の観測を反映し、デモデータだと明示するはずです。観測と矛盾するなら、確認済みの答えとして扱わず、最後のリクエストとプロンプトを見直します。

## 学んだこと { #what-you-have-learned }

| 要素 | 確認できる証拠 |
| --- | --- |
| モデルへのリクエスト | 最初の答えはGroqから返された |
| 行動の提案 | モデルが関数と入力を示した |
| 実行 | Pythonが実際に`get_weather`を呼んだ |
| 観測 | 関数の戻り値が次のリクエストに入った |
| 最終応答 | モデルが渡された結果を使った |

天気の関数はダミーの例です。完全なエージェントでは、**実際のタイムゾーンの時刻取得とWeb検索**を使います。

**次へ：** [テンプレートをダウンロードして実行](run-your-first-agent.md)し、[smolagentsによるループ管理を理解](understand-the-template.md)します。
