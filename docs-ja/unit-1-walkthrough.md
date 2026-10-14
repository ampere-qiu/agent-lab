# エージェントの基礎と小テスト { #agent-foundations-and-quick-quizzes }

[基本設定](prepare-your-computer.md)の後に読みます。各項目には元のHugging Faceレッスンへの直接リンクがあり、Alfredのイラストなどの図解を参照できます。その下に、この教材だけでも学べる説明を用意しています。ローカルPythonとGroqの実習は、このガイドの手順で進めてください。

!!! note "元のHF演習が動かない場合"

    元のHugging Faceコースの演習やプレイグラウンドには、現在使えないものや、アカウント・環境によって動かないものがあります。説明やAlfredのイラストは引き続き読めます。

    読み込めない、または動かないHF演習は**飛ばして、説明を読み進めてください**。壊れたプレイグラウンドを終える必要はありません。この教材の実習は、ここにあるローカルのダミー演習とGroqエージェント実習です。

## 1. エージェントとは？ { #1-what-is-an-agent }

**Hugging Faceで読む：** [What is an Agent?](https://huggingface.co/learn/agents-course/en/unit1/what-are-agents) — Alfredの図解があります。

エージェントは、モデルを使って目標に向けた行動を選び、ソフトウェアで実行し、その結果から次の行動を決めるプログラムです。

モデルは東京の時刻らしい文章を生成できます。一方、エージェントはタイムゾーンの関数を選んで実行し、返された値を利用できます。実際の関数呼び出しから得た情報は、文章の生成だけでは確認できないものです。

**目標（goal）**は達成したいこと、**ツール（tool）**は使える機能です。**行動（action）**はその機能の具体的な使用で、例えば`Asia/Tokyo`を引数に時刻関数を呼ぶことです。計画は適切な手順を選ぶことで、単純な課題なら1手で済むこともあります。

どのプログラムにもエージェントが必要なわけではありません。入力と計算方法が決まっていれば、関数を直接呼ぶ方が簡単です。依頼ごとに異なる機能や複数の判断が必要な場合に、エージェントが役立ちます。

## 2. 小テスト1 { #2-quick-quiz-1 }

[Hugging Faceの小テスト1](https://huggingface.co/learn/agents-course/en/unit1/quiz1)に取り組んでから戻ってきてください。問題を転載せず、元の対話型演習を利用します。一時的に使えない場合は先に読み進め、後で再試行します。

## 3. モデル、プロバイダー、ローカルプログラム { #3-the-model-provider-and-local-program }

**Hugging Faceで読む：** [What are LLMs?](https://huggingface.co/learn/agents-course/en/unit1/what-are-llms)

大規模言語モデル（LLM）は、与えられた文脈からテキストを生成します。学習によって言語のパターンや幅広い知識を獲得しますが、流暢な答えでも誤りや古い情報が含まれることがあります。PCやWebサイトの現在の状態を自動的に知っているわけではありません。

この教材ではQwenがモデル、GroqがAPI経由でモデルを提供するサービスです。Pythonプログラムがリクエストを送ります。APIはプログラム同士でリクエストと応答をやり取りするためのインターフェースです。Groqキーはそのリクエストの認証に使います。

モデルは**トークン（token）**単位でテキストを処理します。トークンは単語の一部や句読点などを表す符号化された単位です。入力トークンには指示や会話履歴、出力トークンには生成された文字列が含まれます。この利用量のトークンと、アクセストークンとも呼ばれるAPIキーは別物です。

前の結果をリクエストに加えると文脈が増えますが、利用量も増えます。モデルが扱える文脈には上限があります。メッセージを送ってもモデルの重みが学習・更新されるわけではありません。

## 4. メッセージと役割 { #4-messages-and-roles }

**Hugging Faceで読む：** [Messages and Special Tokens](https://huggingface.co/learn/agents-course/en/unit1/messages-and-special-tokens)

APIには、役割と内容を持つメッセージのリストを渡します。

```python
messages = [
    {"role": "system", "content": "Answer briefly and state when information is missing."},
    {"role": "user", "content": "What information would you need to tell me the local time?"},
]
```

**system**メッセージは指示、**user**メッセージは課題を与えます。**assistant**メッセージはモデルの応答を記録し、後のリクエストにも含められます。サービスはモデルのチャット形式を適用して役割を区別します。特殊トークンが役割の境界や列の終わりを示す場合もありますが、この教材の辞書に手で貼り付ける必要はありません。

ダミー演習では自分で観測結果を追加します。完全なエージェントではsmolagentsが履歴を管理します。

## 5. ツールと説明 { #5-tools-and-descriptions }

**Hugging Faceで読む：** [What are Tools?](https://huggingface.co/learn/agents-course/en/unit1/tools)

ツールは目的、入力、出力を持つ実行可能なコードです。ローカルのデータを使うことも、外部サービスに接続することもあります。

| 必須ツール | 入力 | 結果の取得元 | 確認する証拠 |
| --- | --- | --- | --- |
| タイムゾーンの時刻取得 | `Asia/Tokyo`などのタイムゾーン | PCの時計とタイムゾーン規則 | 関数呼び出しと返された時刻 |
| Web検索 | 検索語句 | 外部の検索サービス | 検索の実行と返された関連資料 |

モデルはツールの説明を見て機能を選び、引数を組み立てます。説明を書くことと関数を実装することは別です。関数を定義してもエージェントに登録したことにはならず、生成文に名前が出ても実行の証拠にはなりません。

検索結果も確認が必要です。返されたページを開き、一次資料を優先し、必要なら日付を確認します。モデルの記憶から生成されたURLは検索した証拠ではありません。

## 6. 小テスト2 { #6-quick-quiz-2 }

モデル、メッセージ、ツールを扱う[Hugging Faceの小テスト2](https://huggingface.co/learn/agents-course/en/unit1/quiz2)に取り組みます。この教材のテストはこの2回です。アカウントが必要な最終テストや認定の流れは対象外です。

## 7. 行動と観測のループ { #7-the-actionobservation-loop }

### Hugging Faceで読む { #read-on-hugging-face }

1. [Thought–Action–Observation Cycle](https://huggingface.co/learn/agents-course/en/unit1/agent-steps-and-structure)
2. [Thought: Internal Reasoning and the ReAct Approach](https://huggingface.co/learn/agents-course/en/unit1/thoughts)
3. [Actions: Enabling the Agent to Engage with Its Environment](https://huggingface.co/learn/agents-course/en/unit1/actions)
4. [Observe: Integrating Feedback to Reflect and Adapt](https://huggingface.co/learn/agents-course/en/unit1/observations)

### この教材でのまとめ：ループの動き { #local-summary-how-the-loop-runs }

上のレッスンを、1回のエージェントループの流れとしてまとめます。

1. 課題、指示、利用できる機能をモデルに送ります。
2. 行動の提案を受け取ります。
3. プログラムでその行動を実行します。
4. 結果またはエラーを観測（observation）として記録します。
5. 観測をモデルに渡し、次の行動か終了を選ばせます。

課題について考えることと行動することを結びつける方式で、ReActとして説明されることもあります。画面に表示される「Thought」は生成された説明であり、実行の証拠でも、内部推論の完全な記録でもありません。実際の呼び出しと結果を確認してください。

行動の形式には、関数名と入力を表す構造化データやコードがあります。ダミー演習では文章で行動を記述し、完全な`CodeAgent`ではフレームワークが実行するPythonを生成します。これらはAPI設定として置き換え可能な形式ではありません。

観測は、無効なタイムゾーンや検索のブロックなどのエラーの場合もあります。推測を確認済みの結果として扱わず、この違いを維持します。ステップ数の上限はループを制限しますが、正しさを保証しません。

## 8. 実習で確かめる { #8-put-the-concepts-into-practice }

**元のHF実習：** [Dummy Agent Library](https://huggingface.co/learn/agents-course/en/unit1/dummy-agent-library)、[Let’s Create Our First Agent Using smolagents](https://huggingface.co/learn/agents-course/en/unit1/tutorial)。背景理解のために読めますが、実行環境の構築は以下のローカル手順で進めます。

[ダミーを3段階で作成](dummy-agent-local.md)し、[スターターを入手](run-your-first-agent.md)、[構成を理解](understand-the-template.md)、[時刻とWeb検索を有効化](first-agent-practical.md)します。

最後に、両方のツールが実行されたことを示し、結果を説明します。自作ツールは任意で、画像生成は含めません。

原典と補足資料：[Hugging Face Agents Course Unit 1](https://huggingface.co/learn/agents-course/en/unit1/introduction)。このサイトの説明はGroq実習向けに書いたもので、原典をそのまま転載したものではありません。
