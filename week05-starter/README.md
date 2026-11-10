# Week 5 — LlamaIndex, English / 日本語

Open this whole `week05-exercises` folder in your editor. Start with
`lessons/en/week-5-learning-plan.md` or `lessons/ja/week-5-learning-plan.md`.
Follow the lessons in their numbered order, using a separate Python 3.11 environment.

Supplied: requirements.txt, prepare_personas.py, week05_common.py, week05_rag.py,
NOTICE.md, HF-LICENSE.txt, the English/Japanese lessons and original HF figures in images/. Create the named `my_*.py`
programs from their lesson blocks, beside these helpers. Do not edit your Week 4 files.

The setup page gives Windows Command Prompt and Mac Terminal commands. Create
`.env` locally with GROQ_API_KEY and GROQ_MODEL=qwen/qwen3.8-27b. Keep it private.
`prepare_personas.py` downloads the first ten public HF finepersonas records.
The first local embedding run downloads BAAI/bge-small-en-v1.5. Neither needs Groq tokens.

Groq programs require an account with access and capacity. Local workflows and
retrieval can be tested separately. Do not repeatedly restart on 429; waiting does
not replenish credits or guarantee success. The model programs disable API retries.

Generated locally: data/, dataset-source.json, .venv/, .env, .cache/,
alfred_chroma_db/, flow.html, evidence.md and your own programs. None belongs in a
public repository with credentials. Source/adaptation details are in NOTICE.md.

Follow one program at a time and use the file/result checklist at the end of each
lesson. Comparison activities show the exact line to change and the line to restore.
The setup lesson explains first-run warnings and gives recovery actions for errors.
The Bob helper explicitly preserves conversation memory between shared-context runs.
Persona tools return original SOURCE/EXCERPT text separately from a GENERATED ANSWER;
quote only an original excerpt and check its source file. Diagram export saves HTML
without launching the operating-system browser.

Starter helper version: **2026-11-10.2**. After installing requirements, check it
with `python week05_common.py`. Reuse only the Week 4 key; set the Week 5 model
line as shown in setup. Diagram HTML contains its libraries and works offline.

Starter 2026-11-10.2 uses a checked original-dataset fallback, loads a complete
embedding cache locally, cleans model thinking tags from terminal answers, and
adds automatic/manual diagram fitting. Missing-match claims cover retrieved
passages only. The setup help explains the adapter’s optional-extra pip warning.

日本語版は `lessons/ja/week-5-learning-plan.md` から始めてください。
英語版と同じヘルパー、コード、質問、元のHF図を使います。説明は日本語で、
コードと英語の出力はそのままです。図の直下の説明はクリックして開けます。
