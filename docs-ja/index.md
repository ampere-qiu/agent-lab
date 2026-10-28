<div class="course-hero" markdown>

<p class="eyebrow">Agent Lab / 第01〜03週</p>

# はじめてのAIエージェントを作ろう { #build-your-first-ai-agent }

モデルの仕組みを理解し、ツールをつなぎ、エージェントが実際に動くところを確かめます。

Hugging Face Agents Courseとそのスターターテンプレートを基にした、ローカル環境で学ぶ教材です。

[第1週を始める](week-1-learning-plan.md){ .md-button .md-button--primary }
[第2週の内容を見る](week-2-learning-plan.md){ .md-button }

<p class="course-meta">Windows・Mac対応 · アプリはローカル、LLMはリモート · 第1〜3週 · ローカル実習</p>

</div>

**第03週：**[smolagentsの学習](week-3-learning-plan.md)では、アルフレッドのパーティーを題材に、ターミナル用エージェント、関数型・クラス型のツール、任意のAgentic RAG練習を扱います。原典の図には出典を記載しています。レッスンは英語と日本語で読めます。

## この教材で変更した点 { #about-this-adaptation }

[Hugging Face Agents Course](https://huggingface.co/learn/agents-course/en/unit1/introduction)のスターターテンプレートを取り入れ、実習向けに調整しています。APIへのアクセス、モデルの提供状況、ホスティング条件に対応するため、アプリをローカルで動かし、モデルへの問い合わせに**Groq**を使います。Pythonライブラリは引き続きHugging Faceの**smolagents**を使います。

**画像生成は扱いません。** 第2週の必須の実習では、**タイムゾーン別の時刻取得**と**ウェブ検索**の2つを使います。独自ツールの作成は第2週では任意の発展課題で、第03週には手順に沿って取り組む必須の課題になります。

学習内容と実行手順はこのサイト内に用意しています。外部のHFレッスンは補足資料です。第1〜2週では小テスト2つを残し、アカウントが必要な最終テストと認定取得はこの教材に含めていません。

当初の環境準備では無料でSpaceを複製できず、その後HF推論APIでもクレジット不足のエラーが発生しました。画面をローカルで動かしても、リモート推論が無制限になるわけではありません。自分のGroqキーを使い、[利用制限](https://console.groq.com/docs/rate-limits)を確認してください。

## コースの進め方 { #course-route }

ターミナルやPythonの編集が初めてなら、まず[始める前に](before-you-start.md)を読んでください。使うウィンドウ、ファイルの場所、編集の保存方法を説明しています。

1. **第1週 — ループを理解してたどる：**[エージェントの基礎](unit-1-walkthrough.md)と小テスト2つに取り組み、[ローカル環境を準備](prepare-your-computer.md)して、[3段階のダミーエージェント](dummy-agent-local.md)を作ります。
2. **第2週 — 動くエージェントを拡張する：**[テンプレートを起動](run-your-first-agent.md)し、[各部の役割](understand-the-template.md)を理解してから、[ツールを有効にして検証](first-agent-practical.md)し、[実習の完了確認](quizzes.md#finish-the-practical)を行います。

3. **第03週 — ターミナル用エージェントを作る：**[環境準備とファイル作成の手順](week-3-learning-plan.md)に沿ってプログラムを動かし、[関数型・クラス型のツール](week-3-custom-tool.md)を変更し、任意で[Agentic RAG](week-3-retrieval.md)を予習できます。RAGは来週あらためて扱います。[エージェントのチームと画像・ブラウザの話題は第04週に続きます](week-4-preview.md)。

学習目標と、各週の振り返りで示す内容は、[コース全体の流れ](course-route.md)を参照してください。

**完全なテンプレートを使うのは、ダミー演習の後です。** まずモデルへの問い合わせ、関数、観測結果がどうつながるかを見てから、CodeAgentによる自動化に進みます。

[第1週の学習計画へ →](week-1-learning-plan.md){ .md-button .md-button--primary }

小テストのリンクは原典の活動を開きます。それ以外は、このローカルガイドで進められます。

## 実行環境の変更 { #environment-changes }

| 原典の手順 | この教材での手順 |
| --- | --- |
| Spaceを複製する | Groq対応スターターZIPをダウンロードする |
| SpaceのシークレットにHF_TOKENを追加する | 起動時にGroqキーを入力する |
| Space上でファイルを編集する | ダウンロードしたファイルを編集する |
| Spaceの再ビルドを待つ | 保存し、ローカルアプリを停止・再起動する |
| 公開されたアプリを開く | 表示されたローカルアドレスを開く |
| Spaceを公開・共有する | ローカルアプリを実演する。ホスティングは任意 |

基礎から手動のダミーループへ、さらにフレームワークを使うエージェントへという順序は保っています。テンプレートには原典の帰属表示を残し、提供サービス、実行場所、ツールの範囲、評価方法を調整しています。

## バージョンについて { #version-note }

Groqスターターは`OpenAIServerModel`、`smolagents==1.13.0`、Groq経由の`qwen/qwen3.8-27b`を使います。オンラインのチュートリアルとはモデル接続が異なります。実行するコードの編集には、この教材のローカルスターターを使ってください。応答とツールのチェックポイントは自分の環境で確認します。提供サービスやモデルを変えると挙動が変わる場合があります。

## モデル互換性への対応 { #model-compatibility-update }

以前のGPT-OSS設定では、実機テスト中に「Tool choice is none, but model called a tool」というエラーが発生しました。このコースのCodeAgentが受け取るのは、テキストとして生成されたPythonコードです。APIのネイティブ関数呼び出しは別の形式です。Groqにも、この[ツール指定に関するエラー](https://console.groq.com/docs/tool-use/local-tool-calling)の説明があります。更新版は[Qwen 3.8 27B](https://console.groq.com/docs/model/qwen/qwen3.8-27b)を使い、推論モードを無効にしてコード形式を明示しています。英語原文では、[無料プランの制限](https://console.groq.com/docs/rate-limits)があるプレビューモデルとして扱っています。授業前に利用可否と動作を確認してください。
