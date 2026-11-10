# 20 · 文書に質問して答える仕組みを作る { #week-5-components }

**目標：**同じデータが、読み込み、索引化、保存、問い合わせ、評価へ進む流れを追います。[準備](week-5-learning-plan.md#environment)で作った10件の人物像ファイルを使ってください。

[![HFのRAG図：データを索引化し、質問と関連情報をLLMへ渡して回答する流れ](images/huggingface-week05/rag.png)](images/huggingface-week05/rag.png){ .course-figure-link }

??? info "この図の説明を読む"

    左の「Your data」が手元のデータです。インデックスで検索できる形にし、質問に合う文章を選んでモデルへ渡します。モデルは質問とその文章から回答を作ります。この演習では10件の人物像がデータです。シンシナティについて質問すると`persona_0.txt`が見つかるはずです。検索は文章を取り出し、Groqは回答を作ります。生成文には誤りが入り得るので、元の文章と照合します。

*HFの図を変更せず使用しています。[原典のレッスン](https://huggingface.co/learn/agents-course/en/unit2/llama-index/components) · [図を拡大する](images/huggingface-week05/rag.png)。*

## 1. 5つの段階を理解する { #stages }

| 段階 | 行うこと | 確認するもの |
| --- | --- | --- |
| 読み込み | テキストを`Document`にする。 | ファイル名と文書数。 |
| 索引化 | 文書を`Node`という断片に分け、埋め込みを作る。 | 断片の数と設定。 |
| 保存 | ベクトルとメタデータをChromaに保存する。 | 生成される`alfred_chroma_db`フォルダー。 |
| 問い合わせ | 似た断片を検索し、必要に応じて回答を生成する。 | 取り出した文章、出典名、回答。 |
| 評価 | 回答の根拠と有用性を調べる。 | 出典との比較、評価器の結果。 |

`Node`は、元の文書にひも付いた文章の断片です。質問のたびに文書を埋め込み直さず、ベクトルを保存して再利用します。文書と質問のベクトルを比較するため、同じ埋め込みモデルを使います。

## 2. 読み込み、分割、埋め込み、保存 { #ingest }

**`my_ingest.py`を作成します。**10個のローカルテキストを読み、分割し、CPUで埋め込みを計算してChromaへ保存します。生成用LLMとGroqのトークンは使いません。最初のモデル取得には通信が必要です。文書数などはターミナル、保存先はファイル管理画面でも確認できます。

```python title="my_ingest.py"
from llama_index.core import SimpleDirectoryReader
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from week05_common import ROOT, run
from week05_rag import embedding_model, get_store

async def main():
    files = [ROOT / "data" / f"persona_{number}.txt" for number in range(10)]
    missing = [path.name for path in files if not path.is_file()]
    if missing:
        raise FileNotFoundError(
            "Missing persona files: " + ", ".join(missing)
            + ". Run python prepare_personas.py; see setup troubleshooting if data is incomplete."
        )
    documents = SimpleDirectoryReader(
        input_files=[str(path) for path in files], filename_as_id=True,
    ).load_data()
    print("Documents:", len(documents))
    if len(documents) != 10:
        raise ValueError("Use the ten supplied-dataset persona files for this first run.")
    collection, vector_store = get_store()
    if collection.count():
        if collection.count() < len(documents):
            raise ValueError("The saved index is incomplete. Close its programs, rename alfred_chroma_db as a backup, then rerun my_ingest.py.")
        print("Index already exists. Reuse it; no documents were added.")
        return
    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=256, chunk_overlap=20),
            embedding_model(),
        ],
        vector_store=vector_store,
    )
    nodes = await pipeline.arun(documents=documents)
    print("Indexed chunks:", len(nodes))
    print("Stored vectors:", collection.count())
    print("Saved in alfred_chroma_db/")

if __name__ == "__main__":
    run(main)
```

??? info "パイプラインの説明を読む"

    `files`は読み込む10個を明示しています。不足があれば、何を取得すべきか表示します。`SimpleDirectoryReader`はこの一覧を読み、ファイル名をメタデータに残すため、親に隠しフォルダーがあっても読み込めます。`SentenceSplitter`は256トークンを目安に分割し、20トークンを重ねます。短い文書は1断片に収まります。埋め込みは`BAAI/bge-small-en-v1.5`で作ります。`get_store()`がChromaの`alfred`コレクションとLlamaIndex用の接続を返し、`pipeline.arun`が変換と保存を行います。既存のコレクションを再利用するため、成功後の単純な再実行では重複追加しません。

**保存して実行：**`python my_ingest.py`。

**`Documents: 10`**、0より大きい断片数・ベクトル数、スクリプトと同じ場所の`alfred_chroma_db`を確認します。まだモデルの回答は出ません。同じファイルをもう一度実行すると、インデックスが既にあると表示され、保存件数は増えないはずです。

後でデータや埋め込み設定を変えても、古いデータベースは自動更新されません。記録を残し、利用中のプログラムを閉じ、`alfred_chroma_db`の名前を変えてバックアップしてから、再度取り込んでください。最初は元の10件を変えずに使います。途中で取り込みが止まった場合も、不完全な索引を使わず、この方法で作り直します。

## 3. 回答生成の前に検索を試す { #retrieve }

**`my_retrieve.py`を作成します。**保存済みのインデックスを開き、質問をPCで埋め込み、似ている上位2つの断片をファイル名・類似度とともに表示します。Groqのモデルやトークンは使いません。埋め込みモデルを保存した後は、モデルサービスへ接続せず確認できます。

```python title="my_retrieve.py"
from week05_rag import open_index

index = open_index()
retriever = index.as_retriever(similarity_top_k=2)
hits = retriever.retrieve("Cincinnati art historian and museum professional")
for hit in hits:
    print("FILE:", hit.node.metadata.get("file_name"))
    print("SCORE:", round(hit.score or 0.0, 3))
    print("TEXT:", hit.node.get_content())
    print()
```

??? info "検索の説明を読む"

    `open_index()`は同じ埋め込みモデルでデータベースを開き直します。ベクトルがなければ止まります。`as_retriever`が返すのは断片とスコアです。上位2件という指定は件数であり、両方が質問に関連する保証ではありません。類似度は、主張が正しい確率でもありません。

**実行：**`python my_retrieve.py`。

`persona_0.txt`と、シンシナティの美術史家の説明を探します。そのファイルを開き、表示された文章と照合してください。出典名と該当箇所をメモの20の欄に残します。

**同じ`my_retrieve.py`で比較します。**次の1行を探してください。

```python
hits = retriever.retrieve("Cincinnati art historian and museum professional")
```

この1行へ置き換えて保存し、`python my_retrieve.py`を実行します。

```python
hits = retriever.retrieve("What is this person's full legal name?")
```

質問は「この人の正式な氏名は何か」です。検索は2件の断片を返すかもしれませんが、その中に氏名はありますか？文章が返ることと、質問へ答えられることの違いを記録します。その後、最初の行へ戻して保存し、シンシナティの検索を残してください。ファイル全体やimportを置き換える必要はありません。

??? success "検索の確認"

    このデータには人物像の説明があり、実名はありません。根拠のない質問でも類似検索は候補を返します。内容を読んで、求めた名前が書かれていないと記録します。

## 4. クエリエンジンで回答と出典を調べる { #query }

**`my_query.py`を作成します。**保存したインデックスとGroqを使い、説明文について1つ答えます。生成した回答と、検索で取り出した元の文章をターミナルに表示します。Groqのトークンを使います。

```python title="my_query.py"
from week05_common import get_llm, run
from week05_rag import open_index

async def main():
    engine = open_index().as_query_engine(
        llm=get_llm(), similarity_top_k=2,
        response_mode="tree_summarize", use_async=True,
    )
    question = "Which persona is interested in Cincinnati's cultural heritage? Use only the supplied descriptions; do not invent a name."
    response = await engine.aquery(question)
    print("QUESTION:", question)
    print("ANSWER:", response)
    for source in response.source_nodes:
        print("SOURCE:", source.node.metadata.get("file_name"))
        print(source.node.get_content())

if __name__ == "__main__":
    run(main)
```

??? info "クエリエンジンの説明を読む"

    `as_query_engine`は検索と回答生成を組み合わせます。`tree_summarize`は取り出した内容を要約してまとめる方式で、モデルを複数回呼ぶ場合があります。`use_async=True`で非同期の回答生成を使い、`aquery`の結果を待ちます。`source_nodes`は実際に使った文章です。表示されたというだけで回答が忠実とは判断せず、照合してください。

**実行：**`python my_query.py`。

回答が美術史家を説明し、名前を作っていないか確認します。各事実を表示された出典と対応させてください。プログラムが成功しても、裏付けのない記述は誤りとして記録します。

??? info "問い合わせ方法と回答のまとめ方を詳しく読む"

    HFは3つの窓口を区別します。**retriever**は文章を返し、**query engine**は質問への回答を作り、**chat engine**は会話を扱います。ここではquery engineを使います。回答をまとめる方式には、断片を順に処理する`refine`、内容を詰めて呼び出しを減らす`compact`、要約をまとめる`tree_summarize`があります。どの方式でも、回答の確認は必要です。

??? info "任意：執筆や旅行について質問する"

    **話題を変えて比較します。**執筆や旅行に関心がある人物像を、既存の文章から探します。

    元へ戻せるように、`my_query.py`の`question = ...`の行を`evidence.md`へ控えます。`main`内のその行を次の行へ置き換え、先頭の空白4個を残してください。

    ```text
        question = "Find a persona interested in writing or travel. Describe it using only the supplied text. If the retrieved passages contain no matching interest, say no match was found in those passages."
    ```

    保存し、利用可能な範囲で`python my_query.py`を1回実行します。表示された出典に執筆や旅行の関心が実際に書かれていますか？なければ「取り出した文章内には一致なし」と記録します。2件の検索結果だけで、10件すべてに該当がないとは言えません。

    記録したら、`main`内を次の元の1行へ戻し、先頭の空白4個を残して保存します。

    ```text
        question = "Which persona is interested in Cincinnati's cultural heritage? Use only the supplied descriptions; do not invent a name."
    ```

## 5. 評価と動きの記録 { #evaluate }

まず手作業で、回答の各詳細が元の文章にあるか確認します。追加のモデル呼び出しは不要です。**忠実性（faithfulness）**は回答が文脈に裏付けられるか、**関連性（relevance）**は質問へ答えているか、**正確性（correctness）**は信頼できる答えや事実と一致するかを調べます。それぞれ別の確認です。

**任意のモデル評価：`my_evaluate.py`を作成します。**短い回答を作り、LLMの評価器に、元の文章で支えられているか判定させます。入力は検索結果で、回答、判定、理由、出典がターミナルに出ます。生成と評価の両方でGroqのトークンを使うので、先の出典確認ができてから取り組みます。

```python title="my_evaluate.py"
from llama_index.core.evaluation import FaithfulnessEvaluator
from week05_common import get_llm, run
from week05_rag import open_index

async def main():
    llm = get_llm()
    engine = open_index().as_query_engine(
        llm=llm, similarity_top_k=2, response_mode="compact", use_async=True,
    )
    response = await engine.aquery("Describe the Cincinnati art historian using only the provided text.")
    print("ANSWER:", response)
    judgement = await FaithfulnessEvaluator(llm=llm).aevaluate_response(response=response)
    print("PASS:", judgement.passing)
    print("FEEDBACK:", judgement.feedback)
    for source in response.source_nodes:
        print("SOURCE:", source.node.metadata.get("file_name"))
        print(source.node.get_content())

if __name__ == "__main__":
    run(main)
```

??? info "評価の説明を読む"

    `FaithfulnessEvaluator`が、回答を検索結果で支えられるか判定します。これもモデルの判断なので、間違える可能性があります。`passing=True`はこの確認の判定であり、事実全体の正しさを保証するものではありません。理由と元の文章を照合してください。データに含まれない事実まで検証したことにはなりません。

**任意の実行：**`python my_evaluate.py`。手作業の確認とモデルの判定を比べて記録します。実行しない場合は「未実施」と書いてください。

HFは**可観測性（observability）**も紹介します。各部品が何をしたか記録することです。この演習では、出典名、文章、件数、後で使うツールの実行記録が根拠になります。Phoenix／LlamaTraceは外部の記録サービスと追加アカウント・キーを使う発展内容です。ローカル演習の必須条件ではありません。接続例へ自分の認証情報を貼り付けないでください。

*原典・演習の出典：[HF Unit 2.2 — components](https://huggingface.co/learn/agents-course/en/unit2/llama-index/components)。Apache-2.0。`NOTICE.md`と`HF-LICENSE.txt`を参照してください。*

## ここで確認 { #checkpoint }

| 残しておく新しいファイル | 確認する結果 |
| --- | --- |
| `my_ingest.py` | 文書10件、保存したベクトル、再実行で増えない件数。 |
| `my_retrieve.py` | 元のシンシナティの質問で`persona_0.txt`と本文が出る。 |
| `my_query.py` | 表示された出典が回答を裏付けている。 |
| `my_evaluate.py` — 任意 | 実施した場合、評価器の判定と元の文章を比較する。 |

`alfred_chroma_db`と3つの必須プログラムを残します。比較で変えた行は元へ戻し、結果を`evidence.md`の20の欄に保存してください。

**次へ：**[21 · ツール](week-5-tools.md)。
