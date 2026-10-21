# エージェントの基礎と小テスト { #agent-foundations-and-quick-quizzes }

第1週はこの基礎から始めます。[ローカル環境の準備](prepare-your-computer.md)は読んだ後に行います。各項目にはHF原典への直接リンクがあり、Alfredの図解などを見ることができます。リンクの下にある解説だけでも学べるようにしています。実行するPythonとGroqの手順はこのガイドを使ってください。

!!! note "HF原典の活動が動かない場合"

    Hugging Faceの実習や実験画面には、利用できなかったり、アカウントや環境に合わなかったりするものがあります。説明やAlfredの図解は引き続き参照できます。

    原典の活動が読み込めない・動かない場合は、**その活動を飛ばして読み進めてください**。動かないHF実験画面を完了する必要はありません。この教材の実習は、後で行うローカルのダミー演習とGroqエージェントです。

## 1. エージェントとは？ { #1-what-is-an-agent }

**HF原典：**[エージェントとは？（What is an Agent?）](https://huggingface.co/learn/agents-course/en/unit1/what-are-agents) — Alfredの図解もあります。

エージェントとは、目標に向けた行動をモデルで選び、ソフトウェアを通じて実行し、その結果を使って次の行動を決めるプログラムです。

例えばモデルは東京の時刻らしい文字列を生成できます。一方、エージェントならタイムゾーン関数を選んで実行し、戻り値を使えます。実際の関数呼び出しは、テキスト生成だけでは確認できない情報をもたらします。

**目標**は達成したいこと、**ツール**は利用可能な機能、**行動**はその機能を具体的に使うことです。例えば時刻関数に`Asia/Tokyo`を渡すのが行動です。計画とは適切な手順を選ぶことで、簡単な課題なら1手で済むこともあります。

すべてのプログラムにエージェントが必要なわけではありません。入力が決まった計算なら、関数を直接呼ぶ方が簡単なことが多いでしょう。要求に応じて機能を選ぶ必要があるときや、複数の判断が必要なときにエージェントが役立ちます。

## 2. 小テスト1 { #2-quick-quiz-1 }

[Hugging Faceの小テスト1](https://huggingface.co/learn/agents-course/en/unit1/quiz1)に取り組んで戻ってきてください。問題を複製せず、原典の対話式活動を使います。一時的に利用できなければ先を読み、後で再試行します。

## 3. モデル・提供サービス・ローカルプログラム { #3-the-model-provider-and-local-program }

**HF原典：**[LLMとは？（What are LLMs?）](https://huggingface.co/learn/agents-course/en/unit1/what-are-llms)

大規模言語モデル（LLM）は与えられた文脈からテキストを生成します。訓練により言語のパターンや広い知識を得ていますが、流暢な回答でも間違いや古い情報が含まれます。PCやウェブサイトの現在の状態が自動的に分かるわけではありません。

このコースではモデルがQwen、それをAPIで提供するサービスがGroq、リクエストを送るのが手元のPythonプログラムです。APIはプログラム間で要求と応答をやり取りするために定められた窓口です。Groqキーは要求の認証に使います。

モデルは**トークン**という符号化されたテキストの単位を処理します。単語の一部や句読点などが単位になります。入力トークンには指示と会話履歴、出力トークンには生成されたテキストが含まれます。これらの使用量を表すトークンと、アクセストークンとも呼ばれるAPIキーは別です。

前の結果をリクエストに含めると文脈になりますが、使用量も増えます。扱える文脈の容量は有限です。メッセージを送っても、モデルの重みが訓練・更新されるわけではありません。

## 4. メッセージと役割 { #4-messages-and-roles }

**HF原典：**[メッセージと特殊トークン](https://huggingface.co/learn/agents-course/en/unit1/messages-and-special-tokens)

APIには役割と本文を持つメッセージのリストを渡します。

```python
messages = [
    {"role": "system", "content": "Answer briefly and state when information is missing."},
    {"role": "user", "content": "What information would you need to tell me the local time?"},
]
```


例では「短く答え、情報が不足する場合は伝える」という指示と、「現地時刻を知るにはどんな情報が必要か」という質問を送っています。

**system**は指示、**user**は課題を渡します。**assistant**はモデルの応答を記録し、後の問い合わせにも含められます。サービス側がチャットの書式を適用して役割を区別します。特殊トークンは役割の境界や列の終わりなどを示しますが、この教材の辞書にそのマーカーを手動で貼る必要はありません。

ダミー演習では自分で観測結果を追加します。完全なエージェントではsmolagentsが履歴を管理します。

## 5. ツールと説明文 { #5-tools-and-descriptions }

**HF原典：**[ツールとは？（What are Tools?）](https://huggingface.co/learn/agents-course/en/unit1/tools)

ツールは目的・入力・出力を持つ実行可能なコードです。ローカルデータを使う場合も、外部サービスに接続する場合もあります。

| 必須ツール | 入力 | 結果の出所 | 確認する根拠 |
| --- | --- | --- | --- |
| タイムゾーン別時刻 | `Asia/Tokyo`など | PCの時計とタイムゾーン規則 | 関数呼び出しと戻り値 |
| ウェブ検索 | 検索語句 | 外部の検索サービス | 検索の実行と、返された関連情報源 |

モデルは説明文を使って機能を選び、入力を組み立てます。説明文は実装ではありません。関数を定義してもエージェントに登録したことにはならず、生成テキストに名前が出ても実行の証明にはなりません。

検索結果も確認が必要です。返されたページを開き、一次情報を優先し、必要に応じて日付を確かめます。モデルが記憶から作ったURLは検索の根拠ではありません。

## 6. 小テスト2 { #6-quick-quiz-2 }

モデル・メッセージ・ツールを扱う[Hugging Faceの小テスト2](https://huggingface.co/learn/agents-course/en/unit1/quiz2)に取り組みます。この教材のテスト活動はこの2つです。アカウントが必要な最終テストと認定取得は範囲外です。

## 7. 行動と観測のループ { #7-the-actionobservation-loop }

### HF原典を読む { #read-on-hugging-face }

1. [Thought–Action–Observationのサイクルで理解するAIエージェント](https://huggingface.co/learn/agents-course/en/unit1/agent-steps-and-structure)
2. [Thought：内部推論とReAct](https://huggingface.co/learn/agents-course/en/unit1/thoughts)
3. [Action：環境に働きかける](https://huggingface.co/learn/agents-course/en/unit1/actions)
4. [Observe：結果を取り入れて調整する](https://huggingface.co/learn/agents-course/en/unit1/observations)

### この教材での要点：ループの動き { #local-summary-how-the-loop-runs }

上のレッスンを、1回のエージェントループの流れにまとめると次のようになります。

1. 課題、指示、利用可能な機能をモデルに送る。
2. 提案された行動を受け取る。
3. プログラムで行動を実行する。
4. 結果またはエラーを観測結果として記録する。
5. 観測結果をモデルに渡す。モデルは次の行動を提案するか、終了する。

課題を考えることと実際の行動を結び付ける考え方で、ReActとして説明されます。表示される「Thought」は生成された説明文であり、実行の証明でも、内部推論を完全に示したものでもありません。実際の呼び出しと結果を確認します。

行動は、関数名と入力を示す構造化データの場合も、コードの場合もあります。ダミー演習ではテキストで行動を示し、完全な`CodeAgent`ではフレームワークが実行するPythonを生成します。これらをAPI設定で同じ形式として扱うことはできません。

無効なタイムゾーンや検索の遮断など、観測結果がエラーの場合もあります。推測を検証済みの結果として扱わず、その違いを残します。ステップ数の上限はループを制限しますが、正しさは保証しません。

## 8. 基礎を実習につなげる { #8-put-the-concepts-into-practice }

**HF原典の実習：**[Dummy Agent Library](https://huggingface.co/learn/agents-course/en/unit1/dummy-agent-library)と[smolagentsで最初のエージェントを作る](https://huggingface.co/learn/agents-course/en/unit1/tutorial)。背景理解に使い、実行環境は下のローカル実習に従います。

第1週は[環境を準備](prepare-your-computer.md)して[3段階のダミー演習](dummy-agent-local.md)を行います。第2週は[スターターを入手](run-your-first-agent.md)し、[各部を理解](understand-the-template.md)してから、[時刻と検索を有効にします](first-agent-practical.md)。

第2週の最後に、両方のツールが実行されたことを示し、結果を説明します。独自ツールは任意です。画像生成は扱いません。

原典・発展資料：[Hugging Face Agents Course Unit 1](https://huggingface.co/learn/agents-course/en/unit1/introduction)。この解説はGroq実習向けに執筆したもので、原典をそのまま転載したものではありません。

**第1週の次のステップ：**[PCの環境を準備する](prepare-your-computer.md)。
