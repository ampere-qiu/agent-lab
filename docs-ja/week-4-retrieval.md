# 14 · 第03週のRAGを確認する { #week-4-retrieval }

**要点：**RAGは関連する文章を取得し、モデルがその根拠を使って回答する仕組みです。Agentic RAGでは、いつ、何を取得するかをエージェントが選びます。出典を確認し、情報がなければ不足していると伝えます。

**目標：**取得した文章が回答を裏付けているか確認します。

!!! note "コードの実習は第03週へ"

    RAG実習がまだの場合は、[12 · Agentic RAGシステムを作る](week-3-retrieval.md)へ戻り、**`First_agent_template`**で準備・ファイル作成・実行の手順を進めてください。実習済みなら、保存したコードと実行記録を見直します。[13 · 第03週の完了確認](week-3-completion.md#optional-rag)に対象ファイルの一覧があります。`week04-exercises`に同じファイルを作り直したり、第04週の環境にRAG用パッケージを追加したりする必要はありません。

第03週の自分の結果、または下の例を使って問題に答えます。何を根拠にしたか分かるよう、メモに**「Week 3 run（第03週の実行）」**または**「provided example（教材の例）」**と記してください。今回の確認用に新しいPythonプログラムは作りません。

**記入する場所：**[第04週の準備](week-4-preview.md#evidence-file)で作成した`evidence.md`を開き、**Topic 14 — Week 3 RAG review**の下に回答を書きます。

## BM25とは？ { #bm25 }

**BM25は、キーワードの一致を使って文書を順位付けする方法です。**検索語の出現回数、文書全体の中でその語がどれだけ珍しいか、文書の長さなどを考慮します。同じ語を繰り返す効果には上限があります。候補の文章を取得するための方法であり、回答を生成したり、主張の正しさを検証したりするものではありません。

第03週の例では、BM25がPC上の5つのパーティーメモを検索します。LLM、埋め込み、ベクトルデータベースは使いません。一方、検索語を選び、返された観測結果から回答を書くのはモデルです。ツールは5つの短いメモから最大5件を返すため、質問に必要な情報がなくても結果が出ることがあります。上位に出たというだけでは、答えが含まれている証拠にはなりません。また、キーワード検索が自動で同義語を理解するとは限りません。

参考：[BM25のスコアと正規化](https://www.elastic.co/docs/reference/elasticsearch/index-settings/similarity#bm25-similarity-default)。今回の確認に数式は必要ありません。

## 根拠を読む { #retrieve-first }

**次は読むための例です。Pythonファイルに貼り付けたり実行したりしないでください。**第03週の検索ループの主な流れを示しています。自分のツール出力には、複数のメモが含まれることがあります。

```text
Task: Suggest a superhero dish and cite its source.
Agent action: party_planning_retriever(query="superhero catering")
Tool observation:
  For catering, serve dishes named after superheroes, like
  'The Hulk's Green Smoothie' and 'Iron Man's Power Steak.'
  Source: Catering Ideas
Final answer: Try The Hulk's Green Smoothie [Catering Ideas].

Second query: caterer allergy policy
Observation: the five party notes contain no allergy policy.
```

例では、エージェントが料理案を検索し、`Catering Ideas`という出典ラベルの文章を受け取っています。2つ目の検索語`caterer allergy policy`は「ケータリング業者のアレルギー対応方針」です。

## 比較して理解を確かめる { #compare }

解答を開く前に、自分で答えてください。第03週の出力または教材の例から、実際のアクション、文章、出典を引用します。

**1. おすすめの料理を裏付ける文章と出典ラベルを示してください。その文章から何が分かりますか？**

??? success "解答1 — 文章と出典"

    料理の文章にある**「The Hulk's Green Smoothie」**と**`Source: Catering Ideas`**を示します。料理案の根拠にはなりますが、材料やアレルギー対応の根拠にはなりません。メモでは太字にするか、該当する語句をそのまま引用してください。

**2. どの行から、エージェントが検索したと分かりますか？Pythonからツールを直接試す場合と何が違いますか？**

??? success "解答2 — 実行された検索アクション"

    `party_planning_retriever(query="superhero catering")`というエージェントのアクションと、その後に返された文章です。ツールを直接呼んだ結果だけでは、モデルが検索を選んだことは示せません。回答と取得文を照合すれば利用可能な根拠を確認できますが、モデルが事前知識を一切使わなかったとまでは証明できません。

**3. 2つ目の質問について、メモにアレルギー対応方針はありますか？それでもBM25が結果を返すのはなぜですか？**

??? success "解答3 — 根拠の不足"

    **ありません。**上位5件を返す処理は、どれかに方針が書いてあることを条件にしていません。**「配布されたメモには、業者のアレルギー対応方針が示されていません」**と答えます。「業者に方針がない」という意味ではありません。

**4. 「この業者はナッツを使わないメニューを保証し、全参加者のアレルギーを確認します」という、根拠のない回答を書き直してください。次に何をすべきですか？**

??? success "解答4 — 根拠に合った限界の伝え方"

    **「このメモではアレルギー対応方針を確認できません。業者の正式な方針を入手してから答える必要があります」**とします。詳しい保証を書くと、根拠を作り足してしまいます。断定的な表現にしても、足りない出典は補えません。

**5. 「最終回答」「検索の観測結果」「モデルが検索語を選ぶ」「ツールがメモを検索する」を順番に並べてください。LLMを使わないのはどの部分ですか？**

??? success "解答5 — 処理の流れ"

    モデルが検索語を選ぶ → ツールがメモを検索する → 検索の観測結果 → 最終回答、の順です。BM25によるローカル検索はLLMを使いません。検索語の選択と回答の生成にはLLMを使います。

**確認：**回答1〜5を`evidence.md`に保存し、使った根拠を記してください。コードの練習は[第03週のRAG実習](week-3-retrieval.md)へ戻ります。次は複数のエージェントを連携させます。

**出典：**[HF Retrieval Agents](https://huggingface.co/learn/agents-course/en/unit2/smolagents/retrieval_agents)を基にした復習です。Apache-2.0。RAGの実習は第03週にあります。

**次：**[15 · Batmanエージェントチームを作る](week-4-batman.md)。
