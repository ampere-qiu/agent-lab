# 12 · 完了確認 { #week-3-completion }

今週は関数型・クラス型のツールまでを扱います。保存したファイルと、実際のターミナル出力を示してください。このサイトは進捗を保存せず、修了証も発行しません。

## ファイルと実行の根拠 { #required-evidence }

新しく作ったファイルはすべて`First_agent_template`内の、`app.py`と配布された`week03_common.py`と同じ場所に保存します。

| ファイル | 示すもの |
| --- | --- |
| `my_playlist.py` | ウェブ検索の呼び出し、返された抜粋・URL、それを使った回答。サービスが失敗した場合は、その事実を記録する。 |
| `my_menu.py` | `suggest_menu`の呼び出しと、返されたメニュー。 |
| `my_tool_calling.py` | 構造化された`web_search`の呼び出し、返された結果、それを使った回答。`my_playlist.py`とアクションの形式を比べる。 |
| `my_timing.py` | 生成された`datetime`のコード、PCの開始時刻、180分という所要時間、終了時刻。 |
| `my_tool_check.py` | モデルに問い合わせずに表示された`PASS: menu, catering, theme, and unknown-category checks.`。 |
| `my_catering.py` | ケータリングツールの呼び出し、返された業者名、最終回答。 |
| `my_theme.py` | テーマツールの呼び出し、保存済みの説明文、最終回答。 |
| `week03_tools.py`への自分の変更 | 業者やカテゴリの変更が、直接テストとエージェントの結果に反映されていること。 |

直接テストは、アサーションを書き換えるまで配布時のケータリング業者名を期待します。新しく追加した業者が最高評価になったら、期待する名前も変更してください。再実行前には編集を保存します。

新しいターミナルを開いた場合は、[Windows・Macの環境有効化手順](week-3-learning-plan.md#activate-environment)に戻ってから実行してください。結果はそのターミナルに表示され、第2週のブラウザチャットには表示されません。

## 考え方を説明する { #explain-concepts }

それぞれ1〜2文で説明してください。

- Groq上で動く部分と、自分のPCで動く部分はどれですか？
- CodeAgentは何をつないで管理しますか？
- Pythonアクションと構造化されたツール呼び出しは、どう違いますか？
- ツールの名前、説明、入力、出力型は、モデルに何を伝えますか？
- デコレーター付きの関数と、`forward(...)`を持つ`Tool`クラスは、どう違いますか？
- パーティーの例のうち、架空のPythonデータはどれで、ウェブ検索から来る結果はどれですか？
- ツールが本当に動いたことを、どう確認しますか？

検索・取得、知識ベース、エージェントのチーム、画像・ブラウザの話題は[第04週のページ](week-4-preview.md)に続きます。

## 小テストと出典 { #optional-hf }

[HF Quick Quiz 1](https://huggingface.co/learn/agents-course/en/unit2/smolagents/quiz1)は任意です。それ以降の小テストには、今週扱わない内容も含まれます。

考え方と例は、[Hugging Face Agents Course Unit 2.1](https://huggingface.co/learn/agents-course/en/unit2/smolagents/introduction)を基にしています。

**振り返り：**[第03週の学習計画](week-3-learning-plan.md) · **次へ：**[第04週 · 次回の内容](week-4-preview.md)。
