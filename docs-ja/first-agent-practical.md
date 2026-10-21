# テンプレートのツールを登録し、動作を確かめる { #build-the-first-agent-local-walkthrough }

[テンプレートの入手](run-your-first-agent.md)で準備・起動した`First_agent_template`を引き続き使います。モデルの応答を確認し、[仕組みの解説](understand-the-template.md)を読んでから始めます。

動くアプリで**タイムゾーン別の時刻取得**と**ウェブ検索**を使えるようにします。どちらも実装済みです。必須の実習ではテストと登録を行い、新しいツールを書くのは任意です。同じプロジェクト、その`.venv`、Groqキーを使ってください。

**必須の作業：**直接テスト用のファイルを2つ作り、エージェントの既存の`tools=[...]`に配布済みツールを2つ追加します。その後、アプリを再起動し、チャットの実行ログで正常な呼び出しと結果を示します。`Gradio_UI.py`やモデル接続の編集は不要です。

[Hugging Faceのスターターチュートリアル](https://huggingface.co/learn/agents-course/en/unit1/tutorial)を、ローカルアプリ用に構成した実習です。

## 1. 既存のアプリを編集する準備 { #1-open-the-adapted-starter }

実行中のターミナルで**Control + C**を押して止めます。テンプレートの仮想環境は有効にしたままにし、エディターで既存の`First_agent_template`を開きます。比較用に`app.py`を`app.before-tools.py`としてコピーしておきます。

編集ごとに保存し、同じターミナルで`python app.py`を実行し、キーを入力してチャット画面を再読み込みします。次の編集前には止めます。新しいターミナルで再開する場合は[再起動のコマンド](run-your-first-agent.md#11-stop-and-restart)でこのプロジェクトの環境を有効にします。

## この実習で使うファイル { #files-used-in-this-practical }

小さなテストスクリプトは、**このレッスンで新しく作るファイル**です。元のZIPにはありません。`checktime.py`ではなく、アンダースコア付きの`check_time.py`という正確な名前を使います。

| ファイル | 作業 |
| --- | --- |
| `app.py` | 既存プログラムを編集してツールを登録する |
| `check_time.py` | ステップ3Bで`app.py`の横に新規作成し、時刻関数を直接試す |
| `check_search.py` | ステップ4Bで`app.py`の横に新規作成し、検索を直接試す |
| `tools/web_search.py` | 配布済み。`tools`内に置いたまま使う |

テスト2つを作ると、次の構成になります。

```text
First_agent_template/
├── app.py
├── check_time.py
├── check_search.py
├── Gradio_UI.py
├── prompts.yaml
├── requirements.txt
├── tools/
│   ├── final_answer.py
│   └── web_search.py
└── .venv/
```


テストは`tools/`や`.venv/`に入れず、この場所に保存します。各コードはそれぞれのファイルに入れ、`app.py`に混ぜません。`.txt`を余分に付けないでください。

!!! note "完成版のapp.pyを持っている場合"

    完成版はすでに両ツールを登録しています。既存のリストを保ち、**3B**と**4B**の直接テスト、続いて**3D**と**4D**のチャットテストを行います。**3C**と**4C**の登録編集は飛ばせます。任意の独自ツールは未完成のままです。

## 用意済みのツールと編集する部分 { #what-you-will-add }

| すでにあるもの | 今回の作業 |
| --- | --- |
| 動作するが未登録の時刻関数 | 直接テスト、登録、実際のエージェント呼び出しを確認 |
| 未登録の検索ツール | 直接テスト、インスタンスの登録、情報源の検証 |
| 未登録の独自ツールの仮実装 | 任意で実装・テスト・登録 |

## 2. ツールの登録箇所を見つける { #2-walk-through-apppy }

`app.py`の`main()`内で`CodeAgent(...)`を探します。最初は次の登録です。

```python
tools=[final_answer],
```


この時点で登録されているのは`final_answer`だけです。時刻関数と検索クラスはファイル内にあっても、エージェントからはまだ呼べません。`WebSearchTool`をインポートしただけでは検索は有効になりません。登録前にモデルが`web_search(...)`を生成しても呼び出しは失敗し、モデルが記憶から出したリンクも検索結果にはなりません。

`final_answer`は残します。次の手順で既存の時刻関数と検索インスタンスを加えます。`STUDENT TASK`コメントが編集箇所の目印です。動いている接続設定と画面設定は保ちます。

独自ツールは後の[ステップ6](#6-optional-create-your-own-tool)で扱います。

### エージェントは使えるツールをどう知るのか？ { #how-does-the-agent-know-which-tools-it-can-use }

`tools=[...]`がPythonツールとエージェントの接続点です。`CodeAgent`は登録済みツールの**名前、説明、入力の説明と型**をモデルへの指示に含めます。モデルはそれをチャットの依頼と一緒に受け取り、適切な行動を選びます。

東京の現在時刻は`get_current_time_in_timezone`、公式サイト探しは`web_search`の説明に合います。モデルはその名前を使うPythonを生成し、ローカル実行器が動かします。[CodeAgentの自動処理](understand-the-template.md#what-codeagent-handles-automatically)も参照してください。

| 部分 | 編集場所 | 役割 |
| --- | --- | --- |
| 関数の実装 | `app.py`の`main()`より上の関数本体 | 実際の処理 |
| 関数の説明 | `def`直下のdocstring | いつ使う機能かを伝える |
| 入力の説明 | docstringの`Args:` | 適切な引数を作る手掛かり |
| ツール登録 | `main()`の`CodeAgent(...)`内の`tools=[...]` | このエージェントから利用可能にする |

時刻関数はすでに`app.py`にあり、別の実装ファイルを作る必要はありません。`check_time.py`はテスト専用です。検索は`tools/web_search.py`に定義され、クラスの`description`が説明を持ちます。`app.py`のインポートでプログラムから使えますが、エージェントには`WebSearchTool(max_results=3)`を登録して初めて公開されます。

### 呼ぶタイミングはどう決まるのか？ { #how-does-it-decide-when-to-call-a-tool }

「timeと言われたら必ず呼ぶ」という固定ルールではありません。モデルが依頼と説明を見て選びます。初回は**「Use get_current_time_in_timezone with Asia/Tokyo.」**と、ツールと入力を明示しましょう。その後、コードと実行出力を確かめます。登録しても、選択や引数が正しいとは限りません。

`prompts.yaml`には一般的な指示と例があります。`search`や`wiki`が例に出ても、登録されたことにはなりません。`search(...)`という生成コードは検索成功の証拠ではなく、この教材の検索名は`web_search`です。ツールのリストと実際のログで判断します。

## 3. 時刻ツールを有効にする { #3-enable-the-time-zone-tool }

**目標：**実際の関数呼び出しから時刻を取得し、モデルの推測と区別します。

### A. 関数を読む { #a-read-the-function }

`app.py`で`get_current_time_in_timezone`を探します。入力は`Asia/Tokyo`などの識別子で、出力は日付と時刻の文字列です。

| コード | 働き |
| --- | --- |
| `@tool` | エージェントが使うメタデータを付ける |
| `timezone: str` | 入力が文字列だと示す |
| `pytz.timezone(timezone)` | 識別子のタイムゾーン規則を取得する |
| `datetime.datetime.now(tz)` | PCの時計から、その地域の現在時刻を読む |
| `.strftime(...)` | 読みやすい書式にする |
| `return ...` | 呼び出し元に結果を返す |
| `except Exception ...` | 入力や処理の失敗時にエラー文を返す |

タイムゾーン名は固定の時差ではなく地域を表します。夏時間で時差が変わる地域もあります。最初は`Asia/Tokyo`を使います。PCの時計自体のずれは、この関数では直せません。

### B. エージェントなしでテストする { #b-test-it-without-the-agent }

アプリを止め、テンプレートの仮想環境は有効にしたまま進めます。

1. エディターで**新規ファイル**を選びます。
2. 下のコードを貼ります。
3. 既存の`First_agent_template`内、`app.py`の横に**`check_time.py`**として保存します。

```python
from app import get_current_time_in_timezone

print(get_current_time_in_timezone(timezone="Asia/Tokyo"))
print(get_current_time_in_timezone(timezone="Not/A_Real_Zone"))
```


ターミナルが`First_agent_template`にあり、`(.venv)`が有効な状態で実行します。

```bash
python check_time.py
```


1行目は東京の日付と時刻、2行目は`Error fetching time`で始まるエラーになるはずです。2つ目は不正入力の扱いを試すもので、時刻取得の成功ではありません。どちらもGroqやキーは不要です。`app`のインポートではチャットは起動せず、ツールだけが定義されます。

**確認：**正常な結果を東京の時計と比較します。2行目の不正タイムゾーンのエラーは意図したものです。正常な呼び出しが失敗したら、エージェント経由のテスト前に直します。

ファイルを開けないと言われたら、`app.py`の横に保存したか、ターミナルがその場所にあるかを確認します。`dir`／`ls`で両方が見えるはずです。時刻関数を示す`ImportError`なら、`app.py`に関数を残して保存したかを確認します。

### C. エージェントに登録する { #c-register-it-with-the-agent }

すでに`tools`に`get_current_time_in_timezone`があればそのままDへ進みます。なければ、元のスターターの`CodeAgent(...)`内の`tools=[final_answer]`という引数だけを置き換えます。

```python
tools=[final_answer, get_current_time_in_timezone],
```


行頭の空白と末尾のカンマを保ち、`tools=`は1つだけにします。ここでは`get_current_time_in_timezone()`と書きません。起動時に呼ぶのではなく、機能を登録するためです。

保存し、`python app.py`で起動し、キーを入力して画面を再読み込みします。

### D. 実際の呼び出しを頼む { #d-ask-for-a-real-tool-call }

チャットで次を送ります。「Asia/Tokyoで関数を使い、戻った時刻とその出所を報告して」というテストです。

> Use get_current_time_in_timezone with Asia/Tokyo. Report the returned time and say where it came from.

**Used tool python_interpreter**（使用したツール）を開き、その中の**Execution Logs**（実行ログ）を開いて値を確認します。ターミナルでも確認できます。次は行動の例です。

```python
result = get_current_time_in_timezone(timezone="Asia/Tokyo")
print(result)
```


これは実行記録で見分けるための出力例で、`app.py`に追加するコードではありません。変数名が異なったり、同じブロックで`final_answer`まで呼んだりする場合もあります。

**確認：**関数呼び出し、返された日時、それと一致する最終回答を探します。実行の根拠なしに「東京は10時」と言っただけでは不十分です。

直接テストが成功しても未定義と言われたら、登録、綴り、保存、再起動を確認します。無視される場合は、再起動して履歴を新しくし、明示的な依頼を試します。

## 4. 検索ツールを使う { #4-explore-the-search-tool }

**目標：**検索結果を取得して回答に使わせ、情報源の根拠と裏付けのない主張を区別します。

### A. 何が返るツールかを理解する { #a-understand-what-this-tool-returns }

配布済みの`tools/web_search.py`の`WebSearchTool`は、小さな接続用コードです。smolagentsと保守されている`ddgs`パッケージをつなぎ、検索先に**DuckDuckGoを明示**しています。モデルから見える名前は**`web_search`**、入力は文字列の`query`、出力はタイトル・リンク・短い抜粋です。

検索サービスに接続するのはPythonツールです。Groqは行動と回答を生成し、検索自体は行いません。追加の検索APIキーは不要ですが、失敗や制限は起こり得ます。

**検索はページ全文の読解ではありません。** 返るのは検索結果の抜粋で、リンク先全文を取得するツールではありません。要約も抜粋しか見ていない可能性があります。自分で情報源を開いて確認します。自動の全文取得には別ツールが必要で、この必須実習の範囲外です。

### B. LLMを使う前に直接検索する { #b-test-search-directly-before-using-the-llm }

アプリが動いていれば**Control + C**で止め、`.venv`は有効なままにします。

1. エディターで**新規ファイル**を選びます。
2. 次のコードを貼ります。
3. `First_agent_template`内の`app.py`、`check_time.py`の横に**`check_search.py`**として保存します。

```python
from tools.web_search import WebSearchTool

search_tool = WebSearchTool(max_results=3)
print("Agent-facing name:", search_tool.name)
print(search_tool(query="Python official documentation tutorial"))
```


有効なターミナルで、`First_agent_template`から実行します。

```bash
python check_search.py
```


Groq要求やキーなしで検索サービスに直接接続するため、LLMと独立して通信を調べられます。

`max_results=3`は最大3件を求めます。読みやすくし、後でモデルに送る文字量を抑えるためです。エージェントの検索回数を制限するものではありません。

`web_search`という名前に続いて`Search Results`の見出しと、タイトル・URL・抜粋が出ることを確認します。内容と順序は変動します。以下は短縮した**説明用の例**で、実際の検索結果ではありません。

```text
Agent-facing name: web_search
## Search Results

[The Python Tutorial](https://docs.python.org/3/tutorial/)
A short search-result description would appear here.
```


**確認：**関連する結果が1つ以上あり、リンクが開くことを確認します。ファイルが開けない場合は3Bと同じく名前・保存場所・作業フォルダーを確認します。検索の障害なら、モデルやキーを変える前に下の対応表を使います。

### C. 検索インスタンスを登録する { #c-register-the-search-instance }

すでに`tools`に`WebSearchTool(max_results=3)`があればそのままDへ進みます。元のスターターは`app.py`上部ですでに`tools.web_search`からインポートしていますが、それだけでは登録されません。既存の`tools=`引数を置き換えます。

```python
tools=[
    final_answer,
    get_current_time_in_timezone,
    WebSearchTool(max_results=3),
],
```


`CodeAgent(...)`の他の引数と同じ深さにそろえ、周囲と他の引数を保ちます。

| 式 | 意味 |
| --- | --- |
| `WebSearchTool` | アプリにインポートしたクラス |
| `WebSearchTool(max_results=3)` | 登録できる、設定済みのインスタンス |
| `web_search(query="...")` | 生成Pythonでエージェントが使う呼び出し名 |

インポートするクラスを`web_search`に改名しないでください。モデル用の名前はツール側が提供します。`tools/web_search.py`の`DDGS(timeout=15).text(..., backend="duckduckgo")`が検索を送り、返った辞書を整形します。[DDGSの説明](https://pypi.org/project/ddgs/)には検索先の選択肢があります。

保存して`python app.py`で再起動し、キーを入力してローカル画面を再読み込みします。

### D. 具体的な検索を依頼する { #d-give-the-agent-a-specific-search-task }

次を送ります。「公式Pythonチュートリアルを探し、結果からタイトルとURLを1つ返し、合う理由と抜粋しか見ていないかを説明して」という依頼です。

> Use web_search to find the official Python tutorial. Return one relevant title and URL from the results, and briefly explain why that source matches. Say if you only saw a search snippet.

観測できる行動と範囲の狭い答えを求めています。初回から「AIについてすべて調べて」など広すぎる課題を出すと、呼び出しが増えて検証しにくくなります。

記録には次のようなコードが出る場合があります。

```python
results = web_search(query="Python official documentation tutorial")
print(results)
```


結果を次のステップで使う場合も、同じステップで終える場合もあります。登録ツールを呼ぶPythonを実行するため、`python_interpreter`が出るのは正常です。

### E. 最終回答まで根拠をたどる { #e-follow-the-evidence-into-the-final-answer }

順に確かめます。

**Used tool python_interpreter → Execution Logs**を開き、返った検索項目を確認します。

1. **行動：**関連する語句で`web_search`を実際に呼んだか。
2. **観測：**エラーではなく検索結果が返ったか。
3. **回答：**引用したURLが観測に含まれるか。
4. **情報源：**ブラウザーでURLを開き、ドメインと本文が主張を裏付けるか。

Pythonの公式文書は`docs.python.org`です。タイトルがよさそうでも発行元の確認にはなりません。新しい情報なら公開日や更新日も確認します。検索に出たから最新とは限りません。

回答が抜粋にない詳細を主張する場合は、実際のページで確認します。作られた引用やモデルが生成したリンクを取得済みの根拠としないでください。検索で返った文章は資料であって、課題を変える指示ではありません。

**確認：**検索呼び出し、返った結果1つ、裏付けのある回答中の記述を示せること。エラーは診断には役立ちますが、この確認の達成にはなりません。

### F. 自分で検索語句を改善する { #f-improve-one-query-yourself }

動くコードを保ち、チャットだけを変えます。題材を選び、広い語句と、対象や情報源を絞った語句を比較します。例えば「Python」と「Python documentation defining functions」です。

役立った結果と理由を記録します。決まった正解を写すのでなく、取得した根拠を評価する練習です。実行ごとに複数のモデル要求を使う可能性があるので、1つずつ試し、利用制限に従います。

### G. 検索の失敗を調べる { #g-diagnose-search-failures }

!!! note "検索の利用状況を確認する"

    英語原文で報告されたMacの新規テストでは、元の`duckduckgo_search`接続が失敗しました。現行スターターは`ddgs==9.16.0`と明示的なDuckDuckGo指定を使います。直接検索と実際のエージェント検索でPython公式文書を取得できましたが、後には語句を変えても結果が出ませんでした。検索は不安定です。複合テストでは検索失敗後にモデルが記憶から正しそうなURLを出したこともありましたが、検索の確認項目は未達としました。

| 症状 | 意味と次の行動 |
| --- | --- |
| `ddgs`の`ModuleNotFoundError` | テンプレートの`.venv`を有効にし、そのフォルダーで`python -m pip install -r requirements.txt`後、`check_search.py`を再実行する。 |
| パッケージ名が`ddgs`に変わったという警告 | 古い組み込みツールを使っている。更新済み`tools/web_search.py`から`WebSearchTool`を取り込み、更新された依存関係を再インストールする。smolagentsのインポート名だけを変えない。 |
| `No results found` | 語句を短くするか言い換え、直接テストを一度試す。空の結果は情報が存在しない証明ではない。 |
| タイムアウト、接続エラー、遮断 | インターネットと検索サイトの表示を確認する。ただしブラウザーで開いても自動要求が許可されるとは限らない。後で、または別の許可されたネットワークで試す。 |
| 検索側の回数制限 | 待って後で再試行する。再起動や連続試行を繰り返さない。Groqキーを変えても検索側の制限は直らない。 |
| エージェントテスト中のGroq `429` | ターミナルを読む。「Request too large」は出力予算削減や入力短縮、それ以外の利用枠不足は指定のリセットを待つ。接続設定ページの対応表を参照。直接検索成功はGroq枠の残りを保証しない。 |
| 生成コードの`web_search`が未定義 | `tools`に検索インスタンスがあるか確認し、保存・再起動する。 |
| 直接検索は成功するが呼ばれない | Dの明示的な依頼を使い、登録を確認し、再起動で履歴を新しくして試す。 |
| 結果と違うURLを回答する | 観測と照合し、実際に返ったURLを使うよう頼む。 |

検索が使えなければ実行記録の説明を読み進め、後で動作確認に戻ります。検索テストは未完了とし、架空の結果で置き換えません。

## 5. 必須の2ツールを検証する { #5-verify-the-two-core-tools }

時刻は確認しやすいローカル結果、検索は外部サービスと情報源評価を学ぶ、最初の組み合わせです。追加キーは不要ですが、検索はGroqと独立に遮断・制限され得ます。

まず別々に試してから組み合わせます。複合テストでは次を送ります。時刻を取得した後、公式文書を検索し、検索が失敗したら記憶のリンクで代用しないよう依頼しています。

> Get the current time in Asia/Tokyo using the time tool, then search for the official Python documentation. Give me a source link actually returned by web_search. If search fails, say that it failed; do not substitute a link from memory.

**両方**の呼び出しと正常な出力を確認します。時刻を信頼できる時計と比べ、返った文書リンクを開きます。正しいと知っているリンクでも、検索観測に含まれる必要があります。飛ばされたら明示的に依頼し直して次の実行を確認します。架空の時刻や記憶からのリンクを成功に数えません。明確な依頼をしても、自分での確認は必要です。

`final_answer`は終了の仕組みとして登録を保ちます。今回有効にする2機能とは別です。

画像生成は除外されています。登録する画像ツールも画像サービスの設定もありません。

## 6. 任意：自分のツールを作る { #6-optional-create-your-own-tool }

目的は自分で決めます。以下は、コードと説明の書き場所を示す**架空のモルドール風単語集**です。実在の翻訳ではなく、汎用翻訳器でもありません。自分のツールは別の題材でも構いません。

**書く → 説明する → 直接試す → 登録する → 依頼する → 実行を確認する**の順で進めます。説明を付けても実装は必要です。

### A. 関数と説明を書く { #a-scaffold-if-python-functions-are-new }

**Control + C**で止め、`app.py`の**`main()`より上**にある任意の`@tool`／`my_custom_tool`を探します。デコレーター、古いdocstring、`raise NotImplementedError(...)`を含む関数全体を次に置き換えます。時刻関数と他の部分は残します。

```python
@tool  # Make the function's name, description, and inputs available to smolagents.
def translate_to_mordor(text: str) -> str:
    """Translate one supported English word using an invented Mordor-style demo glossary.

    Args:
        text: One English word to translate: hello, friend, or goodbye.
    """
    glossary = {"hello": "mor", "friend": "dur", "goodbye": "nak"}  # Invented demo words.
    word = text.strip().lower()  # Ignore surrounding spaces and capital letters.
    if word not in glossary:
        return "Unsupported word. Choose hello, friend, or goodbye."
    return glossary[word]  # Return the dictionary result; no model or online translator is called.
```


この例の辞書は`hello → mor`、`friend → dur`、`goodbye → nak`の3語だけです。前後の空白と大文字小文字を整え、未対応なら「hello、friend、goodbyeから選んでください」というエラー文を返します。モデルやオンライン翻訳は使いません。

| コード | 意味 |
| --- | --- |
| `translate_to_mordor` | エージェントが呼ぶ名前 |
| `text: str` | 入力は文字列 |
| `-> str` | 戻り値は文字列 |
| 三重引用符内の最初の文 | 機能と用途を説明するdocstring |
| `Args:`／`text:` | モデルが渡す入力の説明 |
| `glossary`、検索、`return` | 実際のPython処理 |

**説明はどこを変える？** チャットや`prompts.yaml`ではなく、`def`直下のdocstringです。実際の機能と限界を書きます。3語だけに対応するので、説明もその範囲にします。

### B. エージェントの前に関数を試す { #check-the-function-before-the-agent-calls-it }

エディターで`app.py`の横に**`check_my_tool.py`**を作り、次を貼って保存します。アプリは止めたまま、`.venv`を有効にします。

```python
from app import translate_to_mordor  # Import the new function; do not launch the chat.

print(translate_to_mordor(text="Hello"))  # Normal input; capital letters are accepted.
print(translate_to_mordor(text="unknown"))  # Unsupported input checks the function's limit.
```


`First_agent_template`から実行します。

```bash
python check_my_tool.py
```


期待する出力：

```text
mor
Unsupported word. Choose hello, friend, or goodbye.
```

Groqもキーも使わない直接のPythonテストです。別のツールならインポートと入力を合わせ、実行前に期待結果を書き出します。直接テストの失敗を直してからエージェントを試します。

### C. CodeAgentにつなぐ { #c-connect-the-tool-to-codeagent }

`main()`の`CodeAgent(...)`で、時刻・検索・完了用のツールを残し、**既存**のリストに関数名を追加します。

```python
tools=[
    final_answer,
    get_current_time_in_timezone,
    WebSearchTool(max_results=3),
    translate_to_mordor,  # ADDED: allow the agent to call the new function.
],
```


デコレーター付き関数は括弧なしの`translate_to_mordor`で登録します。`translate_to_mordor(...)`では起動時に呼んでしまいます。`WebSearchTool(max_results=3)`の括弧はクラスのインスタンス作成なので必要です。`tools=`は1つだけにします。

`app.py`内で定義したなら、ツール本体用の別ファイルは不要です。`check_my_tool.py`はテスト専用です。

### D. 再起動して呼び出しを頼む { #d-restart-and-ask-for-a-tool-call }

保存して`python app.py`で起動し、キーを入力して画面を再読み込みします。「Helloをデモ辞書で訳して戻り値を報告して」というテストです。

> Use translate_to_mordor to translate the word Hello using the demo glossary. Report the returned value.

`CodeAgent`は登録された名前とdocstringをモデルに渡します。モデルは次のような行動を生成できます。

```python
translated = translate_to_mordor(text="Hello")
print(translated)
final_answer(translated)
```


実行記録で認識するための例で、関数定義に貼るコードではありません。ローカル実行器が呼び出し、必要ならCodeAgentが結果やエラーをモデルに渡して続きを進めます。ダミー演習のように自分で行動ループを書く必要はありません。

### E. 本当に実行されたか確認する { #e-check-that-the-new-tool-actually-ran }

**Used tool python_interpreter → Execution Logs**で`translate_to_mordor`の呼び出し、`mor`、それと一致する最終回答を探します。「翻訳しました」という発言だけでは不十分です。

次に未対応の語を頼みます。翻訳を作らず、関数の限界を伝えるか確認します。直接動くのにエージェントで失敗する場合は、保存、登録、正確な名前、docstring、生成引数、再起動を確認します。名前を明示しても選ぶのはモデルなので、記録を読みます。

### 後で別ファイルに移す場合 { #if-you-later-put-the-tool-in-a-separate-file }

初めは`app.py`の`main()`より上が簡単です。`tools/mordor.py`に分けるなら、デコレーター付きの関数全体を移し、そのファイル上部に追加します。

```python
from smolagents import tool
```


次に`app.py`上部でインポートします。

```python
from tools.mordor import translate_to_mordor
```


`CodeAgent`の登録は残し、`app.py`の重複定義を削除します。直接テストのインポート先も`tools.mordor`に変えます。**インポートはプログラムへの読み込み、登録はエージェントへの公開です。** `tools/`というフォルダー名だけでは接続されません。

仕様は[smolagents 1.13.0ツールガイド](https://huggingface.co/docs/smolagents/v1.13.0/en/tutorials/tools)、引数・戻り値・docstringは[Pythonの関数ガイド](https://docs.python.org/3.11/tutorial/controlflow.html#defining-functions)を参照してください。

## 7. 指示と設定を確認する { #7-inspect-instructions-and-settings }

プロンプトはモデル要求の一部として送るテキストです。`prompts.yaml`のシステム指示は使えるツールと応答形式を示します。生成を導きますが、関数を実行したりモデルを訓練したりしません。エージェントが指示を組み立てるとき、ツール説明などをプレースホルダーに埋めます。

ファイルを開いて指示を探し、書式の指示を1つ選んで実際の応答と比べます。[指示がモデルに届く仕組み](understand-the-template.md#instructions-and-agent-construction)も参照します。試しに変える場合はバックアップを取り、YAMLのインデントとテンプレートのプレースホルダーを保ちます。

`app.py`のモデル識別子と`max_steps`を探します。初回は動く設定を保ちます。`max_steps`はループ、`max_tokens`は個々の生成の出力上限で、追加クレジットも正確さも保証しません。他モデルの実験は、アクセス権とライブラリ互換性の範囲で可能です。

## 8. 結果を実演する { #8-demonstrate-the-result }

時刻と検索について、それぞれ呼び出し・観測・最終回答を示します。独自ツールを完成した場合はそれも実演します。エラーを手掛かりに実装や説明を直し、試し直します。

ローカルアプリの実演で構いません。Space公開は実行環境に依存するため必須ではありません。意図的に有効にした一時公開リンクは所有者の認証情報を使い、恒久的なホスティングではありません。

## 9. ローカル実習を完了する { #9-complete-the-local-practical }

[完了確認](quizzes.md#finish-the-practical)を振り返ります。小テスト2つは基礎レッスン内にあり、最終テストや認定取得は必須ではありません。
