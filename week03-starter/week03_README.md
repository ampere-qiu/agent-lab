日本語の手順は、このファイル後半の「日本語の手順」を参照してください。

# Week 03 support files

This week uses Python programs in the terminal with your Groq key.
Results appear in the terminal. No Gradio interface or browser chat is used.

1. Extract the ZIP. Open its week03-exercises folder.
2. Copy the six files into your EXISTING First_agent_template folder beside app.py.
3. Open First_agent_template in your code editor.

WINDOWS: open Command Prompt and run each line:

    cd /d "%USERPROFILE%\agent-course\First_agent_template"
    .venv\Scripts\activate.bat
    python --version
    python -m pip install -r week03-requirements.txt

MAC: open Terminal and run each line:

    cd ~/agent-course/First_agent_template
    source .venv/bin/activate
    python --version
    python -m pip install -r week03-requirements.txt

Use the existing Week 2 Python 3.11 environment. If your project is saved in a
different place, use its actual folder path. Repeat cd and activation each time
you open a new terminal. The package list is only smolagents, openai, and ddgs.

Supplied files:
- week03_common.py: Groq connection, classroom settings, and result/error printing.
- week03_tools.py: menu, catering, and theme tool implementations.
- week03_search.py: web-search tool.
- week03-requirements.txt: terminal package list.
- week03_README.md: these instructions.
- week03-HF-LICENSE.txt: source license.

Follow the lesson pages to CREATE your own small programs:
- Step 09: my_playlist.py, my_menu.py, my_timing.py.
- Step 10: my_tool_calling.py.
- Step 11: my_tool_check.py, my_catering.py, my_theme.py.

For each file: File > New Text File, paste the complete code from the lesson,
File > Save As, save the exact .py filename beside app.py and week03_common.py.
Save changes with Ctrl+S (Windows) or Command+S (Mac). Do not add .txt.

Run the saved file in the activated terminal, for example:

    python my_playlist.py

Enter your Groq key at the hidden prompt if asked, then press Enter. The direct
my_tool_check.py test does not contact Groq or ask for a key. Never save a key
inside a Python file.

Menu, catering ratings, and theme descriptions are fixed fictional examples in
the supplied Python tools. Web search returns external snippets and URLs.
Inspect the actual tool call, observation, and final answer.

If a module cannot be found, check the folder and active environment, then run
the requirements command again. If a file cannot be opened, check its exact
name, saved location, and .py extension. Show model/search errors to the teacher.

Week 03 ends at tools. Retrieval and later demos continue in Week 04; no
retrieval data, BM25/LangChain packages, UI files, or demo runners are included.

Credits: examples adapted from Hugging Face Agents Course Unit 2.1:
https://huggingface.co/learn/agents-course/en/unit2/smolagents/introduction
See week03-HF-LICENSE.txt for the Apache 2.0 license.

---

## 日本語の手順

今週は、Groqキーを使う小さなPythonプログラムをターミナルで動かします。
結果もターミナルに表示します。Gradioやブラウザチャットは起動しません。

1. ZIPを展開し、week03-exercisesフォルダーを開きます。
2. 中の6ファイルを、既存のFirst_agent_template内のapp.pyと同じ場所にコピーします。
3. コードエディターでFirst_agent_templateを開きます。
4. 第03週の学習計画ページにあるWindows・Macの手順で、既存のPython 3.11環境を有効にします。
5. python -m pip install -r week03-requirements.txt を実行します。

新しいターミナルを開いた場合は、プロジェクトフォルダーへの移動と環境の有効化をやり直します。
追加するパッケージはsmolagents、openai、ddgsだけです。

配布される6ファイル：
- week03_common.py：Groq接続、授業用の設定、結果・エラーの表示。
- week03_tools.py：メニュー、ケータリング、テーマのツール。
- week03_search.py：ウェブ検索ツール。
- week03-requirements.txt：必要なPythonパッケージの一覧。
- week03_README.md：この手順書。
- week03-HF-LICENSE.txt：原典のライセンス。

教材ページのコード全体を使い、次のファイルを自分で作ります。
- ステップ09：my_playlist.py、my_menu.py、my_timing.py。
- ステップ10：my_tool_calling.py。
- ステップ11：my_tool_check.py、my_catering.py、my_theme.py。

エディターで新規ファイルを作り、コードを貼り付け、指定の.py名でapp.pyと同じ場所に保存します。
WindowsはCtrl+S、MacはCommand+Sで保存します。.txtを付けないでください。
実行例：python my_playlist.py

Groqキーを求められたら入力してEnterを押します。入力中の文字は表示されません。
my_tool_check.pyはGroqに接続しないので、キーは不要です。キーをPythonファイルに保存しないでください。

メニュー、業者の評価、テーマの説明は、Pythonに保存された架空のデータです。
ウェブ検索は外部から抜粋とURLを取得します。実際の呼び出し、観測結果、最終回答を確認します。

モジュールが見つからなければ、現在のフォルダーと有効な環境を確認し、パッケージの導入をやり直します。
ファイルが開けなければ、名前、保存場所、.py拡張子を確認します。
モデルや検索のエラーは、実際の表示を教員に見せてください。

第03週はツールまでです。検索・取得や、その先の内容は第04週で扱います。
このZIPには取得用データ、BM25・LangChain、UI、デモ実行ファイルは含みません。
例の原典はHugging Face Agents Course Unit 2.1です。Apache 2.0ライセンスは同梱ファイルを参照してください。
