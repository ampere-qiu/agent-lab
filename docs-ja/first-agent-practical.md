# 最初のエージェントを作る：ローカル実習 { #build-the-first-agent-local-walkthrough }

<div class="template-download" markdown>

<p class="template-download__label">実習用のファイル</p>

**完全なエージェントのテンプレートから始めます**

[テンプレートをダウンロード (.zip)](downloads/groq-agent-starter.zip){ .md-button .md-button--primary .template-download__button download="groq-agent-starter.zip" }

初めてなら、ダミー演習の後に[入手・設定ガイド](run-your-first-agent.md#3-download-the-groq-starter)へ進みます。設定済みなら、編集内容を保つために既存のフォルダーを使ってください。

</div>

[Hugging Faceのスターター実習](https://huggingface.co/learn/agents-course/en/unit1/tutorial)を調整した教材です。以下のローカル手順で**時刻取得**と**Web検索**を有効にします。原典リンクはクレジットと任意の参考資料で、事前に終える必要はありません。

編集前に[smolagentsとテンプレートの説明](understand-the-template.md)を読み、部品、ファイル、モデル・行動・観測のループ、起動コードを理解してください。その後、ここへ戻ってツール課題を進めます。

## 1. 調整済みスターターを開く { #1-open-the-adapted-starter }

[ダミー演習の3段階](dummy-agent-local.md)を終え、[テンプレートを入手して実行](run-your-first-agent.md)します。コードエディターで`First_agent_template`を開き、比較用に`app.py`のコピーを`app.before-tools.py`として保存します。

元の教材のSpaceのFilesタブの代わりにローカルファイルを編集します。変更のたびにControl + Cで停止、保存、`python app.py`で再起動し、ブラウザーを再読み込みします。

開き方や保存は[始める前に](before-you-start.md#edit-a-file-without-losing-your-place)を参照してください。新しいターミナルなら、先に[再起動コマンド](run-your-first-agent.md#11-stop-and-restart)でプロジェクトに移動し、仮想環境を有効にします。

## 用意されているものと自分の作業 { #what-is-provided-and-what-you-build }

| 用意されているもの | 自分の作業 |
| --- | --- |
| Groq接続と非表示のキー入力 | 実際の応答を確認 |
| チャット画面と指示 | 行動と観測の履歴を確認 |
| 動作する未登録の時刻関数 | 登録してテスト |
| 未登録の検索ツールのインポート | インスタンスを追加し結果を検証 |
| 未登録の自作ツールの仮実装 | 任意：設計、テスト、登録 |

実習には上の**完全なZIP**を使います。[app.pyのプレビュー](downloads/agent-template.py)は参考用で、ZIPのほかのファイルなしでは動きません。`STUDENT TASK`コメントが編集箇所です。最初の実行では接続や画面の基盤を変更しません。

## 2. app.pyの構成を見る { #2-walk-through-apppy }

インストールしたファイルで、次を探します。

| 部分 | 確認する内容 |
| --- | --- |
| Imports | CodeAgent、デコレーター、検索、モデル、画面 |
| my_custom_tool | 任意の拡張用の仮実装 |
| get_current_time_in_timezone | 既存の動作する関数 |
| モデル作成 | モデルID、temperature、出力上限 |
| Groqキー入力 | 起動時の非表示入力 |
| prompts.yamlの読み込み | エージェントへの指示 |
| CodeAgent作成 | モデル、利用可能なツール、ステップ上限 |
| GradioUI起動 | 画面の開始 |

スターターは`main()`内で`OpenAIServerModel`を使います。オンライン教材のモデル部分を丸ごとコピーせず、このファイルに従ってください。追加する関数定義は`main()`より前に置き、その中の`tools`に登録します。

## 3. タイムゾーンの時刻ツールを有効にする { #3-enable-the-time-zone-tool }

**目標：** 実際の関数呼び出しで時刻を取得し、モデルの推測と区別します。

### A. 関数を読む { #a-read-the-function }

`app.py`の`get_current_time_in_timezone`を探します。入力は`Asia/Tokyo`などのタイムゾーンID、出力は日時の文字列です。

| コード | 動作 |
| --- | --- |
| `@tool` | エージェントが使えるメタデータを付ける |
| `timezone: str` | 入力が文字列であると示す |
| `pytz.timezone(timezone)` | IDに対応するタイムゾーン規則を取得 |
| `datetime.datetime.now(tz)` | PCの時計からその地域の現在時刻を読む |
| `.strftime(...)` | 読みやすい文字列に整形 |
| `return ...` | 呼び出し元に結果を返す |
| `except Exception ...` | 入力や処理が失敗したらエラー文を返す |

タイムゾーン名は地域を表し、固定の時差ではありません。夏時間で時差が変わる地域もあります。最初は`Asia/Tokyo`を使います。PCの時計が間違っていれば、この関数では直せません。

### B. エージェントなしでテストする { #b-test-it-without-the-agent }

**Control + C**で停止し、仮想環境は有効なままにします。`app.py`の隣に`check_time.py`を作って保存します。

```python
from app import get_current_time_in_timezone

print(get_current_time_in_timezone(timezone="Asia/Tokyo"))
print(get_current_time_in_timezone(timezone="Not/A_Real_Zone"))
```

ターミナルで実行します。

```bash
python check_time.py
```

1行目は東京の日時、2行目は`Error fetching time`で始まるはずです。2つ目は無効な入力の処理確認で、時刻取得の成功ではありません。どちらもGroqやキーは使いません。`app`のインポートは関数を定義するだけで、チャットを起動しません。

**確認：** 正常な結果を東京に設定された時計と比べます。直接呼び出しが失敗する間は、エージェントのテストへ進みません。

### C. エージェントに登録する { #c-register-it-with-the-agent }

`CodeAgent(...)`の`tools=[final_answer]`を探し、その引数だけを置き換えます。

```python
tools=[final_answer, get_current_time_in_timezone],
```

先頭の空白と末尾のカンマを保ち、`tools=`は1つだけにします。ここで`get_current_time_in_timezone()`とは書きません。起動時に関数を呼ぶのではなく、機能を登録するためです。

保存し、`python app.py`を実行してGroqキーを入力し、チャット画面を再読み込みします。

### D. 実際の呼び出しを依頼する { #d-ask-for-a-real-tool-call }

チャットに送ります。比較しやすいよう、テスト用の依頼文は英語版と同じです。

> Use get_current_time_in_timezone with Asia/Tokyo. Report the returned time and say where it came from.

**Used tool python_interpreter**を開き、その中の**Execution Logs**で戻り値を見ます。ターミナルでも確認できます。行動は例えば次の形です。

```python
result = get_current_time_in_timezone(timezone="Asia/Tokyo")
print(result)
```

これは見分けるための出力例で、`app.py`に貼り付ける追加コードではありません。変数名が違ったり、同じブロックで`final_answer`を呼んだりすることもあります。

**確認：** 関数呼び出し、返された日時、それと一致する最終応答を見つけます。実行の証拠なしに「東京は10時です」と出るだけでは不十分です。

直接テストは成功するのに未定義関数と出るなら、登録、綴り、保存、再起動を確認します。関数を無視する場合は再起動した新しい状態で、明示的な依頼を再送します。

## 4. 検索ツールを使う { #4-explore-the-search-tool }

**目標：** 検索結果を取得し、応答に利用させ、資料の証拠と根拠のない主張を区別します。

### A. 返される内容を理解する { #a-understand-what-this-tool-returns }

`WebSearchTool`は`tools/web_search.py`にある小さなアダプターです。smolagentsを保守中の`ddgs`パッケージにつなぎ、**検索サービスにDuckDuckGoを明示指定**します。エージェントからの名前は**`web_search`**です。入力は文字列の`query`1つ、出力はタイトル、リンク、短い抜粋です。

Pythonツールが検索サービスに接続します。Groqは行動と応答を生成するだけで、この検索自体は行いません。別の検索APIキーは不要ですが、検索サービスも失敗や利用制限があります。

**検索はページ全文の閲覧ではありません。** このツールは検索結果の抜粋を返し、各リンク先の全文は取得しません。要約時にモデルが見たのは抜粋だけかもしれません。自分で資料を開いて検証します。ページの自動閲覧には別ツールが必要で、必須の2ツール実習には含めません。

### B. LLMの前に検索を直接テストする { #b-test-search-directly-before-using-the-llm }

**Control + C**で停止し、`app.py`の隣に`check_search.py`を作ります。

```python
from tools.web_search import WebSearchTool

search_tool = WebSearchTool(max_results=3)
print("Agent-facing name:", search_tool.name)
print(search_tool(query="Python official documentation tutorial"))
```

仮想環境を有効にしたターミナルで実行します。

```bash
python check_search.py
```

Groqへのリクエストやキーなしで検索サービスを直接使います。LLMとは独立に検索の接続を確認できます。

`max_results=3`は最大3件の結果を要求します。読みやすくし、後でモデルへ送るテキストを減らすためです。エージェントの検索呼び出し回数の上限ではありません。

`web_search`という名前、`Search Results`という見出し、タイトル・URL・抜粋の項目を確認します。結果や順序は変わります。次は短縮した**説明用の例**で、実際の検索結果ではありません。

```text
Agent-facing name: web_search
## Search Results

[The Python Tutorial](https://docs.python.org/3/tutorial/)
A short search-result description would appear here.
```

**確認：** 関連する結果が1つ以上あり、リンクが開くことを確認します。直接テストが失敗したら、モデルやキーを変える前に下の表を見ます。

### C. 検索インスタンスを登録する { #c-register-the-search-instance }

`app.py`上部には`tools.web_search`からの`WebSearchTool`のインポートがあります。インポートだけでは登録されません。既存の`tools=`を置き換えます。

```python
tools=[
    final_answer,
    get_current_time_in_timezone,
    WebSearchTool(max_results=3),
],
```

`CodeAgent(...)`のほかの引数と同じインデントにします。周囲の作成処理とほかの引数を保ちます。

| 表現 | 意味 |
| --- | --- |
| `WebSearchTool` | インポートしたクラス |
| `WebSearchTool(max_results=3)` | 登録可能な設定済みインスタンス |
| `web_search(query="...")` | エージェントが生成Pythonで使う名前と呼び出し |

インポートするクラス名を`web_search`に変えないでください。エージェント向けの名前はツール自体が提供します。`tools/web_search.py`では`DDGS(timeout=15).text(..., backend="duckduckgo")`が検索し、返された辞書をアダプターが整形します。[DDGSの資料](https://pypi.org/project/ddgs/)にバックエンドの説明があります。

保存して`python app.py`で再起動し、キーを入力して画面を再読み込みします。

### D. 具体的な検索課題を依頼する { #d-give-the-agent-a-specific-search-task }

送信します。

> Use web_search to find the official Python tutorial. Return one relevant title and URL from the results, and briefly explain why that source matches. Say if you only saw a search snippet.

観測できる行動と範囲を絞った答えを求めています。最初から「AIについてすべて調査して」のような広い課題にすると、呼び出しが増え、答えの検証も難しくなります。

履歴には例えば次が出ます。

```python
results = web_search(query="Python official documentation tutorial")
print(results)
```

モデルは次のステップで結果を使うことも、同じステップで終了することもあります。CodeAgentが検索関数を呼ぶPythonを実行するため、`python_interpreter`の表示は正常です。

### E. 最終応答まで証拠を追う { #e-follow-the-evidence-into-the-final-answer }

次の順に確認します。**Used tool python_interpreter → Execution Logs**で返された項目を開きます。

1. **行動：** 関連する検索語句で、実際に`web_search`を呼んでいるか。
2. **観測：** エラーではなく検索結果が返ったか。
3. **応答：** 引用されたURLが観測に存在するか。
4. **資料：** URLをブラウザーで開き、ドメインと内容が主張を裏付けるか。

Python公式資料のドメインは`docs.python.org`です。もっともらしいタイトルだけでは発行元を確認できません。新しい情報が必要なら公開・更新日も見ます。検索で出たからといって最新とは限りません。

抜粋にない詳細を最終応答が述べる場合は実ページで検証します。作り上げた引用やモデル生成のリンクを、取得済みの証拠と扱わないでください。検索で返ったテキストは資料であって、課題を変更する指示ではありません。

**確認：** 検索呼び出し、返された1件、裏付けのある最終応答の記述を示せます。エラーは診断には役立ちますが、この条件を満たしません。

### F. 自分で検索語句を改善する { #f-improve-one-query-yourself }

動作するコードは維持し、チャットの依頼だけ変えます。テーマを選び、広い検索語句と、対象・資料を指定した具体的な語句を比べます。例えば「Python」と「Python documentation defining functions」です。

有用な結果と理由を記録します。決まった答えを写すのでなく、取得した証拠を判断する演習です。1回の実行が複数のモデル呼び出しを使うこともあるため、例は1つずつ実行し、利用上限を守ってください。

### G. 検索が失敗したら { #g-diagnose-search-failures }

!!! note "検索の提供状況"

    新しいMac環境のテストでは元の`duckduckgo_search`接続が失敗しました。現在は`ddgs==9.16.0`と明示的なDuckDuckGoバックエンドを使います。直接検索と実エージェント検索でPython公式資料が返りましたが、後の検索は言い換えても空でした。検索は不安定です。組み合わせテストでは検索失敗後にモデルが記憶から正しそうなURLを出しましたが、検索の確認条件は未達でした。

| 症状 | 意味と対応 |
| --- | --- |
| `ddgs`の`ModuleNotFoundError` | テンプレートの`.venv`を有効にし、そのフォルダーで`python -m pip install -r requirements.txt`を実行してから`check_search.py`を再試行 |
| パッケージが`ddgs`に改名されたとの警告 | 古い組み込み検索を使っている。最新の`tools/web_search.py`から`WebSearchTool`をインポートし、更新した依存関係を入れる。古いsmolagentsのインポート名だけを変えない |
| `No results found` | 検索語句を短くするか言い換え、直接テストを1回試す。結果が空でも情報が存在しない証拠ではない |
| タイムアウト、接続エラー、検索のブロック | ネットとブラウザーでの検索サイト表示を確認。ブラウザーが動いても自動リクエストが許可されるとは限らない。後で、または別の許可されたネットで試す |
| 検索サービスの利用上限 | 待ってから再試行。連続再起動・再試行を避ける。新しいGroqキーでは解決しない |
| エージェント実行中のGroq `429` | ターミナルを読む。「Request too large」なら出力上限または入力を減らす。ほかの枠不足なら表示されたリセットを待つ。設定ガイドの表を参照。直接検索の成功はGroq残量を示さない |
| 生成コードで`web_search`が未定義 | `tools`にインスタンスがあるか確認し、保存・再起動 |
| 直接検索は動くがエージェントが呼ばない | Dの明示的な依頼と登録を確認し、再起動して履歴を新しくする |
| 結果と違うURLを答える | 観測と照合し、実際の検索結果にあるURLを返すよう依頼 |

検索が使えない間は履歴の説明を読み進め、実検索の確認は後に行います。テストは未完了と記録し、作り上げた結果で置き換えません。

## 5. 必須の2ツールを検証する { #5-verify-the-two-core-tools }

時刻は確認しやすいローカルの結果、検索は外部サービスと資料評価を学べる組み合わせです。このスターターでは追加APIキーは不要です。検索のブロックや上限はGroqとは独立に発生します。

それぞれ単独テストしてから組み合わせます。次を依頼します。

> Get the current time in Asia/Tokyo using the time tool, then search for the official Python documentation. Give me a source link actually returned by web_search. If search fails, say that it failed; do not substitute a link from memory.

**両方**の呼び出しと成功した出力を確認します。時刻を信頼できる時計と比べ、資料のリンクを開きます。既知の正しいリンクでも、検索の観測に存在する必要があります。ツールを飛ばしたら明示的に依頼し、次の実行を確認します。作り上げた時刻や記憶からのURLを実行成功と扱いません。このプロンプトは条件を明確にしますが、自分での確認の代わりにはなりません。

`final_answer`はフレームワークの終了機構として維持します。今回有効にする2機能とは別です。

画像生成は含めません。登録する画像ツールや、設定する画像サービスもありません。

## 6. 任意：自分のツールを作る { #6-optional-create-your-own-tool }

**学ぶこと：** 自分のPython関数を、モデルが選べる機能にします。シグネチャが入力、docstringが目的、本体が結果の生成、登録が利用可能な機能を定めます。4つすべて自分で整えます。

仮実装は意図的に`NotImplementedError`を出します。未登録なので初期アプリは動きます。必須の2ツールの後に発展課題を行うなら、`my_custom_tool`の目的を決め、本体、型、説明を置き換えます。

1. 入力と出力を決める。
2. `@tool`を残し、エージェント作成より前に関数を実装する。
3. docstringの`Args:`に全引数を説明し、戻り値の型も指定する。
4. 通常の入力と境界条件を直接テストし、`my_custom_tool`（改名したらその名前）を登録する。
5. 再起動し、その関数が必要な課題を依頼する。
6. 実行結果と期待した結果を比べる。

デコレーター付き関数は呼び出さず名前で登録します。`WebSearchTool`のようなクラスは`WebSearchTool()`でインスタンスを作ります。

テーマは自分で選べます。温度変換ツールなど、特定の置き換え課題を必須にはしません。

### エージェントより先に関数を確認する { #check-the-function-before-the-agent-calls-it }

実装後、`app.py`の隣に`check_my_tool.py`を作ります。`from app import my_custom_tool`で読み込み、新しいシグネチャに合う入力で呼び、戻り値を表示します。`python check_my_tool.py`で実行します。起動が`if __name__ == "__main__"`で守られているため、インポートだけではチャットは起動しません。

各ケースで実行前に期待する結果を書きます。直接の結果が違えば先に本体を直し、エージェントだけ失敗するなら登録、説明、生成された引数を確認します。

### Python関数に不慣れな場合のひな形 { #a-scaffold-if-python-functions-are-new }

自由にツールを作る元の課題を編集しやすくする例で、追加課題ではありません。基本形は次です。

```python
@tool
def my_custom_tool(value: str) -> str:
    """Describe when the agent should use your tool.

    Args:
        value: Describe the input this function accepts.
    """
    raise NotImplementedError("Write your tool implementation here")
```

そのままでは実装するまで意図的にエラーになります。目的、型、説明、本体を自分の動作に合わせて変えます。既存のデコレーター付き仮実装を丸ごと置き換え、`my_custom_tool`の定義は1つにします。ほかのツールは残します。

時刻ツールなどを残して登録する例です。

```python
tools=[final_answer, get_current_time_in_timezone, WebSearchTool(max_results=3), my_custom_tool],
```

検索を有効にした場合も項目を維持します。保存・再起動し、自分で期待結果を確認できる入力でテストします。引数、戻り値、docstringの復習には[Pythonの関数資料](https://docs.python.org/3.11/tutorial/controlflow.html#defining-functions)を参照してください。

## 7. 指示と設定を読む { #7-inspect-instructions-and-settings }

プロンプトはモデルへのリクエストに含めるテキストです。`prompts.yaml`のsystem指示は、ツールと応答構造を説明します。生成を導きますが、関数の実行やモデルの学習は行いません。指示を組み立てるとき、ツールの説明などがテンプレートのプレースホルダーに入ります。

`prompts.yaml`で指示を探し、形式の指示1つと実行履歴の応答を比べます。[テンプレートの説明](understand-the-template.md#instructions-and-agent-construction)でモデルへの渡し方を確認できます。実験するなら先にバックアップし、YAMLのインデントとプレースホルダーを維持します。

`app.py`でモデルIDと`max_steps`を探します。最初は動作する設定を保ちます。`max_steps`は行動ループ、`max_tokens`は1応答の出力枠を制限します。追加クレジットや正答を保証しません。ほかのモデルの実験はアクセス権とライブラリ互換性の範囲で可能です。

## 8. 結果を実演する { #8-demonstrate-the-result }

時刻取得とWeb検索の呼び出し、観測、最終応答を示します。任意の自作ツールも完成したら実演します。エラーを使って本体や説明を修正し、再試行します。

ローカルアプリを実演してください。Spaceの公開は環境固有の手順なので必須ではありません。意図的に一時公開リンクを有効にした場合は、起動者の認証情報で動き、恒久的なホスティングにはなりません。

## 9. 実習を完了する { #9-complete-the-local-practical }

[完了条件](quizzes.md#finish-the-practical)を確認します。基礎レッスンの小テストは2回で、最終テストや認定証は要件ではありません。
