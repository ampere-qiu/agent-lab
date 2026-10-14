<div class="course-hero" markdown>

<p class="eyebrow">Agent Lab / 第1週</p>

# はじめてのAIエージェントを作ろう { #build-your-first-ai-agent }

モデルを理解し、ツールをつなぎ、エージェントの動きを確かめます。

Hugging FaceのAgents Courseとスターターテンプレートを基にした、ローカル環境で学ぶコースです。

[環境構築を始める](prepare-your-computer.md){ .md-button .md-button--primary }
[レッスンに進む](unit-1-walkthrough.md){ .md-button }

<p class="course-meta">Windows・Mac対応 · ローカルアプリとリモートLLM · このサイトで学習 · 小テスト2回</p>

</div>

## この教材について { #about-this-adaptation }

[Hugging Face Agents Course](https://huggingface.co/learn/agents-course/en/unit1/introduction)のスターターテンプレートを基に、授業向けに構成を調整しています。元の環境ではAPIへのアクセス、モデルの提供状況、ホスティングの条件が実行に影響したため、この版はローカルで動かし、モデルの呼び出しには**Groq**を使います。PythonライブラリはHugging Faceの**smolagents**を引き続き使います。

**画像生成は含めません。** 必須の実習では**タイムゾーンの時刻取得**と**Web検索**の2つのツールを使います。自作ツールの実装は任意の発展課題です。

学習内容と実行手順はこのサイトにまとめています。外部のHFレッスンは補足資料です。元の小テスト2回だけを残し、アカウントへのアクセスが必要な最終テストと認定は本教材の対象外とします。

最初の環境構築ではSpaceの無料複製が使えず、その後HF推論でクレジット不足のエラーも発生しました。画面をローカルで動かしても、リモート推論が無制限になるわけではありません。自分のGroqキーを使い、[利用上限](https://console.groq.com/docs/rate-limits)を確認してください。

## 学習の順序 { #course-route }

ターミナルやPythonの編集に慣れていない方は、先に[始める前に](before-you-start.md)を読んでください。操作する画面、ファイルの場所、保存方法を説明しています。

1. [Python、ダミー演習のフォルダー、Groqキーを準備する](prepare-your-computer.md)。
2. [この教材の説明](unit-1-walkthrough.md)と[元のHugging Faceレッスン](https://huggingface.co/learn/agents-course/en/unit1/introduction)を読み、この教材からリンクしているHFの小テスト2回に取り組む。
3. [ダミーエージェントを3段階で作る](dummy-agent-local.md)。
4. [テンプレートをダウンロードして実行](run-your-first-agent.md)し、[構成を理解する](understand-the-template.md)。
5. [ツールを登録し、動作を検証する](first-agent-practical.md)。
6. [実習の完了条件を確認する](quizzes.md#finish-the-practical)。

**完全なテンプレートを使うのはダミー演習の後です。** まずモデル呼び出し、関数、観測結果の関係を手動で確かめ、その後CodeAgentでループを自動化します。

[エージェントのテンプレートを入手 →](run-your-first-agent.md){ .md-button .md-button--primary }

小テストのリンクは元のサイトの演習を開きます。それ以外の手順はこのガイドで進められます。

## 元の環境からの変更 { #environment-changes }

| 元の手順 | この教材の手順 |
| --- | --- |
| Spaceを複製する | Groq用に調整したスターターZIPをダウンロードする |
| SpaceのシークレットにHF_TOKENを追加する | 起動時にGroqキーを入力する |
| Space内のファイルを編集する | ダウンロードしたファイルを編集する |
| Spaceの再ビルドを待つ | 保存し、ローカルアプリを停止して再起動する |
| ホストされたアプリを開く | 表示されたローカルアドレスを開く |
| Spaceを公開・共有する | ローカルアプリを実演する。ホスティングは任意 |

概念の学習、手動のダミーループ、フレームワークを使うエージェントという順序は維持しています。テンプレートには原典のクレジットを残し、プロバイダー、実行場所、ツールの範囲、評価へのアクセス条件を調整しています。

## 使用バージョン { #version-note }

Groqスターターは`OpenAIServerModel`、`smolagents==1.13.0`、Groq経由の`qwen/qwen3.8-27b`を使います。現在のオンライン教材のモデル接続とは異なります。実行するコードの編集には、このローカル版のスターターを使ってください。自分の環境で応答とツールの確認を行います。プロバイダーやモデルを変更すると、動作も変わることがあります。

## モデル互換性の更新 { #model-compatibility-update }

以前のGPT-OSS設定では、実際のテストで「Tool choice is none, but model called a tool」というエラーが発生しました。この教材のCodeAgentはテキスト内のPythonコードを想定しています。APIネイティブの関数呼び出しは別の形式です。Groqにも、この[tool-choiceエラー](https://console.groq.com/docs/tool-use/local-tool-calling)の説明があります。更新したスターターでは[Qwen 3.8 27B](https://console.groq.com/docs/model/qwen/qwen3.8-27b)を使い、推論モードを無効にし、コード形式を明示しています。これは現時点ではプレビューモデルで、[無料プランの上限](https://console.groq.com/docs/rate-limits)があります。授業前に提供状況と動作を確認してください。
