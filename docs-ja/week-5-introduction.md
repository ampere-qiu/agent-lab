# 18 · LlamaIndex入門 { #week-5-introduction }

**目標：**今週つなぐ4つの部品の役割を説明できるようにします。先に[準備](week-5-learning-plan.md#download)を終えてください。

アルフレッドに、人物像の説明文を集めたデータについて答えてもらいます。モデルは一般的な知識を持っていても、PC内のファイルを自動で読んでいるわけではありません。必要な文章を検索し、その結果を使えるようにします。

[![HF Unit 2.2の表紙：LlamaIndexフレームワーク](images/huggingface-week05/thumbnail.png)](images/huggingface-week05/thumbnail.png){ .course-figure-link }

??? info "この図の説明を読む"

    HF Unit 2.2で扱うLlamaIndexの表紙です。今週は「シンシナティの美術に関心がある人物像はどれか」という質問を例にします。まず関連する文章を探し、モデルへ渡す仕組みを作ります。次に、検索するかどうかをエージェントに選ばせ、最後にワークフローで処理をつなぎます。

*HFの図を変更せず使用しています。[原典のレッスン](https://huggingface.co/learn/agents-course/en/unit2/llama-index/introduction) · [図を拡大する](images/huggingface-week05/thumbnail.png)。*

## 4つの部品と役割 { #four-parts }

| 部品 | 役割 | 今週の例 |
| --- | --- | --- |
| コンポーネント | アプリの一部分の処理を行う。 | ファイルの読み込み、埋め込み、文章の検索、回答の生成。 |
| ツール | 名前・説明・入力を持つ形で機能を公開する。 | 掛け算や人物像の検索。 |
| エージェント | モデルがツールを選び、その結果を使う。 | 計算と人物像の検索のどちらを使うか判断する。 |
| ワークフロー | 型のあるイベントと共有状態で処理をつなぐ。 | 次の処理への受け渡し、1回の繰り返し、別のエージェントへの受け渡し。 |

**埋め込み（embedding）**は、似た文章を探すために文章を数値の列に変えたものです。**インデックス**は、情報を検索できるように整理したものです。**クエリエンジン**は、関連する文章を取り出し、モデルで回答を作ります。検索結果は根拠の候補なので、回答と照らし合わせて確認します。

## 情報の流れを追う { #information-flow }

```text
Persona files → text chunks → embeddings → stored index
Question → retrieve relevant chunks → model composes answer
Agent → chooses a tool → receives its result → answers or takes another step
Workflow → event → matching step → another event or a final result
```

上の英語の図式を順に読むと、「人物像のファイル → 文章の断片 → 埋め込み → 保存したインデックス」です。質問すると関連する断片を取り出し、モデルが回答します。エージェントはツールを選び、結果を見て次の行動を決めます。ワークフローはイベントに合う処理を実行し、次のイベントか最終結果を返します。

これまでのRAGとツールの演習を、今週はLlamaIndexで組み立てます。どの部分が検索し、どの部分がモデルを呼び、どの部分が次の行動を決めるのかを確認してください。

LlamaIndexのワークフローは**イベント駆動**です。イベントの種類によって、実行できる処理が決まります。また、**非同期処理を前提**にしており、`await`で結果を待つ間、ほかの非同期処理を進められます。自分で並列プログラムを書く必要はありません。各演習は通常のPythonファイルなので、`python filename.py`で実行できます。

## 理解を確かめる { #check }

`evidence.md`の18の欄に短く答えてください。ファイルを読み込み、その内容について1つ答えるプログラムは、それだけでエージェントだと言えますか？

??? success "答え"

    言えません。決められた検索・回答の処理は、エージェントがツールを選ばなくても実行できます。エージェントと呼ぶ前に、判断のループと実際のツール呼び出しを確認します。

*原典・演習の出典：[HF Unit 2.2 — introduction](https://huggingface.co/learn/agents-course/en/unit2/llama-index/introduction)。Apache-2.0。スターターの`NOTICE.md`と`HF-LICENSE.txt`を参照してください。*

## ここで確認 { #checkpoint }

このページではPythonファイルを作りません。`evidence.md`の18の欄で、コンポーネント、ツール、エージェント、ワークフローの違いを自分の言葉で説明してください。決められた文書検索だけではエージェントとは限らない理由を説明できたら、次へ進みます。

**次へ：**[19 · LlamaHub](week-5-llamahub.md)。
